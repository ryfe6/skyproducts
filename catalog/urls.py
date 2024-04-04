from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from catalog.views import (CatalogListView, ContactsView,  ProductsDetailView, ProductCreateView, ProductUpdateView,
                           ProductDeleteView, BlogCreateView, BlogListView, BlogDetailView, BlogDeleteView,
                           BlogUpdateView)
from catalog.apps import CatalogConfig

app_name = CatalogConfig.name

urlpatterns = [
    path('', CatalogListView.as_view(), name='product_list'),
    path("contacts/", ContactsView.as_view(), name='contacts'),
    path('catalog/<int:pk>/',  ProductsDetailView.as_view(), name='product_view'),
    path('catalog/create/', BlogCreateView.as_view(), name='create'),
    path('catalog/blog_list/', BlogListView.as_view(), name='blog'),
    path('catalog/blog/<int:pk>/', BlogDetailView.as_view(), name='blog_detail'),
    path('catalog/delete/<int:pk>', BlogDeleteView.as_view(), name='blog_delete'),
    path('catalog/edit/<int:pk>', BlogUpdateView.as_view(), name='blog_update'),
    path('catalog/product_create', ProductCreateView.as_view(), name='product_create'),
    path('catalog/product_edit/<int:pk>', ProductUpdateView.as_view(), name='product_update'),
    path('catalog/product_delete/<int:pk>', ProductDeleteView.as_view(), name='product_delete')

    ]
