from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Product, SARetailer, Category
from shopping_assistant.sa_retailers import SARetailers

def get_retailers(request):
    retailers = SARetailer.objects.all()
    retailers_data = []
    
    for retailer in retailers:
        retailers_data.append({
            'id': retailer.id,
            'name': retailer.name,
            'description': retailer.description,
            'delivery_time': retailer.delivery_time,
            'min_order': float(retailer.min_order),
            'website': retailer.website
        })
    
    return JsonResponse({'retailers': retailers_data})

@csrf_exempt
def search_products(request):
    search_term = request.GET.get('search', '')
    retailer = request.GET.get('retailer', '')
    
    if search_term:
        # Search in database first
        products = Product.objects.filter(
            name__icontains=search_term,
            in_stock=True
        )
        
        if retailer:
            products = products.filter(retailer__name__iexact=retailer)
        
        products_data = []
        for product in products:
            products_data.append({
                'id': product.id,
                'name': product.name,
                'description': product.description,
                'price': float(product.price),
                'retailer': product.retailer.name,
                'category': product.category.name,
                'availability': product.availability_text,
                'delivery_info': product.delivery_info,
                'brand': product.brand,
                'image_url': product.image.url if product.image else '/static/images/default_product.jpg'
            })
        
        return JsonResponse({'products': products_data})
    
    return JsonResponse({'products': []})

@csrf_exempt
def compare_prices(request, product_name):
    """
    Compare prices for a product across all retailers
    """
    products = Product.objects.filter(
        name__icontains=product_name,
        in_stock=True
    ).select_related('retailer')
    
    comparison_data = []
    for product in products:
        comparison_data.append({
            'retailer': product.retailer.name,
            'product_name': product.name,
            'price': float(product.price),
            'availability': product.availability_text,
            'delivery': product.retailer.delivery_time
        })
    
    # Sort by price (lowest first)
    comparison_data.sort(key=lambda x: x['price'])
    
    return JsonResponse({'comparison': comparison_data})