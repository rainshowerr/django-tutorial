from django.contrib import admin

from .models import Question, Choice

# question 등록시 choice도 등록할수있게
# admin.StackedInline은 공간 많이 잡아먹음
class ChoiceInline(admin.TabularInline):
	model = Choice
	extra = 3 # 기본으로 3가지 선택 항목 제공

class QuestionAdmin(admin.ModelAdmin):
	fieldsets = [
		# 각 튜플의 첫번째 요소는 fieldset의 제목
		(None, {"fields":["question_text"]}),
		("Date information", {"fields":["pub_date"]}),
	]
	inlines = [ChoiceInline]
	list_display = ["question_text", "pub_date", "was_published_recently"]
	list_filter = ["pub_date"] # 장고에서 적절한 date 필터링 기준을 제공함
	search_fields = ["question_text"]

admin.site.register(Question, QuestionAdmin)