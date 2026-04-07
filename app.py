import database

MENU_PROMPT = """ -- Video Game Tracker --
 
Please choose one of these options:
 
1) Add a new game
2) See all games.
3) Find a game by name.
4) See which platform is best for a game.
5) Exit
 
Your selection:"""

def menu():
    connection = database.connect()
    database.create_tables(connection)
 
    while (user_input := input(MENU_PROMPT)) != "5":
        if user_input == "1":
            prompt_add_new_game(connection)
        elif user_input == "2":
            prompt_see_all_games(connection)
        elif user_input == "3":
            prompt_find_game(connection)
        elif user_input == "4":
            prompt_find_best_platform(connection)
        else:
            print("Invalid input, please try again.")
 
def prompt_add_new_game(connection):
    name = input("Enter game name: ")
    platform = input("Enter the platform you played it on: ")
    rating = int(input("Enter your rating score (0-100): "))
    database.add_game(connection, name, platform, rating)
 
def prompt_see_all_games(connection):
    games = database.get_all_games(connection)
    for game in games:
        print(f"{game[1]} ({game[2]}) - {game[3]}/100")
 
def prompt_find_game(connection):
    name = input("Enter game name to find: ")
    games = database.get_games_by_name(connection, name)
    for game in games:
        print(f"{game[1]} ({game[2]}) - {game[3]}/100")
 
def prompt_find_best_platform(connection):
    name = input("Enter game name to find: ")
    best_platform = database.get_best_platform_for_game(connection, name)
    print(f"The best platform for {name} is: {best_platform[2]}")
 
 
menu()