from polls import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('admin/polls', views.PollViewSet, basename='admin-polls')
router.register('admin/questions', views.QuestionViewSet, basename='admin-questions')
router.register('admin/options', views.OptionViewSet, basename='admin-options')
router.register('admin/answers', views.AnswerViewSet, basename='admin-answers')
router.register('polls', views.UserPollView, basename='polls')
router.register('answers', views.UserAnswersView, basename='answers')

urlpatterns = router.urls
