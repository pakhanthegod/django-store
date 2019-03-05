# TODO: Create form for creating an order
from django import forms
from django.utils.translation import gettext_lazy as _

from .models import OrderList, Order
from products.models import Product


class OrderListForm(forms.ModelForm):
    class Meta:
        model = OrderList
        fields = '__all__'

    def clean_quantity(self):
        product = self.cleaned_data.get('product')
        quantity = self.cleaned_data.get('quantity')

        if (product and quantity):
            if quantity > product.quantity:
                self.add_error('quantity', 'Product is out')
                raise forms.ValidationError(_('Product is out'), code="Invalid")

        return quantity
