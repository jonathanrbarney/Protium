from rest_framework import serializers
from accounts.models import *
from django.contrib.auth.hashers import make_password
from rest_framework.exceptions import PermissionDenied

class OwnAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account

        fields = ('id','usafa_id','discus_id','first_name','middle_name','last_name', 'dob', 'email','official_email',
                  'official_phone_number','gender','room_number', 'building','class_year','profile_pic',
                  'academic_advisor','proper_name', 'full_name', 'email_verified','phone_verified',
                  'official_email_verified','official_phone_verified','bio', 'hometown', 'last_four', 'phone_number',
                  'account_type', 'has_attended','programs')

        read_only_fields = ('id','usafa_id','proper_name', 'full_name', 'email_verified','phone_verified',
                            'official_email_verified','official_phone_verified','last_four', 'account_type',
                            'has_attended')

class PublicAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account

        fields = ('id', 'usafa_id', 'first_name', 'middle_name', 'last_name', 'official_email',
        'official_phone_number', 'gender', 'room_number', 'building', 'class_year', 'profile_pic',
        'academic_advisor', 'proper_name', 'full_name', 'email_verified', 'phone_verified',
        'official_email_verified', 'official_phone_verified', 'bio', 'hometown', 'account_type', 'has_attended','programs')

        read_only_fields = ['id', 'usafa_id', 'proper_name', 'full_name', 'email_verified', 'phone_verified',
                            'official_email_verified', 'official_phone_verified', 'last_four', 'account_type',
                            'has_attended','programs']


class AccountSnapshot(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('id','usafa_id','first_name','middle_name','last_name', 'official_email','gender','class_year','profile_pic',
                  'proper_name','account_type', 'full_name')
        read_only_fields = ('id','usafa_id','first_name','middle_name','last_name', 'official_email','gender','class_year','profile_pic',
                  'proper_name', 'account_type', 'full_name')


class CreateAccountSerializer(serializers.ModelSerializer):
    ticket_official_email_verify = serializers.BooleanField(required=True)
    token = serializers.CharField(required=True)
    class Meta:
        model = Account

        fields = ('id','usafa_id','discus_id','first_name','middle_name','last_name', 'dob', 'email',
                  'official_phone_number','gender','room_number', 'building','class_year','profile_pic',
                  'academic_advisor', 'phone_number', 'email_verified','official_email_verified')

        read_only_fields = ['id', 'usafa_id']

    def validate(self, data):
        tk = data['token']
        ticket = CreationTicket.objects.get(token=tk)
        if len(ticket) == 0 and ticket.is_valid():
            pass
        else:
            raise serializers.ValidationError('Must have a valid ticket to create account.')
        if data['ticket_official_email_verify']:
            data['official_email']=ticket.email
            data['official_email_verified']=True
            data['email_verified'] = False
        else:
            data['official_email']=data['email']
            data['email']=ticket.email
            data['official_email_verified']=False
            data['email_verified'] = True
        data['account_type'] = ticket.account_type
        return super(CreateAccountSerializer, self).validate(data)

    def save(self, **kwargs):
        tk = self.validated_data['token']
        ticket = CreationTicket.objects.get(token=tk)
        ticket.delete()
        return super(CreateAccountSerializer, self).save(**kwargs)

class CTSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreationTicket

        fields = ('issuer','email')

        read_only_fields = ['issuer']

    def validate(self, data):
        request = self.context.get("request")
        if request.user.account_type in ['Instructor',
                                         'Permanent Party','Coach','Medical Staff',
                                         'Facilities']:
            pass
        else:
            raise PermissionDenied('This type of account cannot issue tickets.')
        return super(CTSerializer, self).validate(data)

    def save(self, **kwargs):
        request = self.context.get("request")
        self.validated_data['issuer'] = request.user
        self.validated_data['account_type'] = request.user.account_type
        return super(CTSerializer, self).save(**kwargs)

