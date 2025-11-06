"""
South African Retailers Integration
Simplified version without external dependencies for development
"""

class SARetailers:
    """
    Integration with South African grocery retailers
    Using mock data for development
    """
    
    @staticmethod
    async def search_products_online(product_name, retailer=None):
        """
        Search products across major SA retailers - Mock data version
        """
        # Mock data for all SA retailers
        all_products = [
            # Checkers products
            {
                'name': 'Fresh Milk 2L',
                'price': 35.99,
                'retailer': 'Checkers',
                'brand': 'Checkers Fresh',
                'category': 'Dairy',
                'availability': 'In Stock',
            },
            {
                'name': 'Brown Bread 700g',
                'price': 18.50,
                'retailer': 'Checkers',
                'brand': 'Blue Ribbon',
                'category': 'Bakery',
                'availability': 'In Stock',
            },
            {
                'name': 'Free Range Eggs 12pk',
                'price': 42.99,
                'retailer': 'Checkers',
                'brand': 'Checkers',
                'category': 'Dairy',
                'availability': 'In Stock',
            },
            
            # Woolworths products
            {
                'name': 'Free Range Chicken Breast 500g',
                'price': 89.99,
                'retailer': 'Woolworths',
                'brand': 'Woolworths',
                'category': 'Meat & Poultry',
                'availability': 'In Stock',
            },
            {
                'name': 'Organic Apples 1kg',
                'price': 45.50,
                'retailer': 'Woolworths',
                'brand': 'Woolworths Organic',
                'category': 'Fruits & Vegetables',
                'availability': 'In Stock',
            },
            {
                'name': 'Artisan Bread',
                'price': 28.99,
                'retailer': 'Woolworths',
                'brand': 'Woolworths Bakery',
                'category': 'Bakery',
                'availability': 'In Stock',
            },
            
            # Pick n Pay products
            {
                'name': 'Coca-Cola 2L',
                'price': 25.99,
                'retailer': 'Pick n Pay',
                'brand': 'Coca-Cola',
                'category': 'Beverages',
                'availability': 'In Stock',
            },
            {
                'name': 'Tastic Rice 2kg',
                'price': 52.99,
                'retailer': 'Pick n Pay',
                'brand': 'Tastic',
                'category': 'Pantry',
                'availability': 'In Stock',
            },
            {
                'name': 'Fresh Milk 2L',
                'price': 33.99,
                'retailer': 'Pick n Pay',
                'brand': 'Pick n Pay',
                'category': 'Dairy',
                'availability': 'In Stock',
            },
            
            # SPAR products
            {
                'name': 'Fresh Eggs Large 12 pack',
                'price': 41.99,
                'retailer': 'SPAR',
                'brand': 'SPAR',
                'category': 'Dairy',
                'availability': 'In Stock',
            },
            {
                'name': 'White Sugar 2kg',
                'price': 38.50,
                'retailer': 'SPAR',
                'brand': 'SPAR',
                'category': 'Pantry',
                'availability': 'In Stock',
            },
            {
                'name': 'Brown Bread 600g',
                'price': 16.99,
                'retailer': 'SPAR',
                'brand': 'SPAR Bakery',
                'category': 'Bakery',
                'availability': 'In Stock',
            }
        ]
        
        # Filter by retailer if specified
        if retailer:
            filtered_products = [p for p in all_products if p['retailer'].lower() == retailer.lower()]
        else:
            filtered_products = all_products
        
        # Filter by product name search
        search_results = [p for p in filtered_products if product_name.lower() in p['name'].lower()]
        
        # If no direct matches, return some related products
        if not search_results and not retailer:
            # Return products from the same category
            related_terms = {
                'milk': 'dairy',
                'bread': 'bakery', 
                'eggs': 'dairy',
                'chicken': 'meat',
                'rice': 'pantry',
                'fruit': 'fruits',
                'vegetable': 'fruits'
            }
            
            for term, category in related_terms.items():
                if term in product_name.lower():
                    search_results = [p for p in all_products if p['category'].lower() == category]
                    break
        
        return search_results[:6]  # Return max 6 results
    
    @staticmethod
    def get_retailer_info():
        """
        Get information about available retailers
        """
        return [
            {
                'name': 'Checkers',
                'description': 'Checkers Sixty60 - Fast grocery delivery',
                'delivery_time': '60 minutes',
                'min_order': 50.00,
                'delivery_fee': 35.00
            },
            {
                'name': 'Woolworths',
                'description': 'Premium quality groceries and food',
                'delivery_time': '2-4 hours',
                'min_order': 100.00,
                'delivery_fee': 45.00
            },
            {
                'name': 'Pick n Pay',
                'description': 'Affordable groceries and household items',
                'delivery_time': '2-3 hours',
                'min_order': 75.00,
                'delivery_fee': 40.00
            },
            {
                'name': 'SPAR',
                'description': 'Neighborhood convenience store',
                'delivery_time': '1-2 hours',
                'min_order': 60.00,
                'delivery_fee': 30.00
            }
        ]
    
    @staticmethod
    async def get_current_specials(retailer=None):
        """
        Get current specials and promotions
        """
        specials = [
            {
                'retailer': 'Checkers',
                'product': 'Fresh Milk 2L',
                'original_price': 35.99,
                'special_price': 29.99,
                'valid_until': '2024-12-31'
            },
            {
                'retailer': 'Woolworths',
                'product': 'Free Range Chicken Breast 500g',
                'original_price': 89.99,
                'special_price': 79.99,
                'valid_until': '2024-12-25'
            },
            {
                'retailer': 'Pick n Pay',
                'product': 'Coca-Cola 2L',
                'original_price': 25.99,
                'special_price': 19.99,
                'valid_until': '2024-12-28'
            },
            {
                'retailer': 'SPAR',
                'product': 'Brown Bread 600g',
                'original_price': 16.99,
                'special_price': 12.99,
                'valid_until': '2024-12-26'
            }
        ]
        
        if retailer:
            return [s for s in specials if s['retailer'].lower() == retailer.lower()]
        return specials