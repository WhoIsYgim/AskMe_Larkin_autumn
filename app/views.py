from django.shortcuts import render
from app import models
from django.core.paginator import Paginator


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
        "name": f"Tag#{i}",
        "t_num": i
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
    page = request.GET.get('page')
    content = paginator.get_page(page)
    return content


def profile(request, i: int):
    user = models.Profile.objects.get_user_by_id(i)
    return render(request, 'profile.html', {"tags": TAGS, "questions": QUESTIONS, "user": user})


def index(request):
    content = pagination(QUESTIONS, request)
    return render(request, 'index.html', {"questions": content, "tags": TAGS})


def ask(request):
    return render(request, 'ask.html', {"tags": TAGS})


def question(request, i: int):
    return render(request, 'question.html', {"question": QUESTIONS[i - 1], "tags": TAGS})


def answer(request, i: int, j: int):
    return render(request, 'answer.html', {"question": QUESTIONS[i - 1], "answer": QUESTIONS[i - 1].answers[j]})


def tag(request, title: str):
    return render(request, 'questions_for_tag.html', {"tag": TAGS[int(title) - 1], "questions": QUESTIONS, "tags": TAGS})


def login(request):
    return render(request, 'login.html', {"tags": TAGS})


def register(request):
    return render(request, 'regster.html', {"tags": TAGS})
