from django.shortcuts import render,redirect
from .models import Techniques, Document, Document_download
from django.http import HttpResponseRedirect,HttpResponse
from .my_forms import UploadFileForm
from django.utils import timezone


import sys,os
import importlib.util
import mimetypes

def homepage(request):
    if request.method =="POST":
    #breakpoint()
        filename=Document.objects.filter(user_token=request.COOKIES['csrftoken']\
        ).order_by('-date_added').values()[0]['myfile']
        path_to_bin=os.path.join(os.path.abspath("files"),filename)

        file_path=os.path.abspath('.')+"/scripts/"+request.POST['script']
        module_name = request.POST['script'].split('.')[0]

        spec = importlib.util.spec_from_file_location(module_name, file_path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        report = module.main(request,path_to_bin)
        
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
            file = form.save(commit=False)
            file.myfile =request.FILES['myfile']
            file.date_added  = timezone.now()
            file.user_token = request.COOKIES['csrftoken']
            file.save()
            return redirect("main:homepage")



     return render(request=request,
                    template_name="main/upload.html",
                    context={"form":form})


def download(request):
    if request.method == 'GET':
        files_of_user = Document_download.objects.filter(user_token=request.COOKIES['csrftoken'])\
        .values()

        path_to_gzip= "{}.gzip".format(files_of_user[0]['id'])
        abs_path = os.path.join(os.path.abspath("."),"scripts/dumps/")

        cd = f'cd {abs_path}'

        tar_command = '{};tar -czf {}'.format(cd,path_to_gzip)
        for file in files_of_user:
            tar_command+=' '+file['path_to_file']

        os.system(tar_command)

    path_f = os.path.join("scripts/dumps/",path_to_gzip)
    fl = open(path_f, 'rb')
    mime_type, _ = mimetypes.guess_type(path_f)
    response = HttpResponse(fl,content_type='application/gzip')
    response['Content-Disposition']='attachment; filename={}'.format(path_f)
    Document_download.objects.all().delete() #erases all entrys of unpacking
    return response
