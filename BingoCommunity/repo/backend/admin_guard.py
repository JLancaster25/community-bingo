from supabase import create_client
import os

supabase = create_client(
    os.environ["SUPABASE_URL"],
    os.environ["SUPABASE_SERVICE_KEY"]
)

def is_admin(jwt):
    user = supabase.auth.get_user(jwt)
    profile = supabase.table("profiles").select("role").eq(
        "id", user.user.id
    ).single().execute()
    return profile.data["role"] == "admin"