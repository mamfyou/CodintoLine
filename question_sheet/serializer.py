from rest_framework import serializers

from question_sheet.models import QuestionSheet, Question


class QuestionSheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionSheet
        fields = ['id', 'name']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        validated_data['name'] = "Untitled"
        return super().create(validated_data)


class QuestionSheetQuestionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'

    # not configured
