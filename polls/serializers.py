from re import L
from django.db import transaction
from rest_framework import serializers, validators
from polls.models import Answer, Option, Poll, Question, UserPoll


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'question', 'choice', 'text']

    def validate(self, attrs):
        if not attrs.get('choice') and not attrs.get('text'):
            raise serializers.ValidationError('choice или text должны быть установлены')
        return super().validate(attrs)


class AnswerInlineSerializer(serializers.ModelSerializer):
    question = serializers.StringRelatedField()
    choice = serializers.StringRelatedField()
    class Meta:
        model = Answer
        fields = ['question', 'choice', 'text']

    def validate(self, attrs):
        if not attrs.get('choice') and not attrs.get('text'):
            raise serializers.ValidationError('choice или text должны быть установлены')
        return super().validate(attrs)


class OptionSerizlizer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['id', 'question', 'text']


class OptionInlineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['text']


class QuestionSerializer(serializers.ModelSerializer):
    options = OptionInlineSerializer(many=True)
    class Meta:
        model = Question
        fields = ['id', 'poll', 'text', 'type', 'options']

    @transaction.atomic
    def create(self, validated_data):
        question = Question(poll=validated_data['poll'], text=validated_data['text'], type=validated_data['type'])
        question.save()
        for option in validated_data['options']:
            Option.objects.create(question=question, **option)
        return question


class PollSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poll
        fields = ['id', 'name', 'start_date', 'end_date', 'description']


class PollDetailSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)
    class Meta:
        model = Poll
        fields = ['id', 'name', 'start_date', 'end_date', 'description', 'questions']


class UserPollSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True)
    class Meta:
        model = UserPoll
        fields = ['id', 'user_id', 'poll', 'answers']
        validators = [
            validators.UniqueTogetherValidator(
                queryset=UserPoll.objects.all(),
                fields=['user_id', 'poll']
            )
        ]

    @transaction.atomic
    def create(self, validated_data):
        user_poll = UserPoll(user_id=validated_data['user_id'], poll=validated_data['poll'])
        user_poll.save()
        
        for answer in validated_data['answers']:
            Answer.objects.create(user_poll=user_poll, **answer)
        return user_poll


class UserPollDetailSerializer(serializers.ModelSerializer):
    answers = AnswerInlineSerializer(many=True)
    poll = PollSerializer()
    class Meta:
        model = UserPoll
        fields = ['id', 'user_id', 'poll', 'answers']
