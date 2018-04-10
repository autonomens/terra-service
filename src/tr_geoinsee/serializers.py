# coding: utf8
from rest_framework import serializers, fields


class StateSerializer(serializers.Serializer):
    insee_code = serializers.IntegerField()
    name = serializers.CharField()


class SparQLSerializer(serializers.Serializer):
    def get_fields(self):
        '''
        Set all fields as CharField based on first item of list in case of
        ListSerializer or instance item
        '''
        if type(self.instance) is list:
            instance = self.instance[0]
        else:
            instance = self.instance
        return {key: fields.CharField() for key in dict(instance).keys()}
