import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from shopping_assistant.sa_retailers import SARetailers
from .models import UserSession, Conversation
from products.models import Product, SARetailer, Category

class AssistantConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.session_id = self.scope['session'].get('session_id', 'unknown')
        self.room_group_name = f'assistant_{self.session_id}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_type = text_data_json.get('type')
        message = text_data_json.get('message')

        if message_type == 'user_input':
            # Save user message
            await self.save_conversation(message, True)
            
            # Process user input and generate AI response
            response = await self.process_user_input(message)
            
            # Save assistant response
            await self.save_conversation(response, False)
            
            # Send response back to WebSocket group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'assistant_message',
                    'message': response
                }
            )

    async def assistant_message(self, event):
        message = event['message']
        
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'assistant_response',
            'message': message
        }))

    @sync_to_async
    def save_conversation(self, message, is_user):
        try:
            session = UserSession.objects.get(session_id=self.session_id)
            Conversation.objects.create(
                session=session,
                message=message,
                is_user=is_user
            )
        except UserSession.DoesNotExist:
            pass

    async def process_user_input(self, user_input):
        # Define user_input_lower at the start of the function
        user_input_lower = user_input.lower()
        
        # SA Retailer specific responses
        if any(word in user_input_lower for word in ['hello', 'hi', 'hey', 'sawubona']):
            return await self.get_sa_greeting()
        
        elif any(word in user_input_lower for word in ['retailer', 'shop', 'store', 'checkers', 'woolworths', 'picknpay', 'spar']):
            return await self.handle_retailer_query(user_input)
        
        elif any(word in user_input_lower for word in ['grocery', 'food', 'buy', 'shop']):
            return await self.handle_grocery_query(user_input)
        
        elif any(word in user_input_lower for word in ['price', 'cost', 'how much', 'rand']):
            return await self.handle_price_query(user_input)
        
        elif any(word in user_input_lower for word in ['delivery', 'deliver', 'collect']):
            return await self.handle_delivery_query()
        
        elif any(word in user_input_lower for word in ['special', 'promo', 'sale']):
            return "I can check for current promotions at SA retailers! Which store would you like to check: Checkers, Woolworths, Pick n Pay, or SPAR?"
        
        elif any(word in user_input_lower for word in ['help', 'support']):
            return await self.get_sa_help_response()
        
        else:
            return "I'm here to help with your grocery shopping in South Africa! I can search products, compare prices across retailers, and help with delivery. What would you like to know?"

    async def get_sa_greeting(self):
        return "Sawubona! 👋 I'm your AI shopping assistant for South African grocery stores. I can help you find products at Checkers, Woolworths, Pick n Pay, and SPAR. How can I assist you today?"

    async def handle_retailer_query(self, user_input):
        user_input_lower = user_input.lower()  # Define here as well
        retailers = await self.get_retailers()
        user_retailer = None
        
        for retailer in retailers:
            if retailer['name'].lower() in user_input_lower:
                user_retailer = retailer
                break
        
        if user_retailer:
            products = await self.get_products_by_retailer(user_retailer['name'])
            if products:
                response = f"Here are some popular products at {user_retailer['name']}:\n"
                for product in products[:3]:
                    response += f"• {product['name']} - R{product['price']}\n"
                response += f"\n{user_retailer['description']}\nDelivery: {user_retailer['delivery_time']}, Min order: R{user_retailer['min_order']}"
                return response
            else:
                return f"I found {user_retailer['name']}: {user_retailer['description']}. What would you like to search for there?"
        else:
            retailer_list = ", ".join([r['name'] for r in retailers])
            return f"I can help you shop at these South African retailers: {retailer_list}. Which store would you like to browse?"

    async def handle_grocery_query(self, user_input):
        user_input_lower = user_input.lower()  # Define here as well
        # Extract product names from user input
        common_products = ['milk', 'bread', 'eggs', 'rice', 'chicken', 'fruit', 'vegetables', 'meat']
        found_products = [p for p in common_products if p in user_input_lower]
        
        if found_products:
            # Search across all retailers for this product
            search_results = []
            for product in found_products[:2]:  # Limit to 2 products
                results = await SARetailers.search_products_online(product)
                search_results.extend(results)
            
            if search_results:
                response = f"I found these options for {', '.join(found_products)}:\n\n"
                for result in search_results[:4]:  # Show top 4 results
                    response += f"🏪 {result['retailer']}: {result['name']} - R{result['price']} ({result['availability']})\n"
                response += "\nWould you like more details about any of these products?"
                return response
            else:
                return f"I couldn't find {', '.join(found_products)} in stock. Would you like to try another product or check a specific retailer?"
        else:
            return "I'd be happy to help you find groceries! What specific product are you looking for? (e.g., milk, bread, chicken, etc.)"

    async def handle_price_query(self, user_input):
        # Extract product name for price comparison
        products = await self.search_products_in_db(user_input)
        if products:
            # Group by product name and show prices across retailers
            product_groups = {}
            for product in products:
                if product['name'] not in product_groups:
                    product_groups[product['name']] = []
                product_groups[product['name']].append(product)
            
            response = "Here are the price comparisons:\n\n"
            for product_name, retailers in list(product_groups.items())[:3]:
                response += f"{product_name}:\n"
                for product in retailers:
                    response += f"  • {product['retailer']}: R{product['price']}\n"
                response += "\n"
            
            response += "Which retailer would you prefer?"
            return response
        else:
            return "I can compare prices across SA retailers! What product would you like to price check?"

    async def handle_delivery_query(self):
        retailers = await self.get_retailers()
        response = "Delivery options at major SA retailers:\n\n"
        for retailer in retailers:
            response += f"• {retailer['name']}: {retailer['delivery_time']} (Min order: R{retailer['min_order']})\n"
        
        response += "\nWhich retailer would you like to order from?"
        return response

    async def get_sa_help_response(self):
        return """I can help you with grocery shopping in South Africa! 🛒

1. **Find Products** - Search across Checkers, Woolworths, Pick n Pay, SPAR
2. **Compare Prices** - See prices for the same product at different retailers  
3. **Delivery Info** - Check delivery times and minimum orders
4. **Retailer Info** - Learn about each store's offerings
5. **Product Availability** - Check stock status

You can ask me things like:
• "Find milk at Checkers"
• "Compare bread prices" 
• "What's the delivery time for Woolworths?"
• "Show me chicken specials"

How can I assist you today?"""

    @sync_to_async
    def get_retailers(self):
        retailers = SARetailer.objects.all()
        return [{
            'id': r.id,
            'name': r.name,
            'description': r.description,
            'delivery_time': r.delivery_time,
            'min_order': float(r.min_order)
        } for r in retailers]

    @sync_to_async
    def get_products_by_retailer(self, retailer_name):
        products = Product.objects.filter(
            retailer__name__iexact=retailer_name,
            in_stock=True
        )[:5]
        return [{
            'id': p.id,
            'name': p.name,
            'price': float(p.price),
            'retailer': p.retailer.name
        } for p in products]

    @sync_to_async
    def search_products_in_db(self, search_term):
        products = Product.objects.filter(
            name__icontains=search_term,
            in_stock=True
        )[:10]
        return [{
            'id': p.id,
            'name': p.name,
            'price': float(p.price),
            'retailer': p.retailer.name,
            'availability': p.availability_text
        } for p in products]