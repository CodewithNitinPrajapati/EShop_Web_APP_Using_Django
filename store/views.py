from django.shortcuts import render, redirect ,HttpResponseRedirect
from django.views.generic import ListView
from .models import Products, Categary, Custmer,Order
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from django.views import View



class Index(View):
    def get(self,request):
        # product = Products.get_all_product()
        cart=request.session.get('cart')
        if not cart:
            request.session['cart']={}
        product = None
        categaries = Categary.get_all_categary()
        CategaryId = request.GET.get('categary')
        #print(request.GET)
        if CategaryId:
            product = Products.get_all_product_by_catery_id(CategaryId)
        else:
            product = Products.get_all_product();
        data = {}
        data['product'] = product
        data['categaries'] = categaries

        #print(request.session.get('customer_email'))
        return render(request, 'Home.html', data)

    def post(self, request):
        product = request.POST.get('product')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity <= 1:
                        cart.pop(product)
                    else:
                        cart[product] = quantity - 1
                else:
                    cart[product] = quantity + 1

            else:
                cart[product] = 1
        else:
            cart = {}
            cart[product] = 1
        request.session['cart'] = cart
        #print('cart', request.session['cart'])
        return redirect('Home')


class Signup(View):
    def get(self,request):
        return render(request, 'signup.html')
    def post(self,request):
        postdata = request.POST
        first_name = postdata.get('firstname')
        last_name = postdata.get('lastname')
        email = postdata.get('email')
        passward = postdata.get('passward')
        c_passward = postdata.get('confirmpassward')
        # print(first_name, last_name, email, passward, c_passward)

        customer = Custmer(first_name=first_name, last_name=last_name, email=email, password=passward,c_password=c_passward)

        error_massage =self.User_validation(customer)
        values = {'first_name': first_name, 'last_name': last_name, 'email': email}

        if error_massage:
            data = {'error': error_massage, 'values': values}
            return render(request, 'signup.html', data)

        else:
            customer.password = make_password(customer.password)
            customer.c_password = make_password(customer.c_password)
            customer.register()
            msg = 'You are succesfully registered now login here'
            #return redirect('Login')
            return render(request,'login.html',{'msg':msg})



    def User_validation(self,customer):
        error_massage = None
        if not customer.first_name:
            error_massage = 'First Name Required '
        elif len(customer.first_name) < 4:
            error_massage = 'First name more than 4 latter '
        elif not customer.last_name:
            error_massage = 'Last Name Required '
        elif len(customer.last_name) < 4:
            error_massage = 'Last name more than 4 latter '
        elif not customer.email:
            error_massage = ' email Required '
        elif not customer.password:
            error_massage = 'Password Required '
        elif len(customer.password) < 6:
            error_massage = 'First name more than 6 latter '
        elif not customer.c_password:
            error_massage = 'Conform Password Required '
        elif customer.password != customer.c_password:
            error_massage = "Password dosn't match"
        elif Custmer.isExist(Custmer):
            error_massage = 'Email already registered'

        return error_massage



class Login(View):
    def get(self,request):
        return render(request, 'login.html')

    def post(self,request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        # print(email,password)
        customer = Custmer.get_email_for_check(email)
        print(customer)
        error_massage = None
        if customer:
            flag = check_password(password, customer.password)
            if flag:
                request.session['customer_id'] = customer.id
                request.session['customer_email'] = customer.email
                return redirect('Home')
            else:
                error_massage = "Password Incorrect"
                return render(request, 'login.html', {'error': error_massage})
        else:
            error_massage = "invalid email or password"
            return render(request, 'login.html', {'error': error_massage})



def logout(request):
    request.session.clear()
    return redirect('Home')



class Cart(View):
    def get(self,request):

        #print(request.session.get('cart'))
        #print(request.session.get('cart').keys())
        #print(list(request.session.get('cart').keys()))

        ids = list(request.session.get('cart').keys())
        products = Products.get_all_product_by_id(ids)
        #print(products)
        return render(request, 'cart.html' , {'products' : products})



class CheckOut(View):
    def post(self, request):
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        customer = request.session.get('customer_id')
        cart = request.session.get('cart')
        products = Products.get_all_product_by_id(list(cart.keys()))
        #print(address, phone, customer, cart, products)

        for product in products:
            #print(cart.get(str(product.id)))
            order = Order(customer=Custmer(id=customer),
                          product=product,
                          price=product.price,
                          address=address,
                          phone=phone,
                          quantity=cart.get(str(product.id)))
            order.save()
        request.session['cart'] = {}

        return redirect('Cart')



class OrderView(View):
    def get(self, request):
        customer = request.session.get('customer_id')
        #print(customer)
        orders = Order.get_orders_by_customer(customer)
        orders = orders.reverse()
        print(orders)
        return render(request,'order.html' , {'orders': orders} )
