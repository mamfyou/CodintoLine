from rest_framework import serializers
from question_sheet.serializers.qsheet_serializer import QuestionSheetSerializer
from user.models import Folder, CodintoLineUser
import re


class FolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Folder
        fields = ['id', 'name', 'questionSheets', 'QuestionSheet']
        extra_kwargs = {
            'questionSheets': {'write_only': True},
        }

    QuestionSheet = QuestionSheetSerializer(many=True, read_only=True, source='questionSheets')

    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)

    def validate(self, attrs):
        for i in attrs.get('questionSheets'):
            if i.owner != self.context['request'].user:
                raise serializers.ValidationError("شما فقط میتوانید پرسشنامه هایی را اضافه کنید که برای شماست!")
        return attrs


class CodintoLineUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodintoLineUser
        fields = ['id', 'username', 'password', 'confirm_password', 'email', 'phone_number', 'folders']
        extra_kwargs = {'password': {'write_only': True}}
        read_only_fields = ['folders']

    confirm_password = serializers.CharField(write_only=True, max_length=500)

    def validate(self, attrs):
        persian_letters = re.compile(r'[\u0600-\u06FF]+')
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError("رمز عبور و تکرار آن یکسان نیستند")
        elif re.search(persian_letters, attrs.get('username')):
            raise serializers.ValidationError("رمز عبور نباید شامل حروف فارسی باشد")
        elif len(attrs['password']) < 8:
            raise serializers.ValidationError("رمز عبور باید حداقل 8 کاراکتر باشد")
        return attrs
