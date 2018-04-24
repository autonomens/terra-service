import re
import requests

from django.conf import settings

from rest_framework import permissions

class IsJWTAuthenticated(permissions.BasePermission):
    """
    Verify use is use is logged against JWT
    """

    def has_permission(self, request, view):
        if 'HTTP_AUTHORIZATION' in request.META:
            match = re.findall('^JWT\ ([\w\d\.\-]+)', request.META.get('HTTP_AUTHORIZATION'))
            if match:
                payload = {
                    'token': match[0],
                } 
                response = requests.post(settings.JWT_TOKEN_VERIFY_URL, data=payload)
                if response.status_code == 200:
                    return True
        return False