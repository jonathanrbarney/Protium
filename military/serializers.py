from rest_framework import serializers
from military.models import *
from rest_framework.exceptions import PermissionDenied


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = ['id','name','holder','supervisors','is_cadet_job','subordinate_ids']
        read_only_fields = ('id', 'subordinate_ids')

    def validate(self, data):
        request = self.context.get("request")
        valid = []
        for pos in request.user.jobs.all():
            valid.append(pos)
            valid = valid + get_all_subordinates(pos)
        prop_sups = data['supervisors']
        if len({*prop_sups} & {*valid}) == len(prop_sups):
            pass
        else:
            raise serializers.ValidationError(
                'Positions created can only be supervised by one of your positions or their subordinates')
        return super(PositionSerializer, self).validate(data)

    def save(self, **kwargs):
        if self.instance is not None:
            all_sups = self.validated_data['supervisors']
            for p in self.validated_data['supervisors']:
                all_sups = all_sups + get_all_supervisors(p)
            all_subs = get_all_subordinates(self.instance)
            all_subs.append(self.instance)
            if len({*all_sups} & {*all_subs}) == 0:
                pass
            else:
                raise serializers.ValidationError(
                    'None of the position\'s supervisors can be, or be supervised by the position or one of its subordinates')
        return super(PositionSerializer, self).save(**kwargs)


class AMISerializer(serializers.ModelSerializer):
    class Meta:
        model = AMI
        fields = '__all__'
        read_only_fields=['id','creator']

    def validate(self, data):
        request = self.context.get("request")
        cadet=data['cadet']
        if len({*request.user.jobs.all()} & {*get_all_account_supervisors(cadet)}) > 0:
            pass
        else:
            raise PermissionDenied(
                'You can only create scores for your subordinates.')
        return super(AMISerializer, self).validate(data)

    def save(self, **kwargs):
        if (self.instance is None) or (self.instance and (self.instance.creator is None)):
            request = self.context.get("request")
            self.validated_data['creator'] = request.user
        return super(AMISerializer, self).save(**kwargs)



class SAMISerializer(serializers.ModelSerializer):
    class Meta:
        model = SAMI
        fields = '__all__'
        read_only_fields = ['id', 'creator']

    def validate(self, data):
        request = self.context.get("request")
        cadet = data['cadet']
        if len({*request.user.jobs.all()} & {*get_all_account_supervisors(cadet)}) > 0:
            pass
        else:
            raise PermissionDenied(
                'You can only create scores for your subordinates.')
        return super(SAMISerializer, self).validate(data)

    def save(self, **kwargs):
        if (self.instance is None) or (self.instance and (self.instance.creator is None)):
            request = self.context.get("request")
            self.validated_data['creator'] = request.user
        return super(SAMISerializer, self).save(**kwargs)


class PAISerializer(serializers.ModelSerializer):
    class Meta:
        model = PAI
        fields = '__all__'
        read_only_fields = ['id', 'creator']

    def validate(self, data):
        request = self.context.get("request")
        cadet = data['cadet']
        if len({*request.user.jobs.all()} & {*get_all_account_supervisors(cadet)}) > 0:
            pass
        else:
            raise PermissionDenied(
                'You can only create scores for your subordinates.')
        return super(PAISerializer, self).validate(data)

    def save(self, **kwargs):
        if (self.instance is None) or (self.instance and (self.instance.creator is None)):
            request = self.context.get("request")
            self.validated_data['creator'] = request.user
        return super(PAISerializer, self).save(**kwargs)


class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = '__all__'
        read_only_fields=['id']

    def validate(self, data):
        request = self.context.get("request")
        p_coms = data['commanders']
        p_subs = data['subordinates']
        valid = []
        for i in request.user.jobs.all():
            valid=valid+get_all_subordinates(i)
        if len({*valid} & {*p_subs}) == len(p_subs):
            pass
        else:
            raise PermissionDenied(
                'You can only assign positions you supervise to this unit')
        if len({*p_coms} & {*get_all_account_subordinates(request.user)})==len(p_coms):
            pass
        else:
            raise PermissionDenied(
                'You can only assign yourself or your subordinates to command a unit')

        return super(UnitSerializer, self).validate(data)

