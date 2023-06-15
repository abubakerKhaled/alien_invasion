class Settings():
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initializes the game's settings."""

        # Screen settings
        self.screen_width = 1200
        self.screen_height = 750
        self.bg_color = (230, 230, 230)
        self.SCREEN_TOP = 0

        # Ship Settings
        self.ship_speed_factor = 1.5

        # Bullet settings
        self.bullet_speed_factor = 1
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 60, 60, 60
