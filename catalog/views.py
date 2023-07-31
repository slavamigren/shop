from django.contrib.messages import success
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, TemplateView, DetailView, CreateView
from catalog.models import Product, Contact



class ProductListView(ListView):
    model = Product
    template_name = 'catalog/index.html'
    paginate_by = 3




class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product.html'


class ProductCreateView(CreateView):
    model = Product
    fields = ('name', 'description', 'photo', 'category', 'price')
    success_url = reverse_lazy('catalog:index')


class ContactListView(ListView):
    model = Contact
    template_name = 'catalog/contacts.html'


class ContactCreateView(CreateView):
    model = Contact
    fields = ('name', 'phone_number', 'user_text')
    success_url = reverse_lazy('catalog:contacts')

