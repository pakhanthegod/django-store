from django.shortcuts import render, redirect
from django.views.generic.base import View, TemplateResponseMixin, ContextMixin
from django.views.generic.list import MultipleObjectMixin
from django.views.generic.detail import SingleObjectMixin

from .models import Product, Category


class ProductListView(MultipleObjectMixin, TemplateResponseMixin, View):
    model = Product
    template_name = 'products\\product_list.html'
    paginate_by = 9

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        context = self.get_context_data()

        return self.render_to_response(context)

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.kwargs.get('category', 't-shirt')

        return queryset.filter(category__slug=category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()

        return context


class ProductDetailView(SingleObjectMixin, TemplateResponseMixin, View):
    model = Product
    template_name = 'products\\product_detail.html'
    
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)

        return self.render_to_response(context)