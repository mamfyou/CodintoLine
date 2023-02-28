from rest_framework import serializers
from question_sheet.serializers.qsheet_serializer import QuestionSheetSerializer
from user.models import Folder, CodintoLineUser
import re


class FolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Folder
        fields = ['id', 'name', 'questionSheets']

    # TODO serializer for qsheet id, name
    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)


class CodintoLineUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodintoLineUser
        fields = ['id', 'first_name', 'last_name', 'phone_number', 'is_active', 'is_staff', 'is_superuser']
        read_only_fields = ['is_active', 'is_staff', 'is_superuser']

    def validate(self, attrs):
        if not re.match(r'^09\d{9}$', attrs['phone_number']):
            raise serializers.ValidationError('فرمت شماره تلفن نادرست می باشد!')
        return attrs
