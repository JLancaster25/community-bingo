from db import get_db

def record_game(room, pattern):
    db=get_db(); cur=db.cursor()
    cur.execute("insert into games (room_code,pattern) values (%s,%s) returning id",(room,pattern))
    gid=cur.fetchone()["id"]
    db.commit(); cur.close(); db.close()
    return gid

def record_player(gid, uid, win):
    db=get_db(); cur=db.cursor()
    cur.execute("insert into game_players (game_id,user_id,is_winner) values (%s,%s,%s)",(gid,uid,win))
    cur.execute("""
      insert into user_stats (user_id,games_played,games_won)
      values (%s,1,%s)
      on conflict (user_id)
      do update set
        games_played=user_stats.games_played+1,
        games_won=user_stats.games_won+excluded.games_won
    """,(uid,1 if win else 0))
    cur.execute("""
      update user_stats set win_rate=games_won::numeric/nullif(games_played,0)
      where user_id=%s
    """,(uid,))
    db.commit(); cur.close(); db.close()

def leaderboard():
    db=get_db(); cur=db.cursor()
    cur.execute("""
      select u.username,s.games_won,s.games_played,s.win_rate
      from user_stats s join users u on u.id=s.user_id
      order by games_won desc
      limit 10
    """)
    r=cur.fetchall(); cur.close(); db.close()
    return r
