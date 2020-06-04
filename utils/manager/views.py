# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import Http404
from utils.manager.main import manager_children




@login_required(login_url=settings.ADMIN_LOGIN_URL)
def process_main_page(request, manager_name):
    for manager in manager_children:
        if manager.manager_name == manager_name:
            manager_obj = manager(http_request=request)
            if manager_obj.can_view():
                return manager_obj.render_main_list()
            break
    raise Http404()


@login_required(login_url=settings.ADMIN_LOGIN_URL)
def process_actions(request, manager_name):
    for manager in manager_children:
        if manager.manager_name == manager_name:
            manager_obj = manager(http_request=request)
            if manager_obj.can_view():
                return manager_obj.process_action_request()
            break
    raise Http404()