from django.shortcuts import render, redirect, reverse, get_object_or_404, get_list_or_404
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from app.models import Question, Answer, Profile,Tag
from django.contrib import auth
from app.forms import LoginForm, AskForm, RegistrForm, SettingsForm, AnswerForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError

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


def index(request):
    return render(request, 'index.html', {
        'title': 'New questions',
        'questions': pagination(Question.objects.new(), request),
    })


def hot(request):
    return render(request, 'index.html', {
        'title': 'Hot questions',
        'questions': pagination(Question.objects.hot(), request),
    })


def tag(request, tag):
    request.session['redirect'] = request.path
    return render(request, 'index.html', {
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
    print(request.session['redirect'])
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
            print(answer_pages)
            return redirect(request.path + '?page='+str(answer_pages))
    return render(request, 'question.html', {
        'title': f'Question {id}',
        'questions': question,
        'answers': pagination(Answer.objects.by_question(id), request, per_page=3),
        'form': form,
    })
