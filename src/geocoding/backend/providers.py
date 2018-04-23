from hashlib import md5
import logging

from django.conf import settings
from django.core.cache import cache

from opencage.geocoder import OpenCageGeocode, RateLimitExceededError, InvalidInputError, UnknownError

from . import GeocodingBackend

logger = logging.getLogger(__name__)

class OpenCage(GeocodingBackend):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.opencage = OpenCageGeocode(**settings.GEOCODING_OPTION)

    def get_cache_key(self, prefix, item):
        item_key = md5(item.encode('utf-8')).hexdigest()
        return '{0}_{1}'.format(prefix, item)

    def geocode(self, search):
        return self.handle_call(
            self.get_cache_key('geocode', search),
            self.opencage.geocode,
            args=(search,),
            kwargs={"language": settings.LANGUAGE_CODE}
        )
    
    def reverse_geocode(self, lat, lon):
        return self.handle_call(
            self.get_cache_key('rgeocode', '{}_{}'.format(lat, lon)),
            self.opencage.reverse_geocode,
            args=(lat, lon),
            kwargs={"language": settings.LANGUAGE_CODE}
        )

    def handle_call(self, cache_key, callback, args=None, kwargs=None):
        """ Handle api call and caching """
        # TODO caching can be used in many place. We should use a cache_memoize decorator

        if args is None:
            args = []

        if kwargs is None:
            kwargs = {}

        # Cache exists ? return it !
        data = cache.get(cache_key)
        if data is not None:
            return data

        try:
            results = callback(*args, **kwargs)
        except RateLimitExceededError as e:
            logger.exception("Rate limit exeeeded")
            return {'error': 'Rate limit exceded, please, slow down your queries.'}
        except InvalidInputError as e:
            logger.exception("Invalid query")
            return {'error': 'Invalid input'}
        except UnknownError:
            logger.exception("Unknown error from provider")
            return {'error': 'Unknown error'}
        except Exception:
            logger.exception("Internal error while doing request to provider")
            raise

        final_result = self._adapt_result(results)

        # Cache result for next use
        cache.set(cache_key, final_result, 3600)

        return final_result

    def _adapt_result(self, in_data):
        """ Adapt service response to a generic terralego formed response """
        # TODO Today adapts result to mimic mapzen api
        # TODO next step is to make an independant conversion
        final_result = {
            'geocoding': {
                'version': '3.0'
            },
            'type': 'FeatureCollection',
            'features': []
        }

        for feat in in_data:
            try:
                data = {
                    "type": "Feature",
                    "geometry": {
                        "type": "Point",
                        "coordinates": [
                            feat["geometry"]["lng"],
                            feat["geometry"]["lat"]
                        ]
                    },
                    "properties": {
                        "_type": feat["components"]["_type"],
                        "housenumber": feat["components"].get("house_number", None),
                        "street": feat["components"].get("road", None),
                        "postalcode": feat["components"].get("postcode", ''),
                        "country": feat["components"]["country"],
                        "macroregion": feat["components"].get("state", ''),
                        "county": feat["components"].get("county"),
                        "locality": feat["components"].get("town", feat["components"].get("city", '')),
                        "neighbourghood": feat["components"].get("neighbourhood", None),
                        "label": feat["formatted"],
                        "confidence": feat["confidence"] / 10,
                    },

                }

                if "bounds" in feat:
                    data["bbox"] = [
                        feat["bounds"]["southwest"]["lng"],
                        feat["bounds"]["southwest"]["lat"],
                        feat["bounds"]["northeast"]["lng"],
                        feat["bounds"]["northeast"]["lat"]
                    ]
                else:
                    # TODO Quick hack to have bounding box
                    # We should use better computations
                    data["bbox"] = [
                        feat["geometry"]["lng"] - 0.009,
                        feat["geometry"]["lat"] - 0.009,
                        feat["geometry"]["lng"] + 0.009,
                        feat["geometry"]["lat"] + 0.009
                    ]

                final_result["features"].append(data)
            except KeyError:
                # if conversion fails again we should raise it
                logger.exception("Fails to convert feat", repr(feat))
        final_result['bbox'] = self.get_results_bounding_box(final_result)
        return final_result

    def get_results_bounding_box(self, results): 
        lngs = [r.get('geometry').get('coordinates')[0] for r in results.get('features')]
        lats = [r.get('geometry').get('coordinates')[1] for r in results.get('features')]
        return [
            min(lngs) - 0.009,
            min(lats) - 0.009,
            max(lngs) + 0.009,
            max(lats) + 0.009,
        ]