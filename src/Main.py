"""
Retro Racing Game - Main Game Loop
A simple 1-player 2D retro racing game with an AI-driven car on a looping track.
"""
import pygame
import sys
import time
from game_engine import GameEngine
from car import Car
from track import Track
from ui import UI

# Initialize pygame
pygame.init()

# Game constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GAME_TITLE = "Retro Racing Game"
FPS = 60
TIME_LIMIT = 120  # seconds

def main():
    """Main game function that initializes and runs the game loop."""
    # Set up the display
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(GAME_TITLE)
    clock = pygame.time.Clock()
    
    # Initialize game components
    track = Track()
    player_car = Car(is_player=True)
    game_engine = GameEngine(track, player_car)
    ui = UI(screen)
    
    # Game state variables
    running = True
    game_time = 0
    start_time = time.time()
    
    # Main game loop
    while running:
        # Calculate elapsed time
        current_time = time.time()
        elapsed_time = current_time - start_time
        remaining_time = max(0, TIME_LIMIT - elapsed_time)
        
        # Process events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        # Update game state
        keys = pygame.key.get_pressed()
        game_engine.update(keys, elapsed_time)
        
        # Check if time limit reached
        if remaining_time <= 0:
            running = False
        
        # Render the game
        screen.fill((0, 0, 0))  # Clear screen with black
        game_engine.render(screen)
        ui.render(screen, game_engine.lap_count, remaining_time, game_engine.best_lap_time)
        
        # Update the display
        pygame.display.flip()
        
        # Cap the frame rate
        clock.tick(FPS)
    
    # Game over
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
