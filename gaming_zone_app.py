import mysql.connector

#create tables
def create_database_and_tables(cursor):
    cursor.execute("DROP DATABASE IF EXISTS GamingZone")
    cursor.execute("CREATE DATABASE GamingZone")
    cursor.execute("USE GamingZone")

    cursor.execute("""
        CREATE TABLE Games (
            game_id INT AUTO_INCREMENT PRIMARY KEY,
            game_name VARCHAR(50),
            charge_per_hour DECIMAL(5,2)
        )
    """)

    cursor.execute("""
        CREATE TABLE Members (
            member_id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100),
            membership_type ENUM('Yearly', 'Monthly', 'Daily'),
            hours_spent INT DEFAULT 0,
            hours_left INT
        )
    """)

    cursor.execute("""
        CREATE TABLE GameLogs (
            log_id INT AUTO_INCREMENT PRIMARY KEY,
            member_id INT,
            game_id INT,
            hours_played INT,
            FOREIGN KEY (member_id) REFERENCES Members(member_id),
            FOREIGN KEY (game_id) REFERENCES Games(game_id)
        )
    """)

#insert data
def insert_sample_data(cursor):
    games = [
        ('Air Hockey', 50.00),
        ('VR Racing', 120.00),
        ('Bowling', 100.00),
        ('Archery', 70.00),
        ('Turf', 80.00),
        ('SnowPlaying', 500.00),
        ('Car dashing', 100.00),
        ('Shooting', 99.00),
        ('Ball in Basket', 70.00)
    ]
    cursor.executemany("INSERT INTO Games (game_name, charge_per_hour) VALUES (%s, %s)", games)

    members = [
        ('Arjun', 'Yearly', 10, 90),
        ('Bindhu', 'Monthly', 5, 25),
        ('Ravi', 'Daily', 2, 6),
        ('Sneha', 'Monthly', 7, 23),
        ('Kiran', 'Daily', 4, 4),
        ('Divya', 'Yearly', 15, 85),
        ('Manoj', 'Monthly', 6, 24),
        ('Pooja', 'Yearly', 8, 92),
        ('Vikram', 'Daily', 3, 5),
        ('Meena', 'Monthly', 4, 26)
    ]
    cursor.executemany("INSERT INTO Members (name, membership_type, hours_spent, hours_left) VALUES (%s, %s, %s, %s)", members)

    game_logs = [
        (1, 1, 3), (2, 2, 2), (3, 3, 1), (4, 2, 2), (5, 1, 1),
        (6, 4, 2), (7, 5, 2), (8, 4, 1), (9, 1, 1), (10, 2, 1),
        (1, 2, 2), (2, 2, 2), (3, 1, 1)
    ]
    cursor.executemany("INSERT INTO GameLogs (member_id, game_id, hours_played) VALUES (%s, %s, %s)", game_logs)

def run_reports(cursor):
    print("1) Games Available:")
    cursor.execute("SELECT * FROM Games")
    for row in cursor.fetchall():
        print(row)

    print("\n2) Members Registered:")
    cursor.execute("SELECT * FROM Members")
    for row in cursor.fetchall():
        print(row)

    print("\n3) Yearly Members:")
    cursor.execute("SELECT name FROM Members WHERE membership_type = 'Yearly'")
    for row in cursor.fetchall():
        print(row[0])

    print("\n   Monthly Members:")
    cursor.execute("SELECT name FROM Members WHERE membership_type = 'Monthly'")
    for row in cursor.fetchall():
        print(row[0])

    print("\n   Daily Members:")
    cursor.execute("SELECT name FROM Members WHERE membership_type = 'Daily'")
    for row in cursor.fetchall():
        print(row[0])

    print("\n4) Members with Membership Type and Hours Left:")
    cursor.execute("SELECT name, membership_type, hours_left FROM Members")
    for row in cursor.fetchall():
        print(row)

    print("\n5) Total Monthly Members:")
    cursor.execute("SELECT COUNT(*) FROM Members WHERE membership_type = 'Monthly'")
    print(cursor.fetchone()[0])

    print("\n6) Players Per Game:")
    cursor.execute("""
        SELECT G.game_name, COUNT(DISTINCT L.member_id) as player_count
        FROM GameLogs L JOIN Games G ON L.game_id = G.game_id
        GROUP BY L.game_id
    """)
    for row in cursor.fetchall():
        print(row)

    print("\n7) Total Hours Played per Game:")
    cursor.execute("""
        SELECT G.game_name, SUM(L.hours_played) as total_hours
        FROM GameLogs L JOIN Games G ON L.game_id = G.game_id
        GROUP BY L.game_id
    """)
    for row in cursor.fetchall():
        print(row)

    print("\n8) Most Played Game:")
    cursor.execute("""
        SELECT G.game_name
        FROM GameLogs L JOIN Games G ON L.game_id = G.game_id
        GROUP BY G.game_name
        ORDER BY SUM(L.hours_played) DESC
        LIMIT 1
    """)
    print(cursor.fetchone()[0])


def main():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="BindhuSha@157"
    )
    cursor = conn.cursor()
    
    create_database_and_tables(cursor)
    insert_sample_data(cursor)
    conn.commit()
    
    run_reports(cursor)
    
    cursor.close()
    conn.close()

main()
# This code assumes your base setup (create tables, insert sample data, run initial reports) is already done.
# Let's continue from that and implement Q1 to Q20 as new functions.

import mysql.connector
from mysql.connector import Error

def connect():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="BindhuSha@157",
            database="GamingZone"
        )
    except Error as e:
        print("Connection Error:", e)
        return None

# Q1: Add new game
def add_game(cursor):
    name = input("Enter game name: ")
    game_type = input("Enter game type: ")
    charge = float(input("Enter charge per hour: "))

    # Check if 'game_type' column exists
    cursor.execute("SHOW COLUMNS FROM Games LIKE 'game_type'")
    result = cursor.fetchone()
    if not result:
        cursor.execute("ALTER TABLE Games ADD COLUMN game_type VARCHAR(50)")
        print("'game_type' column added to Games table.")

    cursor.execute(
        "INSERT INTO Games (game_name, game_type, charge_per_hour) VALUES (%s, %s, %s)",
        (name, game_type, charge)
    )
    print("Game added successfully.")


# Q2: Register new member
def register_member(cursor):
    name = input("Enter member name: ")
    mem_type = input("Enter membership type (Yearly/Monthly/Daily): ")
    hours_map = {"Yearly": 100, "Monthly": 30, "Daily": 8}
    cursor.execute("INSERT INTO Members (name, membership_type, hours_spent, hours_left) VALUES (%s, %s, %s, %s)",
                   (name, mem_type, 0, hours_map.get(mem_type, 8)))

# Q3: Log gameplay and update hours
def log_gameplay(cursor):
    member_id = int(input("Enter Member ID: "))
    game_id = int(input("Enter Game ID: "))
    hours = int(input("Enter hours played: "))
    cursor.execute("SELECT hours_left FROM Members WHERE member_id = %s", (member_id,))
    result = cursor.fetchone()
    if result and result[0] >= hours:
        cursor.execute("INSERT INTO GameLogs (member_id, game_id, hours_played) VALUES (%s, %s, %s)", (member_id, game_id, hours))
        cursor.execute("UPDATE Members SET hours_spent = hours_spent + %s, hours_left = hours_left - %s WHERE member_id = %s",
                       (hours, hours, member_id))
        print("Gameplay logged successfully.")
    else:
        print("Insufficient hours.")

# Q4: Delete inactive member
def delete_inactive_members(cursor):
    cursor.execute("""
        DELETE FROM Members
        WHERE member_id NOT IN (SELECT DISTINCT member_id FROM GameLogs)
    """)

# Q5: Games with charges > 100
def games_above_100(cursor):
    cursor.execute("SELECT game_name, charge_per_hour FROM Games WHERE charge_per_hour > 100")
    for row in cursor.fetchall():
        print(row)

# Q6: Count game types
def count_game_types(cursor):
    cursor.execute("SELECT game_type, COUNT(*) FROM Games GROUP BY game_type")
    for row in cursor.fetchall():
        print(row)

# Q7: Members with <10 hours left
def members_less_than_10(cursor):
    cursor.execute("SELECT name, hours_left FROM Members WHERE hours_left < 10")
    for row in cursor.fetchall():
        print(row)

# Q8: Members played >2 different games
def members_multiple_games(cursor):
    cursor.execute("""
        SELECT member_id, COUNT(DISTINCT game_id)
        FROM GameLogs
        GROUP BY member_id
        HAVING COUNT(DISTINCT game_id) > 2
    """)
    for row in cursor.fetchall():
        print("Member ID:", row[0])

# Q9: Total hours remaining by membership type
def total_hours_by_type(cursor):
    cursor.execute("SELECT membership_type, SUM(hours_left) FROM Members GROUP BY membership_type")
    for row in cursor.fetchall():
        print(row)

# Q10: Total income from game plays
def total_income(cursor):
    cursor.execute("""
        SELECT SUM(G.charge_per_hour * L.hours_played)
        FROM GameLogs L JOIN Games G ON L.game_id = G.game_id
    """)
    print("Total Income: ₹", cursor.fetchone()[0])

# Q11: Most active member
def most_active_member(cursor):
    cursor.execute("SELECT name FROM Members ORDER BY hours_spent DESC LIMIT 1")
    print("Most Active Member:", cursor.fetchone()[0])

# Q12: Top 3 most played games
def top_3_games(cursor):
    cursor.execute("""
        SELECT G.game_name, SUM(L.hours_played) AS total_hours
        FROM GameLogs L JOIN Games G ON L.game_id = G.game_id
        GROUP BY G.game_id
        ORDER BY total_hours DESC
        LIMIT 3
    """)
    for row in cursor.fetchall():
        print(row)

# Q13: Report of hours per member per game
def report_hours_per_member_game(cursor):
    cursor.execute("""
        SELECT M.name, G.game_name, SUM(L.hours_played)
        FROM GameLogs L
        JOIN Members M ON L.member_id = M.member_id
        JOIN Games G ON L.game_id = G.game_id
        GROUP BY M.name, G.game_name
    """)
    for row in cursor.fetchall():
        print(row)

# Q14: Take member name & game, log gameplay if hours left OK


# MAIN to run these tasks
if __name__ == "__main__":
    conn = connect()
    if conn:
        cur = conn.cursor()
        # Uncomment any function below to test
        # add_game(cur)
        # register_member(cur)
        # log_gameplay(cur)
        # delete_inactive_members(cur)
        # games_above_100(cur)
        # count_game_types(cur)
        # members_less_than_10(cur)
        # members_multiple_games(cur)
        # total_hours_by_type(cur)
        # total_income(cur)
        # most_active_member(cur)
        # top_3_games(cur)
        # report_hours_per_member_game(cur)

        conn.commit()
        cur.close()
        conn.close()
    else:
        print("❌ Unable to proceed without DB connection.")
# Q14: Log gameplay with name check and hour validation
def log_gameplay_by_name(cursor):
    member_name = input("Enter member name: ")
    game_name = input("Enter game name: ")
    hours = int(input("Enter hours played: "))
    cursor.execute("SELECT member_id, hours_left FROM Members WHERE name = %s", (member_name,))
    member = cursor.fetchone()
    cursor.execute("SELECT game_id FROM Games WHERE game_name = %s", (game_name,))
    game = cursor.fetchone()
    if member and game:
        if member[1] >= hours:
            cursor.execute("INSERT INTO GameLogs (member_id, game_id, hours_played) VALUES (%s, %s, %s)", (member[0], game[0], hours))
            cursor.execute("UPDATE Members SET hours_spent = hours_spent + %s, hours_left = hours_left - %s WHERE member_id = %s",
                           (hours, hours, member[0]))
            print("✅ Gameplay logged successfully")
        else:
            print("❌ Not enough hours left")
    else:
        print("❌ Invalid member or game name")

# Q15: Members used more than 75% of hours
def members_used_75_percent(cursor):
    cursor.execute("SELECT name, hours_spent, hours_left FROM Members WHERE hours_spent > 0.75 * (hours_spent + hours_left)")
    for row in cursor.fetchall():
        print(row)

# Q16: Detailed report per member
def detailed_member_report(cursor):
    cursor.execute("""
        SELECT M.name, M.membership_type, COUNT(DISTINCT L.game_id), SUM(L.hours_played), M.hours_left
        FROM Members M
        LEFT JOIN GameLogs L ON M.member_id = L.member_id
        GROUP BY M.name, M.membership_type, M.hours_left
    """)
    for row in cursor.fetchall():
        print(row)

# Q17: Members who never played any game
def members_never_played(cursor):
    cursor.execute("""
        SELECT name FROM Members
        LEFT JOIN GameLogs ON Members.member_id = GameLogs.member_id
        WHERE GameLogs.member_id IS NULL
    """)
    for row in cursor.fetchall():
        print(row[0])

# Q18: Menu system
def show_menu():
    print("""
========= GamingZone Menu =========
1. Add Game
2. Register Member
3. Log Gameplay (by ID)
4. Delete Inactive Members
5. Games with charge > ₹100
6. Count of Game Types
7. Members with <10 hrs left
8. Members who played >2 games
9. Total hrs remaining by membership
10. Total income from plays
11. Most active member
12. Top 3 most played games
13. Hours/member/game report
14. Log Gameplay (by name)
15. Members used >75% hours
16. Detailed member report
17. Members never played
18. Exit
==================================
""")  # ✔️ Triple-quote closed correctly


def menu_system():
    conn = connect()
    if conn:
        cur = conn.cursor()
        while True:
            show_menu()
            choice = input("Enter choice (1-18): ")
            if choice == '1': add_game(cur)
            elif choice == '2': register_member(cur)
            elif choice == '3': log_gameplay(cur)
            elif choice == '4': delete_inactive_members(cur)
            elif choice == '5': games_above_100(cur)
            elif choice == '6': count_game_types(cur)
            elif choice == '7': members_less_than_10(cur)
            elif choice == '8': members_multiple_games(cur)
            elif choice == '9': total_hours_by_type(cur)
            elif choice == '10': total_income(cur)
            elif choice == '11': most_active_member(cur)
            elif choice == '12': top_3_games(cur)
            elif choice == '13': report_hours_per_member_game(cur)
            elif choice == '14': log_gameplay_by_name(cur)
            elif choice == '15': members_used_75_percent(cur)
            elif choice == '16': detailed_member_report(cur)
            elif choice == '17': members_never_played(cur)
            elif choice == '18': break
            else: print("Invalid choice")
            conn.commit()
        cur.close()
        conn.close()
    else:
        print("Unable to connect to DB")

# To run the menu system
if __name__ == "__main__":
    menu_system()


# Q20: You can now separate this script into a new module `gaming_utils.py` with sections like:
# - connect()
# - game_operations.py: add_game, count_game_types, games_above_100...
# - member_operations.py: register_member, delete_inactive_members...
# - report_functions.py: all report and analytics queries...
# This will make it modular, testable, and clean for reuse.

