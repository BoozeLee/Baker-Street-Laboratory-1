#!/bin/bash

echo "☁️ Baker Street Laboratory - AWS Deployment"
echo "=========================================="

# Contact information
echo "📞 Contact Information:"
echo "   Email: iamthatiamresearch@gmail.com"
echo "   Phone: +32 471 315 269"
echo "   Location: Belgium/Netherlands"
echo ""

# Install AWS CLI
echo "📦 Installing AWS CLI..."
pip install awscli boto3

# Configure AWS
echo "🔐 Please configure AWS:"
echo "Run: aws configure"
echo "You'll need:"
echo "   - AWS Access Key ID"
echo "   - AWS Secret Access Key"
echo "   - Default region (e.g., eu-west-1)"
echo ""

# Deploy CloudFormation stack
echo "🏗️ Deploying AWS infrastructure..."
aws cloudformation create-stack \
    --stack-name baker-street-laboratory \
    --template-body file://aws_infrastructure.json \
    --parameters ParameterKey=ContactEmail,ParameterValue=iamthatiamresearch@gmail.com \
                ParameterKey=ContactPhone,ParameterValue=+32 471 315 269 \
    --capabilities CAPABILITY_IAM

# Wait for stack creation
echo "⏳ Waiting for stack creation..."
aws cloudformation wait stack-create-complete \
    --stack-name baker-street-laboratory

# Deploy Lambda function
echo "⚡ Deploying Lambda function..."
zip lambda_function.zip lambda_handler.py
aws lambda update-function-code \
    --function-name baker-street-ai-processor \
    --zip-file fileb://lambda_function.zip

# Create API Gateway integration
echo "🌐 Setting up API Gateway..."
aws apigateway create-deployment \
    --rest-api-id $(aws apigateway get-rest-apis --query 'items[?name==`baker-street-ai-api`].id' --output text) \
    --stage-name prod

# Test deployment
echo "🧪 Testing deployment..."
aws lambda invoke \
    --function-name baker-street-ai-processor \
    --payload '{"action": "analyze", "data": "test"}' \
    response.json

echo ""
echo "✅ AWS deployment complete!"
echo ""
echo "🌐 Access Points:"
echo "   API Gateway: https://api.bakerstreetlab.com"
echo "   Lambda: baker-street-ai-processor"
echo "   S3: baker-street-laboratory-models"
echo "   RDS: baker-street-db"
echo ""
echo "📞 Support:"
echo "   Email: iamthatiamresearch@gmail.com"
echo "   Phone: +32 471 315 269"
echo ""
echo "🎉 Baker Street Laboratory is now live on AWS!"
echo "The game is afoot! 🕵️‍♂️"
