from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import get_template
from Apps.suppliers.models import Supplier
from Apps.products.models import Product, RuleSupply 
from .models import BuyDetail, Buy, ShoppingList
from django.utils import timezone
from django.db import transaction
from django.db.models import Sum
from datetime import datetime
from xhtml2pdf import pisa
from io import BytesIO
from django.http import JsonResponse
import json
import warnings
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import get_object_or_404 

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

@login_required(login_url="/accounts/login/")
def ShoppingListView(request):
    shoppinglists = ShoppingList.objects.filter(status="ACTIVO")
    context = {
        "active_icon": "buys_list",
        "shoppinglists": shoppinglists,
    }
    return render(request, "buys/shopping_list.html", context=context)

@login_required(login_url="/accounts/login/")
def ShoppingLisSupplierstView(request):
    suppliers = Supplier.objects.all()
    context = {
        "active_icon": "buys_list",
        "suppliers": suppliers,
    }

    return render(request, "buys/shopping_list_suppliers.html", context=context)

@login_required(login_url="/accounts/login/")
def BuysListAddView(request, supplier_id):
    rule_supply = RuleSupply.objects.filter(supplier_id=supplier_id).first()
    supplier = Supplier.objects.get(id=supplier_id) 

    if rule_supply:
        products = Product.objects.filter(ruleSupply=rule_supply, quantity__lte=rule_supply.minimumAmount)
    else:
        products = Product.objects.filter(warehouse__supplier_id=supplier_id, quantity__lte=rule_supply.minimumAmount)
    context = {
        "active_icon": "buys_list",
        "products": products,
        "supplier": supplier,
    }
    if request.method == 'POST':
        if is_ajax(request=request):
            data = json.loads(request.body)
            today = datetime.now()
            supplier = Supplier.objects.get(id=supplier_id)
            buy_attributes = {
                "supplier": supplier,
                "grand_total": float(data["grand_total"]),
                "status": "ACTIVO",
                "opening_date": today,
            }
            try:
                with transaction.atomic():
                    new_shopinglist = ShoppingList.objects.create(**buy_attributes)
                    new_shopinglist.save()

                products = data["products"]
                for product in products:
                    detail_attributes = {
                        "shoppinglist": ShoppingList.objects.get(id=new_shopinglist.id),
                        "product": Product.objects.get(id=int(product["id"])),
                        "quantity": product["quantity"],
                        "total_detail": product["total_product"]
                    }
                    buy_detail_new = BuyDetail.objects.create(
                        **detail_attributes)
                    buy_detail_new.save()
                    product_instance = Product.objects.get(id=int(product["id"]))
                    product_instance.save()
                messages.success(
                    request, '¡Compra creada con exito!', extra_tags="success")
            except Exception as e:
                messages.success(
                    request, '¡Hubo un error al obtener la compra!', extra_tags="danger")
        return redirect('Apps.buys:shopping_list')

    return render(request, "buys/shopping_list_add.html", context=context)

@login_required(login_url="/accounts/login/")
def BuysAddView(request, shopping_id):
    try:
        today = timezone.now()
        shoppinglist = ShoppingList.objects.get(id=shopping_id)
        
        # Crea una nueva instancia de Buy basada en la ShoppingList existente
        new_buy = Buy.objects.create(
            shoppinglist=shoppinglist,  # Asigna directamente la instancia de ShoppingList
            opening_date=today,
            grand_total=shoppinglist.grand_total,
        )

        # Cambia el estado de la ShoppingList a "INACTIVO" después de crear el Buy
        shoppinglist.status = "INACTIVO"
        shoppinglist.save()

        return redirect('Apps.buys:shopping_list')

    except ShoppingList.DoesNotExist:
        messages.error(request, 'La lista de compras no existe.', extra_tags="danger")
        return redirect('Apps.buys:shopping_list')
    
@login_required(login_url="/accounts/login/")
def BuysView(request):
    context = {
        "active_icon": "buyss",
        "buys": Buy.objects.all()
    }
    return render(request, "buys/buys.html", context=context)


@login_required(login_url="/accounts/login/")
def ShoppingLisDetailsView(request, shopping_id):
    shopping_list = ShoppingList.objects.get(id=shopping_id)
    products = Product.objects.filter(buydetail__shoppinglist=shopping_list)

    product_data = [] 
    for product in products:
        buy_detail = product.buydetail_set.filter(shoppinglist=shopping_list).first()
        quantity = buy_detail.quantity if buy_detail else 0
        product_data.append({
            "product": product,
            "quantity": quantity,
        })

    context = {
        "active_icon": "buys_list",
        "products": product_data, 
        "shopping_id": shopping_id,
    }
    return render(request, "buys/shopping_list_details.html", context=context)

@login_required(login_url="/accounts/login/")
def delete_product_list(request, shopping_id, product_id):
    shopping_list = get_object_or_404(ShoppingList, id=shopping_id)
    product = get_object_or_404(Product, id=product_id)
    try:
        buy_detail = BuyDetail.objects.get(product=product, shoppinglist=shopping_list)
        buy_detail.delete()
    except BuyDetail.DoesNotExist:
        pass

    return redirect('Apps.buys:shopping_list_details', shopping_id=shopping_id)


def BoughtProductsView(request, shopping_id):
    shopping_list = ShoppingList.objects.get(id=shopping_id)
    bought_products = BuyDetail.objects.filter(shoppinglist=shopping_list)

    context = {
        "active_icon": "buyss",
        "bought_products": bought_products,
        "shopping_list": shopping_list,
    }
    return render(request, "buys/buys_details.html", context=context)