from django.shortcuts import render
from .views_api import *          # import all functions from views_api file
from .models import *             # import all models from EHA app

def demo(request):
	return render(request,'eha_app/demo.html')

#------------------------- HOME PAGE ----------------------
def index(request):
	customer_id = request.session.get("customer_id")

	# IF CUSTOMER LOGGEN IN
	if Customer.objects.filter(id=customer_id).exists():
		customer = Customer.objects.get(id=customer_id)
		context = {
			'customer' : customer,
		}
		return render(request,'eha_app/index.html',context)
	else:
		# if NO CUSTOMER LOGGED IN
		return render(request,'eha_app/index.html')


#------------------------- REPORT DETAILS ----------------------
def report_details(request):
	customer_id = request.session.get("customer_id")

	# IF CUSTOMER LOGGEN IN
	if Customer.objects.filter(id=customer_id).exists():
		customer = Customer.objects.get(id=customer_id)
		context = {
			'customer' : customer,
		}
		return render(request,'eha_app/report_details.html',context)
	else:
		# if NO CUSTOMER LOGGED IN
		return render(request,'eha_app/report_details.html')



#------------------------- EXAPMPLE REPORT----------------------
def example_report(request):
	customer_id = request.session.get("customer_id")

	# IF CUSTOMER LOGGEN IN
	if Customer.objects.filter(id=customer_id).exists():
		customer = Customer.objects.get(id=customer_id)
		context = {
			'customer' : customer,
		}
		return render(request,'eha_app/example_report.html',context)
	else:
		# if NO CUSTOMER LOGGED IN
		return render(request,'eha_app/example_report.html')




#------------------------- TECHNICAL DETAILS ----------------------
def technical_details(request):
	customer_id = request.session.get("customer_id")

	# IF CUSTOMER LOGGEN IN
	if Customer.objects.filter(id=customer_id).exists():
		customer = Customer.objects.get(id=customer_id)
		context = {
			'customer' : customer,
		}
		return render(request,'eha_app/technical_details.html',context)
	else:
		# if NO CUSTOMER LOGGED IN
		return render(request,'eha_app/technical_details.html')




#------------------------- POLLUTANT_INFORMATION_PM_25 ----------------------
def pollutant_information_pm_25(request):
	customer_id = request.session.get("customer_id")

	# IF CUSTOMER LOGGEN IN
	if Customer.objects.filter(id=customer_id).exists():
		customer = Customer.objects.get(id=customer_id)
		context = {
			'customer' : customer,
		}
		return render(request,'eha_app/pollutant_information_pm_25.html',context)
	else:
		# if NO CUSTOMER LOGGED IN
		return render(request,'eha_app/pollutant_information_pm_25.html')



#------------------------- POLLUTANT_INFORMATION_PM_25 ----------------------
def pollutant_information_particulate_matter(request):
	customer_id = request.session.get("customer_id")

	# IF CUSTOMER LOGGEN IN
	if Customer.objects.filter(id=customer_id).exists():
		customer = Customer.objects.get(id=customer_id)
		context = {
			'customer' : customer,
		}
		return render(request,'eha_app/pollutant_information_particulate_matter.html',context)
	else:
		# if NO CUSTOMER LOGGED IN
		return render(request,'eha_app/pollutant_information_particulate_matter.html')


#------------------------- POLLUTANT_INFORMATION_OZONE ----------------------
def pollutant_information_ozone(request):
	customer_id = request.session.get("customer_id")

	# IF CUSTOMER LOGGEN IN
	if Customer.objects.filter(id=customer_id).exists():
		customer = Customer.objects.get(id=customer_id)
		context = {
			'customer' : customer,
		}
		return render(request,'eha_app/pollutant_information_ozone.html',context)
	else:
		# if NO CUSTOMER LOGGED IN
		return render(request,'eha_app/pollutant_information_ozone.html')


#------------------------- POLLUTANT_INFORMATION_NITROGEN DIOXIDE ----------------------
def pollutant_information_nitrogen_dioxide(request):
	customer_id = request.session.get("customer_id")

	# IF CUSTOMER LOGGEN IN
	if Customer.objects.filter(id=customer_id).exists():
		customer = Customer.objects.get(id=customer_id)
		context = {
			'customer' : customer,
		}
		return render(request,'eha_app/pollutant_information_nitrogen_dioxide.html',context)
	else:
		# if NO CUSTOMER LOGGED IN
		return render(request,'eha_app/pollutant_information_nitrogen_dioxide.html')




#------------------------- PAGE UNDER CONSTRUCTION ----------------------
def page_under_construction(request):
	customer_id = request.session.get("customer_id")

	# IF CUSTOMER LOGGEN IN
	if Customer.objects.filter(id=customer_id).exists():
		customer = Customer.objects.get(id=customer_id)
		context = {
			'customer' : customer,
		}
		return render(request,'eha_app/page_under_construction.html',context)
	else:
		# if NO CUSTOMER LOGGED IN
		return render(request,'eha_app/page_under_construction.html')



#------------------------- SIGN IN ----------------------
def signin(request):
	next = '/'
	email = request.COOKIES.get("email")
	if request.GET.get('next'):
		next = request.GET.get('next')
	if email:
		return render(request,'eha_app/signin.html', {'next':next,'email':email,'checked':True})
	else:
	 	return render(request,'eha_app/signin.html', {'next':next,'checked':False})





#------------------------- SIGN UP ----------------------
def signup(request):
	return render(request,'eha_app/signup.html')



#------------------------- SIGN OUT ----------------------
def signout(request):
	try:
		# Delete CUSTOMER SESSION
		del request.session['customer_id']
		# CLEAR CART ENTRIES
		request.session['cart'] = []

		if request.session.get('address'):
			request.session['address'] = ''
	except KeyError:
		pass
	return redirect("/")



#------------------------- FORGOT PASSWORD ----------------------
def forgot_password(request):
	return render(request,'eha_app/forgot_password.html')



#------------------------- CONTACT US ----------------------
def contact(request):
	customer_id = request.session.get("customer_id")
	# IF CUSTOMER LOGGEN IN
	if Customer.objects.filter(id=customer_id).exists():
		customer = Customer.objects.get(id=customer_id)
		context = {
			'customer' : customer,
		}
		return render(request,'eha_app/contact_us.html',context)
	else:
		# if NO CUSTOMER LOGGED IN
		return render(request,'eha_app/contact_us.html')


#------------------------- SHOP ITEMS ----------------------
def shop(request):
	customer_id = request.session.get("customer_id")

	# IF CUSTOMER LOGGEN IN
	if Customer.objects.filter(id=customer_id).exists():
		customer = Customer.objects.get(id=customer_id)
	else:
		customer = None

	# FEtch SHOP ITEMS from MODEL
	shop_items = ShopItems.objects.all().order_by('-id')
	context = {
		'customer' : customer,
		'shop_items' : shop_items,
	}
	return render(request,'eha_app/shop_items.html',context)




#------------------------- profile ----------------------
def profile(request):
	customer_id = request.session.get("customer_id")

	# IF CUSTOMER LOGGEN IN
	if Customer.objects.filter(id=customer_id).exists():
		customer = Customer.objects.get(id=customer_id)
		context = {
			'customer' : customer,
		}
		return render(request,'eha_app/profile.html',context)
	else:
		# if NO CUSTOMER LOGGED IN
		return render(request,'eha_app/index.html')



#------------------------- profile EDIT ----------------------
def profile_edit(request):
	customer_id = request.session.get("customer_id")

	# IF CUSTOMER LOGGEN IN
	if Customer.objects.filter(id=customer_id).exists():
		customer = Customer.objects.get(id=customer_id)
		context = {
			'customer' : customer,
		}
		return render(request,'eha_app/profile_edit.html',context)
	else:
		# if NO CUSTOMER LOGGED IN
		return render(request,'eha_app/index.html')



#------------------------- CART ----------------------
def cart(request):
	try:
		# if CUSTOMER id LOGGED IN
		customer_id = request.session.get("customer_id")

		# Fetch session CART
		cart = request.session.get('cart',[])
		print(cart)

		total = 0  # To calculate the total amaount of cart items

		if customer_id:
			customer = Customer.objects.get(id=customer_id)
			# fetch CART items from model
			cart_items = Cart.objects.filter(fk_customer=customer).order_by("-id")

			cart = []
			cart_list = []
			for item in cart_items:
				if item.fk_shop_item.id not in cart:
					# add SHOP ITEM ID in the list to update cart session
					cart.append(item.fk_shop_item.id)
					# ADD to CART LIST
					cart_list.append(item.fk_shop_item)
					# calculate total amount
					total += (float(item.fk_shop_item.price))

			# update SESSION CART with MODEL data
			request.session['cart'] = cart
			print(cart_list)
		else:
			# if CUSTOMER is NOT logged in
			customer = ''
			# fetch CART from SESSION
			cart_list = []
			for shop_item_id in cart:
				# fetch SHOP ITEM from Model 
				shop_item = ShopItems.objects.get(id=shop_item_id)
				# Append in CART_list to render in HTML
				cart_list.append(shop_item)
				# Calculate ATotal Amount
				total += (float(shop_item.price))

		print(cart_list)


		# create data to render in HTML
		if request.session.get('address'):
			address = request.session['address']
		else:
			address = None
		context = {
			'customer' : customer,
			'cart_list' : cart_list,
			'total' : total,
			'address' : address,
		}

	except Exception as e:
		print(e)
		return render(request, 'eha_app/cart.html')		
	return render(request, 'eha_app/cart.html', context)


#------------------------- CART CHECKOUT----------------------
def checkout(request):
	try:

		# fetch CUSTOMER ID form SESSISON
		customer_id = request.session.get("customer_id")

		# IF CUSTOMER LOGGEN IN
		if Customer.objects.filter(id=customer_id).exists():
			customer = Customer.objects.get(id=customer_id)

			# # fetch delivery address
			# request.session['address'] = request.POST.get('address')
			# request.session['longitude'] = request.POST.get('pick_longitude')
			# request.session['latitude'] = request.POST.get('pick_latitude')

			# # if coupon is applied then set coupon code in the session
			# # so that we can calculate the final amount durin stripe payment redirection
			# if request.POST.get('coupon'):
			# 	coupon = request.POST.get('coupon')
			# 	if coupon != "":
			# 		request.session['coupon'] = coupon

			context = {
				'customer' : customer,
			}
			return render(request,'eha_app/checkout.html', context)	
		else:
			return redirect("/cart")
	except Exception as e:
		return redirect("/cart")

def cart_checkout(request):
	try:
		# fetch CUSTOMER ID form SESSISON
		customer_id = request.session.get("customer_id")

		# IF CUSTOMER LOGGEN IN
		if Customer.objects.filter(id=customer_id).exists():
			customer = Customer.objects.get(id=customer_id)

			# fetch delivery address
			if request.method == 'POST':
				print('address ', request.POST.get('address'))
				request.session['address'] = request.POST.get('address')
				request.session['longitude'] = request.POST.get('pick_longitude')
				request.session['latitude'] = request.POST.get('pick_latitude')

			# if coupon is applied then set coupon code in the session
			# so that we can calculate the final amount durin stripe payment redirection
			if request.POST.get('coupon'):
				coupon = request.POST.get('coupon')
				if coupon != "":
					request.session['coupon'] = coupon
			else : 
				coupon = None


			# fetch CART items from model
			cart_items = Cart.objects.filter(fk_customer=customer).order_by("-id")
			print('cart_items')
			print(cart_items)

			total = 0  # To calculate the total amaount of cart items
			cart_list = []
			for item in cart_items:
				# ADD to CART LIST
				cart_list.append(item.fk_shop_item)
				# calculate total amount
				total += (float(item.fk_shop_item.price))
			print('coupon' , coupon)
			# create data to render in HTML
			context = {
				'customer' : customer,
				'cart_list' : cart_list,
				'total' : total,
				'address' : request.session['address'] ,
				'coupon' : coupon
			}
			return render(request,'eha_app/checkout_paypal.html', context)	
		else:
			return redirect("/cart")
	except Exception as e:
		return redirect("/cart")


def unique_order_id_generator():
	try:
		if Order.objects.latest('id'):
			last_order = Order.objects.latest('id')
			new_order_no = int(last_order.order_no.split('/')[3]) + 1
		else:
			new_order_no = 1
	except Exception as e:
		new_order_no = 1
	pattern = "O/" + str(date.today().year) + "/" + str(date.today().month) + "/"
	order_no = pattern + str(new_order_no)
	print(order_no)
	return order_no


#------------------------- PAYMENT SUCCESS ----------------------
def payment_success(request):
	# Generate a random order number to save in model
	order_no = unique_order_id_generator()
	# return render(request,'eha_app/success.html')


	# fetch STRIPE SESSION ID from request URL
	stripe_session = ''
	if request.GET.get('session_id'):
		stripe_session = request.GET.get('session_id')

	# fetch CUSTOMER DATA
	customer_id = request.session.get("customer_id")
	customer = Customer.objects.get(id = customer_id)

	# fetch cart data from session
	cart = request.session.get('cart',[])

	for shop_item_id in cart:
		# fetch SHOP ITEM data from model
		shop_item = ShopItems.objects.get(id = shop_item_id)

		# DELETE data from CART Model
		if Cart.objects.filter(fk_customer=customer, fk_shop_item=shop_item).exists():
			cart_obj = Cart.objects.filter(fk_customer=customer, fk_shop_item=shop_item) 
			cart_obj.delete()

		# if COUPON is applied
		if request.session.get('coupon') and request.session.get('coupon') != '':
			fk_coupon = Coupon.objects.get(coupon_code = request.session.get('coupon'))
			discount = float(fk_coupon.discount)
			discount_calculated = round(float(shop_item.price)*discount/100,2)
			payment = round(float(shop_item.price) - discount_calculated, 2)

		else:
			fk_coupon = None
			payment = (float(shop_item.price))


		address = request.session['address']
		longitude = request.session['longitude']
		latitude = request.session['latitude']


		# SAVE  data in PURCHASE HISTORY Model
		order = Order(
			fk_customer = customer,
			fk_shop_item = shop_item,
			order_no = order_no,
			price = shop_item.price,
			payment = payment,
			fk_coupon = fk_coupon,
			address = address,
			longitude = longitude,
			latitude = latitude,
			stripe_session = stripe_session,
		)
		order.save()

	# reset SESSION for CART and COUPON
	request.session['cart'] = []
	# delete session
	if request.session.get('coupon'):
		del request.session['coupon']
	if request.session.get('address'):
		del request.session['address']
	if request.session.get('longitude'):
		del request.session['longitude']
	if request.session.get('latitude'):
		del request.session['latitude']

	if request.GET.get('session_id'):
		print(request.GET.get('session_id'))

	# send order confirmation mail
	orders = Order.objects.filter(order_no=order_no)
	total = 0
	for i in orders:
		total += float(i.payment)
		i.payment = format(float(i.payment), '.2f')
      
	total = format(total, '.2f')
	# send mail
	fullname=' '.join(filter(None, (customer.firstname, customer.lastname)))
	order_confirmation(customer.email, fullname, orders, total, address)
	order_confirmation_admin(fullname, address, orders, total,customer.email)

	context = {
		'customer' : customer,
	}
	return render(request,'eha_app/success.html', context)




#------------------------- PAYMENT CANCELLED ----------------------
def payment_cancelled(request):
	# fetch CUSTOMER DATA
	customer_id = request.session.get("customer_id")
	customer = Customer.objects.get(id = customer_id)

	# delete session
	if request.session.get('coupon'):
		del request.session['coupon']
	if request.session.get('address'):
		del request.session['address']
	if request.session.get('longitude'):
		del request.session['longitude']
	if request.session.get('latitude'):
		del request.session['latitude']

	context = {
		'customer' : customer,
	}
	return render(request,'eha_app/cancelled.html', context)


#------------------------- PAYMENT CANCELLED ----------------------
def purchase_history(request):
	customer_id = request.session.get("customer_id")

	# IF CUSTOMER LOGGEN IN
	if Customer.objects.filter(id=customer_id).exists():
		customer = Customer.objects.get(id=customer_id)

		# fetch PUCHASE HISTORY
		orders = Order.objects.filter(fk_customer=customer).order_by('-id')

		context = {
			'customer' : customer,
			'orders' : orders,
		}
		return render(request,'eha_app/purchase_history.html',context)
	else:
		# if NO CUSTOMER LOGGED IN
		return render(request,'eha_app/index.html')



#------------------------- PAYMENT CANCELLED ----------------------
def receipt(request, id):
	try:
		customer_id = request.session.get("customer_id")

		# IF CUSTOMER LOGGEN IN
		if Customer.objects.filter(id=customer_id).exists():
			customer = Customer.objects.get(id=customer_id)

			# fetch Order data
			order = Order.objects.get(id=id)
			orders = Order.objects.filter(order_no=order.order_no)
			stripe_session = order.stripe_session

			if stripe_session:

				stripe.api_key = settings.STRIPE_SECRET_KEY
				response = stripe.checkout.Session.retrieve(
				  stripe_session,
				)
				amount_total = response['amount_total']
				amount_total = amount_total/100
				payment_intent = response['payment_intent']
				response1 = stripe.PaymentIntent.retrieve(
				  payment_intent,
				)
				payment_method = response1['payment_method']
				response2 = stripe.PaymentMethod.retrieve(
				  payment_method,
				)
				brand = response2['card']['brand']
				last4 = response2['card']['last4']
				payment_type = brand.capitalize() + " ****"+last4
			else : 
				amount_total = 0
				for order in orders:
					amount_total += round(float(order.payment), 2)
				payment_type = 'PayPal'


			context = {
				'customer' : customer,
				'orders' : orders,
				'amount_total' : amount_total,
				'payment_type' : payment_type,
				'date' : order.created_date,
				'order_no' : order.order_no,
			}
			return render(request,'eha_app/receipt.html',context)
		else:
			# if NO CUSTOMER LOGGED IN
			return render(request,'eha_app/index.html')

	except Exception as e:
		print(e)
		return redirect("/profile/purchase-history")	


