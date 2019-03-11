from rest_framework import serializers
from athletics.models import *

class PFTSerializer(serializers.ModelSerializer):
    class Meta:
        model = PFT
        fields = '__all__'
        read_only_fields = ('creator',)

class AFTSerializer(serializers.ModelSerializer):
    class Meta:
        model = AFT
        fields = '__all__'
        read_only_fields = ('creator',)
