from django.db import models
from django.urls import reverse


QUESTION_TYPE_CHOICES = (
    (1, 'Ответ текстом'), 
    (2, 'Ответ с выбором одного варианта'), 
    (3, 'Ответ с выбором нескольких вариантов')
)

class Poll(models.Model):
    name = models.CharField(max_length=255)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    description = models.TextField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("admin-polls-detail", kwargs={"pk": self.pk})
    


class Question(models.Model):
    poll = models.ForeignKey(Poll, related_name='questions', on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    type = models.IntegerField(choices=QUESTION_TYPE_CHOICES)

    def __str__(self):
        return self.text    


class Option(models.Model):
    question = models.ForeignKey(Question, related_name='options', on_delete=models.CASCADE)
    text = models.CharField(max_length=255)

    def __str__(self):
        return self.text


class UserPoll(models.Model):
    user_id = models.IntegerField()
    poll = models.ForeignKey(Poll, related_name='user_polls', on_delete=models.CASCADE)

    class Meta:
        unique_together = ['user_id', 'poll']


class Answer(models.Model):
    user_poll = models.ForeignKey(UserPoll, related_name='answers', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, related_name='answer', on_delete=models.CASCADE)
    choice = models.ForeignKey(Option, related_name='answer', on_delete=models.CASCADE, blank=True, null=True)
    text = models.CharField(max_length=255, blank=True, null=True, default='')
