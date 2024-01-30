from rest_framework import serializers


class OperationError(serializers.Serializer):
    title = serializers.CharField()
    message = serializers.CharField()


class OperationSuccess(serializers.Serializer):
    data = serializers.JSONField(default={})