from django.db.models import F
from django.shortcuts import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic

from .models import Choice, Question

# generic view : ListView와 DetailView

# Create your views here.
# def index(request):
#     latest_question_list = Question.objects.order_by("-pub_date")[:5]
#     context = {
#         "latest_question_list": latest_question_list,
#     }
#     # render(request 객체, 템플릿 이름, context 사전형 객체(optional))
#     # 인수로 지정된 context로 표현된 템플릿의 HttpResponse 객체가 반환됨
#     return render(request, "polls/index.html", context)

class IndexView(generic.ListView):
    # ListView는 기본적으로 <app name>/<model name>_list.html 템플릿 사용
    # 그러므로 template_name을 지정해서 바꿔줘야함
    template_name = "polls/index.html"
    # ListView는 기본적으로 question_list 컨텍스트 변수 제공
    # 그러므로 context_object_name을 따로 지정해서 덮어써줘야함
    context_object_name = "latest_question_list"

    # 다른애들은 model=Question 이런식으로 지정해주는데 얜 함수를 만들어서 가져오네
    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by("-pub_date")[:5]

# def detail(request, question_id):
#     # 정석
#     # try:
#     #     question = Question.objects.get(pk=question_id)
#     # except Question.DoesNotExist:
#     #     raise Http404("Question does not exist")
#     # shortcut
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, "polls/detail.html", {"question": question})

class DetailView(generic.DetailView):
    model = Question
    # DetailView는 기본적으로 <app name>/<model name>_detail.html 템플릿 사용
    # 그러므로 template_name을 지정해서 바꿔줘야함
    template_name = "polls/detail.html"
    # ListView는 기본적으로 question 컨텍스트 변수 제공
    # 그러므로 덮어써줄 필요 x

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(
            request,
            "polls/detail.html",
            {
                "question":question,
                "error_message":"You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes = F("votes") + 1 # F는 database의 vote count를 늘림
        selected_choice.save()
    # POST 데이터를 성공적으로 처리 한 후에는 항상 HttpResponse가 아닌 HttpResponseRedirect
    # reverse는 url을 하드코딩하지 않게 도와주는 함수
    return HttpResponseRedirect(reverse("polls:results", args=(question.id,))) # 콤마 안찍으니까 에러나네

# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, "polls/results.html", {"question":question})

class ResultView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"