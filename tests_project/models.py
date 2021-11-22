from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse_lazy
from model_utils.managers import InheritanceManager

User = get_user_model()


class Test(models.Model):
    title = models.CharField(max_length=250, verbose_name='Test name')
    questions_count = models.IntegerField()

    def get_absolute_url(self) -> str:
        return reverse_lazy('tests:test', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title

    def get_next_question(self, test_pk, question_pk):
        questions_pk = []
        for q in Test.objects.filter(pk=test_pk):
            questions_pk.append(q.pk)
        try:
            next = questions_pk[questions_pk.index(question_pk) + 1]
        except IndexError:
            next = 'DONE'
        return next

    def check_correct_answers(self, queryset, question_pk):
        correct = Answer.objects.filter(question=question_pk).filter(correct=True)
        return list(correct) == list(queryset)


class Question(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE, verbose_name='Test')
    question = models.TextField(verbose_name='Question text')
    #objects = InheritanceManager()

    def __str__(self):
        return self.question


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.CharField(max_length=300)
    correct = models.BooleanField()

    def __str__(self):
        return self.answer


class Result(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE, verbose_name='Test')
    user_name = models.ForeignKey(User, on_delete=models.CASCADE)
    correct_answers = models.PositiveIntegerField(default=0, verbose_name='Numbers of correct answers')
    test_taken = models.DateTimeField(auto_now_add=True, blank=True, verbose_name='Completion time ')
