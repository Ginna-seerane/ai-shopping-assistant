from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import uuid
from .models import UserSession
from products.models import Product, SARetailer

def home(request):
    # Get or create session ID
    session_id = request.session.get('session_id')
    if not session_id:
        session_id = str(uuid.uuid4())
        request.session['session_id'] = session_id
        UserSession.objects.get_or_create(session_id=session_id)
    
    return render(request, 'assistant/home.html', {
        'session_id': session_id
    })

@csrf_exempt
def set_user_type(request):
    if request.method == 'POST':
        session_id = request.session.get('session_id')
        user_type = request.POST.get('user_type')
        
        if session_id and user_type:
            try:
                session = UserSession.objects.get(session_id=session_id)
                session.user_type = user_type
                session.save()
                return JsonResponse({'status': 'success'})
            except UserSession.DoesNotExist:
                pass
                
    return JsonResponse({'status': 'error'}, status=400)

@csrf_exempt
def chat_message(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_input = data.get('message', '').lower()
            
            # Simple AI response logic
            if any(word in user_input for word in ['hello', 'hi', 'hey', 'sawubona']):
                response = "Sawubona! 👋 I'm your AI shopping assistant for South African grocery stores. I can help you find products at Checkers, Woolworths, Pick n Pay, and SPAR. How can I assist you today?"
            
            elif any(word in user_input for word in ['milk']):
                response = "🥛 I found milk at these retailers:\n• Checkers: Fresh Milk 2L - R35.99\n• Pick n Pay: Fresh Milk 2L - R33.99\n• Woolworths: Organic Milk - R42.99\nWhich one would you like?"
            
            elif any(word in user_input for word in ['bread']):
                response = "🍞 I found bread at these retailers:\n• Checkers: Brown Bread 700g - R18.50\n• SPAR: Brown Bread 600g - R16.99\n• Woolworths: Artisan Bread - R28.99\nWant to compare prices?"
            
            elif any(word in user_input for word in ['egg', 'eggs']):
                response = "🥚 I found eggs at these retailers:\n• Checkers: Free Range Eggs 12pk - R42.99\n• SPAR: Fresh Eggs Large 12pk - R41.99\n• Woolworths: Organic Eggs - R49.99"
            
            elif any(word in user_input for word in ['retailer', 'store', 'shop']):
                response = "🛒 I work with these South African retailers:\n• Checkers - Fast 60min delivery (Min: R50)\n• Woolworths - Premium quality (Min: R100)\n• Pick n Pay - Affordable prices (Min: R75)\n• SPAR - Neighborhood convenience (Min: R60)"
            
            elif any(word in user_input for word in ['checkers']):
                response = "🛍️ Checkers (Sixty60) - Fast 60-minute delivery!\nPopular products:\n• Milk 2L - R35.99\n• Bread 700g - R18.50\n• Eggs 12pk - R42.99\nMin order: R50"
            
            elif any(word in user_input for word in ['woolworths', 'woolies']):
                response = "🛍️ Woolworths - Premium quality groceries!\nPopular products:\n• Chicken Breast 500g - R89.99\n• Organic Apples 1kg - R45.50\n• Greek Yogurt 500g - R32.99\nMin order: R100"
            
            elif any(word in user_input for word in ['pick n pay', 'pnp']):
                response = "🛍️ Pick n Pay - Affordable groceries!\nPopular products:\n• Coca-Cola 2L - R25.99\n• Tastic Rice 2kg - R52.99\n• Fresh Milk 2L - R33.99\nMin order: R75"
            
            elif any(word in user_input for word in ['spar']):
                response = "🛍️ SPAR - Neighborhood convenience!\nPopular products:\n• Fresh Eggs 12pk - R41.99\n• White Sugar 2kg - R38.50\n• Brown Bread 600g - R16.99\nMin order: R60"
            
            elif any(word in user_input for word in ['price', 'cost', 'how much']):
                response = "💰 I can help you compare prices! Tell me which product you're interested in (like milk, bread, eggs, chicken, rice, etc.)"
            
            elif any(word in user_input for word in ['delivery', 'deliver']):
                response = "🚚 Delivery options:\n• Checkers: 60 minutes (R35 fee)\n• SPAR: 1-2 hours (R30 fee)\n• Pick n Pay: 2-3 hours (R40 fee)\n• Woolworths: 2-4 hours (R45 fee)"
            
            elif any(word in user_input for word in ['help']):
                response = "❓ I can help you with:\n• Finding products (milk, bread, eggs, etc.)\n• Comparing prices across retailers\n• Checking delivery options\n• Learning about each store\n• Product availability\n\nWhat would you like to do?"
            
            else:
                response = "I'm here to help with your grocery shopping in South Africa! 🛒 Try asking about:\n• Specific products (milk, bread, eggs)\n• Retailers (Checkers, Woolworths, etc.)\n• Price comparisons\n• Delivery information"
            
            return JsonResponse({'response': response})
            
        except Exception as e:
            return JsonResponse({'error': 'Server error'}, status=500)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)