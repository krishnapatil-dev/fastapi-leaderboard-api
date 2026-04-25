from fastapi import APIRouter, HTTPException, Depends
from app.database import get_db
from app.models import Player, Score, User, UserLogin
from app.utils import row_to_dict
from app.auth import (
    create_access_token,
    get_current_user,
    hash_password,
    verify_password,
    require_role
)
from datetime import datetime

router = APIRouter()


@router.post("/signup")
def signup(user: User):
    conn = get_db()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO users(username, password, role) VALUES(?, ?, ?)",
            (user.username, hash_password(user.password), "user")
        )
        conn.commit()
    except Exception as e:
        conn.close()
        raise HTTPException(status_code=400, detail="User already exists")

    conn.close()
    return {"message": "Signup successful"}


@router.post("/login")
def login(user: UserLogin):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT password, role FROM users WHERE username = ?",
        (user.username,)
    )
    data = cursor.fetchone()
    conn.close()

    if not data or not verify_password(user.password, data["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({
        "username": user.username,
        "role": data["role"]
    })

    return {"access_token": token}


@router.post("/players")
def add_player(player: Player, user=Depends(get_current_user)):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO players(name) VALUES(?)",
        (player.name,)
    )
    conn.commit()
    conn.close()

    return {"message": "Player added"}


@router.get("/players")
def get_players():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM players")
    rows = cursor.fetchall()
    conn.close()

    return [row_to_dict(r) for r in rows]


@router.post("/scores")
def add_score(score: Score, user=Depends(get_current_user)):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM players WHERE id = ?",
        (score.player_id,)
    )
    if not cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="Player not found")

    cursor.execute(
        "INSERT INTO scores(player_id, score, created_at) VALUES(?, ?, ?)",
        (score.player_id, score.score, datetime.utcnow())
    )
    conn.commit()
    conn.close()

    return {"message": "Score added"}


@router.get("/leaderboard")
def get_leaderboard(limit: int = 10, offset: int = 0, min_score: int = 0):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT P.id, P.name, MAX(S.score) as best_score
        FROM players P JOIN scores S ON P.id = S.player_id
        GROUP BY P.id
        HAVING best_score >= ?
        ORDER BY best_score DESC
        LIMIT ? OFFSET ?
    """, (min_score, limit, offset))

    rows = cursor.fetchall()
    conn.close()

    return [row_to_dict(r) for r in rows]


@router.delete("/admin/reset")
def delete_all(user=Depends(require_role("admin")), confirm: bool = False):
    if not confirm:
        raise HTTPException(status_code=400, detail="Set confirm=true")

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM scores")
    cursor.execute("DELETE FROM players")

    conn.commit()
    conn.close()

    return {"message": "All records deleted"}


@router.get("/rank/{player_id}")
def get_rank(player_id: int):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT P.id, P.name, MAX(S.score) as best_score
        FROM players P JOIN scores S ON P.id = S.player_id
        GROUP BY P.id
        ORDER BY best_score DESC
    """)

    rows = cursor.fetchall()
    conn.close()

    rank = 1
    prev_score = None

    for i, row in enumerate(rows):
        if prev_score is None or row["best_score"] < prev_score:
            rank = i + 1

        if row["id"] == player_id:
            return {
                "rank": rank,
                "name": row["name"],
                "score": row["best_score"]
            }

        prev_score = row["best_score"]

    raise HTTPException(status_code=404, detail="Player not found")


@router.get("/scores/{player_id}")
def score_history(player_id: int):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT score, created_at
        FROM scores
        WHERE player_id = ?
        ORDER BY score DESC
    """, (player_id,))

    rows = cursor.fetchall()
    conn.close()

    return [row_to_dict(r) for r in rows]


@router.delete("/players/{player_id}")
def delete_player(player_id: int, user=Depends(require_role("admin"))):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM players WHERE id = ?",
        (player_id,)
    )

    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Player not found")

    conn.commit()
    conn.close()

    return {"message": "Player and scores deleted"}