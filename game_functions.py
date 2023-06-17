import sys

import pygame

from bullet import Bullet


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


def update_screen(ai_settings, screen, ship, alien, bullets):
    """Redraw the screen during each pass through the loop."""

    # Fills the entire screen with the color.
    screen.fill(ai_settings.bg_color)

    # draw the ship on the screen.
    ship.blitme()
    alien.blitme()

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
