from django.contrib import admin

from tests_project.models import Test, Question, Answer, Result

from tests_project import models


@admin.register(Test)
class TestModelAdmin(admin.ModelAdmin):
    list_display = ['title', 'questions_count']
    search_fields = ['title']


class QuestionsInline(admin.TabularInline):
    model = Answer


class TestQuestionFilter(admin.SimpleListFilter):
    title = 'test'
    parameter_name = 'test'

    def lookups(self, request, model_admin):
        tests = models.Test.objects.all()
        lookups = ()
        for test in tests:
            lookups += ((test.title, test.title),)
        return lookups

    def queryset(self, request, queryset):
        if self.value():
            test_title = self.value()
            return queryset.filter(test__title=test_title)


@admin.register(Question)
class QuestionModelAdmin(admin.ModelAdmin):
    list_display = ['question', 'test']
    list_filter = [TestQuestionFilter]
    inlines = [QuestionsInline]


class AnswerQuestionFilter(admin.SimpleListFilter):
    title = 'test'
    parameter_name = 'test'

    def lookups(self, request, model_admin):
        tests = models.Test.objects.all()
        lookups = ()
        for test in tests:
            lookups += ((test.title, test.title),)
        return lookups

    def queryset(self, request, queryset):
        if self.value():
            test_title = self.value()
            return queryset.filter(question__test__title=test_title)


@admin.register(models.Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['answer', 'correct', 'question']
    list_filter = [AnswerQuestionFilter]


@admin.register(Result)
class ResultModelAdmin(admin.ModelAdmin):
    list_display = ['test', 'user_name', 'correct_answers', 'test_taken']

    def has_add_permission(self, request):
        return False
