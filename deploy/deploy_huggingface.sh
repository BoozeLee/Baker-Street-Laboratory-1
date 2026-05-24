#!/bin/bash

echo "🤗 Baker Street Laboratory - Hugging Face Deployment"
echo "=================================================="

# Contact information
echo "📞 Contact Information:"
echo "   Email: iamthatiamresearch@gmail.com"
echo "   Phone: +32 471 315 269"
echo "   Location: Belgium/Netherlands"
echo ""

# Install dependencies
echo "📦 Installing dependencies..."
pip install huggingface_hub[cli] transformers torch streamlit

# Login to Hugging Face
echo "🔐 Please login to Hugging Face:"
echo "Run: huggingface-cli login"
echo "Get token from: https://huggingface.co/settings/tokens"
echo ""

# Create organization (if not exists)
echo "🏢 Creating organization: BakerStreetLab"
echo "Visit: https://huggingface.co/new-organization"
echo "Organization name: BakerStreetLab"
echo ""

# Deploy models
echo "🚀 Deploying models to Hugging Face..."

for model in baker-street-analyzer psychedelic-research enterprise-security financial-analysis; do
    echo "📁 Creating repository: BakerStreetLab/$model"
    
    # Create repository
    huggingface-cli repo create BakerStreetLab/$model --type model
    
    # Upload files
    cd models/$model
    git init
    git remote add origin https://huggingface.co/BakerStreetLab/$model
    git add .
    git commit -m "Initial model upload"
    git push origin main
    cd ../..
    
    echo "✅ Deployed $model"
done

# Deploy Streamlit app
echo "🌐 Deploying Streamlit app..."
streamlit run streamlit_app.py --server.port 8501

echo ""
echo "✅ Hugging Face deployment complete!"
echo ""
echo "🌐 Access Points:"
echo "   Organization: https://huggingface.co/BakerStreetLab"
echo "   Streamlit App: https://app.bakerstreetlab.com"
echo "   Models: https://huggingface.co/BakerStreetLab/baker-street-analyzer"
echo ""
echo "📞 Support:"
echo "   Email: iamthatiamresearch@gmail.com"
echo "   Phone: +32 471 315 269"
echo ""
echo "🎉 Baker Street Laboratory is now live on Hugging Face!"
echo "The game is afoot! 🕵️‍♂️"
