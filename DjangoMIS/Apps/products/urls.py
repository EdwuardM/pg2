from django.urls import path

from . import views

app_name = "Apps.products"
urlpatterns = [

     path(' ', views.CategoriesListView, name='categories_list'),
     path('categories/add', views.CategoriesAddView, name='categories_add'),
     path('categories/update/<str:category_id>',
          views.CategoriesUpdateView, name='categories_update'),
     path('categories/delete/<str:category_id>',
          views.CategoriesDeleteView, name='categories_delete'),


     path('', views.ProductsListView, name='products_list'),
     path('add', views.ProductsAddView, name='products_add'),
     path('update/<str:product_id>',
          views.ProductsUpdateView, name='products_update'),
     path('delete/<str:product_id>',
          views.ProductsDeleteView, name='products_delete'),
     path("get", views.GetProductsAJAXView, name="get_products"),


     path('warehouses', views.WarehousesListView, name='warehouses_list'),
     path('warehouses/add', views.WarehousesAddView, name='warehouses_add'),
     path('warehouses/update/<str:warehouse_id>', 
          views.WarehousesUpdateView, name='warehouses_update'),
     path('warehouses/delete/<str:warehouse_id>',
          views.WarehousesDeleteView, name='warehouses_delete'),

     path('Regla/add', views.RuleSupplyAddView, name='rulesupply_add'),
]
