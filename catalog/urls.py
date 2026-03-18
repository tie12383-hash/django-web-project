from django.urls import path
from django.views.decorators.cache import cache_page
from . import views

app_name = 'catalog'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('contacts/', views.ContactsView.as_view(), name='contacts'),
    path('product/<int:pk>/', cache_page(60 * 15)(views.ProductDetailView.as_view()), name='product_detail'),  # кеш 15 минут
    path('add/', views.ProductCreateView.as_view(), name='product_create'),
    path('product/<int:pk>/update/', views.ProductUpdateView.as_view(), name='product_update'),
    path('product/<int:pk>/delete/', views.ProductDeleteView.as_view(), name='product_delete'),
    path('product/<int:pk>/unpublish/', views.ProductUnpublishView.as_view(), name='product_unpublish'),
    path('category/<int:pk>/', views.CategoryProductsView.as_view(), name='category_products'),
]
