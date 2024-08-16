# simple buffer function to pass in parameters
import shlex

def launch_game_or_feature(game_function, custom_args=None):
    try:
        print("Preparing to launch...")

        if custom_args:
            # parse the custom_args string into a list of arguments
            args = shlex.split(custom_args)
            game_function(args)
        else:
            game_function()

        print("game or feature completed.")
    except Exception as e:
        print(f"an error occurred while running the game or feature: {e}")
    finally:
        print("Returning to main menu...")