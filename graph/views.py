from django.shortcuts import render

from .models import TestForm, Hashtag
import json

from django.http import HttpResponse
import re


# Create your views here.


def show_graph(request):
    return render(request, 'graph/index.html')


def render_post(request):
    if request.method == 'POST':
        testForm = TestForm(request.POST)
        if testForm.is_valid():
            description = request.POST['description']
            listOfHashtages = set(re.findall(r"#(\w+)", description))
            testFormModel = testForm.save()
            for hashtagText in listOfHashtages:
                hashtagModel = Hashtag.objects.get_or_create(tag=hashtagText)[0]
                testFormModel.hashtags.add(hashtagModel)
    else:
        testForm = TestForm()
    return render(request, 'graph/render_post.html', {'testForm': testForm})


def hashtag(request):
    if request.method == "GET":
        listOfHashtagsModel = Hashtag.objects.filter(tag__startswith=request.GET['query'])
        listOfHashtagsInFormOfCkeditor = []

        for hashtag in listOfHashtagsModel:
            listOfHashtagsInFormOfCkeditor.append({'id': hashtag.id, 'name': hashtag.tag})
        return HttpResponse(
            json.dumps(listOfHashtagsInFormOfCkeditor),
            content_type="application/json")
