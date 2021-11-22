from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse_lazy
from django.views.generic import FormView, ListView, DetailView

from tests_project.forms import SignUpForm, LoginForm, QuestionForm

from tests_project.models import Test, Question, Answer, User, Result


class SignUpView(FormView):
    form_class = SignUpForm
    success_url = reverse_lazy('tests:home')
    template_name = 'tests_project/signup.html'

    def form_valid(self, form):
        form.save()
        user = authenticate(
            username=form.cleaned_data.get('username'),
            password=form.clean_password2(),
        )
        login(self.request, user)
        return super().form_valid(form)


class LoginView(LoginView):
    form_class = LoginForm
    template_name = 'tests_project/login.html'


class HomeView(ListView):
    model = Test
    template_name = 'tests_project/home.html'


class AllTestsView(ListView):
    model = Test
    template_name = 'tests_project/all_tests.html'


class TestView(LoginRequiredMixin, DetailView):
    model = Test
    template_name = 'tests_project/test.html'


class TestTake(FormView):
    model = Test
    form_class = QuestionForm
    template_name = 'tests_project/question.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['question_pk'] = self.kwargs['pk']
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['question'] = Question.objects.get(pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        now_test = self.kwargs['pk']
        session = self.request.session
        if not now_test in session:
            session[now_test] = 0
        if Test.check_correct_answers(self, form.cleaned_data['answers'], self.kwargs['pk']):
            session[now_test] += 1
        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        next_question = Test.get_next_question(self, self.kwargs.get('pk'), self.kwargs['pk'])
        if next_question != 'DONE':
            return reverse_lazy('tests:question', kwargs={'pk': next_question})
        else:
            self.save_score()
            return reverse_lazy('tests:all_tests')

    def save_score(self):
        test = Test.objects.get(pk=self.kwargs['pk'])
        correct_answers = self.request.session[self.kwargs['pk']]
        if self.request.user.is_authenticated:
            user = User.objects.get(username=self.request.user)
            try:
                s = Result.objects.get(user_name=user, test=test)
                s.correct_answers = correct_answers
            except ObjectDoesNotExist:
                s = Result(user_name=user, test=test, correct_answers=correct_answers)
            s.save()
        self.request.session.pop(test.pk, None)
