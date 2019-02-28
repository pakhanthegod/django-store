from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import View, TemplateResponseMixin, ContextMixin
from django.views.generic.list import MultipleObjectMixin
from django.views.generic.detail import SingleObjectMixin

from .models import Product, Category


class ProductListView(MultipleObjectMixin, TemplateResponseMixin, View):
    model = Product
    template_name = 'products/product_list.html'
    paginate_by = 3

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        context = self.get_context_data()

        return self.render_to_response(context)

    def get_queryset(self):
        queryset = super().get_queryset()
        category_raw = self.kwargs.get('category')
        search_query = self.request.GET.get('q')

        if search_query:
            return queryset.filter(name__icontains=search_query)

        if category_raw:
            category = get_object_or_404(Category, slug=category_raw)
            return queryset.filter(category=category)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['category'] = self.kwargs.get('category')

        return context


class ProductDetailView(SingleObjectMixin, TemplateResponseMixin, View):
    model = Product
    template_name = 'products/product_detail.html'
    
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)

        return self.render_to_response(context)