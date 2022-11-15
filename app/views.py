from django.shortcuts import render
from app import models
from django.core.paginator import Paginator
from django.db.models import Count, Subquery


ANSWERS = [
    {
        "text": f"# {i} ANSWER text",
        "a_num": i,
        "is_true": True if i % 2 != 0 else False
    } for i in range(1, 4)
]

QUESTIONS = [
    {
        "title": f"Question №{i}",
        "text": f"# {i} Question text",
        "q_num": i,
        "answers": [ANSWERS[0], ANSWERS[1]]
    } for i in range(1, 100)
]

TAGS = [
    {
        "title": f"Tag#{i}",
        "id": i
    } for i in range(1, 10)
]

USERS = [
    {
        "nickname": "user",
        "answers": i,
        "reg_date": f"01.01.201{i}"
    } for i in range(1, 10)
]

PAGINATION_SIZE = 10


def pagination(objects, request):
    paginator = Paginator(objects, PAGINATION_SIZE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return page


def create_content_right():
    content = {
               "tags": models.Tag.objects.get_hot_tags(),
               "users": models.Profile.objects.get_top_users()
               }
    return content


def create_content(objects, request):
    page = pagination(objects, request)
    content = create_content_right()
    content["content"] = page
    return content


def index(request):
    return render(request, 'index.html', create_content(models.Question.objects.get_hot_questions(), request))


def recent(request):
    return render(request, 'questions_recent.html', create_content(models.Question.
                                                                   objects.get_recent_questions(), request))


def question(request, i: int):
    content = create_content(models.Answer.objects.get_answers_for_question(i), request)
    content["question"] = models.Question.objects.get(id=i)
    return render(request, 'question.html', content)


def tag(request, title: str):
    content = create_content(models.Question.objects.get_questions_for_tag(title), request)
    content["tag"] = models.Tag.objects.get_tag_by_title(title)
    return render(request, 'questions_for_tag.html', content)


def profile(request, i: int):
    content = create_content(models.Question.objects.get_questions_for_user(i), request)
    content["user"] = models.Profile.objects.get_user_by_id(i)
    return render(request, 'profile.html', content)


def ask(request):
    return render(request, 'ask.html', create_content_right())


def login(request):
    return render(request, 'login.html', create_content_right())


def register(request):
    return render(request, 'register.html', create_content_right())
