from rest_framework import serializers

class StateSerializer(serializers.Serializer):
    insee_code = serializers.IntegerField()
    name = serializers.CharField()
