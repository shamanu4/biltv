# -*- coding: utf-8 -*-

from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100)
    
    def save(self,request):
        from django.contrib.auth import authenticate
        from django.contrib.auth import login

        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                ok = True
                login(request, user)
                title = "Авторизация успешная."
                msg = "Login success."
            else:
                ok = False
                title = "Сбой авторизации."
                msg = "Account disabled."
        else:
            ok = False
            title = "Сбой авторизации."
            msg = "Incorrect login or password"

        return dict(success=True, ok=ok, title=title, msg=msg)
