from itertools import count
import os
from django.http import HttpResponse
from django.shortcuts import redirect, render
import threading
from msadmin.decorators import login_is_required
from . models import Adminusers, Item
from django.core.paginator import Paginator
from django.db.models import Sum
from django.http import JsonResponse
from django.contrib import messages
from django.core.files.storage import FileSystemStorage


def Adminpage(request):
    if 'adminuser_email' in request.session:
            adminuser_email = request.session['adminuser_email']
            return render(request,'admin-template/index.html', {'adminuser_email' : adminuser_email})
    return render(request,'admin-template/pages/examples/login.html')

def Item_show(request):
    if request.method == "GET":
        items = Item.objects.all()
        paginator = Paginator(items, 5)
        page_number = request.GET.get('page')
        usersfinal = paginator.get_page(page_number)
        totalpage = usersfinal.paginator.num_pages

        data={
            'items': usersfinal,    
            'lastpage': totalpage,
            'totalPagelist': [n+1 for n in range(totalpage)],
        }
        return render(request, "admin-template/itemshow.html",data)

def Item_editdelete(request):
    if 'delete' in request.POST:
        check = request.POST.getlist('checks[]')
        if check:
            for i in check:
                delete = Item.objects.get(id=i)
                messages.success (request,'The Item has deleted successfully.') 
                os.remove(delete.upload_image.path)
                os.remove(delete.barcode_image.path)
                delete.delete()
        else:
            messages.warning (request,'Please select one item.')
            return redirect ('itemshow')
    elif 'edit' in request.POST:
        checkbox = request.POST.getlist('checks[]')
        if checkbox:
            if len(checkbox) == 1:
                for i in checkbox:
                    edit = Item.objects.get(id=i)
                    return render (request,'admin-template/itemedit.html', {'edit' : edit })
            else:
                messages.warning (request,'Please select one item.')
                return redirect ('itemshow')
        else:
            messages.warning (request,'Please select one item.')
            return redirect ('itemshow')
    return redirect ('itemshow')


def Item_update(request,id):
    edit1 = Item.objects.get(id=id)
    if request.method == "POST":
        edit = Item()
        edit.id = id
        edit.type=request.POST.get('type')
        edit.name=request.POST.get('name')
        edit.sku=request.POST.get('sku')
        edit.unit=request.POST.get('unit')
        edit.returnable_item=request.POST.get('returnable_item') or False
        if 'upload_image' in request.FILES:
            os.remove(edit1.upload_image.path)
            edit.upload_image = request.FILES['upload_image']
        else:
            edit.upload_image = edit1.upload_image
        edit.category=request.POST.get('category')
        edit.manufacturer=request.POST.get('manufacturer')
        edit.upc=request.POST.get('upc')
        edit.ean=request.POST.get('ean')
        edit.design=request.POST.get('design')
        edit.color=request.POST.get('color')
        if 'barcode_image' in request.FILES:
            os.remove(edit1.barcode_image.path)
            edit.barcode_image = request.FILES['barcode_image']
        else:
            edit.barcode_image = edit1.barcode_image
        edit.brand=request.POST.get('brand')
        edit.mpn=request.POST.get('mpn')
        edit.isbn=request.POST.get('isbn')
        edit.agency_charge=request.POST.get('agency_charge')
        edit.price_code=request.POST.get('price_code')
        edit.sales_information=request.POST.get('sales_information') or False
        edit.selling_price=request.POST.get('selling_price')
        edit.sales_account=request.POST.get('sales_account')
        edit.sales_description=request.POST.get('sales_description')
        edit.purchase_information=request.POST.get('purchase_information') or False
        edit.cost_price=request.POST.get('cost_price')
        edit.purchase_account=request.POST.get('purchase_account')
        edit.purchase_description=request.POST.get('purchase_description')
        edit.track_inventory=request.POST.get('track_inventory') or False
        edit.inventory_account=request.POST.get('inventory_account')
        edit.reorder_point=request.POST.get('reorder_point')
        edit.preferred_vendor=request.POST.get('preferred_vendor')
        edit.warehouse_name=request.POST.get('warehouse_name')

        edit.save()
        messages.success (request,'The Item has updated successfully.')
        return redirect(Item_show)
    return render (request,'admin-template/itemshow.html')

def Create_item(request):
    if request.method=="GET":
        return render(request, "admin-template/item.html")
    if request.method == "POST":
        item = Item()
        item.type=request.POST.get('type')
        item.name=request.POST.get('name')
        item.sku=request.POST.get('sku')
        item.unit=request.POST.get('unit')
        item.returnable_item=request.POST.get('returnable_item') or False
        item.category=request.POST.get('category')
        item.manufacturer=request.POST.get('manufacturer')
        item.upc=request.POST.get('upc')
        item.ean=request.POST.get('ean')
        item.design=request.POST.get('design')
        item.color=request.POST.get('color')
        item.brand=request.POST.get('brand')
        item.mpn=request.POST.get('mpn')
        item.isbn=request.POST.get('isbn')
        item.agency_charge=request.POST.get('agency_charge')
        item.price_code=request.POST.get('price_code')
        item.sales_information=request.POST.get('sales_information') or False
        item.selling_price=request.POST.get('selling_price')
        item.sales_account=request.POST.get('sales_account')
        item.sales_description=request.POST.get('sales_description')
        item.purchase_information=request.POST.get('purchase_information') or False
        item.cost_price=request.POST.get('cost_price')
        item.purchase_account=request.POST.get('purchase_account')
        item.purchase_description=request.POST.get('purchase_description')
        item.track_inventory=request.POST.get('track_inventory') or False
        item.inventory_account=request.POST.get('inventory_account')
        item.reorder_point=request.POST.get('reorder_point')
        item.preferred_vendor=request.POST.get('preferred_vendor')
        item.warehouse_name=request.POST.get('warehouse_name')
        if 'upload_image' in request.FILES:
            item.upload_image = request.FILES['upload_image']
        if 'barcode_image' in request.FILES:
            item.barcode_image = request.FILES['barcode_image']

        check_existing = Item.objects.filter(name=item.name)
        if check_existing:
            messages.warning (request,'The item name already exists.')
            return redirect ('item')
        else:
            error_message = None
            if not item.upload_image:
                messages.warning (request,'Please Add Item Image.')
                return redirect ('item')
            elif not item.barcode_image:
                messages.warning (request,'Please Add Barcode Image.')
                return redirect ('item')

            if not error_message:         
                item.save()
                messages.success(request,'The Item ' + request.POST['name'] + ' has created successfully.')
                return redirect('itemshow')
    else:
        error_message = "The data not saved. Please try again!"
        fdata = {"error": error_message}
        return render(request, 'admin-template/pages/examples/login.html', fdata)


def Adminlogin(request):
    if request.method=="GET":
        return render(request, "admin-template/pages/examples/login.html")
    if request.method=='POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        adminuser = Adminusers.get_customer_by_email(email)
        error_message=""
        if adminuser:
            match_password = Adminusers.objects.filter(password = password)
            if match_password:
                request.session['adminuser_id'] = adminuser.id
                request.session['adminuser_email'] = adminuser.email
                return redirect(Adminpage)
            else:
                error_message='Invalid Password'
                return render(request,'admin-template/pages/examples/login.html',{'error': error_message})
            
        else:
            error_message = 'Invalid Email, Please contact admin.'
            return render(request,'admin-template/pages/examples/login.html', {'error': error_message})
            
    else:
        return render(request,'admin-template/pages/examples/login.html')

def Logoutpage(request):
    try:
        request.session.flush()
    except:
        return render(request, 'admin-template/pages/examples/login.html')
    return redirect('login')



# def Item_update(request,id):
#     edit = Item.objects.get(id=id)
#     if request.method=="GET":
#         return render(request, "admin-template/itemedit.html")
#     if request.method == "POST":
#         type=request.POST.get('type')
#         name=request.POST.get('name')
#         sku=request.POST.get('sku')
#         unit=request.POST.get('unit')
#         returnable_item=request.POST.get('returnable_item') or False
#         if 'upload_image' in request.FILES:
#             upload_image = request.FILES.get('upload_image')
#         else:
#             upload_image = edit.upload_image
#         category=request.POST.get('category')
#         manufacturer=request.POST.get('manufacturer')
#         upc=request.POST.get('upc')
#         ean=request.POST.get('ean')
#         design=request.POST.get('design')
#         color=request.POST.get('color')
#         if 'barcode_image' in request.FILES:
#             barcode_image = request.FILES.get('barcode_image')
#         else:
#             barcode_image = edit.barcode_image
#         brand=request.POST.get('brand')
#         mpn=request.POST.get('mpn')
#         isbn=request.POST.get('isbn')
#         agency_charge=request.POST.get('agency_charge')
#         price_code=request.POST.get('price_code')
#         sales_information=request.POST.get('sales_information') or False
#         selling_price=request.POST.get('selling_price')
#         sales_account=request.POST.get('sales_account')
#         sales_description=request.POST.get('sales_description')
#         purchase_information=request.POST.get('purchase_information') or False
#         cost_price=request.POST.get('cost_price')
#         purchase_account=request.POST.get('purchase_account')
#         purchase_description=request.POST.get('purchase_description')
#         track_inventory=request.POST.get('track_inventory') or False
#         inventory_account=request.POST.get('inventory_account')
#         reorder_point=request.POST.get('reorder_point')
#         preferred_vendor=request.POST.get('preferred_vendor')
#         warehouse_name=request.POST.get('warehouse_name')

#         update = Item(type=type, name=name, sku=sku, unit=unit, returnable_item=returnable_item, upload_image=upload_image, category=category, manufacturer=manufacturer, upc=upc, ean=ean, design=design, 
#         color=color, barcode_image=barcode_image, brand=brand, mpn=mpn, isbn=isbn, agency_charge=agency_charge, price_code=price_code, sales_information=sales_information, selling_price=selling_price, sales_account=sales_account, sales_description=sales_description,
#         purchase_information=purchase_information, cost_price=cost_price, purchase_account=purchase_account, purchase_description=purchase_description, track_inventory=track_inventory,
#         inventory_account=inventory_account, reorder_point=reorder_point, preferred_vendor=preferred_vendor, warehouse_name=warehouse_name)  
#         update.save()
#         messages.success (request,'The Item has updated successfully.')
#         return redirect(Item_show)
#     return render (request,'admin-template/itemshow.html')