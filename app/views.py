from django.shortcuts import render
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from app.models import Question, Answer


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
        'user_login': user,
        'questions': pagination(Question.objects.new(), request),
    })

def hot(request):
    return render(request, 'index.html', {
        'title': 'Hot questions',
        'user_login': False,
        'questions': pagination(Question.objects.hot(), request),
    })

def tag(request, tag):
    return render(request, 'index.html', {
        'title': f'Tag: {tag}',
        'user_login': user,
        'questions': pagination(Question.objects.by_tag(tag=tag), request),
    })

def ask(request):
    return render(request, 'ask.html', {
        'title': 'ask',
        'user_login': user,
    })

def registr(request):
    return render(request, 'signup.html', {
        'title': 'registr',
        'user_login': False,
    })
def login(request):
    return render(request, 'login.html', {
        'title': 'login',
        'user_login': False,
    })

def settings(request):
    return render(request, 'settings.html', {
        'title': 'settings',
        'user_login': user,
    })

def question(request, id):
    return render(request, 'question.html', {
        'title': f'Question {id}',
        'user_login': user,
        'questions': Question.objects.by_id(id),
        'answers': pagination(Answer.objects.by_question(id), request, per_page=3),
    })
