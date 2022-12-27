from django.shortcuts import render,redirect
from django.views import View
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.order.models import Order
from apps.beat.models import Beat
from apps.PanelNavid.models import SiteSettings
from django.contrib import messages
from django.urls import reverse
from .models import Payment,Order
import random
from django.http import HttpResponseRedirect
from django.conf import settings
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils.translation import gettext as _

# ZARIN PAL
from django.http import HttpResponse
import requests
import json

MERCHANT = settings.MERCHANT
ZP_API_REQUEST = settings.ZP_API_REQUEST
ZP_API_VERIFY = settings.ZP_API_VERIFY
ZP_API_STARTPAY = settings.ZP_API_STARTPAY

# CallbackURL = 'https://prodnavid/' + reverse_lazy('accounts:verify-payment')


__all__ = [
    'OrdersView',
    'ConfirmOrder',
    'ConfirmPayment',
    'VerifyPaymentView',
    'ResendBeat'
]

class OrdersView(LoginRequiredMixin,ListView):
    login_url = reverse_lazy('accounts:login')
    template_name = 'order/orders.html'
    context_object_name = 'orders'

    def get_queryset(self):
        queryset = Order.objects.filter(user=self.request.user)
        return queryset


class ConfirmOrder(LoginRequiredMixin,View):
    login_url = reverse_lazy('accounts:login')
    def get(self,request):
        if not request.user.is_authenticated:
            messages.error(request,_("Log in first or <a class='text-primary' href='{}'>register</a> if you don't have an account").format(reverse('accounts:register')),extra_tags='danger')
            return redirect('accounts:login')

        code_beat = request.GET.get('beat')
        beat = Beat.objects.get(code=code_beat)
    
        if not beat or SiteSettings.objects.first().stop_seling:
            messages.error(request,'Access denied',extra_tags='danger')
            return redirect('beat:index')

        self.request.session['code'] = code_beat

        return render(request,'order/confirm.html',{'beat':beat})

class ConfirmPayment(LoginRequiredMixin,View):
    login_url = reverse_lazy('accounts:login')
    def get(self,request):
        beat_code = self.request.session['code']
        beat = Beat.objects.get(code=beat_code)
        if beat.is_in_order():
            messages.warning(request,_('Beat Not available'),extra_tags='warning')
            return redirect('beat:index')

        if beat_code:
            payment = Payment.objects.create(link='null')
            while True:
                random_num = random.randint(1000,9999)
                if Order.objects.filter(order_code=random_num).exists():
                    continue
                else:
                    break

            order = Order.objects.create(
                order_code=random_num,
                user=request.user,
                beat=beat,
                price=beat.price,
                payment=payment
            )
            CallbackURL = 'http://prodnavid.ir' + reverse_lazy('accounts:verify-payment')
            description = f"Sold > {beat_code}"
            req_data = {
                "merchant_id": MERCHANT,
                "amount": int(str(order.price) + "0"),
                "callback_url": CallbackURL,
                "description": description,
                "metadata": {"mobile": str(order.user.phone_number), "email": order.user.email}
            }
            req_header = {"accept": "application/json","content-type": "application/json'"}
            req = requests.post(url=ZP_API_REQUEST, data=json.dumps(
                req_data), headers=req_header)
            authority = req.json()['data']['authority']
            if len(req.json()['errors']) == 0:
                self.request.session['order_code'] = order.order_code
                payment.link = ZP_API_STARTPAY.format(authority=authority)
                payment.save()
                return redirect(payment.link)
            else:
                e_code = req.json()['errors']['code']
                e_message = req.json()['errors']['message']
                messages.warning(request,_('Have A Error In Payment,Plase Send Message To Email <br>Error code: {}').format(f'{e_code} | {e_message}'))
                return redirect('beat:index')
        else:
            messages.success(request,_('Error'),extra_tags='danger')
            return redirect('beat:index')
    
class VerifyPaymentView(View):
    def get(self,request):
        t_status = request.GET.get('Status')
        t_authority = request.GET['Authority']
        order = Order.objects.get(order_code=self.request.session['order_code'])
        beat = Beat.objects.get(code=self.request.session['code'])
        if request.GET.get('Status') == 'OK':
            req_header = {"accept": "application/json",
                        "content-type": "application/json'"}
            req_data = {
                "merchant_id": MERCHANT,
                "amount": int(str(order.price) + "0"),
                "authority": t_authority
            }
            req = requests.post(url=ZP_API_VERIFY, data=json.dumps(req_data), headers=req_header)
            if len(req.json()['errors']) == 0:
                t_status = req.json()['data']['code']
                if t_status == 100:
                    messages.success(request,_('You Order Paid<br>Tank You For Trust To Me'),extra_tags='success')
                    # Order Operation
                    order.sended = True
                    order.recived = True
                    order.payment.status = "P"
                    order.payment.paid = timezone.now()
                    order.save()
                    order.payment.save()
                    beat.is_sold = True
                    beat.save()

                    # SEND BEAT TO EMAIL
                    message = f"""
                    Hey {order.user},
                    Thank You For Buy Beat
                    This Link Is Your Full Beat
                    {beat.main_beat.url}

                    BeatID:{beat.code}
                    OrderID:{order.order_code}
                    """
                    order.user.send_email('ProdNaid : Full Beat',message)
                    messages.info(request,_('Beat File Sended To Email For You'))
                    return redirect('accounts:order')
                elif t_status == 101:
                    messages.warning(request,_('The transaction has already been paid<br>If You Have Problem Send Email For Me'),extra_tags='warning')
                    return redirect('accounts:order')
                else:
                    messages.warning(request,_('The transaction Failed<br>If You Have Problem Send Email For Me'),extra_tags='warning')
                    order.payment.status = "C"
                    order.payment.save()
                    return redirect('accounts:order')
            else:
                e_code = req.json()['errors']['code']
                e_message = req.json()['errors']['message']
                messages.warning(request,_('Have A Error In Payment,Plase Send Message To Email <br>Error code: {}').format(f'{e_code} | {e_message}'))
                return redirect('beat:index')
        else:
            messages.warning(request,_('Transaction failed or canceled by user'))
            order.payment.status = "C"
            order.payment.save()
            return redirect('beat:index')
    

class ResendBeat(LoginRequiredMixin,View):
    login_url = reverse_lazy('accounts:login')

    def get(self,request,order_id):
        order = get_object_or_404(Order,order_code=order_id)
        if order.user == request.user:
            if order.payment.status == 'P':
                message = f"""
                    Hey {order.user},
                    This is Link Your Beat
                    {order.beat.main_beat.url}

                    BeatID:{order.beat.code}
                    OrderID:{order.order_code}
                """

                order.user.send_email('ProdNaid : ResendBeat',message)
                messages.success(request,_('Resendded Beat TO Your Email'),extra_tags='success')
            else:
                messages.warning(request,_('Must First Pay this Beat'),extra_tags='warning')
        else:
            messages.warning(request,_('Error Internal'),extra_tags='danger')
        
        return redirect('accounts:orders')