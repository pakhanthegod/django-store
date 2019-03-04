from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic.base import View, TemplateResponseMixin, ContextMixin
from django.views.generic.list import MultipleObjectMixin
from django.views.generic.detail import SingleObjectMixin

from .models import Product, Category


class ProductListView(MultipleObjectMixin, TemplateResponseMixin, View):
    model = Product
    template_name = 'products/product_list.html'
    allow_empty = True
    paginate_by = 3

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        context = self.get_context_data()

        return self.render_to_response(context)

    def get_queryset(self):
        queryset = super().get_queryset()
        category_raw = self.kwargs.get('category')
        search_query = self.request.GET.get('q')
        sort = self.request.GET.get('sort')

        if search_query:
            return queryset.filter(name__icontains=search_query)

        if category_raw:
            category = get_object_or_404(Category, slug=category_raw)
            queryset = queryset.filter(category=category)

        if sort:
            if sort == 'priceup':
                queryset = queryset.order_by('price')
            if sort == 'pricedown':
                queryset = queryset.order_by('-price')
            if sort == 'nameup':
                queryset = queryset.order_by('name')
            if sort == 'namedown':
                queryset = queryset.order_by('-name')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['categories'] = Category.objects.all()
        context['category'] = self.kwargs.get('category')

        return context

    def get_sort_base_url(self):
        category = self.kwargs.get('category')

        if category:
            return reverse('products:list', kwargs={'category': category})
        else:
            return reverse('products:list_all')

    def get_price_sort_url(self):
        BASE_URL = self.get_sort_base_url()

        mapping = {
            'priceup': BASE_URL + '?sort=pricedown',
            'pricedown': BASE_URL + '?sort=priceup',
        }

        return mapping.get(self.request.GET.get('sort'), BASE_URL + '?sort=pricedown')

    def get_name_sort_url(self):
        BASE_URL = self.get_sort_base_url()

        mapping = {
            'nameup': BASE_URL + '?sort=namedown',
            'namedown': BASE_URL + '?sort=nameup',
        }

        return mapping.get(self.request.GET.get('sort'), BASE_URL + '?sort=namedown')


class ProductDetailView(SingleObjectMixin, TemplateResponseMixin, View):
    model = Product
    template_name = 'products/product_detail.html'
    
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)

        return self.render_to_response(context)