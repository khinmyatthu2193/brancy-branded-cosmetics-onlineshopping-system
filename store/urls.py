from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.home, name = 'home'),
    path('accsetting/', views.accsetting, name='accsetting'),
    path('brandcover/', views.brandcover , name='brandcover'),
    path('b_brandcover/', views.b_brandcover , name='b_brandcover'),
    path('shoppage/check/', views.check, name='check'),
    path('brandshoppage/check/', views.check, name='check'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('shoppage/', views.shoppage, name='shoppage'),
    path('account/brand/<str:brand_name>/', views.brandshoppage, name='brandshoppage'),
    path('search/',views.search, name = 'search'),
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('update_user/', views.update_user, name='update_user'),
    path('account/productDetail/<int:product_id>/', views.productDetail, name='productDetail'),
    path('aboutus/', views.aboutus, name = 'aboutus'),
    path('blogpost/', views.blogpost, name = 'blogpost'),
    path('product_filter_shop/', views.product_filter_shop, name = 'product_filter_shop'),
    path('product_filter_brand/', views.product_filter_brand, name = 'product_filter_brand'),
    path('category/<int:category_id>/', views.product_list_by_category, name='product_list_by_category'),
    path('subcategory/<int:subcategory_id>/', views.product_list_by_subcategory, name='product_list_by_subcategory'),
    path('create-order/', views.create_order, name='create_order'),
    path('place_order/',views.place_order, name = 'place_order'),
    path('account/order-confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
    path('save_cart_item/', views.save_cart_item, name='save_cart_item'),
    path('save_wishlist_item/', views.save_wishlist_item, name='save_wishlist_item'),
    path('get_user_cart/', views.get_user_cart, name='get_user_cart'),
    path('get_user_wishlist/', views.get_user_wishlist, name='get_user_wishlist'),
    path('save_cart_to_profile/', views.save_cart_to_profile, name='save_cart_to_profile'),
    path('save_wishlist_to_profile/', views.save_wishlist_to_profile, name='save_wishlist_to_profile'),
    path('order-success/', views.order_success, name='order_success'),
    path('order-history/', views.order_history, name='order_history'),
    path('account/order-history/', views.order_history, name='order_history'),
    path('brand/<str:brand_name>/', views.brandshoppage, name='brandshoppage'),
    path('shoppage/category/<str:category_name>/', views.product_filter_shop, name='product_filter_shop'),
    path('skin_quiz/', views.skin_quiz, name='skin_quiz'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)