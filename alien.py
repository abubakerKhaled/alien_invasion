import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """A clas to represent a single alien in the feet."""

    def __init__(self, ai_settings, screen):
        """Initialize the alien and set its starting position."""
        super(Alien, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Loat the alien image and set its rect attribute
        self.image = pygame.image.load('images/alien2.bmp')
        self.rect = self.image.get_rect()

        # Start each new alien near the top left of the screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        

        # Store the alien's exact position.
        self.x = float(self.rect.x)

    def blitme(self):
        """Draw the alien at its current position."""
        self.screen.blit(self.image, self.rect)

    def check_edges(self):
        """Return True if the alien is at edge of screen."""
        screen_rect = self.screen.get_rect()
        return self.rect.right >= screen_rect.right or self.rect.left <= 0

    def update(self):
        """Move the alien right or left."""
        self.x += (self.ai_settings.alien_speed_factor *
                   self.ai_settings.fleet_direction)
        self.rect.x = self.x
