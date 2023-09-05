from typing import Dict, Any, Type

from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic.list import ListView

from .models import Task


class Home(TemplateView):
    template_name = 'base/home.html'


class Login(LoginView):
    template_name: str = 'base/login.html'
    redirect_authenticated_user: bool = True
    fields: str = '__all__'

    def get_success_url(self) -> str:
        return reverse_lazy('to-do')


class Register(FormView):
    template_name: str = 'base/register.html'
    form_class: Type[UserCreationForm] = UserCreationForm
    success_url: str = reverse_lazy('to-do')

    def form_valid(self, form: UserCreationForm) -> Any:
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)

    def get(self, *args: Any, **kwargs: Any) -> Any:
        if self.request.user.is_authenticated:
            return redirect('to-do')
        return super().get(*args, **kwargs)


class TaskListView(LoginRequiredMixin, ListView):
    model: Type[Task] = Task

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context: Dict[str, Any] = super().get_context_data(**kwargs)
        context['task_list'] = context['task_list'].filter(user=self.request.user)
        context['count'] = context['task_list'].filter(completed=False).count()
        searched_value: str = self.request.GET.get('búsqueda') or ''

        if searched_value:
            context['task_list'] = context['task_list'].filter(title__icontains=searched_value)
        # Para que no se borre de la barra de búsqueda
        context['searched_value'] = searched_value
        return context


class TaskDetailView(LoginRequiredMixin, DetailView):
    model: Type[Task] = Task


class TaskCreateView(LoginRequiredMixin, CreateView):
    model: Type[Task] = Task
    fields: list[str] = ['title', 'description', 'completed']
    success_url: str = reverse_lazy('to-do')

    def form_valid(self, form: Any) -> Any:
        form.instance.user = self.request.user
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model: Type[Task] = Task
    fields: list[str] = ['title', 'description', 'completed']
    success_url: str = reverse_lazy('to-do')


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model: Type[Task] = Task
    success_url: str = reverse_lazy('to-do')
