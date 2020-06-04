from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Hashtag
from .forms import PostForm
import json
from django.http import HttpResponse
from django.contrib import messages


# Create your views here.
@login_required
def add_post(request):
    if request.method == 'POST':
        postForm = PostForm(request.POST, request.FILES)
        if postForm.is_valid():
            postForm.save()
            messages.success(request, 'پست با موفقیت افزوده شد.')
    else:
        postForm = PostForm()
    return render(request, 'post/add_post.html', {'postForm': postForm})


@login_required
def hashtag_list(request):
    if request.method == "GET":
        listOfHashtagsModel = Hashtag.objects.filter(tag__startswith=request.GET['query'])
        listOfHashtagsInFormOfCkeditor = []

        for hashtag in listOfHashtagsModel:
            listOfHashtagsInFormOfCkeditor.append({'id': hashtag.id, 'name': hashtag.tag})
        return HttpResponse(
            json.dumps(listOfHashtagsInFormOfCkeditor),
            content_type="application/json")
