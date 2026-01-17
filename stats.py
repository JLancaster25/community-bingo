from db import get_db

def record_game(room_code, pattern):
    db = get_db()
    cur = db.cursor()

    cur.execute("""
        insert into games (room_code, pattern)
        values (%s,%s)
        returning id
    """, (room_code, pattern))

    game_id = cur.fetchone()["id"]
    db.commit()
    cur.close()
    db.close()
    return game_id


def record_player(game_id, user_id, won=False):
    db = get_db()
    cur = db.cursor()

    cur.execute("""
        insert into game_players (game_id, user_id, is_winner)
        values (%s,%s,%s)
    """, (game_id, user_id, won))

    cur.execute("""
        insert into user_stats (user_id, games_played, games_won)
        values (%s,1,%s)
        on conflict (user_id)
        do update set
            games_played = user_stats.games_played + 1,
            games_won = user_stats.games_won + excluded.games_won
    """, (user_id, 1 if won else 0))

    cur.execute("""
        update user_stats
        set win_rate = games_won::numeric / nullif(games_played,0)
        where user_id=%s
    """, (user_id,))

    db.commit()
    cur.close()
    db.close()


def leaderboard(limit=10):
    db = get_db()
    cur = db.cursor()

    cur.execute("""
        select u.username, s.games_won, s.games_played, s.win_rate
        from user_stats s
        join users u on u.id = s.user_id
        order by s.games_won desc, s.win_rate desc
        limit %s
    """, (limit,))

    data = cur.fetchall()
    cur.close()
    db.close()
    return data
