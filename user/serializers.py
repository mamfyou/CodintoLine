import re

from rest_framework import serializers

from question_sheet.models.qsheet_models import QuestionSheet
from user.models import Folder, CodintoLineUser


class QuestionSheetFolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionSheet
        fields = ['uid', 'name']


class FolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Folder
        fields = ['id', 'name', 'questionSheetFolder']

    questionSheetFolder = QuestionSheetFolderSerializer(read_only=True, many=True)

    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)

    def validate(self, attrs):
        if Folder.objects.filter(name=attrs.get('name')).exists():
            raise serializers.ValidationError('این پوشه هم اکنون وجود دارد!')
        return attrs

class CodintoLineUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodintoLineUser
        fields = ['id', 'first_name', 'last_name', 'phone_number', 'is_active', 'is_staff', 'is_superuser']
        read_only_fields = ['is_active', 'is_staff', 'is_superuser']

    def validate(self, attrs):
        if attrs.get('phone_number') is not None and not re.match(r'^09\d{9}$', attrs.get('phone_number')):
            raise serializers.ValidationError('فرمت شماره تلفن نادرست می باشد!')
        return attrs
