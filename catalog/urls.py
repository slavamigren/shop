from django.urls import path
from catalog.views import ProductDetailView, ContactListView, ContactCreateView, ProductCreateView, \
    ProductListView
from catalog.apps import CatalogConfig
app_name = CatalogConfig.name

urlpatterns = [
    path('', ProductListView.as_view(), name='index'),
    path('product/<int:pk>', ProductDetailView.as_view(), name='product'),
    path('create/', ProductCreateView.as_view(), name='create_new_product'),

    path('new_contact/', ContactCreateView.as_view(), name='new_contact'),
    path('contacts/', ContactListView.as_view(), name='contacts'),

]