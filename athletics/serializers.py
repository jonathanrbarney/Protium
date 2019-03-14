from rest_framework import serializers
from athletics.models import *

class PFTSerializer(serializers.ModelSerializer):
    class Meta:
        model = PFT
        fields = '__all__'
        read_only_fields = ('creator','id',)

    def save(self, **kwargs):
        if (self.instance is None) or (self.instance and (self.instance.creator is None)):
            request = self.context.get("request")
            self.validated_data['creator']=request.user
        return super(PFTSerializer, self).save(**kwargs)


class AFTSerializer(serializers.ModelSerializer):
    class Meta:
        model = AFT
        fields = '__all__'
        read_only_fields = ('creator','id',)

    def save(self, **kwargs):
        if (self.instance is None) or (self.instance and (self.instance.creator is None)):
            request = self.context.get("request")
            self.validated_data['creator']=request.user
        return super(AFTSerializer, self).save(**kwargs)


