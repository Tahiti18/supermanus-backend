import os
import stripe
from flask import Blueprint, request, jsonify

# Initialize Stripe
stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')

payments_bp = Blueprint('payments', __name__)

# Define pricing tiers with correct Stripe price IDs
PRICING_TIERS = {
    'free': {
        'price': 0,
        'stripe_price_id': None,  # Free tier doesn't need Stripe
        'credits': 1000,
        'name': 'Free Plan'
    },
    'basic': {
        'price': 1900,  # $19.00 in cents
        'stripe_price_id': os.environ.get('STRIPE_BASIC_PRICE_ID', 'price_basic_monthly'),
        'credits': 5000,
        'name': 'Basic Plan'
    },
    'professional': {
        'price': 9900,  # $99.00 in cents
        'stripe_price_id': os.environ.get('STRIPE_PRO_PRICE_ID', 'price_pro_monthly'),
        'credits': 25000,
        'name': 'Professional Plan'
    },
    'expert': {
        'price': 49900,  # $499.00 in cents
        'stripe_price_id': os.environ.get('STRIPE_EXPERT_PRICE_ID', 'price_expert_monthly'),
        'credits': 100000,
        'name': 'Expert Plan'
    }
}

@payments_bp.route('/payments/create-checkout', methods=['POST'])
def create_checkout_session():
    """Create a Stripe checkout session for the selected plan"""
    try:
        data = request.get_json()
        plan_id = data.get('plan_id')
        email = data.get('email', 'user@example.com')
        
        if not plan_id or plan_id not in PRICING_TIERS:
            return jsonify({'error': 'Invalid plan ID'}), 400
        
        plan = PRICING_TIERS[plan_id]
        
        # Handle free plan
        if plan_id == 'free':
            return jsonify({
                'message': 'Free plan activated',
                'plan': plan['name'],
                'credits': plan['credits']
            })
        
        # Create Stripe checkout session for paid plans
        if not stripe.api_key:
            return jsonify({'error': 'Stripe not configured'}), 500
        
        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': plan['name']
                        },
                        'unit_amount': plan['price'],
                        'recurring': {
                            'interval': 'month'
                        }
                    },
                    'quantity': 1,
                }],
                mode='subscription',
                success_url=os.environ.get('FRONTEND_URL', 'https://thepromptlink.com') + '/success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=os.environ.get('FRONTEND_URL', 'https://thepromptlink.com') + '/cancel',
                customer_email=email,
                metadata={
                    'plan_id': plan_id,
                    'plan_name': plan['name'],
                    'credits': plan['credits']
                }
            )
            
            return jsonify({
                'checkout_url': checkout_session.url,
                'session_id': checkout_session.id,
                'plan': plan['name'],
                'price': plan['price'] / 100  # Convert cents to dollars for display
            })
            
        except stripe.error.StripeError as e:
            return jsonify({'error': f'Stripe error: {str(e)}'}), 500
            
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@payments_bp.route('/payments/webhook', methods=['POST'])
def stripe_webhook():
    """Handle Stripe webhook events"""
    payload = request.get_data()
    sig_header = request.headers.get('Stripe-Signature')
    endpoint_secret = os.environ.get('STRIPE_WEBHOOK_SECRET')
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError:
        return jsonify({'error': 'Invalid payload'}), 400
    except stripe.error.SignatureVerificationError:
        return jsonify({'error': 'Invalid signature'}), 400
    
    # Handle the event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        # Handle successful payment
        # TODO: Update user credits and subscription status in database
        print(f"Payment successful for session: {session['id']}")
        
    elif event['type'] == 'invoice.payment_succeeded':
        invoice = event['data']['object']
        # Handle recurring payment
        print(f"Recurring payment successful: {invoice['id']}")
        
    elif event['type'] == 'customer.subscription.deleted':
        subscription = event['data']['object']
        # Handle subscription cancellation
        print(f"Subscription cancelled: {subscription['id']}")
    
    return jsonify({'status': 'success'})

@payments_bp.route('/payments/plans', methods=['GET'])
def get_pricing_plans():
    """Get all available pricing plans"""
    return jsonify({
        'plans': PRICING_TIERS
    })
