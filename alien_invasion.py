# Imports Syntax.
import sys
import pygame
from settings import Settings
from ship import Ship
import game_functions as gf
from pygame.sprite import Group  # changed _Group to Group


# Start the game function.
try:
    def run_game():
        # Initialize the game and create the a screen object.
        pygame.init()
        ai_settings = Settings()
        screen = pygame.display.set_mode(
            (ai_settings.screen_width, ai_settings.screen_height))
        pygame.display.set_caption('Alien Invasion')

        # Make a ship
        ship = Ship(ai_settings, screen)

        # Make a group to store the bullets in.
        bullets = Group()  # changed _Group to Group

        # Start the main loop of the game.
        while True:

            # Call the check events function to handle events.
            gf.check_events(ai_settings, screen, ship, bullets)

            ship.update()
            bullets.update()
            gf.update_screen(ai_settings, screen, ship, bullets)

    if __name__ == "__main__":
        run_game()
except Exception as e:
    print(e)
    # handle the exception
