from django.conf import settings
from django.urls import path

from . import views

app_name = 'account'

urlpatterns = [
    path('%s/' % settings.ADMIN_BASE_URL, views.admin_dashboard, name='admin_dashboard'),

    path('%s/login/' % settings.ADMIN_BASE_URL, views.login_view, name='admin_login'),

    path('%s/profile/' % settings.ADMIN_BASE_URL, views.profile, name='profile'),

    path('logout/', views.logout, name='logout'),
]

handler404 = views.handler404
handler500 = views.handler500
handler403 = views.handler403
