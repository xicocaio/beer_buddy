from rest_framework_gis.serializers import GeoModelSerializer
from rest_framework import serializers
from .models import PDV
from pycpfcnpj import cpfcnpj


class PDVSerializer(GeoModelSerializer):
    def validate(self, data):
        document_clear = cpfcnpj.clear_punctuation(data['document'])
        if not cpfcnpj.validate(document_clear) \
                or len(document_clear) != 14:
            raise serializers.ValidationError('This document is invalid')

        return data

    class Meta:
        model = PDV

        fields = ('id',
                  'tradingName',
                  'ownerName',
                  'document',
                  'coverageArea',
                  'address')
