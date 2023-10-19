from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Supplier

@login_required(login_url="/accounts/login/")
def suppliersListView(request):
    context = {
        "active_icon": "suppliers",
        "suppliers": Supplier.objects.all()
    }
    return render(request, "suppliers/suppliers.html", context=context)

@login_required(login_url="/accounts/login/")
def suppliersAddView(request):
    context = {
        "active_icon": "suppliers",
    }
    if request.method == 'POST':
        data = request.POST
        attributes = {
            "first_name": data['first_name'],
            "company_name": data['company_name'],
            "address": data['address'],
            "email": data['email'],
            "phone": data['phone'],
            "assessment": data['rating'],
        }
        if Supplier.objects.filter(**attributes).exists():
            messages.error(request, '¡El proveedor ya existe!',
                extra_tags="warning")
            return redirect('Apps.suppliers:suppliers_add')
        try:
            new_suppliers = Supplier.objects.create(**attributes)
            new_suppliers.save()
            messages.success(request, '¡Proveedor: ' + attributes["first_name"] + " de " +
                attributes["company_name"] + ' Creado con éxito!', extra_tags="success")
            return redirect('Apps.suppliers:suppliers_list')
        except Exception as e:
            messages.success(
                request, '¡Hubo un error durante la creación!', extra_tags="danger")
            return redirect('Apps.suppliers:suppliers_add')
    return render(request, "suppliers/suppliers_add.html", context=context)

@login_required(login_url="/accounts/login/")
def suppliersUpdateView(request, supplier_id):
    try:
        supplier = Supplier.objects.get(id=supplier_id)
    except Exception as e:
        messages.success(
            request, '¡Hubo un error al intentar conseguir el proveedor!', extra_tags="danger")
        return redirect('Apps.suppliers:suppliers_list')
    context = {
        "active_icon": "suppliers",
        "supplier": supplier,
    }
    if request.method == 'POST':
        try:
            data = request.POST
            assessment = request.POST.get('rating')
            attributes = {
                "first_name": data['first_name'],
                "company_name": data['company_name'],
                "address": data['address'],
                "email": data['email'],
                "phone": data['phone'],
                "assessment": data['rating'],
            }
            if Supplier.objects.filter(**attributes).exists():
                messages.error(request, '¡El proveedor ya existe!',
                    extra_tags="warning")
                return redirect('Apps.suppliers:supplier_add')
            supplier = Supplier.objects.filter(id=supplier_id).update(**attributes)
            supplier = Supplier.objects.get(id=supplier_id)
            messages.success(request, '¡Proveedor: ' + supplier.get_full_name() +
                ' actualizado exitosamente!', extra_tags="success")
            return redirect('Apps.suppliers:suppliers_list')
        except Exception as e:
            messages.success(
                request, '¡Hubo un error durante la actualización! ', extra_tags="danger")
            return redirect('Apps.suppliers:suppliers_list')
    return render(request, "suppliers/suppliers_update.html", context=context)

@login_required(login_url="/accounts/login/")
def suppliersDeleteView(request, supplier_id):
    try:
        supplier = Supplier.objects.get(id=supplier_id)
        supplier.delete()
        messages.success(request, '¡Proveedor: ' + supplier.get_full_name() +
            ' Eliminado!', extra_tags="success")
        return redirect('Apps.suppliers:suppliers_list')
    except Exception as e:
        messages.success(
            request, '¡Hubo un error durante la eliminación!', extra_tags="danger")
        print(e)
        return redirect('Apps.suppliers:suppliers_list')
