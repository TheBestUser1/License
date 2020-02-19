from django.shortcuts import render,redirect
from .models import Techniques, Document
#from .test import write_file #aici am inclus scriptul
from django.http import HttpResponseRedirect
from .my_forms import UploadFileForm
from django.utils import timezone
#from .file_handle import handle_uploaded_file

from .path_finder import find_path

import sys,os
import importlib.util


def homepage(request):
    if request.method =="POST":
        breakpoint()
        file_path=os.path.abspath('.')+"/scripts/"+request.POST['script']
        module_name = request.POST['script'].split('.')[0]
        #script_path= os.path.abspath(X)
        #pkg = importlib.import_module('..*',request.POST['script'])
        #importlib.import_module("scripts")

        spec = importlib.util.spec_from_file_location(module_name, file_path)
        module = importlib.util.module_from_spec(spec)
        #sys.modules[module_name] = module
        spec.loader.exec_module(module)
        module.printing()
        
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
     form = UploadFileForm()
     if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)

        if form.is_valid():
            #form.save()

            file = form.save(commit=False)
            file.myfile =request.FILES['myfile']
            file.date_added  = timezone.now()
            file.save()
            return redirect("main:homepage")



     return render(request=request,
                    template_name="main/upload.html",
                    context={"form":form})
