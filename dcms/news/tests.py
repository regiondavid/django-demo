# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.utils import timezone
from django.test import TestCase
from django.urls import reverse

from .models import Question
# Create your tests here.
class QuestionMethodTest(TestCase):
    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() should return False for question whose pub_date is in future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() should return False for question whose pub_date is in old.
        """
        time = timezone.now() - datetime.timedelta(days=30)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was
        """
        time = timezone.now() - datetime.timedelta(hours=1)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

def create_question(question_text, days):
    """
    Create a question
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)

class QuestionViewTests(TestCase):
    def test_index_with_no_question(self):
        """
        if not questions exits, an appropriate message should be display
        """
        response = self.client.get(reverse('news:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No news are avalible")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_index_view_with_a_past_question(self):
        """
        question with a pub_date
        """
        create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse('news:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [u'<Question: Past question.>']
        )

    def test_index_view_with_a_future_question(self):
        """
        question with a pub_date in the future
        """
        create_question(question_text="Future question", days=30)
        response = self.client.get(reverse('news:index'))
        self.assertContains(response, "No news are avalible")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_index_view_with_future_question_and_past_quesiton(self):
        create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('news:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [u'<Question: Past question.>']
        )
    def test_index_view_with_two_past_question(self):
        create_question(question_text="Past question 1.", days=-30)
        create_question(question_text="Past question 2.", days=-10)
        response = self.client.get(reverse('news:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [u'<Question: Past question 2.>', u'<Question: Past question 1.>']
        )