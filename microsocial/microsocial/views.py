from django.shortcuts import render


def main(request):
    return render(request, 'Index.html')

def registration(request):
    return render(request, 'registration.html')

def authorization(request):
    return render(request, 'auth.html')

def reset(request):
    return render(request, 'reset.html')

def reset_pass(request):
    return render(request, 'reset_pass.html')