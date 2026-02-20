import os, json, stripe
from fastapi import APIRouter, Request, HTTPException
from supabase import create_client

router = APIRouter()
stripe.api_key = os.getenv('STRIPE_SECRET_KEY', '')
WEBHOOK_SECRET = os.getenv('STRIPE_WEBHOOK_SECRET', '')
supabase = create_client(
    os.getenv('SUPABASE_URL',''), os.getenv('SUPABASE_SERVICE_ROLE_KEY',''))

@router.post('/webhook/stripe')
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig     = request.headers.get('stripe-signature','')
    try:
        event = stripe.Webhook.construct_event(payload, sig, WEBHOOK_SECRET)
    except Exception as e:
        raise HTTPException(400, str(e))
    if event['type'] == 'checkout.session.completed':
        s = event['data']['object']
        supabase.table('subscriptions').upsert({
            'user_id':       s.get('client_reference_id',''),
            'stripe_sub_id': s.get('subscription',''),
            'email':         s.get('customer_email',''),
            'plan':          'pro',
            'status':        'active'
        }).execute()
    if event['type'] == 'customer.subscription.deleted':
        sub_id = event['data']['object']['id']
        supabase.table('subscriptions').update({'status':'cancelled'})
            .eq('stripe_sub_id', sub_id).execute()
    return {'status': 'ok'}