import sys
import pygame
from bullet import Bullet
from alien import Alien


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


def get_number_of_aliens(ai_settings, alien_width):
    """Determines the number of aliens that fit in a row."""
    available_space_x = (ai_settings.screen_width - 2 * alien_width)
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def get_number_rows(ai_settings, ship_height, alien_height):
    """Determine the number of rows of aliens that fit on the screen."""
    available_space_y = (ai_settings.screen_height -
                         (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def create_alien(ai_settings, screen, aliens, alien_number, alien_width, row_number):
    """Creates an alien and place it in the row."""
    # Create an alien and place it in the row.
    alien = Alien(ai_settings, screen)
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens):
    """Create a full fleet of aliens."""
    # Create an alean and find the number of aleans in a row.
    # Spacing between each alien is equal to the number of alean width.
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_of_aliens(ai_settings, alien.rect.width)
    number_rows = get_number_rows(
        ai_settings, ship.rect.height, alien.rect.height)

    # Create the fleet of aliens.
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens,
                         alien_number, alien.rect.width, row_number)
