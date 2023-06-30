"""
В представлениях AdvertisementListView, AdvertisementDetailView и ResponseView
используется класс-based подход для обработки GET и POST запросов.
Они получают данные из моделей и передают их в соответствующие шаблоны для отображения.
"""
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import CreateView

from .models import Advert, Response

from ads.forms import ResponsesForm


class AdvertisementListView(View):
    def get(self, request):
        advertisements = Advert.objects.all()
        return render(request, 'ads/advertisement_list.html', {'advertisements': advertisements})


class AdvertisementDetailView(View):
    def get(self, request, pk):
        advertisement = Advert.objects.get(pk=pk)
        return render(request, 'ads/advertisement_detail.html', {'article': advertisement})


class ResponseCreateView(LoginRequiredMixin, CreateView):
    raise_exception = True
    form_class = ResponsesForm
    model = Response
    template_name = 'response_create.html'

    def post(self, request, pk):
        content = request.POST['response_text']
        user = request.user
        advertisement = Advert.objects.get(pk=pk)
        response = self.model(user=user, advertisement=advertisement, content=content)
        response.save()
        return render(request, 'response_confirmation.html')


# Представление, которое обрабатывает POST-запросы для
# создания нового объявления. Если метод запроса является POST,
# код получает данные из запроса (название, содержание, категорию,
# изображение, видео) и создает новый объект объявления в базе
# данных с помощью модели Advert.
# Затем происходит перенаправление пользователя на страницу
# деталей созданного объявления.
@login_required
def create_advertisement(request):
    if request.method == 'POST':
        # Получаем данные из POST-запроса
        title = request.POST['title']
        content = request.POST['response_text']
        category = request.POST['category']
        image = request.FILES.get('image')
        video = request.POST.get('video')

        # Получаем текущего пользователя
        user = request.user

        # Создаем новое объявление с полученными данными
        advertisement = Advert.objects.create(
            title=title,
            content=content,
            category=category,
            user=user,
            image=image,
            video=video
        )

        # Перенаправляем пользователя на страницу деталей объявления
        return redirect('advertisement_detail', advertisement_id=advertisement.id)

    return render(request, 'create_advertisement.html')


# Представление, которое отображает страницу с деталями конкретного
# объявления. Оно получает идентификатор объявления из URL-адреса,
# затем использует этот идентификатор для получения объекта объявления
# из базы данных. Затем представление передает объект объявления в
# контексте, чтобы он мог быть отображен на странице деталей объявления
@login_required
def advertisement_detail(request, advertisement_id):
    # Получаем объявление по его идентификатору
    advertisement = Advert.objects.get(id=advertisement_id)

    # Отображаем страницу с деталями объявления, передавая объект объявления в контексте
    return render(request, 'advertisement_detail.html', {'article': advertisement})
