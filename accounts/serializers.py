from rest_framework import serializers
from accounts.models import *

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('id','usafa_id','discus_id','first_name','middle_name','last_name', 'dob', 'email','official_email',
                  'official_phone_number','gender','room_number', 'building','class_year','profile_pic',
                  'academic_advisor','proper_name', 'full_name', 'group_dict','email_verified','phone_verified',
                  'official_email_verified','official_phone_verified',)
        read_only_fields = ('proper_name', 'full_name', 'group_dict','email_verified','phone_verified','official_email_verified','official_phone_verified',)
