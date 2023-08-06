from django.urls import path
from catalog.views import ProductDetailView, ContactListView, ContactCreateView, ProductCreateView, \
    ProductListView, ProductUpdateView, ProductDeleteView
from catalog.apps import CatalogConfig
app_name = CatalogConfig.name

urlpatterns = [
    path('', ProductListView.as_view(), name='index'),
    path('product_detail/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('create/', ProductCreateView.as_view(), name='create_new_product'),
    path('update/<int:pk>/', ProductUpdateView.as_view(), name='update_product'),
    path('delete/<int:pk>/', ProductDeleteView.as_view(), name='delete_product'),

    path('new_contact/', ContactCreateView.as_view(), name='new_contact'),
    path('contacts/', ContactListView.as_view(), name='contacts'),

]