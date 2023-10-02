# Imports Syntax.
import pygame
from settings import Settings
from ship import Ship
import game_functions as gf
from pygame.sprite import Group


# Start the game function.
try:
    def run_game():

        # Initialize the game and create the a screen object.
        pygame.init()

        # Instance of the settings class.
        ai_settings = Settings()

        screen = pygame.display.set_mode(
            (ai_settings.screen_width, ai_settings.screen_height))
        pygame.display.set_caption('Alien Invasion')

        # Make a ship
        ship = Ship(ai_settings, screen)

        # Make a group to store the bullets in.
        bullets = Group()

        # Make a group of aliens.
        aliens = Group()

        # Create the fleet of aliens.
        gf.create_fleet(ai_settings, screen, ship, aliens)

        # Start the main loop of the game.
        while True:

            # Call the check events function to handle events.
            gf.check_events(ai_settings, screen, ship, bullets)

            # Update the movement of the ship based on the movements flags.
            ship.update()
            
            gf.update_bullets(aliens, bullets, ai_settings, screen, ship)

            # Update the bullets up to the screen.
            bullets.update()

            # Get rid of bullets that have already been disappeared.
            gf.remove_bullets(bullets, ai_settings)

            gf.update_aliens(ai_settings, aliens, ship)

            # Redraw the screen during each pass through the game loop.
            gf.update_screen(ai_settings, screen, ship, aliens, bullets)

    if __name__ == "__main__":
        run_game()
except Exception as e:
    print(e)
    # handle the exception
