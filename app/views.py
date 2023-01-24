from django.forms import model_to_dict
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib import auth
from django.views.decorators.http import require_POST

from app import models
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

from .forms import LoginForm, RegistrationForm, AskForm, AnswerForm, EditForm

PAGINATION_SIZE = 10
top_users = models.Profile.objects.all()[:10]
top_tags = models.Tag.objects.all()[:10]


def pagination(objects, request):
    paginator = Paginator(objects, PAGINATION_SIZE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return page


def create_content_right():
    content = {
        "tags": top_tags,
        "users": top_users,
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
    if request.method == 'GET':
        form = AnswerForm()
    elif request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect(reverse('login_page'))
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = models.Answer.objects.create(text=form.cleaned_data['text'],
                                                  question=models.Question.objects.get(id=i),
                                                  author=models.Profile.objects.get(user_id=request.user.id))
            answer.save()
            if answer:
                return redirect(reverse("single_q", args=[i]))

    content = create_content(models.Answer.objects.get_answers_for_question(i), request)
    try:
        content["question"] = models.Question.objects.get(id=i)
    except Exception:
        return render(request, 'not_found.html', create_content_right())

    content['form'] = form

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


@login_required(login_url='login_page', redirect_field_name="continue")
def profile_edit(request):
    if request.method == 'GET':
        initial_data = model_to_dict(request.user)
        initial_data['avatar'] = request.user.profile_related.avatar
        initial_data['bio'] = request.user.profile_related.bio
        form = EditForm(initial=initial_data)
    elif request.method == 'POST':
        form = EditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect(reverse("profile_edit"))

    content = create_content_right()
    content['form'] = form
    return render(request, 'profile_edit.html', content)


@login_required(login_url='login_page', redirect_field_name="continue")
def ask(request):
    if request.method == 'POST':
        ask_form = AskForm(request.POST)
        if ask_form.is_valid():
            # TODO form.save()
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
        user_form = RegistrationForm(data=request.POST, files=request.FILES)
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


@require_POST
@login_required(login_url='login_page', redirect_field_name="continue")
def like_question(request):
    quest_id = request.POST['question_id']
    quest = models.Question.objects.get(id=quest_id)
    try:
        like = models.LikeQ.objects.get(question_id=quest_id, user_id=request.user.profile_related.id)
    except models.LikeQ.DoesNotExist:
        like = models.LikeQ.objects.create(question=quest, user=request.user.profile_related)
        like.save()
    else:
        like.delete()

    quest.save()
    return JsonResponse(
        {'status': 'ok',
         'likes_count': quest.get_like_count()})


@require_POST
@login_required(login_url='login_page', redirect_field_name="continue")
def like_answer(request):
    answer_id = request.POST['answer_id']
    answer = models.Answer.objects.get(id=answer_id)
    try:
        like = models.LikeA.objects.get(answer_id=answer_id, user_id=request.user.profile_related.id)
    except models.LikeA.DoesNotExist:
        like = models.LikeA.objects.create(answer=answer, user=request.user.profile_related)
        like.save()
    else:
        like.delete()
    answer.save()
    return JsonResponse(
        {'status': 'ok',
         'likes_count': answer.get_like_count()})


@require_POST
@login_required(login_url='login_page', redirect_field_name="continue")
def correct(request):
    answer_id = request.POST['answer_id']
    answer = models.Answer.objects.get(id=answer_id)
    if answer.question.get_author_id() != request.user.id:
        JsonResponse(
            {'status': 'forbidden'})
        return
    answer.solution = not answer.is_solution()
    answer.save()
    return JsonResponse(
            {'status': 'ok',
             'solution': f'{answer.is_solution()}'}
        )
