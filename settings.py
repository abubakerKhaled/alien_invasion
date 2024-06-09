class Settings():
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initializes the game's static settings."""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 750
        self.bg_color = (230, 230, 230)
        self.SCREEN_TOP = 0

        # Ship Settings
        self.left_ships = 3

        # Bullet settings
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 60, 60, 60
        self.bullets_allowed = 3

        # Alien Settings
        self.fleet_drop_speed = 5
        self.fleet_drop_offset = 15
        
        # How quikly the game speeds up.
        self.speedup_scale = 1.1
        
        # How quikly the alien point values increase.
        self.score_scale = 1.5
        
        self.init_dynamic_settings()

    def init_dynamic_settings(self):
        """Initialize the settings that change through out the game."""
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        # fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1
        self.alien_speed_factor = 1
        
        # Scoring
        self.alien_points = 50
        
    def increase_speed(self):
        """increase the speed settings and alien points values."""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
