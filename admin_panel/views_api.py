from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
import traceback 
from django.http import JsonResponse
import os
import json

from .models import *             # import all models from ADMIN PANEL
from eha_app.models import *      # import all models from EHA APP



# --------- Validate ADMIN USER LOGIN ------------
@csrf_exempt
def api_admin_login(request):
	try:
		# fetch data from api request
		email = request.POST.get('email')
		password = request.POST.get('password')

		# Check whether USER EXIST or NOT
		if AdminUser.objects.filter(username=email,password=password).exists():
			user = AdminUser.objects.get(username=email,password=password)
			request.session['admin_id'] = str(user.id)

			send_data = {'status':"1", 'msg':"Login successfull"}
		else:
			# If NO USERNAME PASSWORD GET MATCHED
			send_data = {'status':"0", 'msg':"Invalid Credentials"}

	except Exception as e:
		send_data = {'status':"0", 'msg':"Something Went Wrong", 'error':str(traceback.format_exc())}
	return JsonResponse(send_data)


# =================== API for SHOP ITEMS =====================

# ------------------- ADD SHOPITEMS -----------------------------
@csrf_exempt
def api_shop_item_add(request):
	try:
		# fetch data from api request
		title = request.POST.get('title')
		description = request.POST.get('description')
		image = request.FILES.get('image')
		price = request.POST.get('price')
		category = request.POST.get('category')

		# Create new SHOP ITEM object
		shop_item = ShopItems(
			title = title,
			description = description,
			image = image,
			price = price,
			category = category
		)
		shop_item.save()
		
		# If saved send success message
		send_data = {'status':"1", 'msg':"Shop item saved successfully"}

	except Exception as e:
		print(e)
		send_data = {'status':"0", 'msg':"Something Went Wrong", 'error':str(traceback.format_exc())}
	return JsonResponse(send_data)

# ------------------- EDIT SHOP ITEM -----------------------------
@csrf_exempt
def api_shop_item_edit(request):
	try:
		# fetch data from api request
		id = request.POST.get('id')
		title = request.POST.get('title')
		description = request.POST.get('description')
		image = request.FILES.get('image')
		price = request.POST.get('price')
		category = request.POST.get('category')

		# Check id data exist with given ID
		if ShopItems.objects.filter(id=id).exists():
			shop_item = ShopItems.objects.get(id=id)
			# Update data
			shop_item.title = title
			shop_item.description = description 
			# if image is present in request
			if image :
				shop_item.image = image
			shop_item.price = price
			shop_item.category = category 
			shop_item.save()

			# If saved send success message
			send_data = {'status':"1", 'msg':"Shop item updated successfully"}
		else:
			# Error message
			send_data = {'status':"0", 'msg':"Shop item does not exist."}

	except Exception as e:
		print(e)
		send_data = {'status':"0", 'msg':"Something Went Wrong", 'error':str(traceback.format_exc())}
	return JsonResponse(send_data)

# ------------------- DELETE SHOP ITEM -----------------------------
@csrf_exempt
def api_shop_item_delete(request):
	try:
		# fetch data from api request
		data = json.loads(request.body.decode('utf-8'))
		id = data['id']

		if ShopItems.objects.filter(id=id).exists():
			# Fetch Model data
			shop_item = ShopItems.objects.get(id=id)
			shop_item.delete()
		
			# If delete send success message
			send_data = {'status':"1", 'msg':"Shop item deleted successfully"}
		else:
			# Error message
			send_data = {'status':"0", 'msg':"Shop item does not exist."}

	except Exception as e:
		send_data = {'status':"0", 'msg':"Something Went Wrong", 'error':str(traceback.format_exc())}
	return JsonResponse(send_data)
	

# =================== API for COUPON =====================

# -------------------- ADD COUPON -----------------------
@csrf_exempt
def api_coupon_add(request):
	try:
		# fetch data from api request
		data = json.loads(request.body.decode('utf-8'))
		coupon_code = data['coupon_code'].upper()
		discount = data['discount']
		expiry_date = data['expiry_date']
		total_uses = data['total_uses']
		uses_remain = data['uses_remain']
		# Create new coupon object
		coupon = Coupon(
			coupon_code = coupon_code,
			discount = discount,
			expiry_date = expiry_date,
			total_uses = total_uses,
			uses_remain = uses_remain
		)
		coupon.save()
		
		# If Save send success message
		send_data = {'status':"1", 'msg':"Coupon saved successfully"}

	except Exception as e:
		print(e)
		send_data = {'status':"0", 'msg':"Something Went Wrong", 'error':str(traceback.format_exc())}
	return JsonResponse(send_data)


# ------------------ EDIT COUPON ---------------------
@csrf_exempt
def api_coupon_edit(request):
	try:
		# fetch data from api request
		data = json.loads(request.body.decode('utf-8'))
		id = data['id']
		coupon_code = data['coupon_code'].upper()
		discount = data['discount']
		expiry_date = data['expiry_date']
		total_uses = data['total_uses']
		uses_remain = data['uses_remain']

		if Coupon.objects.filter(id=id).exists():
			coupon = Coupon.objects.get(id=id)
			coupon.coupon_code = coupon_code
			coupon.discount = discount 
			coupon.expiry_date = expiry_date
			coupon.total_uses = total_uses
			coupon.uses_remain = uses_remain
			coupon.save()

			# If saved send success message
			send_data = {'status':"1", 'msg':"Coupon updated successfully"}
		else:
			# Error message
			send_data = {'status':"0", 'msg':"Coupon does not exist."}


	except Exception as e:
		print(e)
		send_data = {'status':"0", 'msg':"Something Went Wrong", 'error':str(traceback.format_exc())}
	return JsonResponse(send_data)


# --------------------- DELETE COUPON --------------------------
@csrf_exempt
def api_coupon_delete(request):
	try:
		# fetch data from api request
		data = json.loads(request.body.decode('utf-8'))
		id = data['id']

		if Coupon.objects.filter(id=id).exists():
			# Fetch Model data
			coupon = Coupon.objects.get(id=id)
			coupon.delete()
		
			# If delete send success message
			send_data = {'status':"1", 'msg':"Coupon deleted successfully"}
		else:
			# Error message
			send_data = {'status':"0", 'msg':"Coupon does not exist."}

	except Exception as e:
		print(e)
		send_data = {'status':"0", 'msg':"Something Went Wrong", 'error':str(traceback.format_exc())}
	return JsonResponse(send_data)
