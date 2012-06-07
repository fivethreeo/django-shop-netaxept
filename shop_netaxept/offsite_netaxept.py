#-*- coding: utf-8 -*-
from decimal import Decimal

from django.conf import settings
from django.conf.urls.defaults import patterns, url, include
from django.contrib.sites.models import get_current_site
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect

from djnetaxept.models import NetaxeptPayment
from djnetaxept.utils import TERMNAL, CURRENCY_CODE, MERCHANTID, TOKEN

class OffsiteNetaxeptBackend(object):
    '''
    Glue code to let django-SHOP talk to django-netaxept.

    The django-netaxept package already defines models with managers that sends data to netaxept, and logs everything
    to the database (desirable)
    '''

    backend_name = "Netaxept"
    url_namespace = "netaxept"

    #===========================================================================
    # Defined by the backends API
    #===========================================================================

    def __init__(self, shop):
        self.shop = shop

    def get_urls(self):
        urlpatterns = patterns('',
            url(r'^$', self.view_that_asks_for_money, name='netaxept'),
            url(r'^return/$', self.netaxept_return_view, name='netaxept_return'),
            url(r'^error/$', self.netaxept_error_view, name='netaxept_error'),
            url(r'^success/$', self.netaxept_success_view, name='netaxept_success')
        )
        return urlpatterns

    #===========================================================================
    # Views
    #===========================================================================

    def view_that_asks_for_money(self, request):
        order = self.shop.get_order(request)
        url_scheme = 'https' if request.is_secure() else 'http'
        url_domain = get_current_site(request).domain
        redirect_url = '%s://%s%s' % (url_scheme, url_domain, reverse('netaxept_return'))
        payment = NetaxeptPayment.objects.register_payment(
            redirect_url=redirect_url,
            amount=str(int(self.shop.get_order_total(order)*100)),
            currencycode=CURRENCY_CODE,
            ordernumber=self.shop.get_order_unique_id(order),
            description=self.shop.get_order_short_name(order)
        )
        if payment.completed():
            return HttpResponseRedirect('%s?merchantId=%s&transactionId=%s' % (TERMNAL, MERCHANTID, payment.transaction_id))
        else:
            rc = RequestContext(request, {})
            return render_to_response("shop_netaxept/registrationerror.html", rc)

    @csrf_exempt
    def netaxept_return_view(self, request):
        payment = NetaxeptPayment.objects.get(transaction_id=request.GET.get('transactionId'))
        transaction = payment.auth()
        if transaction.completed():
            amount = Decimal(payment.amount) / 100
            self.shop.confirm_payment(self.shop.get_order_for_id(payment.ordernumber), amount, payment.transaction_id, self.backend_name)
            return HttpResponseRedirect(reverse('netaxept_success'))
        else:
            return HttpResponseRedirect(reverse('netaxept_error') + '?error=%s' % transaction.message)

    def netaxept_error_view(self, request):
        rc = RequestContext(request, {'message': request.GET.get('error')})
        return render_to_response("shop_netaxept/error.html", rc)
    
    def netaxept_success_view(self, request):
        rc = RequestContext(request, {})
        return render_to_response("shop_netaxept/success.html", rc)