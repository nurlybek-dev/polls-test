from django.utils import timezone
from django.db import transaction

from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status

from polls.models import Answer, Option, Poll, Question, UserPoll
from polls.serializers import AnswerSerializer, OptionSerizlizer, PollDetailSerializer, PollSerializer, QuestionSerializer, UserPollDetailSerializer, UserPollSerializer


class PollViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAdminUser]
    queryset = Poll.objects.all()
    serializer_class = PollSerializer

class QuestionViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAdminUser]
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class OptionViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAdminUser]
    queryset = Option.objects.all()
    serializer_class = OptionSerizlizer

class AnswerViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAdminUser]
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer


class UserPollView(viewsets.ViewSet):
    def list(self, request):
        """
        Возвращает список всех активных опросников
        """
        now = timezone.now()
        polls = Poll.objects.filter(end_date__gte=now).filter(start_date__lte=now)
        serializer = PollSerializer(polls, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk):
        """
        Возвращает опрос с вложенными вопросами и вариантами ответов. Если ответ на вопрос текстовый, то список вариантов будет пуст
        """
        poll = Poll.objects.filter(end_date__gte=timezone.now()).filter(start_date__lte=timezone.now()).get(pk=pk)
        serializer = PollDetailSerializer(poll)
        return Response(serializer.data)

    @transaction.atomic
    def create(self, request):
        """
        Принимает список объектов Answer. 
        Для ответов в множественным выбором, ответы дублируются меняя поле choice
        {
            "user_id": user id,
            "poll_id": poll id,
            "answers": [
                {"question": id, "text": Текстовый ответ, "choice": Ответ выбором}
            ]
        }
        """
        try:
            serializer = UserPollSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors)
        except KeyError:
            return Response({'error': 'Не все ключи переданы'})


class UserAnswersView(viewsets.ViewSet):
    def list(self, request):
        """
        Метод нужен для отоброжения в списке ApiRoot
        """
        return Response({'List view does not support'})

    def retrieve(self, request, pk):
        """
        Возвращает все UserPoll для переданного pk, либо пустой список
        """
        user_polls = UserPoll.objects.filter(user_id=pk)
        serializer = UserPollDetailSerializer(user_polls, many=True)
        return Response(serializer.data)
