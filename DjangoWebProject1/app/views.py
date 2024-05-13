"""
Definition of views.
"""

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from datetime import datetime
from django.shortcuts import render
from django.http import HttpRequest
from .forms import ReviewForm
from django.db import models
from .models import Blog
from .models import Comment # Модель комментариев
from .forms import CommentForm # Форма ввода комментариев
from .forms import BlogForm # Импорт формы блога



def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Домашняя страница',
            'year':datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Наша контактная информация',
            'message':'Наш главный офис',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)

    message_parts = [
    'Мы имеем более 10 лет опыта в сфере IT и безопасности данных.\n',
    'Наша команда состоит из опытных разработчиков, инженеров и менеджеров.\n',
    'Наши серверы расположены в странах с надежной законодательной базой в области защиты данных.\n',
    'Мы соблюдаем все требования законодательства в области защиты данных и конфиденциальности.',
]
    message = ''.join(message_parts)
    return render(
        request,
        'app/about.html',
        {
            'title':'Информация о нас',
            'message':message,
            'year':datetime.now().year,
        }
    )

def resources(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    resources = [
        {'name': 'CloudFlare', 'url': 'https://www.cloudflare.com/', 'logo': 'cloud.png'},
        {'name': 'Gogle Cloud', 'url': 'https://cloud.google.com/', 'logo': 'google.png'},
        {'name': 'Microsoft Azure', 'url': 'https://azure.microsoft.com/', 'logo': 'azure.png'},
    ]
    return render(request, 'app/resources.html', {'resources': resources , 'year':datetime.now().year})

def feedback(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    data = None
    gender = {'1': 'Мужчина', '2':'Женщина'}
    internet = {'1': 'Ежедневно' , '2': 'Пару часов в день', '3': 'Пару часов в неделю', '4': 'Пару часов в месяц'}

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            data = dict()
            data['name'] = form.cleaned_data['name']
            data['city'] = form.cleaned_data['city']
            data['job'] = form.cleaned_data['job']
            data['gender'] = gender[ form.cleaned_data['gender'] ]
            data['internet'] = internet[ form.cleaned_data['internet'] ]
            if(form.cleaned_data['notice'] == True):
                data['notice'] = 'Да'
            else:
                data['notice'] = 'Нет'
            data['email'] = form.cleaned_data['email']
            data['message'] = form.cleaned_data['message']
            form = None
    else:
        form = ReviewForm()
    return render(
        request,
        'app/feedback.html',
        {
            'form': form,
            'data': data,
            'year':datetime.now().year},
        )

def registration(request):
    """Renders the registration page."""
    assert isinstance(request, HttpRequest)

    if request.method == "POST": # после отправки формы
        regform = UserCreationForm (request.POST)
        if regform.is_valid(): #валидация полей формы
            reg_f = regform.save(commit=False) # не сохраняем автоматически данные формы
            reg_f.is_staff = False # запрещен вход в административный раздел
            reg_f.is_active = True # активный пользователь
            reg_f.is_superuser = False # не является суперпользователем
            reg_f.date_joined = datetime.now() # дата регистрации
            reg_f.last_login = datetime.now() # дата последней авторизации
            reg_f.save() # сохраняем изменения после добавления данных

            return redirect('home') # переадресация на главную страницу после регистрации
        else:
            # возвращает форму с сообщениями об ошибках, если форма недействительна
            return render(request, 'app/registration.html',
                            {
                                'regform': regform,
                                'year': datetime.now().year,
                            }
                          )
    else:
        regform = UserCreationForm()  # создание пустого объекта формы для регистрации пользователя

        return render(request, 'app/registration.html',
                  {
                      'regform': regform,
                      'year': datetime.now().year,
                  }
                  )

def blog(request):
        """Renders the blog page."""
        assert isinstance(request, HttpRequest)

        posts = Blog.objects.all() # запрос на выбор всех статей блога из модели

        return render(request, 'app/blog.html',
        {
            'title':'Блог',
            'posts': posts, # передача списка статей в шаблон веб-страницы
            'year':datetime.now().year,
        }
        )

def blogpost(request, parametr):
    """Renders the blogpost page."""
    assert isinstance(request, HttpRequest)

    post_1 = Blog.objects.get(id=parametr) # запрос на выбор конкретной статьи по параметру
    comments = Comment.objects.filter(post=parametr)

    form = CommentForm()

    if request.method == "POST": # после отправки данных формы на сервер методом POST
        form = CommentForm(request.POST) # Выбор всех комментариев к конкретной статье

        if form.is_valid():

            comment_f = form.save(commit=False)
            comment_f.author = request.user # добавляем (так как этого поля нет в форме) в модель Комментария (Comment) в поле автор авторизованного пользователя
            comment_f.date = datetime.now() # добавляем в модель Комментария (Comment) текущую дату
            comment_f.post = Blog.objects.get(id=parametr) # добавляем в модель Комментария (Comment) статью, для которой данный комментарий
            comment_f.save() # сохраняем изменения после добавления полей
            return redirect('blogpost', parametr=post_1.id) # переадресация на ту же страницу статьи после отправки комментария

    return render(request, 'app/blogpost.html',
    {
        'post_1': post_1, # передача конкретной статьи в шаблон веб-страницы
        'comments': comments, # передача всех комментариев к данной статье в шаблон веб-страницы
        'form': form, # передача формы добавления комментария в шаблон веб-страницы
        'year':datetime.now().year,
    }
    )

def newpost(request):
    """Renders the blogpost page."""
    assert isinstance(request, HttpRequest)

    if request.method == "POST":        # После отправки формы
        blogform = BlogForm(request.POST, request.FILES)
        if blogform.is_valid():
            blog_f = blogform.save(commit=False)
            blog_f.posted = datetime.now()
            blog_f.author = request.user
            blog_f.save()

            return redirect('blog')
    else:
        blogform = BlogForm()

    return render(request, 'app/newpost.html', # передача формы в шабон html страницы
                    {
                        'blogform': blogform,
                        'title': 'Добавить статью блога',

                        'year':datetime.now().year,
                    }
                  )

def videopost(request):
    """Renders the videopost page."""
    assert isinstance(request, HttpRequest)

    return render(request, 'app/videopost.html',
                  {
                      'title': 'Видеоролики',
                      'year':datetime.now().year,
                  }
                )

def audio(request):
    """Renders the videopost page."""
    assert isinstance(request, HttpRequest)

    return render(request, 'app/audio.html',
                  {
                      'title': 'Музыка',
                      'year':datetime.now().year,
                  }
                )
