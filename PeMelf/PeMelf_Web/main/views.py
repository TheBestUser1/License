from django.shortcuts import render
from .models import Techniques

def homepage(request):
    return render(request=request,
                    template_name="main/main.html",
                    context={"Tech":Techniques.objects.all})


# Create your views here.
