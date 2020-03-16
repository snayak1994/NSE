from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings
import json
import csv
from os import walk,path

def getdata(request):
    fileList = []
    for (dirpath, dirnames, filenames) in walk(settings.FILES_PATH):
            fileList.extend(filenames)
            break
    fileNewLst = map(lambda x:x[:-4],fileList)
    if request.method=='GET':
        return render(request, "index.html",{'data':fileNewLst})
    elif request.is_ajax() and request.method == 'POST':
        json_data = []
        with open(path.join(settings.FILES_PATH,request.POST.get('symbol')+".csv"), 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    json_data.append(row)
        return HttpResponse(json.dumps(json_data), content_type="application/json")
