from django.db import models
from django.db.models import Count, Case, When
from django.contrib.auth.models import User


# Managers

class QuestionManager(models.Manager):
    def get_hot_questions(self):
        return self.annotate(count=Count('likeq', distinct=True)).order_by('-count')

    def get_recent_questions(self):
        return self.all().order_by('-date')

    def get_questions_for_tag(self, tag_id):
        return self.filter(tag__id=tag_id)

    def get_questions_for_user(self, user_id):
        return self.filter(author_id=user_id)


class AnswerManager(models.Manager):
    def get_answers_for_question(self, a_id):
        return self.filter(answer_id=a_id)


class TagManager(models.Manager):
    def get_tag_by_id(self, tag_id):
        return self.filter(id=tag_id)

    def get_hot_tags(self):
        return self.all().annotate(count=Count('question')).order_by('-count')[:9]

    def get_question_tags(self, q_id):
        return self.filter(question__id=q_id)


class ProfileManager(models.Manager):
    def get_top_users(self):
        return self.all().annotate(rating=0.3 * Count('answer') + Count(
            Case(When(answer__correct=True, then=1))) + 0.1 * Count('question')).order_by('-rating')[:10]

    def get_user_by_id(self, u_id):
        return self.get(id=u_id)


class LikeQManager(models.Manager):
    def get_likes_count_for_question(self, q_id):
        likes = self.filter(question_id=q_id)
        return likes.count()


class LikeAManager(models.Manager):
    def get_likes_count_for_answer(self, a_id):
        return self.count(answer_id=a_id)


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

    title = models.CharField(max_length=30)

    def __str__(self):
        return self.title


class Question(models.Model):
    objects = QuestionManager()

    author = models.ForeignKey(Profile, null=False, on_delete=models.CASCADE)
    tag = models.ManyToManyField(Tag)
    date = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=30)
    text = models.TextField()

    def get_likes(self):
        return self.objects.filter(like__id=self.id)

    def __str__(self):
        return self.title


class Answer(models.Model):
    objects = AnswerManager()

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, null=False)
    date = models.DateTimeField(auto_now=True)
    text = models.TextField()
    solution = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.question.title}_answer"


class LikeQ(models.Model):
    objects = LikeQManager()

    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)


class LikeA(models.Model):
    objects = LikeAManager()

    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
