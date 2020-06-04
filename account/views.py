from django.shortcuts import render

# Create your views here.
from django.urls.base import reverse
from django.http.response import HttpResponseRedirect, HttpResponse
from django.core.exceptions import ObjectDoesNotExist

from django.contrib.auth import authenticate, login
from account.forms import LoginForm, ProfileForm
from utils.persian import arToPersianChar, persianToEnNumb, enToPersianNumb
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache


def login_view(request):
    next_page = request.GET.get('next', '')
    try:
        if request.user.is_superuser or (
                request.user.is_authenticated and request.user.staff and request.user.staff.role_id):
            if not next_page:
                next_page = reverse('account:admin_dashboard')
            return HttpResponseRedirect(next_page)
    except ObjectDoesNotExist:
        pass

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = arToPersianChar(form.cleaned_data.get('username')).lower()
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is None:
                password = persianToEnNumb(password)
                username = persianToEnNumb(username)
                user = authenticate(username=username, password=password)
                if user is None:
                    password = enToPersianNumb(password)
                    username = enToPersianNumb(username)
                    user = authenticate(username=username, password=password)

            if user is None or not user.is_active:
                messages.error(request, u"نام کاربری یا گذرواژه نادرست است.")
            else:
                login(request, user)

                if not next_page:
                    next_page = reverse('admin_dashboard')
                return HttpResponseRedirect(next_page)
        else:
            messages.error(request, u"داده های ارسالی نامعتبر است.")

    else:
        form = LoginForm()

    context = {
        'app_path': request.get_full_path(),
        'next': next_page,
        'form': form,
    }

    return render(request, 'account/login.html', context)


@login_required
def admin_dashboard(request):
    return render(request, 'account/admin_dashboard.html', {})


@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'ویرایش پروفایل با موفقیت انجام شد')
            form = ProfileForm(instance=request.user)
    else:
        form = ProfileForm(instance=request.user)

    return render(request, 'basic_form.html', {'form': form, 'title': 'ویرایش پروفایل'})


@never_cache
def logout(request):
    from django.contrib.auth import logout

    next_page = request.GET.get('next', '/')

    logout(request)
    return HttpResponseRedirect(next_page)


def handler404(request, exception):
    response = render(request, '404.html', {})
    response.status_code = 404
    return response


def handler500(request):
    response = render(request, '500.html', {})
    response.status_code = 500
    return response


def handler403(request, reason=""):
    response = render(request, '403.html', {})
    response.status_code = 403
    return response
