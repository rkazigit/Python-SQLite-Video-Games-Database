import database

AUTH_MENU = """
 -- Video Game Tracker --
 
1) Login
2) Register
3) Exit
 
Your selection: """


MENU_PROMPT = """ -- Video Game Tracker --
 
Please choose one of these options:
 
1) Add a new game
2) See all games.
3) Find a game by name.
4) See which platform is best for a game.
5) Delete a game.
6) Find games by rating range.
7) Logout
 
Your selection:"""

DELETE_MENU = """
How would you like to delete?
 
1) Delete by name
2) Delete by ID
3) Cancel
 
Your selection: """

RATING_MENU = """
Select a rating range to display:
 
1)  0 – 49   (Poor)
2) 50 – 69   (Average)
3) 70 – 89   (Good)
4) 90 – 100  (Excellent)
5) Custom range
6) Cancel
 
Your selection: """


def print_game(game):
    print(f"  [{game[0]}] {game[1]} ({game[2]}) - {game[3]}/100")
 
 
def print_games(games):
    if games:
        for game in games:
            print_game(game)
    else:
        print(" No games found.")


def prompt_login(connection):
    username = input("Username: ")
    password = input("Password: ")
    user = database.get_user(connection, username, password)
    if user:
        print(f"\n  Welcome back, {username}!")
        return True
    else:
        print(" Hm. Invalid username or password.")
        return False
 
 
def prompt_register(connection):
    username = input("Choose a username: ")
    if database.username_exists(connection, username):
        print("  That username is already taken. Try a different one.")
        return False
    password = input("Choose a password: ")
    confirm = input("Confirm password: ")
    if password != confirm:
        print("  Passwords do not match.")
        return False
    success = database.add_user(connection, username, password)
    if success:
        print(f"  Account created! You can now log in as '{username}'.")
    return success

 
def prompt_add_new_game(connection):
    name = input("Enter game name: ")
    platform = input("Enter the platform you played it on: ")
    rating = int(input("Enter your rating score (0-100): "))
    database.add_game(connection, name, platform, rating)
    print(f"  '{name}' added successfully!")
 
def prompt_see_all_games(connection):
    games = database.get_all_games(connection)
    print_games(games)

def prompt_find_game(connection):
    name = input("Enter game name to find: ")
    games = database.get_games_by_name(connection, name)
    print_games(games)
 
def prompt_find_best_platform(connection):
    name = input("Enter game name to find: ")
    best = database.get_best_platform_for_game(connection, name)
    if best:
        print(f"  Best platform for '{name}': {best[2]}  ({best[3]}/100)")
    else:
        print(f"  Hm. No entries found for '{name}'.")
 
 def prompt_delete_game(connection):
    choice = input(DELETE_MENU)
 
    if choice == "1":
        name = input("Enter the exact game name to delete: ")
        rows = database.delete_game_by_name(connection, name)
        if rows:
            print(f"  Deleted {rows} entry/entries named '{name}'.")
        else:
            print(f" Hm. No game named '{name}' was found.")
 
    elif choice == "2":
        try:
            game_id = int(input("Enter the game ID to delete: "))
        except ValueError:
            print("  Hm. Invalid ID. Please enter a number.")
            return
        rows = database.delete_game_by_id(connection, game_id)
        if rows:
            print(f"  Game with ID {game_id} deleted.")
        else:
            print(f"  No game with ID {game_id} was found.")
 
    elif choice == "3":
        print("  Deletion cancelled.")
    else:
        print("  Hm. Invalid option.")

def prompt_games_by_rating(connection):
    choice = input(RATING_MENU)
 
    ranges = {
        "1": (0, 49),
        "2": (50, 69),
        "3": (70, 89),
        "4": (90, 100),
    }
 
    if choice in ranges:
        low, high = ranges[choice]
    elif choice == "5":
        try:
            low = int(input("Enter minimum rating (0-100): "))
            high = int(input("Enter maximum rating (0-100): "))
            if not (0 <= low <= 100 and 0 <= high <= 100 and low <= high):
                print(" Hm. Invalid range.")
                return
        except ValueError:
            print("  Enter valid numbers.")
            return
    elif choice == "6":
        return
    else:
        print("  Hm. Invalid option.")
        return
 
    games = database.get_games_by_rating_range(connection, low, high)
    print(f"\n  Games rated {low}–{high}:")
    print_games(games)

def auth_loop(connection):
    """Returns True once a user has successfully authenticated."""
    while True:
        choice = input(AUTH_MENU)
        if choice == "1":
            if prompt_login(connection):
                return True
        elif choice == "2":
            prompt_register(connection)
        elif choice == "3":
            print("  Goodbye!")
            return False
        else:
            print("  Invalid option.")
 
 
def main_loop(connection):
    while True:
        choice = input(MENU_PROMPT)
        if choice == "1":
            prompt_add_new_game(connection)
        elif choice == "2":
            prompt_see_all_games(connection)
        elif choice == "3":
            prompt_find_game(connection)
        elif choice == "4":
            prompt_find_best_platform(connection)
        elif choice == "5":
            prompt_delete_game(connection)
        elif choice == "6":
            prompt_games_by_rating(connection)
        elif choice == "7":
            print("  Logged out.\n")
            break
        else:
            print("  Invalid input, please try again.")

def menu():
    connection = database.connect()
    database.create_tables(connection)

menu()

