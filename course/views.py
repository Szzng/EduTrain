from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic.edit import FormMixin
from django.views.generic import ListView, DetailView, FormView, TemplateView
from .forms import *
from .models import *
from django.db.models import Q

class TestView(TemplateView):
    template_name = 'course/dd.html'


class SearchMixin:
    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get('q')
        if q:
            searched = queryset.filter(
                Q(category__name__icontains=q) |
                Q(title__icontains=q)
            ).distinct()
            return searched

class CourseIndexView(SearchMixin, ListView):
    model = Course
    template_name = 'course/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()

        # 검색 기능
        queryset = super().get_queryset()
        if queryset is not None:
            if queryset:
                context['searched'] = queryset
            else:
                context['not_found'] = '검색 결과를 찾을 수 없습니다.'
        return context

class CourseDetailView(FormMixin, DetailView):
    model = Course
    template_name = 'course/detail.html'
    form_class = ReviewForm

    def get_success_url(self):
        return reverse('course:detail', kwargs={'pk': self.object.pk})

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        self.object = self.get_object()
        course = get_object_or_404(Course, pk=self.object.pk)
        rate = self.request.POST['star']
        review = form.save(commit=False)
        review.course = course
        review.rate = rate
        review.save()
        return super().form_valid(form)

class ByCategoryView(DetailView):
    model = Category
    template_name = 'course/bycategory.html'