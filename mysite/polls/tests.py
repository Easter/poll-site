import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from .models import Question
from django.test.client import Client
from django.test.utils import setup_test_environment

# Create your tests here.
def creat_question(question_text,days):
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text,pub_date=time)


class QuestionModelsTest(TestCase):
    '''检测未来的问题是否返回Ture,我们期望返回的是false
        python manage.py test polls 会在polls里面寻找测试代码
        然后找到了django.test.TestCase的子类
        创建了一个特殊的数据库供测试使用
        再这个里面找到了以test开头的方法
        在测试方中创建了一个pub_date值为30天后的Question实例
        接着使用assertIs方法，发现was_published_recently()方法返回的是Ture，而我们预期的是False
    '''

    def test_was_published_recently_with_future_question(self):
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(),False)

    def test_was_published_recently_with_old_question(self):
        time = timezone.now() - datetime.timedelta(days=1,seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(),False)

    def test_was_published_recently_with_recent_question(self):
        time = timezone.now() - datetime.timedelta(hours=23,minutes=59,seconds=59)
        recently_question = Question(pub_date=time)
        self.assertIs(recently_question.was_published_recently(),True)

class QuestionIndexTest(TestCase):
    def test_no_question(self):
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code,200)
        self.assertContains(response,"No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'],[])

    def test_past_question(self):
        creat_question(question_text="Past question?",days=-30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context['latest_question_list'],['<Question: Past question?>'])

    def test_future_question(self):
        creat_question(question_text="Future question?",days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

class QuestionDetailTest(TestCase):
    def test_future_question(self):
        Future_question = creat_question(question_text="Future question?",days=30)
        response = self.client.get(reverse("polls:detail",args=(Future_question.id,)))
        self.assertEqual(response.status_code,404)
    def test_past_question(self):
        Past_question = creat_question(question_text="Past question?",days=-30)
        response = self.client.get(reverse("polls:detail",args=(Past_question.id,)))
        self.assertContains(response,Past_question.question_text)
