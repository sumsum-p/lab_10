import pygame
import psycopg2
from datetime import datetime

# === PostgreSQL Connection ===
conn = psycopg2.connect(
    dbname="your_db",
    user="your_user",
    password="your_password",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

# === User Authentication ===
def get_or_create_user(username):
    cur.execute("SELECT id FROM users WHERE username = %s", (username,))
    user = cur.fetchone()
    if user:
        user_id = user[0]
        cur.execute("SELECT level, score FROM user_score WHERE user_id = %s ORDER BY last_played DESC LIMIT 1", (user_id,))
        result = cur.fetchone()
        if result:
            print(f"Welcome back, {username}! Your current level is {result[0]}, score: {result[1]}")
            return user_id, result[0], result[1]
        return user_id, 1, 0
    else:
        cur.execute("INSERT INTO users (username) VALUES (%s) RETURNING id", (username,))
        user_id = cur.fetchone()[0]
        conn.commit()
        print(f"Welcome, {username}! Starting at level 1.")
        return user_id, 1, 0

# === Save Game State ===
def save_game(user_id, score, level):
    cur.execute("""
        INSERT INTO user_score (user_id, score, level, last_played)
        VALUES (%s, %s, %s, %s)
    """, (user_id, score, level, datetime.now()))
    conn.commit()
    print("Game state saved.")

# === Simple Snake Game Template with Save ===
def snake_game():
    username = input("Enter your username: ")
    user_id, level, saved_score = get_or_create_user(username)

    pygame.init()
    screen = pygame.display.set_mode((600, 400))
    pygame.display.set_caption('Snake Game')

    clock = pygame.time.Clock()
    speed = 10 + level * 2  # Increase speed per level
    score = saved_score

    running = True
    paused = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_game(user_id, score, level)
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = not paused
                    if paused:
                        save_game(user_id, score, level)
                        print("Paused and saved.")
                elif event.key == pygame.K_q:
                    save_game(user_id, score, level)
                    running = False

        if paused:
            continue

        # === Игровая логика здесь ===
        screen.fill((0, 0, 0))  # очистка экрана
        # Здесь была бы отрисовка змеи, еды, стен и т.д.
        pygame.display.flip()

        # Имитация счёта (вместо логики столкновений и еды)
        score += 1

        clock.tick(speed)

    pygame.quit()
    cur.close()
    conn.close()

snake_game()
"""
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS user_score (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    score INTEGER DEFAULT 0,
    level INTEGER DEFAULT 1,
    last_played TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

"""