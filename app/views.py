from django.shortcuts import render, redirect, reverse, get_object_or_404, get_list_or_404
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from app.models import Question, Answer, Profile, Tag, LikeAnswer, LikeQuestion
from django.contrib import auth
from app.forms import LoginForm, AskForm, RegistrForm, SettingsForm, AnswerForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.template.defaulttags import register


user = True


def pagination(object_list, request, per_page=5):
    p = request.GET.get('page')
    paginator = Paginator(object_list, per_page)

    try:
        content = paginator.page(p)
    except PageNotAnInteger:
        content = paginator.page(1)
    except EmptyPage:
        content = paginator.page(paginator.num_pages)

    return content

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


def index(request):
    user_likes = {}
    if request.user.is_authenticated:
        user_likes = LikeQuestion.objects.authors_reaction(request.user.profile.id)
    return render(request, 'index.html', {
        'user_reaction': user_likes,
        'title': 'New questions',
        'questions': pagination(Question.objects.new(), request),
    })


def hot(request):
    user_likes = {}
    if request.user.is_authenticated:
        user_likes = LikeQuestion.objects.authors_reaction(request.user.profile.id)
    return render(request, 'index.html', {
        'user_reaction': user_likes,
        'title': 'Hot questions',
        'questions': pagination(Question.objects.hot(), request),
    })


def tag(request, tag):
    user_likes = {}
    if request.user.is_authenticated:
        user_likes = LikeQuestion.objects.authors_reaction(request.user.profile.id)
    return render(request, 'index.html', {
        'user_reaction': user_likes,
        'title': f'Tag: {tag}',
        'questions': pagination(Question.objects.by_tag(tag=tag), request),
    })


@login_required
def ask(request):
    if request.method == 'GET':
        form = AskForm()
    else:
        form = AskForm(data=request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user.profile
            question.save()
            for tag in form.cleaned_data['tags'].split(' '):
                try:
                    tag_id = Tag.objects.get(name=tag).id
                except Tag.DoesNotExist:
                    tag_id = Tag.objects.create(name=tag).id
                question.tags.add(tag_id)
            return redirect(reverse('question', kwargs={'id': question.id}))
    return render(request, 'ask.html', {
        'form': form,
        'title': 'ask',
    })


def registr(request):
    error = None
    if request.method == 'GET':
        form = RegistrForm()
    else:
        form = RegistrForm(data=request.POST)
        if Profile.objects.filter(nickname=request.POST.get('nickname')).count() == 0:
            if form.is_valid():
                form.save()
                auth_data = {
                    'username': form.cleaned_data['username'],
                    'password': form.cleaned_data['password1']
                }
                user = auth.authenticate(request, **auth_data)
                if user is not None:
                    auth.login(request, user)
                profile_info = {
                            'user': request.user,
                }
                if form.cleaned_data['nickname'] is not None:
                    profile_info['nickname'] = form.cleaned_data['nickname']
                else:
                    profile_info['nickname'] = form.cleaned_data['username']
                if request.FILES.get('photo'):
                    profile_info['avatar'] = request.FILES.get('photo')
                new_profile = Profile.objects.create(**profile_info)
                return redirect('/')
        else:
            error = True
    return render(request, 'signup.html', {
        'error': error,
        'form': form,
        'title': 'registr',
    })


def login(request):
    error = None
    if request.method == 'GET':
        form = LoginForm()
        if request.GET.get('next') is not None:
            request.session['redirect'] = request.GET.get('next')
        else:
            request.session['redirect'] = '/'
    else:
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = auth.authenticate(request, **form.cleaned_data)
            if user is not None:
                auth.login(request, user)
                redirect_path = request.session['redirect']
                request.session.pop('redirect')
                return redirect(redirect_path)
            else:
                error = True
    return render(request, 'login.html', {
        'error': error,
        'form': form,
        'title': 'login',
    })

@login_required
def logout(request):
    auth.logout(request)
    return redirect(request.GET.get('next'))


@login_required
def settings(request):
    if request.method == 'GET':
        form = SettingsForm(instance=request.user)
        profile_form = SettingsForm(instance=request.user.profile)
    else:
        form = SettingsForm(data=request.POST, instance=request.user)
        profile_form = SettingsForm(data=request.POST, instance=request.user.profile)
        if form.is_valid():
            user = form.save()
            if request.FILES.get('photo'):
                user.profile.avatar = request.FILES.get('photo')
            profile_form.save()
    return render(request, 'settings.html', {
        'profile_form': profile_form,
        'form': form,
        'title': 'settings',
    })


@login_required
def question(request, id):
    user_likes = {}
    if request.user.is_authenticated:
        user_likes = LikeQuestion.objects.authors_reaction(request.user.profile.id)
    user_likes_answer ={}
    if request.user.is_authenticated:
        user_likes_answer = LikeAnswer.objects.authors_reaction(request.user.profile.id)
    question = get_list_or_404(Question, id=id)
    if request.method == 'GET':
        form = AnswerForm()
    else:
        form = AnswerForm(data=request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.question = question[0]
            answer.author = request.user.profile
            answer.save()
            answer_pages = pagination(Answer.objects.by_question(id), request, per_page=3).paginator.num_pages
            return redirect(request.path + '?page='+str(answer_pages))
    return render(request, 'question.html', {
        'title': f'Question {id}',
        'questions': question,
        'user_reaction': user_likes,
        'user_reaction_answer': user_likes_answer,
        'answers': pagination(Answer.objects.by_question(id), request, per_page=3),
        'form': form,
    })

@require_POST
@login_required
def vote(request):
    data = request.POST
    reaction_data = {
        'user': request.user.profile,
        # 'question': Question.objects.get(id=data['id'])
    }
    if data['action'] == 'like':
        reaction_data['state'] = True
    else:
        reaction_data['state'] = False
    new_data = {
        'type': data['type'],
        'id': data['id'],
        'action': data['action']
    }

    if data['type'] == 'question':
        reaction_data['question'] = Question.objects.get(id=data['id'])
        LikeQuestion.objects.create(**reaction_data)
        new_data['rating'] = Question.objects.get(id=data['id']).rating()
    else:
        reaction_data['answer'] = Answer.objects.get(id=data['id'])
        LikeAnswer.objects.create(**reaction_data)
        new_data['rating'] = Answer.objects.get(id=data['id']).rating()
    return JsonResponse(new_data)

@require_POST
@login_required
def correct(request):
    data = request.POST
    answer = Answer.objects.get(id=data['id'])
    answer.is_correct = not answer.is_correct
    answer.save()
    return JsonResponse(data)