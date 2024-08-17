import shlex
import curses

def launch_game_or_feature(game_function, custom_args=None):
    try:
        print("Preparing to launch...")
        # dest here, i think i was able to manage curses so that asciiquarium could work properly. i'm not sure though.
        if custom_args:
            args = shlex.split(custom_args)
            if game_function.__module__.endswith('asciiquarium'):
                curses.wrapper(lambda stdscr: game_function(stdscr, *args))
            else:
                game_function(args)
        else:
            if game_function.__module__.endswith('asciiquarium'):
                curses.wrapper(game_function)
            else:
                game_function()
        print("Game or feature completed.")
    except Exception as e:
        print(f"An error occurred while running the game or feature: {e}")
    finally:
        print("Returning to main menu...")  # HAHA IDIOT YOU MISSED A PARENTHESIS
