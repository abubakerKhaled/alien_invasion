import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep

# Define some constants for the spacing between aliens
ALIEN_SPACING_X = 2  # The horizontal spacing is equal to 2 times the alien width
ALIEN_SPACING_Y = 2  # The vertical spacing is equal to 2 times the alien height
ALIEN_MARGIN_Y = 0.5  # The top margin is equal to 3 times the alien height


def start_game(ai_settings, screen, ship, bullets, stats, aliens):
    pygame.mouse.set_visible(False)
    # Reset the game statistics.
    stats.reset_stats()
    stats.game_active = True
    
    # Empty the list of aliens and bullets.
    aliens.empty()
    bullets.empty()
    
    # Create a new fleet and center the ship.
    create_fleet(ai_settings, screen, ship, aliens)
    ship.center_ship()
    

def check_events(ai_settings, screen, ship, bullets, stats, play_buttton, aliens):
    """Respond to keypresses and mouse events."""
    # Watch for keyboard and mouse events.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            check_keydown_event(event, ai_settings, screen, ship, bullets, stats, aliens)

        elif event.type == pygame.KEYUP:
            check_keyup_event(event, ship)
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_botton(ai_settings, screen, ship, bullets, stats, play_buttton, aliens, mouse_x, mouse_y)
            

def check_play_botton(ai_settings, screen, ship, bullets, stats, play_buttton, aliens, mouse_x, mouse_y):
    """Start new game when the player clicks play."""
    button_clicked = play_buttton.rect.collidepoint(mouse_x, mouse_y)
    if  button_clicked and not stats.game_active:
        # Reset the game settings.
        ai_settings.init_dynamic_settings()
        start_game(ai_settings, screen, ship, bullets, stats, aliens)


def check_keydown_event(event, ai_settings, screen, ship, bullets, stats, aliens):
    """Respond to keypresses."""

    if event.key == pygame.K_RIGHT:
        ship.moving_right = True

    elif event.key == pygame.K_LEFT:
        ship.moving_left = True

    elif event.key == pygame.K_SPACE:
        # Create new bullet and add it to the bullets group.
        fire_bullet(ai_settings, screen, ship, bullets)
    
    elif event.key == pygame.K_p:
        start_game(ai_settings, screen, ship, bullets, stats, aliens)

    elif (event.key == pygame.K_w and event.mod & pygame.KMOD_CTRL) or event.key == pygame.K_q:
        sys.exit()


def fire_bullet(ai_settings, screen, ship, bullets):
    """Fire bullets if limit not reached yet."""
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def check_keyup_event(event, ship):
    """Respond to key releases."""

    if event.key == pygame.K_RIGHT:
        ship.moving_right = False

    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def update_screen(ai_settings, screen, stats, ship, aliens, bullets, play_buttton):
    """Redraw the screen during each pass through the loop."""

    # Fills the entire screen with the color.
    screen.fill(ai_settings.bg_color)

    # draw the ship on the screen.
    ship.blitme()

    aliens.draw(screen)

    # Redraw all bullets behind ship and aliens.
    for bullet in bullets.sprites():
        bullet.draw_bullet()
        
    # Draw the play button if the game is inactive.
    if not stats.game_active:
        play_buttton.draw_button()

    # Make the most recently drawn screen visible.
    pygame.display.flip()


def remove_bullets(bullets, ai_settings):
    """Remove the bullets that have disappeared from the screen."""
    # Loop through a copy of the group
    for bullet in [b for b in bullets]:
        # Check if the bullet has disappeared
        if bullet.rect.bottom <= ai_settings.SCREEN_TOP:
            # Remove the bullet from the group
            bullet.kill()


# def get_alien_count_per_row(ai_settings, alien):
#     """Determines the number of aliens that fit in a row."""
#     # Get the width of an alien from its rect attribute
#     alien_width = alien.rect.width
#     # Calculate the available space for aliens by subtracting some margin from one side
#     available_space_x = (ai_settings.screen_width -
#                          (2 * alien_width))
#     # Calculate the number of aliens that can fit in one row by dividing the available space by the spacing
#     alien_count_x = int(available_space_x / (2 * alien_width))
#     return alien_count_x


# def get_row_count(ai_settings, ship, alien):
#     """Determine the number of rows of aliens that fit on the screen."""
#     # Get the height of an alien and a ship from their rect attributes
#     alien_height = alien.rect.height
#     ship_height = ship.rect.height
#     # Calculate the available space for aliens by subtracting some margin from the top and bottom
#     available_space_y = (ai_settings.screen_height -
#                          (ALIEN_MARGIN_Y + ALIEN_SPACING_Y) * alien_height - ship_height)
#     # Calculate the number of rows that can fit on the screen by dividing the available space by the spacing
#     row_count = int(available_space_y / (ALIEN_SPACING_Y * alien_height))
#     return row_count


def get_number_aliens_x(ai_settings, alien_width):
    """Determine the number of alines that fit in a row."""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def get_number_rows(ai_settings, ship_height, aline_height):
    """Determine the number of rows of aliens that fit on the screen."""
    available_space_y = (ai_settings.screen_height -
                         (3 * aline_height) - ship_height)
    number_rows = int(available_space_y / (2 * aline_height))
    return number_rows


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """Creates an alien and place it in the row."""
    # Create an alien object
    alien = Alien(ai_settings, screen)
    # Set its x and y coordinates using its rect attribute
    alien_width = alien.rect.width
    alien = Alien(ai_settings, screen)
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens):
    """Create a full fleet of aliens."""
    # Create an alien and find the number of aliens in a row.
    # Spacing between each alien is equal to one alien width.
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(
        ai_settings, ship.rect.height, alien.rect.height)

    # Create the first row of aliens.
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            # Create an alien and place it in the row.
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def check_fleet_edges(ai_settings, aliens):
    """Respond appropriately if any aliens have reached an edge."""
    edge_alien = next((alien for alien in aliens.sprites()
                       if alien.check_edges()), None)
    if edge_alien:
        change_fleet_direction(ai_settings, aliens)


def change_fleet_direction(ai_settings, aliens):
    """Drop the entire fleet and change the fleet's direction."""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed

    ai_settings.fleet_direction *= -1
    
    
def ship_hit(ai_settings, stats, screen, ship, aliens, bullets):
    """Respond to ship being hit by an alien."""

    if stats.left_ships > 0:
        
        # Decrement the number of ship's left.
        stats.left_ships -= 1
        
        # Empty the aliens and bullets groups.
        aliens.empty()
        bullets.empty()

        # Create a new fleet and center the ship.
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
        
        # Pause.
        sleep(0.5)
    
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)
    
    
    
def check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets):
    """Check if any alien have reached the bottom of the screen."""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
            break
    


def update_aliens(ai_settings, stats, screen, ship, aliens, bullets):
    """
    Check if the fleet is at an edge,
        and then update the positions of all aliens in the fleet.
    """
    # Change direction and drop down fleet if any alien reaches an edge
    check_fleet_edges(ai_settings, aliens)
    # Move all aliens horizontally according to their speed and direction
    aliens.update()
    
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
    
    # Look for aliens hitting the bottom of the screen.    
    check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets)

def update_bullets(aliens, bullets, ai_settings, screen, ship):
    # Check for any bullets that have hit the aliens.
    check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets)
    
    # Check if the aliens is destroyed or not.
    if len(aliens) == 0:
        # Destroy existing bullets, speed up game, and create new fleets.
        bullets.empty()
        ai_settings.increase_speed()
        create_fleet(ai_settings, screen, ship, aliens)
        
def check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets):
    """Respond to bullet-alien collisions."""
    # Remove any bullets and aliens that have collided.
    # If so, get rid of the bullet and the alien.
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    