from django.shortcuts import render
from django.http import HttpResponse
from app.forms import FaceRecognitionForm
from app.machinelearning import pipeline_model
from django.conf import settings
from app.models import FaceRecognition  
import os


# Create your views here.

def index(request):
    form = FaceRecognitionForm()
    if request.method == 'POST':
            form = FaceRecognitionForm(request.POST, request.FILES or None)
            if form.is_valid():
                save = form.save(commit=True)

                primary_key = save.pk
                imgobj = FaceRecognition.objects.get(pk=primary_key)
                fileroot = str(imgobj.image)
                image_path = os.path.join(settings.MEDIA_ROOT, fileroot)
                image ,results = pipeline_model(image_path)
                print(results)
                
                
                return render(request, "index.html", {'form': form,'upload':True ,'results': results})


    return render(request, "index.html", {'form': form,'upload':False})