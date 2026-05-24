#!/bin/bash
# Baker Street Laboratory - Payment System Deployment

echo "💰 Baker Street Laboratory - Payment System Deployment"
echo "====================================================="

# Create and activate temporary virtual environment
echo "📦 Creating virtual environment for payment processing..."
python3 -m venv /tmp/payment_venv
source /tmp/payment_venv/bin/activate

# Install required packages
echo "📦 Installing payment processing packages..."
pip install stripe paypalrestsdk web3 eth-account

# Test Stripe integration
echo "🧪 Testing Stripe integration..."
python3 -c "
import stripe
import os
stripe.api_key = os.getenv('STRIPE_SECRET_KEY', '')
if stripe.api_key:
    print('✅ Stripe API key configured')
    try:
        balance = stripe.Balance.retrieve()
        print('✅ Stripe connection successful')
    except Exception as e:
        print(f'⚠️ Stripe connection issue: {e}')
else:
    print('❌ Stripe API key not configured')
"

# Test PayPal integration
echo "🧪 Testing PayPal integration..."
python3 -c "
import paypalrestsdk
import os
paypalrestsdk.configure({
    'mode': 'sandbox' if os.getenv('PAYPAL_SANDBOX', 'true') == 'true' else 'live',
    'client_id': os.getenv('PAYPAL_CLIENT_ID', ''),
    'client_secret': os.getenv('PAYPAL_CLIENT_SECRET', '')
})
if paypalrestsdk.api.default().client_id:
    print('✅ PayPal API configured')
else:
    print('❌ PayPal API not configured')
"

# Test MetaMask integration
echo "🧪 Testing MetaMask integration..."
python3 -c "
from web3 import Web3
import os
private_key = os.getenv('METAMASK_PRIVATE_KEY', '')
if private_key:
    try:
        w3 = Web3(Web3.HTTPProvider('https://polygon-rpc.com'))
        account = w3.eth.account.from_key(private_key)
        print(f'✅ MetaMask account: {account.address}')
    except Exception as e:
        print(f'⚠️ MetaMask integration issue: {e}')
else:
    print('❌ MetaMask private key not configured')
"

# Clean up
deactivate
rm -rf /tmp/payment_venv

echo "🚀 Payment systems deployment complete!"
