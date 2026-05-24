#!/bin/bash
# Baker Street Laboratory - Marketing System Deployment

echo "📢 Baker Street Laboratory - Marketing System Deployment"
echo "======================================================="

# Create and activate temporary virtual environment
echo "📦 Creating virtual environment for marketing packages..."
python3 -m venv /tmp/marketing_venv
source /tmp/marketing_venv/bin/activate

# Install required packages (removed smtplib2 as it's not needed/available)
echo "📦 Installing marketing packages..."
pip install requests schedule

# Create marketing campaigns
echo "📧 Creating marketing campaigns..."

# Email campaign
python3 -c "
from marketing_automation_system import MarketingAutomationSystem
marketing = MarketingAutomationSystem()
print('✅ Marketing automation system initialized')
print('📊 Available campaigns:', list(marketing.marketing_campaigns.keys()))
"

# LinkedIn post creation
echo "💼 Creating LinkedIn marketing post..."
python3 -c "
from marketing_automation_system import MarketingAutomationSystem
marketing = MarketingAutomationSystem()
result = marketing.create_linkedin_post('consciousness_launch')
print(f'LinkedIn Post Status: {result[\"status\"]}')
if result['status'] == 'SUCCESS':
    print('✅ LinkedIn post created successfully')
    print('📝 Post content preview:', result['post_content'][:100] + '...')
"

# Twitter campaign creation
echo "🐦 Creating Twitter marketing campaign..."
python3 -c "
from marketing_automation_system import MarketingAutomationSystem
marketing = MarketingAutomationSystem()
result = marketing.create_twitter_campaign('consciousness_launch')
print(f'Twitter Campaign Status: {result[\"status\"]}')
if result['status'] == 'SUCCESS':
    print('✅ Twitter campaign created successfully')
    print('📝 Tweets created:', len(result['tweets']))
"

# Clean up
deactivate
rm -rf /tmp/marketing_venv

echo "🚀 Marketing systems deployment complete!"
