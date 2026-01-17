from db import get_db

def profile(uid):
    db=get_db(); cur=db.cursor()
    cur.execute("""
      select u.username, p.display_name, p.avatar_url, p.bio, p.is_admin
      from users u left join profiles p on u.id=p.user_id
      where u.id=%s
    """,(uid,))
    r=cur.fetchone(); cur.close(); db.close()
    return r
