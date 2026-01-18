"""
Dragon Haven Cafe - Entry Point
A dragon-raising cafe management simulation game.
"""

import pygame
import sys

from constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, TITLE, BLACK, WHITE


def main():
    """Main entry point for Dragon Haven Cafe."""
    # Initialize pygame
    pygame.init()

    # Create display
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(TITLE)

    # Create clock for FPS control
    clock = pygame.time.Clock()

    # Placeholder font for initial display
    font = pygame.font.Font(None, 48)
    small_font = pygame.font.Font(None, 24)

    # Main loop
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        # Clear screen
        screen.fill(BLACK)

        # Draw placeholder content
        title_text = font.render("Dragon Haven Cafe", True, WHITE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        screen.blit(title_text, title_rect)

        subtitle_text = small_font.render("Project Setup Complete - Press ESC to exit", True, (150, 150, 150))
        subtitle_rect = subtitle_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
        screen.blit(subtitle_text, subtitle_rect)

        # Update display
        pygame.display.flip()

        # Cap framerate
        clock.tick(FPS)

    # Cleanup
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
