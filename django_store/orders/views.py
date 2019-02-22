from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import View, TemplateResponseMixin
from django.views.generic.list import MultipleObjectMixin

from products.models import Product
from .models import Order, OrderList


class AddToCart(LoginRequiredMixin, View):
    login_url = 'profiles:login'

    def get(self, request, *args, **kwargs):
        cart = request.session.get('cart', {})
        product_id = str(self.kwargs['product_id'])
        if product_id in cart:
            cart[product_id] += 1
        else:
            cart[product_id] = 1
        request.session['cart'] = cart

        messages.success(request, 'Товар добавлен')

        return redirect(request.GET.get('from', 'products:product_list'))


class DeleteFromCart(LoginRequiredMixin, View):
    login_url = 'profiles:login'
    
    def get(self, request, *args, **kwargs):
        cart = request.session.get('cart')
        product_id = str(self.kwargs['product_id'])
        cart[product_id] -= 1
        if not cart[product_id]:
            del cart[product_id]
        request.session['cart'] = cart

        messages.success(request, 'Товар удален')

        return redirect('orders:cart')


class CartView(LoginRequiredMixin, MultipleObjectMixin, TemplateResponseMixin, View):
    model = Product
    template_name = 'orders\\cart.html'
    paginate_by = 9
    login_url = 'profiles:login'

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        context = self.get_context_data()

        return self.render_to_response(context)

    def get_queryset(self):
        queryset = super().get_queryset()

        # Get a category from a url if it passed else set the category to 't-shirt'
        category = self.kwargs.get('category', 't-shirt')

        return queryset.filter(category__slug=category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Add the cart list with Product objects to the context
        cart_products = []
        for product_id in self.request.session['cart'].keys():
            product = self.model.objects.get(pk=product_id)
            cart_products.append((product, self.request.session['cart'][product_id]))
        
        context['cart_products'] = cart_products

        return context


class CreateOrderView(LoginRequiredMixin, View):
    login_url = 'profiles:login'
    
    def get(self, request, *args, **kwargs):
        # Populate the cart list with Product objects by IDs from the session
        cart_products = []
        for product_id in request.session['cart'].keys():
            product = Product.objects.get(pk=product_id)
            cart_products.append((product, request.session['cart'][product_id]))

        # Create customer's order
        order = Order.objects.create(customer=request.user.customer)
        order.save()

        # Populate a customer's order with Product objects from the cart list
        for product_tuple in cart_products:
            order_product = OrderList.objects.create(order=order, product=product_tuple[0], quantity=product_tuple[1])
            order_product.save()

        del request.session['cart']

        messages.success(request, 'Ваш заказ оформлен')

        return redirect('products:product_list')