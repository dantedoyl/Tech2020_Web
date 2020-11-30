from django.db import models
from django.contrib.auth.models import User


def avatar_upload_to(instance, filename):
    return 'avatars/{}/{}'.format(instance.user.id, filename)


class ProfileManager(models.Manager):
    def popular_users(self):
        content = {}
        for obj in self.all():
            content[obj.user.username] = obj.rating()
        return [k for k, v in sorted(content.items(), key=lambda item: item[1], reverse=True)][:8]


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=128, unique=True, verbose_name='Nickname')
    avatar = models.ImageField(upload_to=avatar_upload_to, default='/avatars/default_avatar/av.png', verbose_name='Аватар')
    objects = ProfileManager()

    def __str__(self):
        return self.nickname

    def rating(self):
        return Question.objects.by_author(self.user_id) + Answer.objects.by_author(self.user_id)

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"


class TagManager(models.Manager):
    def popular_tags(self):
        content = {}
        for obj in self.all():
            content[obj.name] = Question.objects.by_tag(tag=obj.name).count()
        return [k for k, v in sorted(content.items(), key=lambda item: item[1], reverse=True)][:8]


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Имя')

    objects = TagManager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"


class QuestionManager(models.Manager):
    def new(self):
        return self.order_by('-date_create')

    def hot(self):
        content = {}
        for obj in self.all():
            content[obj] = obj.rating()
        return [k for k, v in sorted(content.items(), key=lambda item: item[1], reverse=True)][:8]

    def by_tag(self, tag):
        return self.filter(tags__name=tag)

    def get(self, id):
        return self.filter(id=id)

    def by_author(self, author_id):
        return self.filter(author__user_id=author_id).count()


class Question(models.Model):
    title = models.CharField(max_length=128, verbose_name='Title')
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name='Author')
    date_create = models.DateTimeField(auto_now_add=True, verbose_name='Creation date')
    text = models.TextField(verbose_name='Text')
    tags = models.ManyToManyField(Tag, blank=True, verbose_name='Tags')

    objects = QuestionManager()

    def __str__(self):
        return self.title

    def rating(self):
        return LikeQuestion.objects.by_question(question_id=self.id).filter(
            state=True).count() - LikeQuestion.objects.by_question(question_id=self.id).filter(state=False).count()

    def question_tags(self):
        return self.tags.all()

    class Meta:
        verbose_name = "Question"
        verbose_name_plural = "Questionss"


class AnswerManager(models.Manager):
    def by_question(self, question_id):
        return self.filter(question__id=question_id)

    def answers_count(self, question_id):
        return self.filter(question__id=question_id).count()

    def by_author(self, author_id):
        return self.filter(author__user_id=author_id).count()


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name='Question')
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name='Author')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Creation date')
    text = models.TextField(verbose_name='Text')
    is_correct = models.BooleanField(default=False, verbose_name='Correct')

    objects = AnswerManager()

    def __str__(self):
        return 'Ответ на вопрос: {}'.format(self.question.title)

    def rating(self):
        return LikeAnswer.objects.by_answer(answer_id=self.id).filter(
            state=True).count() - LikeAnswer.objects.by_answer(answer_id=self.id).filter(state=False).count()

    class Meta:
        verbose_name = "Answer"
        verbose_name_plural = "Answers"


class LikeQuestionManager(models.Manager):
    def by_question(self, question_id):
        return self.filter(question__id=question_id)


class LikeQuestion(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name='Пользователь, который поставил отметку')
    state = models.BooleanField( null=True, default=None, verbose_name='Состояние отметки')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name='Вопрос')

    objects = LikeQuestionManager()

    class Meta:
        verbose_name = "LikeQuestion"
        verbose_name_plural = "LikeQuestions"


class LikeAnswerManager(models.Manager):
    def by_answer(self, answer_id):
        return self.filter(answer__id=answer_id)


class LikeAnswer(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name='Пользователь, который поставил отметку')
    state = models.BooleanField(null=True, default=None, verbose_name='Состояние отметки')
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, verbose_name='Ответ')

    objects = LikeAnswerManager()

    class Meta:
        verbose_name = "LikeAnswer"
        verbose_name_plural = "LikeAnswers"
