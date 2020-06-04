from django import forms
from account.models import User

from utils.forms import BaseModelForm
from utils.persian import persianToEnNumb, arToPersianChar


class LoginForm(forms.Form):
    username = forms.CharField(label="نام کاربری")
    password = forms.CharField(required=True, label=u"رمز عبور", widget=forms.PasswordInput)


class ProfileForm(BaseModelForm):
    old_password = forms.CharField(required=False, label="رمز عبور فعلی",
                                   widget=forms.PasswordInput,
                                   help_text="در صورت خالی بودن رمز عبور تغییر نمیکند.")
    password1 = forms.CharField(required=False, label="تغییر رمز عبور",
                                widget=forms.PasswordInput,
                                help_text="در صورت خالی بودن رمز عبور تغییر نمیکند.")
    password2 = forms.CharField(required=False, label="تکرار رمز عبور",
                                widget=forms.PasswordInput,
                                help_text="در صورت خالی بودن رمز عبور تغییر نمیکند")

    class Meta:
        model = User
        fields = ('old_password', 'password1', 'password2')

    def clean(self):
        cd = super(ProfileForm, self).clean()

        old_password = cd.get('old_password')

        if old_password and not self.instance.check_password(old_password):
            self.errors['old_password'] = self.error_class(['رمز عبور فعلی نادرست است'])

        password1 = cd.get('password1')
        password2 = cd.get('password2')

        if password1 and password1 != password2:
            self.errors['password2'] = self.error_class(['رمز عبور جدید با تکرار آن مطابقت ندارد'])
        elif password1 and not old_password:
            self.errors['old_password'] = self.error_class(['برای تغییر رمز عبور باید رمز عبور فعلی وارد شود'])

        return cd

    def save(self, commit=True):
        obj = super(ProfileForm, self).save(commit=False)
        password1 = self.cleaned_data.get('password1')
        if password1:
            password1 = persianToEnNumb(password1)
            obj.set_password(password1)
        obj.save()
        return obj
