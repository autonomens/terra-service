# coding: utf8
from rest_framework import serializers, fields

class StateSerializer(serializers.Serializer):
    insee_code = serializers.IntegerField()
    name = serializers.CharField()


class SparQLSerializer(serializers.Serializer):
    def get_fields(self):
        '''
        Set all fields as CharField based on first item of list in case of ListSerializer or instance item
        '''
        instance = self.instance[0] if type(self.instance) is list else self.instance
        return { key: fields.CharField() for key in dict(instance).keys() } 
