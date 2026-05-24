#!/bin/bash
# Baker Street Laboratory - API Key Setup Automation

echo "🚀 Baker Street Laboratory - API Key Setup Automation"
echo "=================================================="

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file..."
    cp env_template.txt .env
    echo "✅ .env file created from template"
else
    echo "✅ .env file already exists"
fi

echo ""
echo "🔑 API Key Setup Instructions:"
echo "=============================="
echo ""
echo "1. STRIPE API SETUP:"
echo "   - Go to: https://dashboard.stripe.com/apikeys"
echo "   - Copy your Secret Key and Public Key"
echo "   - Update .env file with:"
echo "     STRIPE_SECRET_KEY=sk_live_your_key_here"
echo "     STRIPE_PUBLIC_KEY=pk_live_your_key_here"
echo ""
echo "2. PAYPAL API SETUP:"
echo "   - Go to: https://developer.paypal.com/developer/applications/"
echo "   - Create new application"
echo "   - Copy Client ID and Secret"
echo "   - Update .env file with:"
echo "     PAYPAL_CLIENT_ID=your_client_id_here"
echo "     PAYPAL_CLIENT_SECRET=your_client_secret_here"
echo ""
echo "3. METAMASK SETUP:"
echo "   - Export private key from MetaMask"
echo "   - Update .env file with:"
echo "     METAMASK_PRIVATE_KEY=your_private_key_here"
echo ""
echo "4. POLYGON API SETUP:"
echo "   - Go to: https://polygon.io/"
echo "   - Get API key"
echo "   - Update .env file with:"
echo "     POLYGON_API_KEY=your_api_key_here"
echo ""
echo "5. MARKETING APIS SETUP:"
echo "   - LinkedIn: https://www.linkedin.com/developers/"
echo "   - Twitter: https://developer.twitter.com/"
echo "   - GitHub: https://github.com/settings/tokens"
echo ""
echo "🕵️‍♂️ The game is afoot! API keys ready for deployment!"
