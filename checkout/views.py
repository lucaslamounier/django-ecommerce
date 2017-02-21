# coding=utf-8

<<<<<<< HEAD
from pagseguro import PagSeguro

from paypal.standard.forms import PayPalPaymentsForm
from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received

from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import (
    RedirectView, TemplateView, ListView, DetailView
=======
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import (
            RedirectView, TemplateView, ListView, DetailView
>>>>>>> 2533ec4fe3943df55b3b4e7a648caf069bcfdb9f
)
from django.forms import modelformset_factory
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse
<<<<<<< HEAD
from django.conf import settings
from django.http import HttpResponse
=======
from django.views.decorators.csrf import csrf_exempt
from pagseguro import PagSeguro
from django.http import HttpResponse
from paypal.standard.forms import PayPalPaymentsForm
>>>>>>> 2533ec4fe3943df55b3b4e7a648caf069bcfdb9f

from catalog.models import Product

from .models import CartItem, Order


class CreateCartItemView(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        product = get_object_or_404(Product, slug=self.kwargs['slug'])
        if self.request.session.session_key is None:
            self.request.session.save()
        cart_item, created = CartItem.objects.add_item(
            self.request.session.session_key, product
        )
        if created:
            messages.success(self.request, 'Produto adicionado com sucesso')
        else:
            messages.success(self.request, 'Produto atualizado com sucesso')
        return reverse('checkout:cart_item')


class CartItemView(TemplateView):

    template_name = 'checkout/cart.html'

    def get_formset(self, clear=False):
        CartItemFormSet = modelformset_factory(
            CartItem, fields=('quantity',), can_delete=True, extra=0
        )
        session_key = self.request.session.session_key
        if session_key:
            if clear:
                formset = CartItemFormSet(
                    queryset=CartItem.objects.filter(cart_key=session_key)
                )
            else:
                formset = CartItemFormSet(
                    queryset=CartItem.objects.filter(cart_key=session_key),
                    data=self.request.POST or None
                )
        else:
            formset = CartItemFormSet(queryset=CartItem.objects.none())
        return formset

    def get_context_data(self, **kwargs):
        context = super(CartItemView, self).get_context_data(**kwargs)
        context['formset'] = self.get_formset()
        return context

    def post(self, request, *args, **kwargs):
        formset = self.get_formset()
        context = self.get_context_data(**kwargs)
        if formset.is_valid():
            formset.save()
            messages.success(request, 'Carrinho atualizado com sucesso')
            context['formset'] = self.get_formset(clear=True)
        return self.render_to_response(context)


class CheckoutView(LoginRequiredMixin, TemplateView):

    template_name = 'checkout/checkout.html'

    def get(self, request, *args, **kwargs):
        session_key = request.session.session_key
        if session_key and CartItem.objects.filter(cart_key=session_key).exists():
            cart_items = CartItem.objects.filter(cart_key=session_key)
            order = Order.objects.create_order(
                user=request.user, cart_items=cart_items
            )
<<<<<<< HEAD
            cart_items.delete()
=======
>>>>>>> 2533ec4fe3943df55b3b4e7a648caf069bcfdb9f
        else:
            messages.info(request, 'Não há itens no carrinho de compras')
            return redirect('checkout:cart_item')
        response = super(CheckoutView, self).get(request, *args, **kwargs)
        response.context_data['order'] = order
        return response


class OrderListView(LoginRequiredMixin, ListView):

    template_name = 'checkout/order_list.html'
    paginate_by = 10

    def get_queryset(self):
<<<<<<< HEAD
        return Order.objects.filter(user=self.request.user).order_by('-pk')
=======
        return Order.objects.filter(user=self.request.user)
>>>>>>> 2533ec4fe3943df55b3b4e7a648caf069bcfdb9f


class OrderDetailView(LoginRequiredMixin, DetailView):

<<<<<<< HEAD
    template_name = 'checkout/order_detail.html'
=======
    template_name =  'checkout/order_detail.html'
>>>>>>> 2533ec4fe3943df55b3b4e7a648caf069bcfdb9f

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

<<<<<<< HEAD

=======
>>>>>>> 2533ec4fe3943df55b3b4e7a648caf069bcfdb9f
class PagSeguroView(LoginRequiredMixin, RedirectView):
    # Integração via redirect
    def get_redirect_url(self, *args, **kwargs):
        order_pk = self.kwargs.get('pk')
        order = get_object_or_404(
            Order.objects.filter(user=self.request.user), pk=order_pk
        )
        pg = order.pagseguro()
        # constroi toda a url http://host/path
        pg.redirect_url = self.request.build_absolute_uri(
            reverse('checkout:order_detail', args=[order.pk])
        )
        # resultado da transação, informa se a compra foi concluida.
        pg.notification_url = self.request.build_absolute_uri(
            reverse('checkout:pagseguro_notification')
        )
        response = pg.checkout()
        return response.payment_url

<<<<<<< HEAD

class PaypalView(LoginRequiredMixin, TemplateView):
=======
def PaypalView(LoginRequiredMixin, TemplateView):
>>>>>>> 2533ec4fe3943df55b3b4e7a648caf069bcfdb9f

    template_name = 'checkout/paypal.html'

    def get_context_data(self, **kwargs):
        context = super(PaypalView, self).get_context_data(**kwargs)
        order_pk = self.kwargs.get('pk')
        order = get_object_or_404(
            Order.objects.filter(user=self.request.user), pk=order_pk
        )
        paypal_dict = order.paypal()
        paypal_dict['return_url'] = self.request.build_absolute_uri(
            reverse('checkout:order_list')
        )
        paypal_dict['cancel_return'] = self.request.build_absolute_uri(
            reverse('checkout:order_list')
        )
<<<<<<< HEAD
        paypal_dict['notify_url'] = self.request.build_absolute_uri(
            reverse('paypal-ipn')
        )
=======
>>>>>>> 2533ec4fe3943df55b3b4e7a648caf069bcfdb9f
        context['form'] = PayPalPaymentsForm(initial=paypal_dict)
        return context


@csrf_exempt
def pagseguro_notification(request):
    notification_code = request.POST.get('notificationCode', None)
    if notification_code:
        pg = PagSeguro(
            email=settings.PAGSEGURO_EMAIL, token=settings.PAGSEGURO_TOKEN,
            config={'sandbox': settings.PAGSEGURO_SANDBOX}
        )
        notification_data = pg.check_notification(notification_code)
        status = notification_data.status
        reference = notification_data.reference
        try:
            order = Order.objects.get(pk=reference)
        except Order.DoesNotExist:
            pass
        else:
            order.pagseguro_update_status(status)
    return HttpResponse('OK')


<<<<<<< HEAD
def paypal_notification(sender, **kwargs):
    ipn_obj = sender
    if ipn_obj.payment_status == ST_PP_COMPLETED and \
        ipn_obj.receiver_email == settings.PAYPAL_EMAIL:
        try:
            order = Order.objects.get(pk=ipn_obj.invoice)
            order.complete()
        except Order.DoesNotExist:
            pass


valid_ipn_received.connect(paypal_notification)


=======
pagseguro_view = PagSeguroView.as_view()
>>>>>>> 2533ec4fe3943df55b3b4e7a648caf069bcfdb9f
create_cartitem = CreateCartItemView.as_view()
cart_item = CartItemView.as_view()
checkout = CheckoutView.as_view()
order_list = OrderListView.as_view()
order_detail = OrderDetailView.as_view()
<<<<<<< HEAD
pagseguro_view = PagSeguroView.as_view()
paypal_view = PaypalView.as_view()
=======
>>>>>>> 2533ec4fe3943df55b3b4e7a648caf069bcfdb9f
