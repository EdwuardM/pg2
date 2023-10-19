from django.shortcuts import render, redirect, get_object_or_404
from django.core.files.uploadedfile import InMemoryUploadedFile
from .models import Category, Product, Warehouse, RuleSupply
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from Apps.suppliers.models import Supplier
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import Max
from django.db.models import F, Q
from PIL import Image
import io


@login_required(login_url="/accounts/login/")
def CategoriesListView(request):
    context = {
        "active_icon": "products_categories",
        "categories": Category.objects.all()
    }
    return render(request, "products/categories.html", context=context)

@login_required(login_url="/accounts/login/")
def CategoriesAddView(request):
    context = {
        "active_icon": "products_categories",
        "category_status": Category.status.field.choices
    }
    if request.method == 'POST':
        data = request.POST
        attributes = {
            "name": data['name'],
            "status": data['state'],
            "description": data['description']
        }
        if Category.objects.filter(**attributes).exists():
            messages.error(request, '¡La categoría ya existe!',
                        extra_tags="warning")
            return redirect('Apps.products:categories_add')
        try:
            new_category = Category.objects.create(**attributes)
            new_category.save()
            messages.success(request, 'Categoría: ' +
                            attributes["name"] + ' Creada con éxito!', extra_tags="success")
            return redirect('Apps.products:categories_list')
        except Exception as e:
            messages.success(
                request, '¡Hubo un error durante la creación!', extra_tags="danger")
            return redirect('Apps.products:categories_add')
    return render(request, "products/categories_add.html", context=context)


@login_required(login_url="/accounts/login/")
def CategoriesUpdateView(request, category_id):
    try:
        category = Category.objects.get(id=category_id)
    except Exception as e:
        messages.success(
            request, '¡Hubo un error al intentar obtener la categoría!', extra_tags="danger")
        return redirect('Apps.products:categories_list')
    context = {
        "active_icon": "products_categories",
        "category_status": Category.status.field.choices,
        "category": category
    }
    if request.method == 'POST':
        try:
            data = request.POST
            attributes = {
                "name": data['name'],
                "status": data['state'],
                "description": data['description']
            }
            if Category.objects.filter(**attributes).exists():
                messages.error(request, '¡La categoría ya existe!',
                            extra_tags="warning")
                return redirect('Apps.products:categories_add')
            category = Category.objects.filter(
                id=category_id).update(**attributes)
            category = Category.objects.get(id=category_id)
            messages.success(request, '¡Categoría: ' + category.name +
                            ' actualizado exitosamente!', extra_tags="success")
            return redirect('Apps.products:categories_list')
        except Exception as e:
            messages.success(
                request, '¡Hubo un error durante la eliminación!', extra_tags="danger")
            return redirect('Apps.products:categories_list')
    return render(request, "products/categories_update.html", context=context)

@login_required(login_url="/accounts/login/")
def CategoriesDeleteView(request, category_id):
    try:
        category = Category.objects.get(id=category_id)
        category.delete()
        messages.success(request, '¡Categoría: ' + category.name +
                        ' eliminado!', extra_tags="success")
        return redirect('Apps.products:categories_list')
    except Exception as e:
        messages.success(
            request, '¡Hubo un error durante la eliminación!', extra_tags="danger")
        return redirect('Apps.products:categories_list')

def ProductsListView(request):
    context = {
        "active_icon": "products2",
        "products": Product.objects.all(),
    }
    return render(request, "products/products.html", context=context)

@login_required(login_url="/accounts/login/")
def ProductsAddView(request):
    context = {
        "active_icon": "products2",
        "product_status": Product.status.field.choices,
        "categories": Category.objects.all().filter(status="ACTIVO"),
        "warehouses": Warehouse.objects.all().filter(status="ACTIVO"),
    }
    buffer = io.BytesIO()
    if request.method == 'POST':
        form = request.POST
        image = request.FILES.get('imagen')  
        attributes = {
            "name": form['name'],
            "status": form['state'],
            "description": form['description'],
            "price": form['price'],
            "priceBuy": form['price_buy'],
            "quantity": form['quantity']  
        }
        try:
            category_id = form['category']
            attributes["category"] = get_object_or_404(Category, id=category_id, status="ACTIVO")

            warehouse_id = form['warehouse']
            attributes["warehouse"] = get_object_or_404(Warehouse, id=warehouse_id, status="ACTIVO")

            latest_rule = RuleSupply.objects.all().aggregate(Max('id'))['id__max']
            if latest_rule:
                latest_rule_instance = RuleSupply.objects.get(id=latest_rule)
                latest_rule_instance.status = 'ACTIVO'
                latest_rule_instance.save()
                attributes["ruleSupply"] = latest_rule_instance
                delete_inactive_rules()
            if Product.objects.filter(**attributes).exists():
                messages.error(request, '¡El producto ya existe!', extra_tags="warning")
                return redirect('Apps.products:products_add')
            new_product = Product(**attributes)
            if image:
                img = Image.open(image)
                img.save(buffer, format=img.format)  
                buffer.seek(0)
                new_product.image.save(image.name, InMemoryUploadedFile(
                    buffer, None, image.name, image.content_type, len(buffer.getvalue()), None))
            new_product.save()
            messages.success(request, '¡Producto: ' + attributes["name"] + ' creado exitosamente!', extra_tags="success")
            return redirect('Apps.products:products_list')
        except Exception as e:
            messages.error(request, 'Hubo un error durante la creación '+ str(e), extra_tags="danger")
    return render(request, "products/products_add.html", context=context)


@login_required(login_url="/accounts/login/")
def ProductsUpdateView(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
    except Exception as e:
        messages.success(request, '¡Hubo un error al intentar obtener el producto!', extra_tags="danger")
        return redirect('Apps.products:products_list')

    context = {
        "active_icon": "products",
        "product_status": Product.STATUS_CHOICES,
        "product": product,
        "categories": Category.objects.all(),
        "warehouses": Warehouse.objects.all()
    }

    if request.method == 'POST':
        try:
            data = request.POST
            image = request.FILES.get('imagen')  
            image_url = product.image.url
            print('aca este es el link'+ image_url)
            price = data['price'].replace(',', '.')
            price_buy = data['price_buy'].replace(',', '.')
            quantity = data['quantity'].replace(',', '.')
            attributes = {
                "name": data['name'],
                "status": data['state'],
                "description": data['description'],
                "category": Category.objects.get(id=data['category']),
                "price": float(price),  
                "priceBuy": float(price_buy),
                "quantity": float(quantity), 
            }
            buffer = io.BytesIO()
            if image:
                print("Imagen cargada: " + image.name)
            else:
                print("No se cargó ninguna imagen")
            if image:
                current_image_url = request.POST.get('current_image', None)
                print("esta es la segunda: " + current_image_url)
                if current_image_url and image.name != current_image_url:
                    product.image.delete(save=False)
                    buffer = io.BytesIO()
                    img = Image.open(image)
                    img.save(buffer, format=img.format)
                    buffer.seek(0)
                    product.image.save(image.name, InMemoryUploadedFile(
                        buffer, None, image.name, image.content_type, len(buffer.getvalue()), None))
                    
            if Product.objects.filter(**attributes).exclude(id=product_id).exists():
                messages.error(request, '¡El producto ya existe!',
                            extra_tags="warning")
                return redirect('Apps.products:products_add')
            
            # Actualiza los otros campos del producto
            for attr, value in attributes.items():
                setattr(product, attr, value)
            
            product.save()  # Guarda el producto con las actualizaciones

            messages.success(request, '¡Producto: ' + product.name +
                            ' actualizado exitosamente!', extra_tags="success")
            return redirect('Apps.products:products_list')
        except Exception as e:
            messages.success(request, '¡Hubo un error durante la actualización!' + str(e), extra_tags="danger")
            return redirect('Apps.products:products_list')

    return render(request, "products/products_update.html", context=context)


@login_required(login_url="/accounts/login/")
def ProductsDeleteView(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
        if product.image:
            default_storage.delete(product.image.path)
        if product.ruleSupply:
            product.ruleSupply.delete()
        product.delete()
        messages.success(request, '¡Producto: ' + product.name + ' Eliminado!', extra_tags="success")
        return redirect('Apps.products:products_list')
    except Exception as e:
        messages.error(request, '¡Hubo un error durante la eliminación!', extra_tags="danger")
        return redirect('Apps.products:products_list')

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

def GetProductsAJAXView(request):
    if request.method == 'POST':
        if is_ajax(request=request):
            data = []

            products = Product.objects.filter(
                name__icontains=request.POST['term'])
            for product in products[0:10]:
                item = product.to_json()
                if 'image' in item:
                    del item['image']
                data.append(item)

            return JsonResponse(data, safe=False)

@login_required(login_url="/accounts/login/")
def WarehousesListView(request):
    context = {
        "active_icon": "products_warehouse",
        "warehouses": Warehouse.objects.all()
    }
    return render(request, "products/warehouses.html", context=context)

@login_required(login_url="/accounts/login/")
def WarehousesAddView(request):
    context = {
        "active_icon": "products_warehouse",
        "warehouse_status": Warehouse.status.field.choices
    }
    if request.method == 'POST':
        data = request.POST
        attributes = {
            "name": data['name'],
            "status": data['state'],
            "description": data['description']
        }
        if Warehouse.objects.filter(**attributes).exists():
            messages.error(request, '¡El almacén ya existe!',
                        extra_tags="warning")
            return redirect('Apps.products:warehouses_add')
        try:
            new_warehouse = Warehouse.objects.create(**attributes)
            new_warehouse.save()
            messages.success(request, 'Almacén: ' +
                            attributes["name"] + ' Creado con éxito!', extra_tags="success")
            return redirect('Apps.products:warehouses_list')
        except Exception as e:
            messages.success(
                request, '¡Hubo un error durante la creación!', extra_tags="danger")
            return redirect('Apps.products:warehouses_add')
    return render(request, "products/warehouses_add.html", context=context)

@login_required(login_url="/accounts/login/")
def WarehousesUpdateView(request, warehouse_id):
    try:
        warehouse = Warehouse.objects.get(id=warehouse_id)
    except Exception as e:
        messages.success(
            request, '¡Hubo un error al intentar obtener el almacén!', extra_tags="danger")

        return redirect('Apps.products:warehouses_list')
    context = {
        "active_icon": "products_warehouse",
        "warehouse_status": Warehouse.status.field.choices,
        "warehouse": warehouse
    }
    if request.method == 'POST':
        try:
            data = request.POST
            attributes = {
                "name": data['name'],
                "status": data['state'],
                "description": data['description']
            }
            if Warehouse.objects.filter(**attributes).exists():
                messages.error(request, '¡El almacén ya existe!',
                            extra_tags="warning")
                return redirect('Apps.products:warehouses_add')
            warehouse = Warehouse.objects.filter(
                id=warehouse_id).update(**attributes)
            warehouse = Warehouse.objects.get(id=warehouse_id)
            messages.success(request, '¡Almacén: ' + warehouse.name +
                            ' actualizado exitosamente!', extra_tags="success")
            return redirect('Apps.products:warehouses_list')
        except Exception as e:
            messages.success(
                request, '¡Hubo un error durante la eliminación!', extra_tags="danger")
            return redirect('Apps.products:warehouses_list')
    return render(request, "products/warehouses_update.html", context=context)

@login_required(login_url="/accounts/login/")
def WarehousesDeleteView(request, warehouse_id):
    try:
        warehouse = Warehouse.objects.get(id=warehouse_id)
        warehouse.delete()
        messages.success(request, '¡Almacén: ' + warehouse.name +
                        ' eliminado!', extra_tags="success")
        return redirect('Apps.products:warehouses_list')
    except Exception as e:
        messages.success(
            request, '¡Hubo un error durante la eliminación!', extra_tags="danger")
        return redirect('Apps.products:warehouses_list')
    
@login_required(login_url="/accounts/login/")
def RuleSupplyAddView(request):
    context = {
        "active_icon": "products2",
        "suppliers": Supplier.objects.all()
    }
    if request.method == 'POST':
        data = request.POST
        attributes = {
            "minimumAmount": data['minimum_amount'] ,
            "maximumQuantity": data['maximum_quantity'],
            "supplier":Supplier.objects.get(id=data['supplier']),
        }
        try:
            new_ruleSupply = RuleSupply.objects.create(**attributes)
            new_ruleSupply.save()
            messages.success(request, '¡La Regla de abastecimiento Creada con éxito!', extra_tags="success")
            return redirect('Apps.products:products_add')
        except Exception as e:
            messages.success(
                request, '¡Hubo un error durante la creación!', extra_tags="danger")
            return redirect('Apps.products:products_add')
    return render(request, "products/rulesupply_add.html", context=context)

def delete_inactive_rules():
    RuleSupply.objects.filter(status="INACTIVO").delete()