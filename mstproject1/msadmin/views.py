from itertools import count
from django.shortcuts import redirect, render
import threading
from msadmin.decorators import login_is_required
from . models import Adminusers, Item
from django.core.paginator import Paginator
from django.db.models import Sum
from django.http import JsonResponse
from django.contrib import messages


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
                #dsuc = {"delsuccess" : success_messages}
                #url = "itemshow?delsuccess={}".format(success_messages)
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
    if request.method == "POST":
        type=request.POST.get('type')
        name=request.POST.get('name')
        sku=request.POST.get('sku')
        unit=request.POST.get('unit')
        returnable_item=request.POST.get('returnable_item') or False
        
        category=request.POST.get('category')
        manufacturer=request.POST.get('manufacturer')
        upc=request.POST.get('upc')
        ean=request.POST.get('ean')
        design=request.POST.get('design')
        color=request.POST.get('color')
        barcode_image = request.FILES['barcode_image']
        brand=request.POST.get('brand')
        mpn=request.POST.get('mpn')
        isbn=request.POST.get('isbn')
        agency_charge=request.POST.get('agency_charge')
        price_code=request.POST.get('price_code')
        sales_information=request.POST.get('sales_information') or False
        selling_price=request.POST.get('selling_price')
        sales_account=request.POST.get('sales_account')
        sales_description=request.POST.get('sales_description')
        purchase_information=request.POST.get('purchase_information') or False
        cost_price=request.POST.get('cost_price')
        purchase_account=request.POST.get('purchase_account')
        purchase_description=request.POST.get('purchase_description')
        track_inventory=request.POST.get('track_inventory') or False
        inventory_account=request.POST.get('inventory_account')
        reorder_point=request.POST.get('reorder_point')
        preferred_vendor=request.POST.get('preferred_vendor')
        warehouse_name=request.POST.get('warehouse_name')

        update = Item(id=id, type=type, name=name, sku=sku, unit=unit, returnable_item=returnable_item, category=category, manufacturer=manufacturer, upc=upc, ean=ean, design=design, 
        color=color, barcode_image=barcode_image, brand=brand, mpn=mpn, isbn=isbn, agency_charge=agency_charge, price_code=price_code, sales_information=sales_information, selling_price=selling_price, sales_account=sales_account, sales_description=sales_description,
        purchase_information=purchase_information, cost_price=cost_price, purchase_account=purchase_account, purchase_description=purchase_description, track_inventory=track_inventory,
        inventory_account=inventory_account, reorder_point=reorder_point, preferred_vendor=preferred_vendor, warehouse_name=warehouse_name)  
        update.save()
        return redirect('Item_show')
    return render (request,'admin-template/itemshow.html')

def Create_item(request):
    if request.method=="GET":
        return render(request, "admin-template/item.html")
    if request.method == "POST":
        type=request.POST.get('type')
        name=request.POST.get('name')
        sku=request.POST.get('sku')
        unit=request.POST.get('unit')
        returnable_item=request.POST.get('returnable_item') or False
        upload_image = request.FILES['upload_image']
        category=request.POST.get('category')
        manufacturer=request.POST.get('manufacturer')
        upc=request.POST.get('upc')
        ean=request.POST.get('ean')
        design=request.POST.get('design')
        color=request.POST.get('color')
        barcode_image = request.FILES['barcode_image']
        brand=request.POST.get('brand')
        mpn=request.POST.get('mpn')
        isbn=request.POST.get('isbn')
        agency_charge=request.POST.get('agency_charge')
        price_code=request.POST.get('price_code')
        sales_information=request.POST.get('sales_information') or False
        selling_price=request.POST.get('selling_price')
        sales_account=request.POST.get('sales_account')
        sales_description=request.POST.get('sales_description')
        purchase_information=request.POST.get('purchase_information') or False
        cost_price=request.POST.get('cost_price')
        purchase_account=request.POST.get('purchase_account')
        purchase_description=request.POST.get('purchase_description')
        track_inventory=request.POST.get('track_inventory') or False
        inventory_account=request.POST.get('inventory_account')
        reorder_point=request.POST.get('reorder_point')
        preferred_vendor=request.POST.get('preferred_vendor')
        warehouse_name=request.POST.get('warehouse_name')

        data = Item(type=type, name=name, sku=sku, unit=unit, returnable_item=returnable_item, upload_image=upload_image, category=category, manufacturer=manufacturer, upc=upc, ean=ean, design=design, 
        color=color, barcode_image=barcode_image, brand=brand, mpn=mpn, isbn=isbn, agency_charge=agency_charge, price_code=price_code, sales_information=sales_information, selling_price=selling_price, sales_account=sales_account, sales_description=sales_description,
        purchase_information=purchase_information, cost_price=cost_price, purchase_account=purchase_account, purchase_description=purchase_description, track_inventory=track_inventory,
        inventory_account=inventory_account, reorder_point=reorder_point, preferred_vendor=preferred_vendor, warehouse_name=warehouse_name)  
        success_message = ("Your data has saved successfully.")     
        #messages.success(request, request.POST['first_name']+", your account is successfully created.")
        data.save()
        sdata = {"success" : success_message}
        return render(request, 'admin-template/item.html', sdata)
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