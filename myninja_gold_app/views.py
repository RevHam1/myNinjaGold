from django.shortcuts import render


def index(request):
    return render(request, 'myninja_gold/index.html')
