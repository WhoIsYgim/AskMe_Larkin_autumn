from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User


# Managers

class QuestionManager(models.Manager):

    def get_hot_questions(self):



    def get_recent_questions(self):



    def get_questions_for_tag(self, tag_id):



    def get_questions_for_user(self, user_id):



class AnswerManager(models.Manager):

    def get_answers_for_question(self, q_id):



class TagManager(models.Manager):

    def get_hot_tags(self):


    def get_question_tags(self, q_id):


class ProfileManager(models.Manager):


class LikeManager(models.Manager):

# Models


class Profile(models.Model):
    objects = ProfileManager()

    user = models.OneToOneField(User, null=True, related_name='profile_related', on_delete=models.CASCADE)
    avatar = models.ImageField(null=True, blank=True, default='default.png', upload_to='avatar/%y/%m/%d')
    reg_date = models.DateField(auto_now=True)
    answers = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.user.username


class Tag(models.Model):
    objects = TagManager()

    title = models.CharField()
    def __str__(self):
        return self.title


class Like(models.Model):
    objects = LikeManager()

    user = models.ForeignKey(Profile)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()

    like_object = GenericForeignKey('content_type', 'object_id')


class Question(models.Model):
    objects = QuestionManager()

    author = models.ForeignKey(Profile, on_delete=models.CASCADE, null = False)
    tags = models.ManyToManyField(Tag)
    date = models.DateTimeField(auto_now=True)
    title = models.CharField()
    text = models.TextField()
    like = GenericRelation(Like)

    def __str__(self):
        return self.title


class Answer(models.Model):
    objects = AnswerManager()

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, null = False)
    date = models.DateTimeField(auto_now=True)
    text = models.TextField()
    solution = models.BooleanField(default=False)
    like = GenericRelation(Like)

    def __str__(self):
        return f"{self.question.title}_answer"
