from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib import auth
from app import models
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

from .forms import LoginForm, RegistrationForm, AskForm

PAGINATION_SIZE = 10


def pagination(objects, request):
    paginator = Paginator(objects, PAGINATION_SIZE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return page


def create_content_right():
    content = {
        "tags": models.Tag.objects.get_hot_tags(),
        "users": models.Profile.objects.get_top_users(),
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
    try:
        content["question"] = models.Question.objects.get(id=i)
    except Exception:
        return render(request, 'not_found.html', create_content_right())

    return render(request, 'question.html', content)


def tag(request, title: str):
    content = create_content(models.Question.objects.get_questions_for_tag(title), request)
    try:
        content["tag"] = models.Tag.objects.get_tag_by_title(title)
    except Exception:
        return render(request, 'not_found.html', create_content_right())

    return render(request, 'questions_for_tag.html', content)


def profile(request, i: int):
    content = create_content(models.Question.objects.get_questions_for_user(i), request)
    content["user"] = models.Profile.objects.get_user_by_id(i)
    return render(request, 'profile.html', content)


@login_required(redirect_field_name="login")
def profile_edit(request):
    return render(request, 'profile_edit.html', )


@login_required(redirect_field_name="login")
def ask(request):
    if request.method == 'POST':
        ask_form = AskForm(request.POST)
        if ask_form.is_valid():
            quest = models.Question.objects.create(
                title=ask_form.cleaned_data['title'],
                text=ask_form.cleaned_data['text'],
                author=models.Profile.objects.get(user=request.user)
            )
            quest.save()
            for tag_ in ask_form.cleaned_data['tags'].split(' '):
                to_add = models.Tag.objects.get_or_create(title=tag_)
                quest.tags.add(to_add[0].id)
            quest.save()
            if quest:
                return redirect("single_q", i=quest.id)

    elif request.method == 'GET':
        ask_form = AskForm()

    content = create_content_right()
    content['form'] = ask_form
    return render(request, 'ask.html', content)


def login_view(request):
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
        user_form = LoginForm()

    content = create_content_right()
    content["form"] = user_form
    return render(request, 'login.html', content)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def register(request):
    if request.method == 'POST':
        user_form = RegistrationForm(data=request.POST)
        if user_form.is_valid():
            user = user_form.save()
            if user:
                login(request, user)
                return redirect(reverse('index'))
            else:
                return redirect(reverse('register'))
    elif request.method == 'GET':
        user_form = RegistrationForm()

    content = create_content_right()
    content["form"] = user_form
    return render(request, 'register.html', content)
