from rest_framework import serializers
from accounts.models import *

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('id','usafa_id','discus_id','first_name','middle_name','last_name', 'dob', 'email','official_email',
                  'official_phone_number','gender','room_number', 'building','class_year','profile_pic',
                  'academic_advisor','proper_name', 'full_name', 'email_verified','phone_verified',
                  'official_email_verified','official_phone_verified','bio', )
        read_only_fields = ('proper_name', 'full_name', 'email_verified','phone_verified','official_email_verified','official_phone_verified',)

class AccountSnapshot(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('id','usafa_id','first_name','middle_name','last_name', 'email','official_email','gender','class_year','profile_pic',
                  'proper_name','account_type',)
        read_only_fields = ('id','usafa_id','first_name','middle_name','last_name', 'email','official_email','gender','class_year','profile_pic',
                  'proper_name', 'account_type',)

