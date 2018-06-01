# coding: utf8
from rest_framework import serializers, fields
from .models import AdministrativeEntity


class StateSerializer(serializers.Serializer):
    insee_code = serializers.IntegerField()
    name = serializers.CharField()


class SparQLSerializer(serializers.Serializer):
    def get_fields(self):
        """
        Set all fields as CharField based on first item of list in case of
        ListSerializer or instance item
        """
        if isinstance(self.instance, list):
            instance = self.instance[0]
        else:
            instance = self.instance
        return {key: fields.CharField() for key in dict(instance).keys()}


class AdministrativeEntitySerializer(serializers.ModelSerializer):

    url = serializers.CharField(source='get_absolute_url', read_only=True)

    class Meta:
        model = AdministrativeEntity
        fields = ('id', 'name', 'insee', 'url')


class GeomAdministrativeEntitySerializer(serializers.ModelSerializer):

    url = serializers.CharField(source='get_absolute_url', read_only=True)

    class Meta:
        model = AdministrativeEntity
        fields = ('id', 'name', 'insee', 'geom', 'url')
