from django.contrib.messages import success
from django.core.exceptions import PermissionDenied
from django.forms import inlineformset_factory, formset_factory
from django.http import Http404
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, TemplateView, DetailView, CreateView, UpdateView, DeleteView

from catalog.forms import ProductForm, ProductVersionForm, ContactForm
from catalog.models import Product, Contact, ProductVersion
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from catalog.services import get_active_products_version


class ProductListView(ListView):
    model = Product
    paginate_by = 12

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        is_actual_data = get_active_products_version()  # ProductVersion.objects.filter(is_actual=True)
        context_data['is_actual_inf'] = is_actual_data
        context_data['pk_of_actual'] = [i.product_id for i in is_actual_data]
        return context_data


class ProductDetailView(DetailView):
    model = Product

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        is_actual_data = ProductVersion.objects.filter(product_id=self.kwargs['pk'], is_actual=True)
        context_data['is_actual_inf'] = is_actual_data

        if self.object.owner != self.request.user:
            context_data['owner'] = False
        else:
            context_data['owner'] = True

        return context_data


class ProductCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):  # LoginRequiredMixin для закрытия доступа неавторизованному
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:index')
    permission_required = 'catalog.add_product'
    #login_url = reverse_lazy('users:login')  # если не авторизован, не даём просмотр, а отправляем на страницу авторизации


    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        ProductVersionFormSet = inlineformset_factory(Product, ProductVersion, form=ProductVersionForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = ProductVersionFormSet(self.request.POST)
        else:
            context_data['formset'] = ProductVersionFormSet()
        return context_data

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:index')
    permission_required = 'catalog.change_product'
    #login_url = reverse_lazy('users:login')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user and not self.request.user.is_staff:
            raise Http404
        return self.object

    def get_success_url(self):
        return reverse('catalog:product_detail', args=[self.kwargs['pk']])

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        ProductVersionFormSet = inlineformset_factory(Product, ProductVersion, form=ProductVersionForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = ProductVersionFormSet(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = ProductVersionFormSet(instance=self.object)
        return context_data

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()
        return super().form_valid(form)


class ProductDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('catalog:index')
    permission_required = 'catalog.delete_product'
    #login_url = reverse_lazy('users:login')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user and not self.request.user.is_staff:
            raise Http404
        return self.object


class ContactListView(ListView):
    model = Contact


class ContactCreateView(CreateView):
    model = Contact
    form_class = ContactForm
    success_url = reverse_lazy('catalog:contacts')

