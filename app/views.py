from django.shortcuts import render
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator


tags_users = {
    'tags': ['tag1', 'tag2', 'tag3', 'tag4', 'tag5', 'tag6', 'tag7', 'tag8'],
    'users': ['mr greeman', 'dr house', 'bender', 'queen victoria', 'pupkin'],
}
colours = ['primary', 'secondary', 'success', 'danger', 'warning', 'info', 'light', 'dark']
def col(colours):
    for colour in colours:
        yield colour

for Type in tags_users:
    zip(colours, tags_users['tags'])

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

questions = []
for i in range(1, 20):
    questions.append({
        'title': str(i),
        'author': 'author ' + str(i),
        'date': 'date ' + str(i),
        'id': i,
        'answer': str(i),
        'tags': ['tag' + str(i), 'tag' + str(i + 1)],
        'rating': str(i),
        'text': 'text ' + str(i)
    })


answers = []
for i in range(1, 30):
    answers.append({
        'author': 'author ' + str(i),
        'date': 'date ' + str(i),
        'id': i,
        'question_id': (i % 5)+1,
        'is_correct': True,
        'text': 'text ' + str(i)
    })


def index(request):
    content = pagination(questions, request)
    return render(request, 'index.html', {
        'title': 'New questions',
        'user_login': user,
        'questions': content,
        'colours': col(colours),
        **tags_users
    })

def hot(request):
    content = pagination(questions, request)
    return render(request, 'index.html', {
        'title': 'Hot questions',
        'user_login': False,
        'questions': content,
        'colours': col(colours),
        'colours': col(colours),
        **tags_users
    })

def findTag(val, tag1):
    content = []
    for q in val:
        for ctag in q['tags']:
            if ctag == tag1:
                content.append(q)

    return content

def tag(request, tag):
    content = pagination(findTag(questions, tag), request)
    return render(request, 'index.html', {
        'title': f'Tag: {tag}',
        'user_login': user,
        'questions': content,
        'colours': colours,
        **tags_users
    })

def ask(request):
    return render(request, 'ask.html', {
        'title': 'ask',
        'user_login': user,
        'colours': col(colours),
        **tags_users
    })

def registr(request):
    return render(request, 'signup.html', {
        'title': 'registr',
        'user_login': False,
        'colours': col(colours),
        **tags_users
    })
def login(request):
    return render(request, 'login.html', {
        'title': 'login',
        'user_login': False,
        'colours': col(colours),
        **tags_users
    })

def settings(request):
    return render(request, 'settings.html', {
        'title': 'settings',
        'user_login': user,
        'colours': col(colours),
        **tags_users
    })

def findById(questions, id):
    content = []
    for question in questions:
        if question['id'] == id:
            content.append(question)

    return content

def findAnswers(answers, id):
    content = []
    for answer in answers:
        if answer['question_id'] == id:
            content.append(answer)

    return content


def question(request, id):
    content = findById(questions, id)
    answer = pagination(findAnswers(answers, id), request, per_page=3)
    return render(request, 'question.html', {
        'title': f'Question {id}',
        'user_login': user,
        'questions': content,
        'answers': answer,
        'colours': col(colours),
        **tags_users
    })