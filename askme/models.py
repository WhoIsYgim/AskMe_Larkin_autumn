from django.db import models
from django.contrib.auth.models import User


class QuestionManager(models.Manager):
    def get_hot_questions(self):
        return


class Question(models.Model):
    objects = QuestionManager()
    title = models.CharField


class AnswerManager(models.Manager):
    def get_question_answer(self, question_id):
        return


class Answer(models.Model):
    objects = AnswerManager()


class LikeManger(models.Manager):
    def get_question_likes_count(self, question_id):
        return


class Like(models.Model):
    objects = LikeManger()


class ProfileManager(models.Manager):
    def get_profile_by_id(self, profile_id):
        return


class Profile(User):
    objects = ProfileManager
