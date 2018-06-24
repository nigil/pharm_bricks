from django.shortcuts import render


def homepage(request):
    print(request.user)
    return render(request, 'base.html')
