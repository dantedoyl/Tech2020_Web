from django.core.management.base import BaseCommand
from app.models import Question, Answer, Tag, Profile, LikeQuestion, LikeAnswer
from django.contrib.auth.models import User
from random import randint, choice, choices
from faker import Faker
from itertools import islice

f = Faker()

small = [100, 100, 1000, 10000, 5000, 15000]
medium = [1000, 1000, 10000, 100000, 50000, 150000]
large = [10000, 10000, 100000, 1000000, 500000, 1500000]


class Command(BaseCommand):
    help = 'Filling the database with some values'

    def add_arguments(self, parser):
        parser.add_argument('--db_size', type=str, help="DB size: small, medium, large")
        parser.add_argument('--users', type=int, help='Users count')
        parser.add_argument('--tags', type=int, help='Tags count')
        parser.add_argument('--questions', type=int, help='Questions count')
        parser.add_argument('--answers', type=int, help='Answers count')
        parser.add_argument('--likes_questions', type=int, help='Questions likes count')
        parser.add_argument('--likes_answers', type=int, help='Answers likes count')

    def obj_bulk_create(self, Obj, objs):
        batch_size = 10000

        while True:
            batch = list(islice(objs, batch_size))
            if not batch:
                break
            Obj.objects.bulk_create(batch, batch_size)

    def fill_users(self, cnt):
        if cnt is None:
            return False

        print('Filling {} users'.format(cnt))
        objs = (
            User(username=f.name() + str(i), email=f.email())
            for i in range(cnt)
        )
        self.obj_bulk_create(User, objs)
        print('End filling users')

        print('Start filling {} profiles'.format(cnt))
        users_id = list(User.objects.values_list('id', flat=True))
        objs = (
            Profile(user_id=users_id[i])
            for i in range(cnt)
        )
        self.obj_bulk_create(Profile, objs)
        print('End filling profiles')

    def fill_tags(self, cnt):
        if cnt is None:
            return False

        print('Filling {} tags'.format(cnt))

        objs = (
            Tag(name=f.word() + str(i))
            for i in range(cnt)
        )
        self.obj_bulk_create(Tag, objs)
        print('End filling tags')

    def fill_questions(self, cnt):
        if cnt is None:
            return False

        print('Filling {} questions'.format(cnt))

        authors = list(Profile.objects.values_list('id', flat=True))
        tags = list(Tag.objects.values_list('id', flat=True))

        objs = (
            Question(title=f.sentence()[:128], author_id=choice(authors), text=f.text())
            for i in range(cnt)
        )
        self.obj_bulk_create(Question, objs)
        print('End filling questions')

        print('Start filling {} question tags'.format(cnt))
        for item in Question.objects.all():
            item.tags.set(set(choices(tags, k=randint(1, 7))))

        print('End filling question tags')

    def fill_answers(self, cnt):
        if cnt is None:
            return False

        print('Filling {} answers'.format(cnt))

        authors = list(Profile.objects.values_list('id', flat=True))
        questions = list(Question.objects.values_list('id', flat=True))
        authors_rand = choices(authors, k=cnt)
        objs = (
            Answer(question_id=choice(questions), author_id=authors_rand[i], text=f.text())
            for i in range(cnt)
        )
        self.obj_bulk_create(Answer, objs)
        print('End filling answers')

    def fill_likes_questions(self, cnt):
        if cnt is None:
            return False

        print('Filling {} questions likes'.format(cnt))

        authors = list(Profile.objects.values_list('id', flat=True))
        questions = list(Question.objects.values_list('id', flat=True))
        questions_rand = choices(questions, k=cnt)
        mark_rand = choices([True, True, True, True, False], k=cnt)
        objs = (
            LikeQuestion(user_id=choice(authors), state=mark_rand[i], question_id=questions_rand[i])
            for i in range(cnt)
        )
        self.obj_bulk_create(LikeQuestion, objs)
        print('End filling questions likes')

    def fill_likes_answers(self, cnt):
        if cnt is None:
            return False

        print('Filling {} answers likes'.format(cnt))

        authors = list(Profile.objects.values_list('id', flat=True))
        answers = list(Answer.objects.values_list('id', flat=True))
        answers_rand = choices(answers, k=cnt)
        mark_rand = choices([True, True, True, True, False], k=cnt)

        objs = (
            LikeAnswer(user_id=choice(authors), state=mark_rand[i], answer_id=answers_rand[i])
            for i in range(cnt)
        )
        self.obj_bulk_create(LikeAnswer, objs)
        print('End filling answers likes')

    def handle(self, *args, **options):
        current = [options.get('users'),
                   options.get('tags'),
                   options.get('questions'),
                   options.get('answers'),
                   options.get('likes_questions'),
                   options.get('likes_answers')]


        if options.get('db_size') == 'small':
            current = small
        elif options.get('db_size') == 'medium':
            current = medium
        elif options.get('db_size') == 'large':
            current = large

        self.fill_users(current[0])
        self.fill_tags(current[1])
        self.fill_questions(current[2])
        self.fill_answers(current[3])
        self.fill_likes_questions(current[4])
        self.fill_likes_answers(current[5])