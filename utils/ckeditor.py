from __future__ import absolute_import

import django
from django.conf.urls import url
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.cache import never_cache

from ckeditor_uploader import views

from account.decorators import staff_only

urlpatterns = [
    url(r'^upload/', staff_only(views.upload), name='ckeditor_upload'),
    url(r'^browse/', never_cache(staff_only(views.browse)), name='ckeditor_browse'),
]
