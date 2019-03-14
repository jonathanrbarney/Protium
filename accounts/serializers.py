from rest_framework import serializers
from accounts.models import *


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

        read_only_fields = ('id', 'usafa_id', 'proper_name', 'full_name', 'email_verified', 'phone_verified',
                            'official_email_verified', 'official_phone_verified', 'last_four', 'account_type',
                            'has_attended','programs')


class AccountSnapshot(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('id','usafa_id','first_name','middle_name','last_name', 'official_email','gender','class_year','profile_pic',
                  'proper_name','account_type', 'full_name')
        read_only_fields = ('id','usafa_id','first_name','middle_name','last_name', 'official_email','gender','class_year','profile_pic',
                  'proper_name', 'account_type', 'full_name')

