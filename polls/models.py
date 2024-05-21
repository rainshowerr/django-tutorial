import datetime
from django.db import models
from django.utils import timezone
from django.contrib import admin


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")
    def __str__(self):
        return self.question_text
    # 이거 중간에 넣어야 작동하네
    # 관리자 폼 커스터마이징하는건데 데코레이터를 모델에 넣는 게 신기하당
    @admin.display(
        boolean=True,
        ordering="pub_date", # 내가 만든 메서드의 ordering 기능은 제공되지 않음. 여기선 클릭하면 pub_date 기준으로 ordering되게 설정함.
        description="Published recently?",
    )
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    # 메서드 추가 (Choice.objects.all()리턴값 보기 편하게)
    def __str__(self):
        return self.choice_text