from django.shortcuts import render
from .views_api import *          # import all functions from views_api file
from .models import *             # import all models from admin panel
from eha_app.models import *      # import all models from EHA app
from eha import settings
import stripe                     # for getting total of amount
from django.views.decorators.csrf import csrf_exempt  
from django.http import HttpResponse 


# ------------------- RENDER LOGIN PAGE -----------------------------

def login(request):
	return render(request,'admin_panel/login.html')


def  logout(request):
	try:
		del request.session['admin_id']
	except KeyError:
		pass
	return redirect("/admin_panel/")	



def page_under_construction(request):
	return render(request,'admin_panel/page_under_construction.html')


# -------------------RENDER CHANGE PASSWORD PAGE-----------------------------

@csrf_exempt   
def change_password_page(request):
    return render(request,'admin_panel/change_password.html')



# ------------------- ADMIN DASHBOARD -----------------------------
def dashboard(request):
    session = request.session.get("admin_id")
    if session:
        admin = AdminUser.objects.get(id=session)
        return render(request,'admin_panel/dashboard.html',{'username':admin.username})
    else:
        return redirect('/admin_panel/')
        
# ------------------- SHOW SHOP ITEMS -----------------------------

def shop_items(request):
	session = request.session.get("admin_id")
	if not session:
		return redirect("/admin_panel/")
	try:
		# Fetch all SHOP ITEMS from MODEL
		shop_items = ShopItems.objects.all().order_by('-id')
		context = {
			'shop_items' : shop_items,
		}
		return render(request, 'admin_panel/shop_items.html', context)

	except Exception as e:
		print(e)


# ------------------- ADD SHOP ITEMS -----------------------------

def shop_item_add(request):
	session = request.session.get("admin_id")
	if not session:
		return redirect("/admin_panel/")
	try:
		return render(request, 'admin_panel/shop_item_add.html')

	except Exception as e:
		print(e)


# ------------------- SHOP ITEMS DETAILS -----------------------------

def shop_item_detail(request, id):
	session = request.session.get("admin_id")
	if not session:
		return redirect("/admin_panel/")
	try:
		# Fetch data from model if exist
		if ShopItems.objects.filter(id = id).exists():
			shop_item = ShopItems.objects.get(id=id)
		else:
			# if data is not present redirect to shop_item
			return redirect("/admin_panel/shop-items")

		context = {
			'shop_item' : shop_item,
		}
		return render(request, 'admin_panel/shop_item_detail.html', context)

	except Exception as e:
		print(e)


# ------------------- EDIT SHOP ITEM -----------------------------

def shop_item_edit(request,id):
	session = request.session.get("admin_id")
	if not session:
		return redirect("/admin_panel/")
	try:
		# Fetch data from model if exist
		if ShopItems.objects.filter(id = id).exists():
			shop_item = ShopItems.objects.get(id=id)
		else:
			# if data is not present redirect to shop items
			return redirect("/admin_panel/shop-items")

		context = {
			'shop_item' : shop_item,
		}
		return render(request, 'admin_panel/shop_item_edit.html', context)

	except Exception as e:
		print(e)


# ------------------- ADD, EDIT, VIEW COUPONS  -----------------------------

def coupons(request):
	session = request.session.get("admin_id")
	if not session:
		return redirect("/admin_panel/")
	try:
		coupons = Coupon.objects.all().order_by('-id')
		context = {
			'coupons' : coupons,
		}
		return render(request, 'admin_panel/coupons.html', context)

	except Exception as e:
		print(e)


# ------------------- VIEW ORDER ITEMS -----------------------------
@csrf_exempt
def order_items(request):
    session = request.session.get("admin_id")
    if not session:
        return redirect("/admin_panel/")
    try:
        order_list = []
        order_dict = {}
        
        order_items = Order.objects.all().order_by('-id')
      
        for i in order_items:
            orders = Order.objects.filter(order_no = i.order_no)
            if orders.count() > 1:
                total = 0
                for order in orders:
                    total += int(order.payment)

                order_dict['id'] = orders[0].id
                order_dict['fk_customer'] = orders[0].fk_customer
                # order_dict['fk_shop_item'] = orders[0].fk_shop_item
                order_dict['order_no'] = orders[0].order_no
                order_dict['total'] = total
                order_dict['created_date'] = orders[0].created_date
                if order_dict not in order_list:
                    order_list.append(order_dict)
                
            else:
                order_dict['id'] = (i.id)
                order_dict['fk_customer'] = (i.fk_customer)
                # order_dict['fk_shop_item'] = (i.fk_customer)
                order_dict['order_no'] = (i.order_no)
                order_dict['total'] = i.payment
                order_dict['created_date'] = (i.created_date)

                order_list.append(order_dict)
                # print(order_list)
            order_dict = {}
        return render(request, 'admin_panel/order_items.html', {'order_items':order_list})
    except Exception as e:
        print(e)        
             

   
# ------------------- VIEW ORDER ITEMS DETAILS -----------------------------  

def order_item_detail(request,id):
    session = request.session.get("admin_id")
    if not session:
        return redirect("/admin_panel/")
    try:
        # Fetch data from model if exist
        if Order.objects.filter(id =id).exists():
            order = Order.objects.get(id=id)
            
            order_item = Order.objects.filter(order_no = order.order_no)
            stripe_session = order.stripe_session 

            if stripe_session:

                stripe.api_key = settings.STRIPE_SECRET_KEY
                response = stripe.checkout.Session.retrieve(
                stripe_session,
                )
                print("lll")
                
                amount_total = response['amount_total']
                amount_total = amount_total/100
            else : 
                amount_total = 0
                amount_total += round(float(order.payment), 2)

        
            context = {
                'order_item' : order_item,
                'address' : order.address,
                'customer' : order.fk_customer,
                'date' : order.created_date,
                'order_no' : order.order_no,
                'amount_total' : amount_total,
            }
        else:
            return redirect("/admin_panel/order-items")
        return render(request, 'admin_panel/order_item_detail.html', context)

    except Exception as e:
        print(e)


# ------------------- CHANGE PASSWORD -----------------------------

@csrf_exempt
def change_password(request):
    session = request.session.get("admin_id")
    if not session:
        return redirect("/admin_panel/")
    try:
        admin_id = request.session.get("admin_id")
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        # Check ADMIN with the given PASSWORD
        if AdminUser.objects.filter(id = admin_id, password=old_password).exists():
            admin = AdminUser.objects.get(id = admin_id)
            print(admin)
            # UPADTE with new password
            admin.password = new_password
            admin.save()
            response = "success"
        else:
            response = "error"
        return HttpResponse(response)
           
    except Exception as e:
        print(e)
        



