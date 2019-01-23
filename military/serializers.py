from rest_framework import serializers
from military.models import *

class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = '__all__'


class AMISerializer(serializers.ModelSerializer):
    class Meta:
        model = AMI
        fields = '__all__'

class SAMISerializer(serializers.ModelSerializer):
    class Meta:
        model = SAMI
        fields = '__all__'


class PAISerializer(serializers.ModelSerializer):
    class Meta:
        model = PAI
        fields = '__all__'


class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = '__all__'

