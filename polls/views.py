from django.db.models import F
from django.shortcuts import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic
from django.utils import timezone

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

    def get_queryset(self):
        """Return the last five published questions."""
        # lte : less than or equal to 조건연산자
        # __ : Django ORM에서 사용되는 특별한 구문
        # 필드 이름과 비교 연산자를 결합하여 특정 조건을 나타냄
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]

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

    # 아직 발행되지 않은 미래 질문이 나타나지 않도록 함
    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())

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

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.method == 'POST' and 'Reset' in request.POST:
        for choice in question.choice_set.all():
            choice.votes = 0
            choice.save()
    return render(request, "polls/results.html", {"question":question})

def add(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        choice_text = request.POST['choice_text']
    # request.POST가 사전 형식이라서 KeyError처리 해워쟈함
    except KeyError:
        return render(
            request,
            "polls/add.html",
            {
                "question":question,
                "error_message":"Choice cannot be empty.",
            },
        )
    else:
        if choice_text:
            question.choice_set.create(choice_text=choice_text)
            return HttpResponseRedirect(reverse('polls:detail', args=(question_id,)))
        # choice가 비어있는 경우
        return render(
            request,
            "polls/add.html",
            {
                "question":question,
                "error_message":"Choice cannot be empty.",
            },
        )
