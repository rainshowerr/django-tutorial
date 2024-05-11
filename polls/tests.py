from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

import datetime

from .models import Question

# Create your tests here.
class QuestionModelTests(TestCase): #TestCase 클래스 상속
	# 메서드 이름이 test로 시작해야 하는듯
	def test_was_publiched_recently_with_old_question(self):
		time = timezone.now() - datetime.timedelta(days=1, seconds=1)
		old_question = Question(pub_date=time)
		self.assertIs(old_question.was_published_recently(), False)
	def test_was_published_recently_with_future_question(self):
		time = timezone.now() + datetime.timedelta(days=30)
		future_question = Question(pub_date=time)
		# 주어진 두 값이 동일한 객체인지 확인
		self.assertIs(future_question.was_published_recently(), False)
	def test_was_publiched_recently_with_recent_question(self):
		time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
		recent_question = Question(pub_date=time)
		self.assertIs(recent_question.was_published_recently(), True)

def create_question(question_text, days):
	time = timezone.now() + datetime.timedelta(days=days)
	return Question.objects.create(question_text=question_text, pub_date=time)

# django.test.TestCase 클래스는 선언 메소드(assertEqual 등등) 제공
class QuestionIndexViewTests(TestCase):
	def test_no_questions(self):
		# reverse : 링크의 하드코딩을 방지해주는 함수 (app:name 형식인듯)
		response = self.client.get(reverse("polls:index"))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "No polls are available.")
		self.assertQuerySetEqual(response.context["latest_question_list"], [])

	def test_past_question(self):
		question = create_question(question_text="Past question.", days=-30)
		response = self.client.get(reverse("polls:index"))
		self.assertQuerySetEqual(response.context["latest_question_list"], [question],)

	def test_future_question(self):
		question = create_question(question_text="Past question.", days=30)
		response = self.client.get(reverse("polls:index"))
		self.assertContains(response, "No polls are available.")
		self.assertQuerySetEqual(response.context["latest_question_list"], [],)

	def test_future_question_and_past_question(self):
		question = create_question(question_text="Past question.", days=-30)
		create_question(question_text="Future question.", days=30)
		response = self.client.get(reverse("polls:index"))
		self.assertQuerySetEqual(
			response.context["latest_question_list"],
			[question],
		)

	def test_two_past_questions(self):
		question1 = create_question(question_text="Past question 1.", days=-30)
		question2 = create_question(question_text="Past question 2.", days=-5)
		response = self.client.get(reverse("polls:index"))
		self.assertQuerySetEqual(
			response.context["latest_question_list"],
			[question2, question1],
		)

class QuestionDetailViewTests(TestCase):
	def test_future_question(self):
		# 사용자가 url을 추측하여 접근했을 때에도 미래 질문이 나타나지 않아야함
		future_question = create_question(question_text="Future question.", days=5)
		url = reverse("polls:detail", args=(future_question.id,))
		response = self.client.get(url)
		self.assertEqual(response.status_code, 404)

	def test_past_question(self):
		past_question = create_question(question_text="Past Question.", days=-5)
		url = reverse("polls:detail", args=(past_question.id,))
		response = self.client.get(url)
		self.assertContains(response, past_question.question_text)