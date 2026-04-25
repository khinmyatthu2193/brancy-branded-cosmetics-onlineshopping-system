from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Category, Brand, Order, OrderItem, SubCategory
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from .forms import UserRegistrationForm
from .forms import UpdateForm # KMT for login
from django.shortcuts import render, redirect
from itertools import chain
from django.contrib.auth import update_session_auth_hash # KMT for login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.contrib import messages

def custom_login_view(request):
    if request.method == "POST" and request.is_ajax():
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return JsonResponse({"status": "success"})  # Login successful
        else:
            # Return an error message as JSON
            errors = {"login": "Invalid username or password"}
            return JsonResponse({"status": "error", "errors": errors})

    return JsonResponse({"status": "error", "errors": {"general": "Invalid request"}})


def home(request):
    # List of specific product IDs you want to display
    product_ids = [ 74, 35, 67, 65]  # Replace these with the actual IDs of the products you want to show
    products = Product.objects.filter(id__in=product_ids)  # Filter products by the specified IDs

    return render(request, 'home.html', {'products': products})

def register_user(request):
    if request.method == 'POST':
        form = UpdateForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Save user but don't commit to DB yet
            
            # Set the password using set_password() to hash it
            user.set_password(form.cleaned_data['password'])
            
            # Save first name and last name manually as they are not in the User model fields by default
            user.first_name = form.cleaned_data['firstname']
            user.last_name = form.cleaned_data['lastname']
            
            user.save()  # Now save the user to the database
            
            # Success message and redirect
            messages.success(request, 'Registration successful.')
            return redirect('login')
        else:
            # If form is invalid, render the form again with errors
            return render(request, 'register.html', {'form': form})
    else:
        form = UserRegistrationForm()  # Provide an empty form for GET requests
    
    return render(request, 'register.html', {'form': form})
def accsetting(request):
    orders = Order.objects.filter(customer=request.user) if request.user.is_authenticated else None
    return render(request, 'accsetting.html', {'orders': orders})


def brandcover(request):
    return render (request, 'brandcover.html',{  })
def b_brandcover(request):
    return render (request, 'b_brandcover.html',{  })

from django.template.loader import render_to_string
def skin_quiz(request):
    if request.method == 'POST':
        # Calculate the user's skin type based on the quiz
        total_score = int(request.POST.get('total_score', 0))
        skin_type = determine_skin_type(total_score)  # Determine the skin type
        recommended_products = Product.objects.filter(skin_type=skin_type)  # Fetch products for the skin type

        # Render the recommendations as HTML
        recommendations_html = render_to_string('recommendations_partial.html', {
            'recommended_products': recommended_products,
        })
        return JsonResponse({
            'recommendations_html': recommendations_html,
        })

    # For GET requests, just render the quiz page
    return render(request, 'skin_quiz.html')

from .models import SkinType

def determine_skin_type(total_score):
    if total_score <= 9:
        return SkinType.objects.filter(name="Normal").first()
    elif total_score <= 13:
        return SkinType.objects.filter(name="Combination").first()
    elif total_score <= 16:
        return SkinType.objects.filter(name="Dry").first()
    elif total_score <= 19:
        return SkinType.objects.filter(name="Oily").first()
    else:
        return SkinType.objects.filter(name="All Skin Type").first()


def order_success(request):
    order_id = request.GET.get('order_id')
    if not order_id:
        return render(request, 'error_page.html', {'error': 'Order ID not provided.'})
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'order_success.html', {'order': order})

from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import Profile
import json

def login_user(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
            user = authenticate(request, username=user.username, password=password)
        except User.DoesNotExist:
            user = None

        if user is not None:
            login(request, user)

            # Ensure the user has a profile
            profile, created = Profile.objects.get_or_create(user=user)

            # Load cart data from Profile.old_cart if available
            cart_data = json.loads(profile.old_cart) if profile.old_cart else []
            wishlist_data = json.loads(profile.old_wishlist) if profile.old_wishlist else []
            print("Cart Data from Profile:", cart_data)  # Log cart data for debugging
            print("Wishlist Data from Profile:", wishlist_data)

            messages.success(request, 'Login successful.')
            return JsonResponse({"status": "success", "cart": cart_data, "wishlist": wishlist_data})

        else:
            messages.error(request, "Invalid email or password. Please try again.")
            return JsonResponse({"status": "error", "message": "Invalid email or password."})

    return render(request, 'login.html')


       
def logout_user(request):
    # Clear cart and wishlist from session data if needed
    if 'cart' in request.session:
        del request.session['cart']
    if 'wishlist' in request.session:
        del request.session['wishlist']
    
    logout(request)
    messages.success(request, "You have been logged out!")
    
    # Redirect with a flag to trigger localStorage clear
    response = redirect('home')
    response.set_cookie('clearLocalStorage', 'true')
    return response


def check(request):
    return render (request, 'check.html',{  })

def wishlist(request):
    return render (request, 'wishlist.html',{  })

def productDetail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render (request, 'productDetail.html', {'product': product})

def aboutus(request):
    return render(request, 'aboutus.html', { })

def blogpost(request):
    return render(request, 'blogpost.html', { })

def shoppage(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    # Setting up pagination
    paginator = Paginator(products, 5000)  # Show 20 products per page
    page_number = request.GET.get('page')  # Get the page number from the URL query parameters
    page_obj = paginator.get_page(page_number)  # Get the specific page of products
    # Render the template with the page object
    combined_items = list(chain(products))
    return render(request, 'shoppage.html', {'combined_items': combined_items, 'page_obj':page_obj, 'categories': categories})
def brandshoppage(request, brand_name):
    # Retrieve the brand object by name
    brand = get_object_or_404(Brand, name=brand_name)
    # Retrieve products for the specified brand
    products = Product.objects.filter(brand=brand)
    
    return render(request, 'brandshoppage.html', {
        'products': products,
        'brand': brand,  # Pass the brand to the template
    })

def search(request):
    if request.method == "POST":
        searched = request.POST.get('searched', '')
        if searched:
            results = Product.objects.filter(name__icontains=searched)
            return render(request, 'shoppage.html', {'searched': searched, 'results': results})
        else:
            return render(request, 'shoppage.html', {'error': 'No search term entered'})
    return render(request, 'shoppage.html', {'searched': None, 'results': None})

from django.db.models import Q

def product_filter_shop(request):
    sort_by = request.GET.get('sort', 'default')
    selected_categories = request.GET.getlist('category')  # Get selected categories from query parameters
    products = Product.objects.all()
    
    # Apply filtering by category
    if selected_categories:
        products = products.filter(category__name__in=selected_categories)

    # Sorting logic
    if sort_by == 'name-asc':
        products = products.order_by('name')
    elif sort_by == 'name-desc':
        products = products.order_by('-name')
    elif sort_by == 'price-asc':
        products = products.order_by('price')
    elif sort_by == 'price-desc':
        products = products.order_by('-price')

    categories = Category.objects.all()  # Fetch all categories
    brands = Brand.objects.all()  # Fetch all brands

    context = {
        'products': products,
        'categories': categories,
        'brands': brands,
        'sort_by': sort_by,
    }
    return render(request, 'shoppage.html', context)

def product_filter_brand(request):
    sort_by = request.GET.get('sort', 'default')
    selected_brands = request.GET.getlist('brand')  # Get selected categories from query parameters
    print(f"Selected brands: {selected_brands}")
    products = Product.objects.all()
    if selected_brands:
        products = products.filter(
            Q(category__name__in=selected_brands) | Q(brand__name__in=selected_brands)
        )
    if sort_by == 'name-asc':
        products = products.order_by('name')
    elif sort_by == 'name-desc':
        products = products.order_by('-name')
    elif sort_by == 'price-asc':
        products = products.order_by('price')
    elif sort_by == 'price-desc':
        products = products.order_by('-price')

    context = {
        'products': products,
    }
    return render(request, 'brandshoppage.html', context)

def product_list_by_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    brands = Brand.objects.all()  # Fetch all brands
    products = Product.objects.filter(category=category)
    categories = Category.objects.all()  # Fetch all categories for side navigation
    
    return render(request, 'shoppage.html', {
        'products': products,
        'brands': brands,
        'categories': categories,  # Use 'categories' instead of 'subcategories'
        'active_category': category,  # This variable name is more appropriate
    })

def product_list_by_subcategory(request, subcategory_id):  # Fixed parameter name
    subcategory = get_object_or_404(SubCategory, id=subcategory_id)
    brands = Brand.objects.all()  # Fetch all brands
    products = Product.objects.filter(subCategory=subcategory)  # Use 'subCategory' instead of 'subcategory'
    categories = Category.objects.all()  # Fetch all categories for side navigation

    return render(request, 'shoppage.html', {
        'products': products,
        'brands': brands,
        'categories': categories,  # Use 'categories' instead of 'subcategories'
        'active_subcategory': subcategory,
    })

######################### K M T for Login Logout #########################
def update_user(request):
    # Check if the user is authenticated
    if request.user.is_authenticated:
        if request.method == 'POST':
            user_form = UpdateForm(request.POST, instance=request.user)  # Use the logged-in user instance
            if user_form.is_valid():
                user = user_form.save(commit=False)  # Save but don't commit yet

                # Handle password update: only change if a new password is provided
                new_password = user_form.cleaned_data.get('password')
                if new_password:  # If there's a new password
                    user.set_password(new_password)  # Hash and set the new password

                # Update other fields (e.g., first name, last name)
                user.first_name = user_form.cleaned_data['firstname']
                user.last_name = user_form.cleaned_data['lastname']

                user.save()  # Now save the updated user to the database

                # Keep the user logged in after changing the password
                update_session_auth_hash(request, user)

                # Success message and redirect
                messages.success(request, 'Your profile has been updated successfully.')
                return redirect('accsetting')  # Redirect to profile or another page
            else:
                # If form is invalid, display errors
                messages.error(request, 'There was an error in the form. Please correct the errors below.')
        else:
            # Pre-fill the form with current user's data
            user_form = UpdateForm(instance=request.user)

        return render(request, 'update_user.html', {'form': user_form})
    else:
        # If the user is not authenticated, redirect to login with a message
        messages.warning(request, 'You need to log in to update your profile.')
        return redirect('login')  # Redirect to the login page
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Cart, Wishlist, Product
import json

# Save a cart item
@require_POST
@login_required
def save_cart_item(request):
    data = json.loads(request.body)
    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)

    product = Product.objects.get(id=product_id)
    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
    cart_item.quantity = quantity
    cart_item.save()
    return JsonResponse({'status': 'success'})

# Save a wishlist item
@require_POST
@login_required
def save_wishlist_item(request):
    data = json.loads(request.body)
    product_id = data.get('product_id')

    product = Product.objects.get(id=product_id)
    Wishlist.objects.get_or_create(user=request.user, product=product)
    return JsonResponse({'status': 'success'})

# Retrieve the user's cart items on login
@login_required
def get_user_cart(request):
    cart_items = Cart.objects.filter(user=request.user).select_related('product')
    data = [{
        'id': item.product.id,
        'title': item.product.name,
        'price': float(item.product.get_price()),
        'mainImage': item.product.main_image.url,
        'quantity': item.quantity
    } for item in cart_items]
    return JsonResponse(data, safe=False)

# Retrieve the user's wishlist items on login
@login_required
def get_user_wishlist(request):
    wishlist_items = Wishlist.objects.filter(user=request.user).select_related('product')
    data = [{
        'id': item.product.id,
        'title': item.product.name,
        'mainImage': item.product.main_image.url,
    } for item in wishlist_items]
    return JsonResponse(data, safe=False)



@require_POST
@login_required
def save_cart_to_profile(request):
    data = json.loads(request.body)
    cart_data = data.get("cart", [])

    # Overwrite the old cart data
    profile = request.user.profile
    profile.old_cart = json.dumps(cart_data)
    profile.save()

    return JsonResponse({"status": "success"})

@require_POST
@login_required
def save_wishlist_to_profile(request):
    data = json.loads(request.body)
    wishlist_data = data.get("wishlist", [])

    # Overwrite the old wishlist data
    profile = request.user.profile
    profile.old_wishlist = json.dumps(wishlist_data)
    profile.save()

    return JsonResponse({"status": "success"})




######################### K M T for Login Logout #########################
from django.db import transaction
import logging
logger = logging.getLogger(__name__)

@login_required
def place_order(request):
    if request.method == 'POST':
        try:
            with transaction.atomic():
                # Retrieve customer details from form
                country = request.POST.get('country')
                first_name = request.POST.get('first_name')
                last_name = request.POST.get('last_name')
                customer_address = request.POST.get('customer_address')
                customer_city = request.POST.get('customer_city')
                customer_phone = request.POST.get('customer_phone')

                # Validate required fields
                if not all([country, first_name, last_name, customer_address, customer_city, customer_phone]):
                    messages.error(request, 'All fields are required.')
                    return redirect('place_order')

                # Calculate order totals
                subtotal = calculate_subtotal(request)
                shipping_fee = calculate_shipping_fee(request)
                total = subtotal + shipping_fee

                # Create Order instance
                order = Order.objects.create(
                    customer=request.user,
                    customer_name=f"{first_name} {last_name}",
                    customer_address=customer_address,
                    customer_city=customer_city,
                    customer_phone=customer_phone,
                    subtotal=subtotal,
                    shipping_fee=shipping_fee,
                    total=total
                )
                #messages.success(request, f"Order placed successfully! Your order ID is: {order.id}")
                return redirect('order_confirmation', order_id=order.id)
        except Exception as e:
            logger.error("Error in place_order: %s", str(e))
            messages.error(request, 'An error occurred while placing the order. Please try again.')
            return redirect('place_order')
    else:
        # Render the order form page for GET requests
        return render(request, 'error_page.html')
    
def calculate_subtotal(request):
    # Assuming `cart_items(request)` provides a list of cart items, each with `quantity` and `price`
    subtotal = 0
    for item in cart_item(request):  # Replace with your cart items retrieval logic
        subtotal += item.quantity * item.price
    return subtotal

def calculate_shipping_fee(request):
    flat_shipping_fee = 5.00  # For example, $5 flat rate
    subtotal = calculate_subtotal(request)
    if subtotal > 50:  # Free shipping for orders over $50
        return 0
    else:
        return flat_shipping_fee

def cart_item(request):
    # Retrieve cart data from the session, defaulting to an empty dictionary if not present
    cart = request.session.get('cart', [])

    # Structure each cart item to match the expected format in the view
    cart_items = []
    for item in cart:
        cart_items.append({
            'product_id': item['id'],
            'product_name': item['name'],
            'quantity': item['quantity'],
            'price': item['price']
        })

    return cart_items

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
import json

@csrf_exempt  # Only if CSRF token is managed separately; remove for production
@login_required
def create_order(request):
    if request.method == "POST":
        data = json.loads(request.body)
        cart = data.get("cart", [])
        total_amount = 0


        # Create a new Order instance
        order = Order.objects.create(customer=request.user)

        for item in cart:
            product_id = item.get("id")
            quantity = item.get("quantity")
            item_type = item.get("type", "Product")  # Default to "Product" if "type" is missing

            product = None
            price = 0

            # Check the type to query Product or BestSeller
            try:
                if item_type == "Product":
                    product = Product.objects.get(id=product_id)
                price = product.price
            except (Product.DoesNotExist):
                print(f"Item with id {product_id} not found in {item_type}.")
                continue

            # Create OrderItem with the found product
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=price
            )
            total_amount += price * quantity

        order.total_amount = total_amount
        order.save()

        return JsonResponse({"status": "success", "order_id": order.id})

    return JsonResponse({"status": "failed", "message": "Invalid request method"}, status=400)

def order_confirmation(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        # Provide a custom error message
        messages.error(request, "Order not found.")
        return redirect('place_order')  # Redirect to an appropriate page
    return render(request, 'order_success.html', {'order': order})

# def order_history(request):
#     orders = Order.objects.filter(customer=request.user)
#     print("Orders fetched for user:", orders)  # Debugging print statement
#     return render(request, 'accsetting.html', {'orders': orders})

from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

@login_required
def order_history(request):
    # Get all orders for the logged-in user, ordered by creation date
    orders = Order.objects.filter(customer=request.user).order_by('-created_at')

    # Get every other order (i.e., orders with even indices)
    every_other_order = orders[::2]  # Slicing to get every other order

    # Create a paginator with the modified queryset
    paginator = Paginator(every_other_order, 10)  # Show 10 orders per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'order_history.html', {'page_obj': page_obj})

from django.shortcuts import render
from .models import Product  # Adjust according to your models

def product_filter_shop(request, category_name):
    # Fetch products belonging to the selected category
    products = Product.objects.filter(category__name=category_name)

    # Pass the category name to the template context
    context = {
        'products': products,
        'category_name': category_name,
    }
    
    return render(request, 'shoppage.html', context)


