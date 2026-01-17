from db import get_db

def is_admin(uid):
    db=get_db(); cur=db.cursor()
    cur.execute("select is_admin from profiles where user_id=%s",(uid,))
    r=cur.fetchone(); cur.close(); db.close()
    return r and r["is_admin"]
