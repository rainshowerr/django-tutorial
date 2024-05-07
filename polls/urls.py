from django.urls import path

from . import views

app_name = "polls"
urlpatterns = [
    # ex: /polls/
    path("", views.IndexView.as_view(), name="index"),
    # ex: /polls/5/
    # <변환기:패턴 이름>
    # path("<int:question_id>/", views.detail, name="detail"),
    # generic view를 사용하기 위해선 pk를 명시해야 하는듯
    path ("<int:pk>/", views.DetailView.as_view(), name="detail"),
    # ex: /polls/5/results/
    # path("<int:question_id>/results/", views.results, name="results"),
    path("<int:pk>/results/", views.ResultView.as_view(), name="results"),
    # ex: /polls/5/vote/
    path("<int:question_id>/vote/", views.vote, name="vote"),
]