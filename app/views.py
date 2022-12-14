from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate
from django.contrib import auth
from app import models
from django.core.paginator import Paginator
from django.db.models import Count, Subquery

from .forms import LoginForm

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
    user_form = "dummy"
    if request.method == 'POST':
        user_form = LoginForm(data=request.POST)
        if user_form.is_valid():
            user = authenticate(request, **user_form.cleaned_data)
            if user:
                auth.login(request, user)
                return redirect(reverse('index'))
            else:
                user_form.add_error(field=None, error="Wrong Login/Password")
    elif request.method == 'GET':
        user_from = LoginForm()

    content = create_content_right()
    content["form"] = user_form
    return render(request, 'login.html', content)


def register(request):
    return render(request, 'register.html', create_content_right())
