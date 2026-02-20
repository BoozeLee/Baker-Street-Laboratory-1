import os
from fastapi import HTTPException, Header
from supabase import create_client

SUPABASE_URL = os.getenv('SUPABASE_URL', '')
SUPABASE_KEY = os.getenv('SUPABASE_SERVICE_ROLE_KEY', '')
supabase = create_client(SUPABASE_URL, SUPABASE_KEY) if SUPABASE_URL else None

async def require_paid_user(authorization: str = Header(...)):
    if not supabase:
        return {'user': 'dev', 'plan': 'unlimited'}
    token = authorization.replace('Bearer ', '')
    try:
        user = supabase.auth.get_user(token)
        uid  = user.user.id
        sub  = supabase.table('subscriptions').select('*')
                .eq('user_id', uid).eq('status', 'active').execute()
        if not sub.data:
            raise HTTPException(402, 'No active subscription')
        return sub.data[0]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(401, str(e))