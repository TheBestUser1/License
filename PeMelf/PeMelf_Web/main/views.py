from django.shortcuts import render,redirect
from .models import Techniques, Document
from django.http import HttpResponseRedirect
from .my_forms import UploadFileForm
from django.utils import timezone

import sys,os
import importlib.util


def homepage(request):
    if request.method =="POST":
#        breakpoint()
        filename=Document.objects.filter(user_token=request.COOKIES['csrftoken']\
        ).order_by('-date_added').values()[0]['myfile']
        path_to_bin=os.path.join(os.path.abspath("files"),filename)

        file_path=os.path.abspath('.')+"/scripts/"+request.POST['script']
        module_name = request.POST['script'].split('.')[0]

        spec = importlib.util.spec_from_file_location(module_name, file_path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        report = module.main(path_to_bin)
        #return redirect("main:homepage")
        return render(request=request,
                        template_name="main/report.html",
                        context=report)

    return render(request=request,
                    template_name="main/main.html",
                    context={"Tech":Techniques.objects.all})

def upload(request):
     form = UploadFileForm()
     if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)

        if form.is_valid():
            #form.save()

            file = form.save(commit=False)
            file.myfile =request.FILES['myfile']
            file.date_added  = timezone.now()
            file.user_token = request.COOKIES['csrftoken']
            file.save()
            return redirect("main:homepage")



     return render(request=request,
                    template_name="main/upload.html",
                    context={"form":form})
