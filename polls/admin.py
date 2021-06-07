from django.contrib import admin
from polls.models import Poll, Question, Option, Answer, UserPoll


admin.site.register(Poll)
admin.site.register(Question)
admin.site.register(Option)
admin.site.register(UserPoll)
admin.site.register(Answer)