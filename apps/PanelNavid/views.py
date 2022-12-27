from django.shortcuts import render,redirect
from django.views import View
from django.views.generic import FormView,CreateView,ListView,UpdateView,RedirectView,DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from apps.accounts.forms import LoginForm
from apps.accounts.models import User
from django.contrib import messages
from django.utils.decorators import method_decorator
from axes.decorators import axes_dispatch
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from django.contrib.auth import signals
from django.urls import reverse_lazy
from .forms import *
from apps.beat.models import *
from .models import SiteSettings,Message
from apps.ear.models import IpLog
from apps.accounts.utils import send_custom_email
from datetime import datetime
from django.db.models import Count
from apps.beat.utils import bucket
from apps.ear.utils import get_client_ip
from apps.order.models import Order
from .mixins import IsAdminMixin

__all__ = [
    'LoginView',
    'DashbordView',
    'AddBeatView',
    'AddFreeBeatView',
    'AddSaleBeatView',
    'AddCategoryView',
    'BeatListView',
    'CategoryListView',
    'SendEmailView',
    'SettingsView',
    'DeleteBeat',
    'DeleteCategory',
    'ModifyBeatView',
    'ModifyCategoryView',
    'MessagesView',
    'MessageView',
    'OrdersView',
    'UserListView',
    'CancellOrder',
    'DeleteUser',
]

@method_decorator(axes_dispatch, name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class LoginView(FormView):
    template_name = 'panel/login.html'
    success_url = reverse_lazy('panel:dashbord')
    form_class = LoginForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_admin:
                return redirect('panel:dashbord')
            else:
                raise Http404
        else:
            return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        cd = form.cleaned_data
        user = authenticate(request=self.request,username=cd.get('email'),password=cd.get('password'))
        
        if user is not None:
            login(self.request, user)
            send_custom_email(SiteSettings.objects.first().email,'AdminPanel',f'You Logined With {get_client_ip(self.request)} IP')
            signals.user_logged_in.send(sender=User,request=self.request,user=user)
            messages.success(self.request,'You Logged',extra_tags='success')
            if not user.is_admin:
                send_custom_email(SiteSettings.objects.first().email,'AdminPanel',f"Login Was From AdminPanel But Don't have Acess {get_client_ip(self.request)} IP")
                return redirect('beat:index')
        else:
            send_custom_email(SiteSettings.objects.first().email,'AdminPanel',f'A Try For Login Founded(Wrong Filed) With {get_client_ip(self.request)} IP')
            signals.user_login_failed.send(sender=User,request=self.request,credentials={'username': form.cleaned_data.get('email')})
            messages.warning(self.request,'Email Or Password Wrong !',extra_tags='danger')
            return redirect('panel:login')


        return super().form_valid(form)

    def form_invalid(self, form):
        send_custom_email(SiteSettings.objects.first().email,'AdminPanel',f'A Try For Login Founded(Form Not Valid) With {get_client_ip(self.request)} IP')

        signals.user_login_failed.send(
                sender=User,
                request=self.request,
                credentials={
                    'username': form.cleaned_data.get('email'),
                },
            )
        messages.warning(self.request,'Form Not Valid',extra_tags='danger')

        return redirect('panel:login')

class DashbordView(IsAdminMixin,View):
    def get(self,request):
        user_count = User.objects.all().count()
        requests_count = IpLog.objects.all().count()
        beats_count = Beat.objects.all().count()

        beat_mustViews = Beat.objects.all().order_by('hits')[:2]
        last_requests = IpLog.objects.all().order_by('-created')[:5]

        categories = Category.objects.all()
        parts = []
        cate_count = Category.objects.annotate(Count('beats')).values_list('name_en', 'beats__count')
        for c in cate_count:
            parts.append(c)

        days = []
        requests_this_month = IpLog.objects.filter(created__month=datetime.now().month)
        for day in range(1,31):
            days.append(requests_this_month.filter(created__day=day).count())


        context = {
            "user_count":user_count,
            "requests_count":requests_count,
            "beats_count":beats_count,
            "beat_mustViews":beat_mustViews,
            "last_requests":last_requests,
            "request_in_month":days,
            'categories':categories,
            "category_beat":parts,
            "messages_user":messages,
            "order_count" : Order.objects.all().count(),
            "route" : 'dashbord',
        }
        return render(request,'panel/dashbord.html',context)

class AddBeatView(IsAdminMixin,View):
    template_name = 'panel/add_beat.html'
    success_url = reverse_lazy('panel:dashbord')
    
    def get(self,request):
        context = {
            'form_sale':CreateSaleBeatForm,
            'form_free':CreateFreeBeatForm,
            'route': 'add-beat'
        }
        return render(request,self.template_name,context)


    def form_valid(self, form):
        messages.success(self.request,'Beat Added',extra_tags='success')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.warning(self.request,'Form Not Valid',extra_tags='warning')
        return super().form_invalid(form)

class AddFreeBeatView(IsAdminMixin,View):
    def post(self,request):
        form = CreateFreeBeatForm(request.POST, request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            Beat.objects.create(
                title=cd['title'],
                audio_beat=cd['audio_beat'],
                image_beat=cd['image_beat'],
                type='F',
                price=0,
                is_show=cd['is_show'],
                category=cd['category'],
            )
            messages.success(self.request,'Beat Added',extra_tags='success')
        else:
            messages.warning(self.request,'Form Not Valid',extra_tags='warning')
        
        return redirect('panel:add-beat')



class AddSaleBeatView(IsAdminMixin,View):
    def post(self,request):
        form = CreateSaleBeatForm(request.POST, request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            Beat.objects.create(
                title=cd['title'],
                audio_beat=cd['audio_beat'],
                main_beat=cd['main_beat'],
                image_beat=cd['image_beat'],
                type='D',
                price=cd['price'],
                is_show=cd['is_show'],
                category=cd['category'],
            )
            messages.success(self.request,'Beat Added',extra_tags='success')
        else:
            messages.warning(self.request,'Form Not Valid',extra_tags='warning')
        
        return redirect('panel:add-beat')


class AddCategoryView(IsAdminMixin,CreateView):
    template_name = 'panel/add_category.html'
    success_url = reverse_lazy('panel:dashbord')
    form_class  = CreateCategoryForm

    def form_valid(self, form):
        messages.success(self.request,'Category Added',extra_tags='success')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.warning(self.request,'Form Not Valid',extra_tags='warning')
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["route"] = 'add-category'
        return context
    

class BeatListView(IsAdminMixin,ListView):
    template_name = 'panel/list_beat.html'
    model = Beat
    context_object_name = 'beats'
    ordering = ('-created',)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["route"] = 'list-beat'
        return context


class CategoryListView(IsAdminMixin,ListView):
    template_name = 'panel/list_category.html'
    model = Category
    context_object_name = 'categories'
    ordering = ('-created',)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["route"] = 'list-category'
        return context

class SendEmailView(IsAdminMixin,FormView):
    template_name = 'panel/send_email.html'
    form_class = SendEmailForm
    success_url = reverse_lazy('panel:dashbord')

    def form_valid(self, form):
        cd = form.cleaned_data
        users = User.objects.all()
        for user in users:
            user.send_email(cd['subject'],cd['message'])

        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.warning(self.request,'Form Not Valid',extra_tags='warning')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["route"] = 'send-email'
        return context
class SettingsView(IsAdminMixin,UpdateView):
    template_name = 'panel/settings.html'
    success_url = reverse_lazy('panel:settings')
    form_class = SettingSiteForm

    def get_object(self):
        return SiteSettings.objects.first()
    
    def form_valid(self, form):
        messages.success(self.request,'Settings Updated',extra_tags='success')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request,'Form Not Valid',extra_tags='warning')
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["route"] = 'settings'
        return context

class DeleteBeat(IsAdminMixin,View):
    def get(self,request,id):
        beat = Beat.objects.get(id=id)
        try:
            bucket.delete_obj(beat.audio_beat.name)
        except:
            messages.error(request,'Error In Delete Client Beat',extra_tags='danger')
        try:
            bucket.delete_obj(beat.main_beat.name)
        except:
            messages.error(request,'Error In Delete Full Beat',extra_tags='danger')
        try:
            bucket.delete_obj(beat.image_beat.name)
        except:
            messages.error(request,'Error In Delete Image Beat',extra_tags='danger')

        try:
            beat.delete()

            messages.success(request,'Beat Deleted',extra_tags='success')
        except:
            messages.error(request,'May exist on an Order And You Can Delete IT',extra_tags='danger')

        
        return redirect('panel:list-beat')

class DeleteCategory(IsAdminMixin,View):
    def get(self,request,id):
        category = Category.objects.get(id=id)

        try:
            category.delete()
            messages.success(request,'Beat Deleted',extra_tags='success')
        except:
            messages.error(request,'This Category Has Beat',extra_tags='danger')

        return redirect('panel:list-category')

class ModifyBeatView(IsAdminMixin,UpdateView):
    template_name = 'panel/modify.html'
    success_url = reverse_lazy('panel:list-beat')
    form_class = UpdateBeatForm
    slug_field = 'id'
    model = Beat
    
    def form_valid(self, form):
        messages.success(self.request,'Beat Updated',extra_tags='success')
        return super().form_valid( form)

    def form_invalid(self, form):
        messages.warning(self.request,'Form Not Valid',extra_tags='warning')
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["route"] = 'beat'
        return context


class ModifyCategoryView(IsAdminMixin,UpdateView):
    template_name = 'panel/modify.html'
    success_url = reverse_lazy('panel:list-category')
    form_class = UpdateCategoryForm
    slug_field = 'id'
    model = Category
    
    def form_valid(self, form):
        messages.success(self.request,'Beat Updated',extra_tags='success')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request,'Form Not Valid',extra_tags='warning')
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["route"] = 'category'
        return context

class MessagesView(IsAdminMixin,ListView):
    template_name = 'panel/messages.html'
    model = Message
    ordering = ('-created',)
    context_object_name = 'messages_user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["route"] = 'messages'
        return context

class MessageView(IsAdminMixin,DetailView):
    template_name = 'panel/message.html'
    model = Message
    slug_field = 'id'
    context_object_name = 'message'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        message = context['message']
        if not message.seen:
            message.seen = True
            message.save()
        subject = message.subject
        persian_list = 'ProdNavid'
        english_count = 0
        persian_count = 0
        for char in subject:
            if char in persian_list:
                persian_count += 1
            else:
                english_count += 1
        
        if persian_count > english_count:
            context['dir'] = 'rtl'
        else:
            context['dir'] = 'ltr'

        context["route"] = 'messages'
        
        return context
    
class OrdersView(IsAdminMixin,ListView):
    template_name = 'panel/list_order.html'
    model = Order
    context_object_name = 'orders'
    ordering = ('-created',)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["route"] = 'order'
        return context

class UserListView(IsAdminMixin,ListView):
    template_name = 'panel/users.html'
    model = User
    context_object_name = 'users'
    ordering = ('-last_login',)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['route'] = 'users'

        context['count_f'] = User.objects.filter(how_meet='fri').count()
        context['count_g'] = User.objects.filter(how_meet='goo').count()
        context['count_s'] = User.objects.filter(how_meet='soc').count()
        context['count_o'] = User.objects.filter(how_meet='oth').count()


        return context
    
class CancellOrder(IsAdminMixin,View):
    def get(self,request,order_code):
        order = Order.objects.get(order_code=order_code)
        order.payment.status = 'C'
        order.payment.save()

        return redirect('panel:orders')

class DeleteUser(IsAdminMixin,View):
    def get(self,request,id):
        try:
            User.objects.get(id=id).delete()
            messages.success(request,'User Deleted',extra_tags='success')
        except:
            messages.warning(request,'Have Problem In Delete User',extra_tags='warning')

        return redirect('panel:users')