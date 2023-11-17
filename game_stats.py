import pickle

class GameStats():
  """Track statistics for alien invasion game."""
  
  def __init__(self, ai_settings):
    """Initialize statistics."""
    self.ai_settings = ai_settings
    
    self.reset_stats()
    
    # Start Alien Invasion as an active state.
    self.game_active = False
      
    # High score should never be reset.
    # Load the previous high score if it exists.
    try:
    # use the same file name as in check_high_score function
      with open('h_score.txt', 'rb') as f:
        self.high_score = pickle.load(f)
    except FileNotFoundError:
    # if the file doesn't exist, set the high score to zero and create the file
      self.high_score = 0
      with open('h_score.txt', 'wb') as f:
        pickle.dump(self.high_score, f)

    
  def reset_stats(self):
    """Initialize statistics that can change during the game."""
    self.left_ships = self.ai_settings.left_ships
    self.score = 0
    self.level = 1
