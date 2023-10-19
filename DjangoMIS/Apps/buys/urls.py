from django.urls import path

from . import views

app_name = "Apps.buys"
urlpatterns = [
    path('', views.ShoppingListView, name='shopping_list'),
    path('list/', views.ShoppingLisSupplierstView, name='shopping_list_suppliers'),
    path('add/<int:supplier_id>/', views.BuysListAddView, name='buys_list_add'),
    path('details/<int:shopping_id>/', views.ShoppingLisDetailsView, name='shopping_list_details'),
    path('delete_product_list/<int:shopping_id>/<int:product_id>/', views.delete_product_list, name='delete_product_list'),
    
    path('buy/<int:shopping_id>/', views.BuysAddView, name='buys_list'),
    path('buys/', views.BuysView, name='buyss_list'),
    path('bought_products/<int:shopping_id>/', views.BoughtProductsView, name='bought_products'),

    
]