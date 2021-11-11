from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
import traceback 
from django.http import JsonResponse
import os
from django.template.loader import render_to_string
from django.http import HttpResponse 
import json
from datetime import datetime, date,time,timedelta
from django.conf import settings
import stripe
import xml.etree.ElementTree
from .email import *
from .models import *      # import all models from EHA APP


# ----------------- CHECK LOGIN CREDENTIALS ---------------------
@csrf_exempt
def api_signin(request):
	try:
		# fetch data from api request
		data = json.loads(request.body.decode('utf-8'))
		email = data['email']
		password = data['password']

		if Customer.objects.filter(email = email, password=password).exists():
			customer = Customer.objects.get(email = email, password=password)
			# Session created for logged in user
			request.session['customer_id'] = customer.id

			send_data = {'status':"1", 'msg':"Logged in successfully."}
			update_cart_with_session(request, customer)
			# clear Address if set
			if request.session.get('address'):
				request.session['address'] = ''

		else:
			# If Customer created send success message
			send_data = {'status':"0", 'msg':"Invalid Credentials"}

	except Exception as e:
		send_data = {'status':"0", 'msg':"Something Went Wrong", 'error':str(traceback.format_exc())}
	return JsonResponse(send_data)


# --------------------- Function to UPDATE CART with SESSION data----------------------
def update_cart_with_session(request, customer):
	# fetch CART from session
	cart = request.session.get('cart',[])

	# Update MODEL with CART data
	for shop_item_id in cart:
		shop_item =  ShopItems.objects.get(id = shop_item_id)
		#  if item is present in CART model 
		if Cart.objects.filter(fk_customer = customer, fk_shop_item = shop_item).exists():
			# do nothing
			pass
		else:
			# If not present then create new one
			cart_obj = Cart(fk_customer = customer, fk_shop_item = shop_item)
			cart_obj.save()

	# If user is logged in then update CART with model
	cart_items = Cart.objects.filter(fk_customer = customer)
	_cart = []
	if cart_items:
		for i in cart_items:
			_cart.append(i.id)
		request.session['cart'] = _cart
	else:
		request.session['cart'] = []






# ------------------- SIGN UP API to create add Customer ------------------------
@csrf_exempt
def api_signup(request):
	try:
		# fetch data from api request
		data = json.loads(request.body.decode('utf-8'))
		firstname = data['firstname']
		lastname = data['lastname']
		email = data['email']
		password = data['password']
		contact_no = data['contact_no']

		if Customer.objects.filter(email = email).exists():
			send_data = {'status':"0", 'msg':"Email already exists."}
		else:
			# Create new CUSTOMER object
			customer = Customer(
				firstname = firstname,
				lastname = lastname,
				email = email,
				password = password,
				contact_no = contact_no,
			)
			customer.save()

			# Session created for logged in user
			request.session['customer_id'] = customer.id
			update_cart_with_session(request, customer)
			# Lear addres if SET
			if request.session.get('address'):
				request.session['address'] = ''

			# If Customer created send success message
			send_data = {'status':"1", 'msg':"Customer created successfully"}

	except Exception as e:
		print(e)
		send_data = {'status':"0", 'msg':"Something Went Wrong", 'error':str(traceback.format_exc())}
	return JsonResponse(send_data)


# ------------------- API to add ITEMITEM in CART ------------------------
@csrf_exempt
def api_cart_add(request):
	try:
		# request.session['cart'] = []
		# fetch customer from session if LOGGED IN
		customer_id = request.session.get("customer_id")
		
		# fetch data from api request
		data = json.loads(request.body.decode('utf-8'))
		shop_item_id = data['shop_item_id']

		# if CART is present in session, then fetch 
		# otherwise create session variable with empty list 
		cart = request.session.get('cart',[])
		print(cart)

		# Check SHOP ITEM is exist with the given ID
		if ShopItems.objects.filter(id = shop_item_id).exists():
			if customer_id:
				# Fetch Customer and SHOP ITEM from Model
				shop_item = ShopItems.objects.get(id = shop_item_id)
				customer = Customer.objects.get(id=customer_id)

				# Check COURSE is EXIT in CART table wth Logged in CUSTOMER
				if Cart.objects.filter(fk_customer=customer, fk_shop_item=shop_item).exists():
					print("Already added in cart")
				else:
					# Add course in CART also
					cart_obj = Cart(fk_customer=customer, fk_shop_item=shop_item)
					cart_obj.save()

					# UPDATE CART table match with SESSION
					# IF is there any SHOP ITEMS in session but not in CART table
					for _shop_item_id in cart:
						# fetch SHOP ITEMS from MODEL
						_shop_item = ShopItems.objects.get(id = _shop_item_id)
						# Add in CART MODEL
						if Cart.objects.filter(fk_customer=customer, fk_shop_item=_shop_item).exists():
							pass
						else:
							_cart_obj = Cart(fk_customer=customer, fk_shop_item=_shop_item)
							_cart_obj.save()

			# Update SESSION CART
			if int(shop_item_id) not in cart:
				cart.append(int(shop_item_id))
				request.session['cart'] = cart
			print(cart)

			# create data to render in HTML
			cart_list = []
			total = 0
			for i in cart:
				if ShopItems.objects.filter(id = i).exists():
					shop_item_obj = ShopItems.objects.get(id = i)
					cart_list.append(shop_item_obj)
					total = total + round(float(shop_item_obj.price),2)
				else:
					cart.remove(i)


			# Render data to html
			rendered_data = render_to_string('eha_app/filters/cart.html', {'cart_list':cart_list,'total':total})
			return HttpResponse(rendered_data)

		else:
			# ERROR message
			send_data = {'status':"0", 'msg':"Shop item does not exists."}
		
	except Exception as e:
		print(e)
		send_data = {'status':"0", 'msg':"Something Went Wrong", 'error':str(traceback.format_exc())}
	return JsonResponse(send_data)



# ------------------- API to DELETE SHOP ITEM from CART ------------------------
@csrf_exempt
def api_cart_delete(request):
	try:
		# fetch data from request
		data = json.loads(request.body.decode('utf-8'))
		shop_item_id = data['shop_item_id']		
		from_cart = data['from_cart']

		# fetch CART from session
		cart = request.session.get('cart',[])
		print(request.session['cart'])

		# If CUSTOMER is logged in
		if request.session.get("customer_id"):
			customer_id = request.session.get("customer_id")
			# Fetch CUSTOMER
			customer = Customer.objects.get(id=customer_id)
			# Fetch SHOPITEMS
			shop_item = ShopItems.objects.get(id=shop_item_id)

			# delete SHOP ITEM from MODEL
			if Cart.objects.filter(fk_customer=customer, fk_shop_item=shop_item).exists():
				cart_obj = Cart.objects.filter(fk_customer=customer, fk_shop_item=shop_item) 
				cart_obj.delete()
		else:
			# if CUSTOMER is NOT logged in
			pass			

		# fetch CART from SESSION
		cart = request.session['cart']
		cart.remove(int(shop_item_id))
		request.session['cart'] = cart

		# create data to render in HTML
		cart_list = []
		total = 0
		for i in cart:
			if ShopItems.objects.filter(id = i).exists():
				shop_item_obj = ShopItems.objects.get(id = i)
				cart_list.append(shop_item_obj)
				total = total + round(float(shop_item_obj.price),2)
			else:
				cart.remove(i)

		if from_cart:
			send_data = {"status":"1","msg":"Shop item removed successfully", 'total':total}
		else:
			# Render data to html
			rendered_data = render_to_string('eha_app/filters/cart.html', {'cart_list':cart_list,'total':total})
			return HttpResponse(rendered_data)

		send_data = {"status":"1","msg":"Shop item removed Successfully", 'total':total}

	except Exception as e:
		send_data = {'status':"0", 'msg':"Something Went Wrong", 'error':str(traceback.format_exc())}
	return JsonResponse(send_data)




# ------------------- API to COUNT SHOP ITEM in CART ------------------------
@csrf_exempt
def api_cart_count(request):
	try:
		# fetch SESSION of CART
		cart = request.session.get('cart',[])

		# if there is items in the cart
		cart_count =  len(cart)

		# Render data as response
		send_data = {"status":"1",'cart_count':cart_count}

	except Exception as e:
		send_data = {'status':"0",'error':str(traceback.format_exc())}
	return JsonResponse(send_data)


# ------------------- API to VALIDATE COUPON and APPLY on TOTAL COUNT ------------------------
@csrf_exempt
def api_validate_coupon(request):
	try:
		# fetch data from request
		data = json.loads(request.body.decode('utf-8'))
		coupon_code = data['coupon_code'].upper()

		# fetch SESSION of CART
		cart = request.session.get('cart',[])

		# Calculate Total
		total = 0
		for i in cart:
			if ShopItems.objects.filter(id = i).exists():
				shop_item_obj = ShopItems.objects.get(id = i)
				total = total + (float(shop_item_obj.price))

		if Coupon.objects.filter(coupon_code = coupon_code).exists():
			coupon = Coupon.objects.get(coupon_code=coupon_code)

			if coupon.expiry_date < date.today():
				print("1")
				# if coupon is expired
				send_data = {"status":"0","msg":"expired","total":total}
			elif coupon.uses_remain == 0:
				send_data = {"status":"0","msg":"usage exceeded","total":total}
			else:
				# fetch discount
				discount = float(coupon.discount)
				
				# calaculate discount
				discount_amount =  round(total*discount/100,2)
				# calculate final amount
				amount_after_discount = total-discount_amount
				# data to return as response
				send_data = {
					'status' : '1',
					'total' : total,
					'discount' : discount_amount,
					'final_amount' : amount_after_discount,
					'coupon_code' : coupon_code,
					'uses_remain' : coupon.uses_remain
				}
		else:
			# if coupon is not present
			send_data = {"status":"0","msg":"not valid","total":total}

	except Exception as e:
		send_data = {'status':"0",'error':str(traceback.format_exc())}
	return JsonResponse(send_data)




# ------------------- API to EDIT PROFILE data ------------------------
@csrf_exempt
def api_profile_edit(request):
	try:
		# fetch data from api request
		data = json.loads(request.body.decode('utf-8'))
		id = data['id']
		firstname = data['firstname']
		lastname = data['lastname']
		address = data['address']
		contact_no = data['contact_no']

		if Customer.objects.filter(id = id).exists():
			# fetch CUSTOMER data from MODEL
			customer = Customer.objects.get(id=id)
			# Update with new data
			customer.firstname = firstname
			customer.lastname = lastname
			customer.address = address
			customer.contact_no = contact_no
			customer.save()

			# If Customer created send success message
			send_data = {'status':"1", 'msg':"Customer updated successfully"}

		else:
			# If Customer does not exist 
			send_data = {'status':"0", 'msg':"Customer does not exiss."}

	except Exception as e:
		send_data = {'status':"0", 'msg':"Something Went Wrong", 'error':str(traceback.format_exc())}
	return JsonResponse(send_data)


# ------------------- API to EDIT PROFILE PICTURE(CUSTOMER) ------------------------
@csrf_exempt
def api_profile_pic_edit(request):
	try:
		# fetch customer ID from SESSION
		customer_id = request.session.get("customer_id")
		# Fetch data from request
		profile_img = request.FILES.get('profile_img')

		# Check if user exist
		if Customer.objects.filter(id=customer_id).exists():
			user_obj = Customer.objects.get(id=customer_id)
			# Update profile picture
			user_obj.profile_img = profile_img #img_url
			user_obj.save()
			# Is Success send SUCCESS message
			send_data = {"status":"1","msg":"Profile picture updated successfully"}
		else:
			# If Customer does not exist 
			send_data = {'status':"0", 'msg':"Customer does not exiss."}

	except Exception as e:
		send_data = {'status':"0", 'msg':"Something Went Wrong", 'error':str(traceback.format_exc())}
	return JsonResponse(send_data)


# ------------------- API to CHANGE PASSWORD (CUSTOMER) ------------------------
@csrf_exempt
def api_change_password(request):
	try:
		# fetch data from request
		data = json.loads(request.body.decode('utf-8'))
		customer_id = request.session.get("customer_id")
		old_password = data['old_password']
		new_password = data['new_password']
		
		# Check CUSTOMER with the given PASSWORD
		if Customer.objects.filter(id = customer_id, password=old_password).exists():
			customer = Customer.objects.get(id = customer_id)
			# UPADTE with new password
			customer.password = new_password
			customer.save()

			# if SUCCESS
			send_data = {"status":"1","msg":"Password updated successfully"}
		else : 
			# If Customer PASSWORD is incorrect
			send_data = {"status":"0","msg":"Incorrect old password"}
			
	except Exception as e:
		send_data = {'status':"0", 'msg':"Something Went Wrong", 'error':str(traceback.format_exc())}
	return JsonResponse(send_data)


# ------------------- API to FORGOT PASSWORD (CUSTOMER) ------------------------
@csrf_exempt
def api_forgot_password(request):
	try:
		# fetch data from request
		data = json.loads(request.body.decode('utf-8'))
		email = data["email"]

		# Chech id email is registered or not
		if 	Customer.objects.filter(email = email).exists():
			customer = Customer.objects.get(email = email)

			# Create random code 
			code = random.randint(1000,9999)
			# save code in Model
			customer.reset_code = code
			print(code)
			customer.save()

			# SEND E-MAIL with VERIFICATION code
			reset_password(code, customer.email, customer.firstname)

			# If SUCCESS
			send_data = {"status":"1","msg":"Code sent Successfully"}
		else:
			# ERROR message if email is not registered
			send_data = {"status":"0","msg":"Email is not registered"} 
	except Exception as e:
		print(e)
		send_data = {'status':"0", 'msg':"Something Went Wrong", 'error':str(traceback.format_exc())}
	return JsonResponse(send_data)


# ------------------- API to VERIFY CODE to change PASSWORD (CUSTOMER) ------------------------
@csrf_exempt
def api_verify_code(request):
	try:
		# fetch data from request
		data = json.loads(request.body.decode('utf-8'))
		email = data["email"]
		code = data["code"]

		# Chech id email is registered or not
		if 	Customer.objects.filter(email = email).exists():
			customer = Customer.objects.get(email = email)

			if customer.reset_code == code:
				# If SUCCESS
				send_data = {"status":"1","msg":"Code verified"}
			else:
				# ERROR
				send_data = {"status":"0","msg":"Code does not match"}

		else:
			# ERROR message if email is not registered
			send_data = {"status":"0","msg":"Email is not registered"} 
	except Exception as e:
		print(e)
		send_data = {'status':"0", 'msg':"Something Went Wrong", 'error':str(traceback.format_exc())}
	return JsonResponse(send_data)



# ------------------- API to RESET PASSWORD (CUSTOMER) ------------------------
@csrf_exempt
def api_reset_password(request):
	try:
		# fetch data from request
		data = json.loads(request.body.decode('utf-8'))
		email = data["email"]
		password = data["password"]

		# Chech id email is registered or not
		if 	Customer.objects.filter(email = email).exists():
			customer = Customer.objects.get(email = email)
			# save updated password
			customer.password = password
			customer.save()
			
			# Session created for logged in user
			request.session['customer_id'] = customer.id

			# If SUCCESS
			send_data = {"status":"1","msg":"Password updated successfully"}
		else:
			# ERROR message if email is not registered
			send_data = {"status":"0","msg":"Email is not registered"} 
	except Exception as e:
		print(e)
		send_data = {'status':"0", 'msg':"Something Went Wrong", 'error':str(traceback.format_exc())}
	return JsonResponse(send_data)



@csrf_exempt
def stripe_config(request):
	stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
	return JsonResponse(stripe_config, safe=False)


@csrf_exempt
def create_checkout_session(request):
	try:
		if request.method == 'GET':
			if request.session.get('coupon') and request.session.get('coupon') != '':
				coupon = Coupon.objects.get(coupon_code = request.session.get('coupon'))
				discount = float(coupon.discount)
				cart = request.session.get('cart')

				items = []
				for shop_item_id in cart:
					shop_item = ShopItems.objects.get(id = shop_item_id)
					name = ''.join(xml.etree.ElementTree.fromstring(shop_item.title).itertext())
					discount_calculated = (float(shop_item.price)*discount/100)
					final_amount = round(float(shop_item.price) - discount_calculated, 2)
					d = {
						'name' : name,
						'quantity' : 1,
						'currency' : 'usd',
						'amount' : int(final_amount * 100),
					}
					items.append(d)
			else:
				cart = request.session.get('cart')
				items = []
				for shop_item_id in cart:
					shop_item = ShopItems.objects.get(id = shop_item_id)
					name = ''.join(xml.etree.ElementTree.fromstring(shop_item.title).itertext())
					final_amount = round(float(shop_item.price),2)
					d = {
						'name' : name,
						'quantity' : 1,
						'currency' : 'usd',
						'amount' : int(final_amount * 100),
					}
					items.append(d)


			# domain_url = 'http://localhost:8000/'
			domain_url = 'https://environmentalhealthanalytics.com/'
			stripe.api_key = settings.STRIPE_SECRET_KEY
			customer_id = request.session.get("customer_id")
			customer = Customer.objects.get(id = customer_id)
			checkout_session = stripe.checkout.Session.create(
				success_url = domain_url + 'success?session_id={CHECKOUT_SESSION_ID}',
				cancel_url = domain_url + 'cancelled/',
				payment_method_types = ['card'],
				mode = 'payment',
				line_items = items,
				customer_email = customer.email
			)
			print(checkout_session)
		return JsonResponse({'sessionId': checkout_session['id']})
	except Exception as e:
		print(e)
		return JsonResponse({'error': str(e)})



# ------------------- API to SEND CONTACT MAIL ------------------------
@csrf_exempt
def api_contact(request):
	try:
		# fetch data from request
		name = request.POST.get('name')
		email = request.POST.get('email')
		subject = request.POST.get('subject')
		message = request.POST.get('message')
		# send Email
		email_contact_us(name=name, email=email, subject=subject, message=message)
		# If SUCCESS
		send_data = 'OK'
	except Exception as e:
		# ERROR MESSAFE
		send_data = 'Something went wrong, please try again later.'
	return HttpResponse(send_data)

	
# ------------------- API to SET CHECKOUT ADDRESS ------------------------
@csrf_exempt
def set_checkout_address(request):
	try:
		# fetch data from request
		address = request.POST.get('address')
		request.session['address'] = address
		send_data = 'OK'
	except Exception as e:
		# ERROR MESSAFE
		send_data = 'Something went wrong, please try again later.'
	return HttpResponse(send_data)
