from django.core.management.base import BaseCommand
from products.models import SARetailer, Category, Product

class Command(BaseCommand):
    help = 'Populate South African retailers and sample products'

    def handle(self, *args, **options):
        # Clear existing data
        Product.objects.all().delete()
        SARetailer.objects.all().delete()
        Category.objects.all().delete()
        
        # Create retailers
        checkers = SARetailer.objects.create(
            name='Checkers',
            description='Checkers Sixty60 - Fast grocery delivery',
            delivery_time='60 minutes',
            min_order=50.00,
            website='https://www.checkers.co.za'
        )
        
        woolworths = SARetailer.objects.create(
            name='Woolworths',
            description='Premium quality food and groceries',
            delivery_time='2-4 hours',
            min_order=100.00,
            website='https://www.woolworths.co.za'
        )
        
        picknpay = SARetailer.objects.create(
            name='Pick n Pay',
            description='Affordable groceries and household items',
            delivery_time='2-3 hours',
            min_order=75.00,
            website='https://www.pnp.co.za'
        )
        
        spar = SARetailer.objects.create(
            name='SPAR',
            description='Neighborhood convenience store',
            delivery_time='1-2 hours',
            min_order=60.00,
            website='https://www.spar.co.za'
        )
        
        # Create categories
        dairy = Category.objects.create(name='Dairy')
        bakery = Category.objects.create(name='Bakery')
        meat = Category.objects.create(name='Meat')
        beverages = Category.objects.create(name='Beverages')
        pantry = Category.objects.create(name='Pantry')
        
        # Create products
        products_data = [
            # Checkers
            {'name': 'Fresh Milk 2L', 'price': 35.99, 'category': dairy, 'retailer': checkers, 'stock_quantity': 50},
            {'name': 'Brown Bread 700g', 'price': 18.50, 'category': bakery, 'retailer': checkers, 'stock_quantity': 30},
            
            # Woolworths
            {'name': 'Chicken Breast 500g', 'price': 89.99, 'category': meat, 'retailer': woolworths, 'stock_quantity': 20},
            {'name': 'Organic Apples 1kg', 'price': 45.50, 'category': pantry, 'retailer': woolworths, 'stock_quantity': 40},
            
            # Pick n Pay
            {'name': 'Coca-Cola 2L', 'price': 25.99, 'category': beverages, 'retailer': picknpay, 'stock_quantity': 60},
            {'name': 'Tastic Rice 2kg', 'price': 52.99, 'category': pantry, 'retailer': picknpay, 'stock_quantity': 25},
            
            # SPAR
            {'name': 'Fresh Eggs 12pk', 'price': 42.99, 'category': dairy, 'retailer': spar, 'stock_quantity': 35},
            {'name': 'White Sugar 2kg', 'price': 38.50, 'category': pantry, 'retailer': spar, 'stock_quantity': 45},
        ]
        
        for product_data in products_data:
            Product.objects.create(
                name=product_data['name'],
                description=f"Quality {product_data['name']}",
                price=product_data['price'],
                category=product_data['category'],
                retailer=product_data['retailer'],
                stock_quantity=product_data['stock_quantity'],
                brand=product_data['retailer'].name
            )
        
        self.stdout.write(
            self.style.SUCCESS('Successfully created SA retailers and products!')
        )