from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('catalog/', views.catalog, name='catalog'),
    path('catalog/<category_id>', views.catalog, name='catalog'),
    path('catalog/<category_id>/<sort>', views.catalog, name='catalog'),
    path('products/<product_id>', views.detailed_product, name='product_detail'),
    path('about/', views.about, name='about'),
    path('add_to_favorite/<int:product_id>/', views.add_to_favorite, name='add_to_favorite'),
    path('remove_from_favorite/<int:product_id>/', views.remove_from_favorite, name='remove_from_favorite'),
    path('favorite/', views.view_favorite, name='favorite'),
]
