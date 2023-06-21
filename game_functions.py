import sys
import pygame
from bullet import Bullet
from alien import Alien


# Define some constants for the spacing between aliens
ALIEN_SPACING_X = 2  # The horizontal spacing is equal to 2 times the alien width
ALIEN_SPACING_Y = 2  # The vertical spacing is equal to 2 times the alien height
ALIEN_MARGIN_Y = 0.5  # The top margin is equal to 3 times the alien height


def check_events(ai_settings, screen, ship, bullets):
    """Respond to keypresses and mouse events."""
    # Watch for keyboard and mouse events.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            check_keydown_event(event, ai_settings, screen, ship, bullets)

        elif event.type == pygame.KEYUP:
            check_keyup_event(event, ship)


def check_keydown_event(event, ai_settings, screen, ship, bullets):
    """Respond to keypresses."""

    if event.key == pygame.K_RIGHT:
        ship.moving_right = True

    elif event.key == pygame.K_LEFT:
        ship.moving_left = True

    elif event.key == pygame.K_SPACE:
        # Create new bullet and add it to the bullets group.
        fire_bullet(ai_settings, screen, ship, bullets)

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


def update_screen(ai_settings, screen, ship, aliens, bullets):
    """Redraw the screen during each pass through the loop."""

    # Fills the entire screen with the color.
    screen.fill(ai_settings.bg_color)

    # draw the ship on the screen.
    ship.blitme()

    aliens.draw(screen)

    # Redraw all bullets behind ship and aliens.
    for bullet in bullets.sprites():
        bullet.draw_bullet()

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


def get_alien_count_per_row(ai_settings, alien):
    """Determines the number of aliens that fit in a row."""
    # Get the width of an alien from its rect attribute
    alien_width = alien.rect.width
    # Calculate the available space for aliens by subtracting some margin from one side
    available_space_x = (ai_settings.screen_width -
                         (ALIEN_SPACING_X + 1) * alien_width)
    # Calculate the number of aliens that can fit in one row by dividing the available space by the spacing
    alien_count_x = int(available_space_x / (ALIEN_SPACING_X * alien_width))
    return alien_count_x


def get_row_count(ai_settings, ship, alien):
    """Determine the number of rows of aliens that fit on the screen."""
    # Get the height of an alien and a ship from their rect attributes
    alien_height = alien.rect.height
    ship_height = ship.rect.height
    # Calculate the available space for aliens by subtracting some margin from the top and bottom
    available_space_y = (ai_settings.screen_height -
                         (ALIEN_MARGIN_Y + ALIEN_SPACING_Y) * alien_height - ship_height)
    # Calculate the number of rows that can fit on the screen by dividing the available space by the spacing
    row_count = int(available_space_y / (ALIEN_SPACING_Y * alien_height))
    return row_count


def create_alien(ai_settings, screen, aliens, x, y):
    """Creates an alien and place it at the given position."""
    # Create an alien object
    alien = Alien(ai_settings, screen)
    # Set its x and y coordinates using its rect attribute
    alien.rect.x = x
    alien.rect.y = y
    # Add the alien to the group of aliens
    aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens):
    """Create a full fleet of aliens."""
    # Create an alean object to get its size and use it as a template
    alien = Alien(ai_settings, screen)

    # Get the number of aliens per row and the number of rows from the helper functions
    alien_count_x = get_alien_count_per_row(ai_settings, alien)
    row_count = get_row_count(ai_settings, ship, alien)

    # Create the fleet of aliens using two nested loops
    for row_index in range(row_count):
        for alien_index in range(alien_count_x):
            # Calculate the x and y coordinates of each alien using its width and height and the spacing constants
            x = ALIEN_SPACING_X * alien.rect.width * (0.5 + alien_index)
            y = ALIEN_SPACING_Y * alien.rect.height * \
                (0.5 + row_index) + ALIEN_MARGIN_Y * alien.rect.height
            # Call the create_alien function and pass the coordinates and other parameters
            create_alien(ai_settings, screen, aliens, x, y)


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


def update_aliens(ai_settings, aliens):
    """
    Check if the fleet is at an edge,
        and then update the positions of all aliens in the fleet.
    """
    # Change direction and drop down fleet if any alien reaches an edge
    check_fleet_edges(ai_settings, aliens)
    # Move all aliens horizontally according to their speed and direction
    aliens.update()
