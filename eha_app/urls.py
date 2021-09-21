from django.urls import path, re_path

from .views import *


urlpatterns = [
	# HOME PAGE
	path('',index, name='index'),
	path('demo', demo, name='demo'),

	# PAGE UNDER CONSTRUCTION
	path('puc', page_under_construction, name='page_under_construction_app'),

	# CUSTOMER SIGN IN
	path('signin', signin, name='signin'),
	path('signup', signup, name='signup'),
	path('signout', signout, name='signout'),
	path('forgot-password', forgot_password, name='forgot_password'),

	# SHOP ITEMS
	path('shop', shop, name = 'shop'),

	# CUSTOMER PROFILE
	path('profile', profile, name = 'profile'),
	path('profile/edit', profile_edit, name = 'profile_edit'),
	path('profile/purchase-history', purchase_history, name = 'purchase_history'),
	re_path('profile/receipt/(?P<id>[0-9]+)', receipt, name = 'receipt'),

	# CART/CHECKOUT
	path('cart', cart, name = 'cart'),
	path('cart/checkout/', cart_checkout, name = 'cart_checkout'), #for PAYPAL
	path('checkout/', checkout, name = 'checkout'),

	# PAYMENT SUCCESS/CANCELLED
    path('success/', payment_success, name = 'success'), 
    path('cancelled/', payment_cancelled, name = 'cancelled'), 

    # CONTACT US
    path('contact-us/', contact, name = 'contact'), 
    path('email_order_details/', email_order_details, name = 'email_order_details'),

    # PRODUCT DETAILS
    path('report-details/', report_details, name = 'report_details'), 
    path('example-report/', example_report, name = 'example_report'), 
    path('technical-details/', technical_details, name = 'technical_details'), 

    # POLLUTANT INFORMATION
    path('pollutant-information/PM-2.5/', pollutant_information_pm_25, name = 'pollutant_information_pm_25'), 
    path('pollutant-information/particulate_matter', pollutant_information_particulate_matter, name = 'pollutant_information_particulate_matter'), 
    path('pollutant-information/ozone', pollutant_information_ozone, name = 'pollutant_information_ozone'), 
    path('pollutant-information/nitrogen-dioxide', pollutant_information_nitrogen_dioxide, name = 'pollutant_information_nitrogen_dioxide'), 

]

# API URLS
urlpatterns += [
	# CUSTOMER : signin, signup
	path('api/signup',api_signup, name='api_signup'),
	path('api/signin',api_signin, name='api_signin'),

	# CONTACT
    path('api/contact', api_contact, name = 'api_contact'), 


	# CART : add, delete
	path('api/cart_add',api_cart_add, name='api_cart_add'),
	path('api/cart_delete',api_cart_delete, name='api_cart_delete'),
	path('api/cart_count',api_cart_count, name='api_cart_count'),
	path('api/validate_coupon',api_validate_coupon, name='api_validate_coupon'),

	# PROFILE
	path('api/profile_edit',api_profile_edit, name='api_profile_edit'),
	path('api/profile_pic_edit',api_profile_pic_edit, name='api_profile_pic_edit'),

	# PASSWORD
	path('api/change_password',api_change_password, name='api_change_password'),
	path('api/forgot_password',api_forgot_password, name='api_forgot_password'),
	path('api/verify_code',api_verify_code, name='api_verify_code'),
	path('api/reset_password',api_reset_password, name='api_reset_password'),

	# CHECKOUT API
    path('config/', stripe_config),  
    path('create-checkout-session/', create_checkout_session), 
    path('api/set_checkout_address', set_checkout_address), 

]