from django.shortcuts import render,redirect
from .models import Techniques
from .test import write_file #aici am inclus scriptul

def homepage(request):
    if request.method == "POST":
        write_file()
        return redirect("main:homepage")

    return render(request=request,
                    template_name="main/main.html",
                    context={"Tech":Techniques.objects.all})
'''
def test(request):
    if request.method == "POST":
        write_file()
        return redirect("main:homepage")
    return render(request = request,
                template_name ="main/test.html")
'''
# Create your views here.

def upload(request):


    return render(request=request,
                template_name="main/upload.html")
