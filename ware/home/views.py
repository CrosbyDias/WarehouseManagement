from django.shortcuts import render , redirect
from .models import *

# Create your views here.

def home(request):
    customers = Customer.objects.all()

    return render(request, 'home/home.html', {'customers': customers})


def add(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        gstin = request.POST.get('gstin')
        email = request.POST.get('email')
        
        customer = Customer(name=name, 
                            address=address, 
                            phone=phone, 
                            gstin=gstin, 
                            email=email)
        customer.save()
        return redirect('home')
        
    return render(request, 'home/add.html')


# def edit(request, id):
#     customer = Customer.objects.get(id=id)
    
#     if request.method == 'POST':
#         customer.name = request.POST.get('name')
#         customer.address = request.POST.get('address')
#         customer.phone = request.POST.get('phone')
#         customer.gstin = request.POST.get('gstin')
#         customer.email = request.POST.get('email')
        
#         customer.save()
#         return render(request, 'home/home.html', {'customers': Customer.objects.all()})
        
    
#     return render(request, 'home/edit.html', {'customer': customer})


def edit(request, id):
    customer = Customer.objects.get(id=id)
    
    if request.method == 'POST':
        customer.name = request.POST.get('name')
        customer.address = request.POST.get('address')
        customer.phone = request.POST.get('phone')
        customer.gstin = request.POST.get('gstin')
        customer.email = request.POST.get('email')
        
        customer.save()
        return redirect('home') 
    
    return render(request, 'home/edit.html', {'customer': customer})



def generate(request):
    customers = Customer.objects.all()
    if request.method == 'POST':
        customer_id = request.POST.get('customer_id')
        customer = Customer.objects.get(id=customer_id)
        return render(request, 'home/generate.html', {'customer': customer})
    
    return render(request, 'home/generate.html', {'customers': customers})

def delete(request, id):
    customer = Customer.objects.get(id=id)
    customer.delete()
    return redirect('home')

# class Customer:
#     def get(sel):
#         ..
#     de  post(self):
#         ...
        
#     def put(self):
        