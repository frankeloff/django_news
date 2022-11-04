from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from typing import Optional

from .models import News, Category
from .forms import NewsForm

class HomeNews(ListView):
    model = News
    template_name: str = 'news/home_news_list.html'
    context_object_name: Optional[str] = 'news'
    # extra_context = {"title": "Главная"}

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Главная страница"
        return context

    def get_queryset(self):
        return News.objects.filter(is_published=True).select_related('category')

class NewsByCategory(ListView):
    nodel = News
    template_name: str = 'news/home_news_list.html'
    context_object_name: Optional[str] = 'news'
    allow_empty: bool = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(pk=self.kwargs['category_id'])
        return context

    def get_queryset(self):
        return News.objects.filter(category_id=self.kwargs['category_id'], is_published=True).select_related('category')

class ViewNews(DetailView):
    model = News
    context_object_name = 'news_item'
    # template_name: str = 'news/news_detail.html'
    # pk_url_kwarg: str = 'news_id'

class CreateNews(CreateView):
    form_class = NewsForm
    template_name: str = "news/add_news.html"
    # success_url = reverse_lazy('home')

# def index(request):
#     news = News.objects.all()
#     context = {
#         "news": news,
#         "title": "Список новостей",
#     }
#     return render(request, "news/index.html", context)


def get_category(request, category_id: int):
    news = News.objects.filter(category_id=category_id)
    # category = Category.objects.get(pk=category_id)
    category = get_object_or_404(Category, pk=category_id)
    return render(
        request,
        "news/category.html",
        {"news": news, "category": category},
    )

# def view_news(request, news_id: int):
#     # news_item = News.objects.get(pk=news_id)
#     news_item = get_object_or_404(News, pk=news_id)
#     return render(request, 'news/view_news.html', {"news_item": news_item})

# def add_news(request):
#     if request.method == 'POST':
#         form = NewsForm(request.POST)
#         if form.is_valid():
#             # print(form.cleaned_data)
#             # news = News.objects.create(**form.cleaned_data)
#             news = form.save()
#             return redirect(news)
#     else:
#         form = NewsForm()
#     return render(request, 'news/add_news.html', {'form': form})