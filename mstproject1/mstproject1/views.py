from django.shortcuts import redirect, render
from . models import Customers
from django.contrib.auth.hashers import make_password, check_password
from . decorators import login_is_required


def Indexpage(request):
    if 'customer_email' in request.session:
            customer_email = request.session['customer_email']
            return render(request,'index.html', {'customer_email' : customer_email})
    return render(request,'index.html')

def base(request):
    return render(request, 'base.html')

def Signuppage(request):
    if request.method=='POST':
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        email=request.POST['email']
        password=request.POST['password']
        cpassword=request.POST['cpassword']
        check_existing = Customers.objects.filter(email=email)
        if check_existing:
            error_message = None
            error_message ="Email already exists!!! Please login"
            return render(request,'register.html', {'error': error_message})
        #validation
        else: 
            error_message = None
            if(not first_name):
                error_message = "First Name Field is Required"
            elif(not last_name):
                error_message = "Last Name Field is Required"
            elif not email:
                error_message = "Email Required"
            elif password!=cpassword:
                error_message= "Passowrd Does not match"

            if not error_message:
                success_message = None
                Rcust = Customers(first_name=first_name, last_name=last_name, email=email, password=password)  
                success_message = (request.POST['first_name']+ ", your account is successfully created.")     
                #messages.success(request, request.POST['first_name']+", your account is successfully created.")
                Rcust.password=make_password(Rcust.password)
                Rcust.save()
                sdata = {"success" : success_message}
                return render(request, 'register.html', sdata)
                #return redirect(Signuppage)
            else:
                data = {"error": error_message}
                return render(request, 'register.html', data)
    else:
        return render(request,'register.html')  

def Loginpage(request):
    if request.method=="GET":
        return render(request, "login.html")
    if request.method=='POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        Lcust = Customers.get_customer_by_email(email)
        error_message=""
        if Lcust:
            match_password = check_password(password, Lcust.password)
            if match_password:
                request.session['customer_id'] = Lcust.id
                request.session['customer_email'] = Lcust.email
                request.session['customer_name'] = Lcust.first_name
                return redirect(Indexpage)
            else:
                error_message='Invalid Password'
                return render(request,'login.html',{'error': error_message})
        else:
            error_message = 'Invalid Email, Please register first.'
            return render(request,'login.html', {'error': error_message})          
    else:
        return render(request,'login.html')

def Logoutpage(request):
    try:
        request.session.flush()

    except:
        return render(request, 'login.html')
    return redirect('index')

@login_is_required
def Myaccount(request):

    cus_name = {
        'customer_id' : request.session.get('customer_id'),
        'customer_name' : request.session.get('customer_name'),
        'customer-email': request.session.get('customer_email')
    }
    return render(request, 'my-account.html',cus_name)