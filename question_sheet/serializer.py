from rest_framework import serializers

from question_sheet.models import QuestionSheet, Question


class QuestionSheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionSheet
        fields = ['id', 'name', 'language', 'start_date', 'end_date', 'duration',
                  'is_active', 'has_progress_bar', 'is_one_question_each_page']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        validated_data['name'] = "Untitled"
        return super().create(validated_data)


class QuestionSheetQuestionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'

    # not configured
