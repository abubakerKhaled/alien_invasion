class GameStats():
  
  """Track statistics for alien invasion game."""
  
  
  def __init__(self, ai_settings):
    """Initialize statistics."""
    self.ai_settings = ai_settings
    self.reset_stats()
    
    # Start Alien Invasion as an active state.
    self.game_active = False
    
  def reset_stats(self):
    """Initialize statistics that can change during the game."""
    self.left_ships = self.ai_settings.left_ships