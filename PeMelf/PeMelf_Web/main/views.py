from django.shortcuts import render

def homepage(request):
    return render(request=request,template_name="main/main.html")


# Create your views here.
