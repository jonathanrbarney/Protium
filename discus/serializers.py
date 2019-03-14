from rest_framework import serializers
from discus.models import *
from rest_framework.exceptions import PermissionDenied

class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ['id', 'created']
    def save(self, **kwargs):
        if (self.instance is None) or (self.instance and (self.instance.creator is None)):
            request = self.context.get("request")
            self.validated_data['creator'] = request.user
        return super(PostSerializer, self).save(**kwargs)

class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = '__all__'
        read_only_fields = ['id','voter']
    def save(self, **kwargs):
        request = self.context.get("request")
        if request.user:
            self.validated_data['voter'] = request.user
        else:
            raise PermissionDenied
        return super(VoteSerializer, self).save(**kwargs)

