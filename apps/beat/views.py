from django.shortcuts import render,get_object_or_404,redirect
from django.views.generic import ListView,DetailView
from django.views import View
from django.db.models import Count, Q
from .models import *
from .forms import MessageForm
from django.contrib import messages
from apps.PanelNavid.models import Message,InfoDeveloper
from django.utils.translation import activate

__all__ = [
    'HomeView',
    'DetailBeatView',
    'ListBeatView',
    'AboutView',
    'DeveloperView',
    'FreeListBeatView',
]


def change_lang(request):

    activate('en')
    return redirect('beat:index')

class HomeView(View):
    def get(self,request):
        all_beats = Beat.objects.published()
        newsted = all_beats.order_by('-created')
        mustview = all_beats.annotate(count=Count('hits')).order_by('-count','-created')
        free = all_beats.filter(price=0).order_by('-created')
        categories_on_home = Category.objects.filter(on_home=True)

        context = {
                "newsted" : newsted,
                "mustview" : mustview,
                "free" : free,
                'categories_on_home':categories_on_home,
            }
        return render(request,'beat/index.html',context)

class DetailBeatView(DetailView):
    template_name = 'beat/detail.html'
    context_object_name = 'beat'

    def get_object(self):
        code_beat = self.kwargs.get('code_beat')
        beat =  get_object_or_404(Beat.objects.published(),code=code_beat)

        ip_address = self.request.user.ip_address
        if not Ipaddress.objects.filter(ip_addr=ip_address).exists():
            ip_obj = Ipaddress.objects.create(ip_addr=ip_address)
        else:
            ip_obj = Ipaddress.objects.get(ip_addr=ip_address)

        if ip_obj not in beat.hits.all():
            try:
                beat.hits.add(ip_obj)
            except:
                pass

        return beat

class ListBeatView(ListView):
    template_name = 'beat/list.html'
    context_object_name = 'beats'

    def get_queryset(self):
        category_slug = self.kwargs.get('category_slug')
        
        if category_slug:
            category = Category.objects.get(slug=category_slug)
            if self.request.GET.get('order') == "view":
                beats = Beat.objects.filter(category=category,is_show=True).annotate(count=Count('hits')).order_by('-count','-created')
            elif self.request.GET.get('order') == "avalible":
                beats = Beat.objects.filter(category=category,is_show=True,is_sold=False).order_by('-created')
            else:
                beats = Beat.objects.filter(category=category,is_show=True).order_by('-created')
        else:
            if self.request.GET.get('order') == "view":
                beats = Beat.objects.published().annotate(count=Count('hits')).order_by('-count','-created')
            elif self.request.GET.get('order') == "avalible":
                beats = Beat.objects.filter(is_show=True,is_sold=False).order_by('-created')
            else:
                beats = Beat.objects.published().order_by('-created')

        return beats

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        context["category_active"] = self.kwargs.get('category_slug')
        context["order"] = self.request.GET.get('order')
        return context

class FreeListBeatView(ListView):
    template_name = 'beat/list.html'
    context_object_name = 'beats'

    def get_queryset(self):
        category_slug = self.kwargs.get('category_slug')
        
        if category_slug:
            category = Category.objects.get(slug=category_slug)
            if self.request.GET.get('order') == "view":
                beats = Beat.objects.filter(category=category,price=0).annotate(count=Count('hits')).order_by('-count','-created')
            else:
                beats = Beat.objects.filter(category=category,price=0).order_by('-created')
        else:
            if self.request.GET.get('order') == "view":
                beats = Beat.objects.free().annotate(count=Count('hits')).order_by('-count','-created')
            else:
                beats = Beat.objects.free().order_by('-created')

        return beats

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        context["category_active"] = self.kwargs.get('category_slug')
        context["order"] = self.request.GET.get('order')
        context["free"] = True
        return context

class AboutView(View):
    def get(self,request):
        form = MessageForm
        return render(request,'about.html',{'form':form})
    
    def post(self,request):
        form = MessageForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            Message.objects.create(
                subject=cd['subject'],
                message=cd['message'],
                user=request.user
                )
            messages.success(request,'Message Sended',extra_tags="success")
        else:
            messages.warning(request,'Form Not Valid',extra_tags="warning")
        return redirect('beat:index')
    

class DeveloperView(View):
    def get(self,request):
        InfoDeveloper.load()
        developer = InfoDeveloper.objects.first()
        return render(request,'developer.html',{'developer':developer})