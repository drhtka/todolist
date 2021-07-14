from django.http import HttpResponse
from django.shortcuts import render
import random
# Create your views here.
def generator(request):
    return render(request, 'generator/generator.html')

def password(request):
    # генерация рендомоного паролля
    characters = list('abcdefghijklmnopqrstuvwxyz')
    if request.GET.get('uppercase'):
        characters.extend(list('ABCDEFGHIJKLMNOPQRSTUVWXYZ'))
    if request.GET.get('special'):
        characters.extend(list('!@#$%^&*()'))
    if request.GET.get('numbers'):
        characters.extend(list('0123456789'))

    lenght = int(request.GET.get('length', 12))
    thepassword = ''

    for x in range(lenght):
        thepassword += random.choice(characters)# choice выбирает слчайные буквы и символы
    return render(request, 'generator/password.html', {'password': thepassword})