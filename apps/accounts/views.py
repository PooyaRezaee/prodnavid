from django.shortcuts import render,redirect
from django.views import View
from django.views.generic import FormView,UpdateView
from django.urls import reverse_lazy
from .forms import *
from .models import User
from django.contrib import messages
from django.utils.decorators import method_decorator
from axes.decorators import axes_dispatch
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth import signals
from django.contrib.auth.mixins import LoginRequiredMixin
from .mixins import WithoutLoginRequiredMixin
from django.utils.translation import gettext as _
from apps.ear.utils import get_client_ip


__all__ = [
    'RegisterView',
    'LoginView',
    'LogoutView',
    'ProfileUserView',
]

class RegisterView(WithoutLoginRequiredMixin,FormView):
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('accounts:login')
    form_class = UserRegisterForm

    def form_valid(self, form):
        cd = form.cleaned_data
        user = User.objects.create_user(full_name=cd['full_name'],email=cd['email'],password=cd['password'],how_meet=cd['meet'])
        if cd.get('phone_number'):
            user.phone_number = cd.get('phone_number')
            user.save()
        
        try:
            user.ip_register = get_client_ip(self.request)
            user.save()
        except:
            pass

        user.send_email('ProdNavid | Registration','Congratulations\nyour account has been successfully created')
        messages.success(self.request,'You Registred',extra_tags='success')
        messages.info(self.request,'Please Login To page',extra_tags='info')

        return super().form_valid(form)


@method_decorator(axes_dispatch, name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class LoginView(WithoutLoginRequiredMixin,FormView):
    template_name = 'accounts/login.html'
    success_url = reverse_lazy('beat:index')
    form_class = LoginForm

    def form_valid(self, form):
        cd = form.cleaned_data
        user = authenticate(request=self.request,username=cd.get('email'),password=cd.get('password'))
        if user is not None:
            login(self.request, user)
            signals.user_logged_in.send(sender=User,request=self.request,user=user)
            messages.success(self.request,_('You Logged'),extra_tags='success')
        else:
            signals.user_login_failed.send(sender=User,request=self.request,credentials={'username': form.cleaned_data.get('email')})
            messages.warning(self.request,_('Email Or Password Wrong !'),extra_tags='danger')
            return redirect('accounts:login')


        return super().form_valid(form)

    def form_invalid(self, form):
        signals.user_login_failed.send(
                sender=User,
                request=self.request,
                credentials={
                    'username': form.cleaned_data.get('email'),
                },
            )
        messages.warning(self.request,_('Form Not Valid'),extra_tags='danger')

        return redirect('accounts:login')

class LogoutView(LoginRequiredMixin,View):
    def get(self, request):
        logout(request)
        return redirect('beat:index')

    
class ProfileUserView(LoginRequiredMixin,UpdateView):
    login_url = reverse_lazy('accounts:login')
    template_name = 'accounts/profile.html'
    success_url = reverse_lazy('accounts:profile')
    form_class = UserProfileForm

    def get_object(self):
        return User.objects.get(id=self.request.user.id)
    
    def form_valid(self, form):
        messages.success(self.request,_('You Information Updated.'))
        return super().form_valid(form)