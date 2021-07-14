# -*- coding: utf-8 -*-


from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

# Create your views here.
from django.utils import timezone

from todo.form import TodoForm
from todo.models import Todo


def home(request):
    #главная
    return render(request, 'todo/home.html')


def signupuser(request):
    #регистрация
    if request.method == 'GET':
        return render(request, 'todo/signupuser.html', {'form': UserCreationForm()})  # если GET показать форму
    else:
        if request.POST['password1'] == request.POST['password2']:  # если из инпутов совпадают пароли
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST[
                    'password1'])  # create_user по ключу username обращаемся к базе
                user.save()
                login(request, user)  # после регистрации перенаправляем на страницу
                return redirect('currenttodos')
            except IntegrityError:  # если пользователь существует
                return render(request, 'todo/signupuser.html', {'form': UserCreationForm(),
                                                                'error': 'Такой пользователь существует'})  # сернуть на стр регистрции
        else:
            return render(request, 'todo/signupuser.html', {'form': UserCreationForm(), 'error': 'Пароли не совпадают'})


def loginuser(request):
    #авторизация
    if request.method == 'GET':
        return render(request, 'todo/loginuser.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])  # authenticate встроенная функция проверяет аутентификацию
        if user is None:
            return render(request, 'todo/loginuser.html',
                          {'form': AuthenticationForm(), 'error': 'Username and password did not match'})
        else:
            login(request, user)
            return redirect('currenttodos')

@login_required
def logoutuser(request):
    #выход
    logout(request)
    # return render(request, "todo/generator.html",)
    return redirect('home')
        # if request.method == 'POST':
        #     logout(request)
        #     # return render(request, "todo/generator.html",)
        #     return redirect('home')
            # return HttpResponseRedirect(reverse_lazy('home'))
            # return redirect(request.META.get('HTTP_REFERER'))



@login_required
def createtodo(request):
    #добавить задачу
    if request.method == 'GET':
        return render(request, 'todo/createtodo.html', {'form': TodoForm()})
    else:
        try:
            form = TodoForm(request.POST)
            newtodo = form.save(commit=False)
            newtodo.user = request.user  # привязываем к пользователю
            newtodo.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todo/createtodo.html',
                          {'form': TodoForm(), 'error': 'Переданы не верныне данные. Попробуйте снова.'})




@login_required
def viewtodo(request, todo_pk):
    #функция пеоехода в детальне пописание и редактирование
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)# user=request.user для того чтобы джанга проверяла не только айди записи но и ее автора
    if request.method == 'GET':
        form = TodoForm(instance=todo)# instance занесли всю запись
        return render(request, 'todo/viewtodo.html', {'todo':todo, 'form':form})
    else:
        try:
            form = TodoForm(request.POST, instance=todo)# instance=todo  сохраняем используемый объект
            form.save()
            return redirect('currenttodos') # если успешно сохраниласб запись пернаправляем на список всех
        except ValueError: # если ошибка, показать форму и ошибку
            return render(request, 'todo/viewtodo.html', {'todo':todo, 'form':form, 'error':'Неверная информация'})

@login_required
def currenttodos(request):
    #список всех задач не выполненных
    todos = Todo.objects.filter(user=request.user, datecompleted__isnull=True)  # user=request.user, фильтр по юзеру datecompleted__isnull=True если
    return render(request, 'todo/currenttodos.html', {'todos': todos})

@login_required
def completedtodos(request):
    #список всех задач выполненных
    todos = Todo.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted') # datecompleted__isnull=False   не выполнены
    return render(request, 'todo/completedtodos.html', {'todos':todos})

@login_required
def completetodo(request, todo_pk):
    # завершеие задачи
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.datecompleted = timezone.now()# заполняем текущей датой
        todo.save()
        return redirect('currenttodos')\

@login_required
def uncompletetodo(request, todo_pk):
    # завершеие задачи
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.datecompleted = None # заполняем текущей датой
        todo.save()
        return redirect('currenttodos')

@login_required
def deletetodo(request, todo_pk):
    #  удалить
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('currenttodos')