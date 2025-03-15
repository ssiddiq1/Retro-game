"""
UI Module - Handles game user interface elements and rendering
"""
import pygame
import math

class UI:
    """
    UI class that handles game user interface elements and rendering.
    Displays lap count, time remaining, and best lap time.
    """
    
    def __init__(self, screen):
        """
        Initialize the UI with screen dimensions.
        
        Args:
            screen: Pygame screen surface
        """
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        
        # UI colors
        self.text_color = (255, 255, 255)  # White text
        self.background_color = (0, 0, 0, 128)  # Semi-transparent black
        self.highlight_color = (255, 255, 0)  # Yellow for highlights
        
        # UI fonts
        pygame.font.init()
        self.font_large = pygame.font.SysFont('Arial', 36)
        self.font_medium = pygame.font.SysFont('Arial', 24)
        self.font_small = pygame.font.SysFont('Arial', 18)
        
        # UI positions
        self.top_margin = 20
        self.side_margin = 20
        
        # Create UI surfaces
        self._create_ui_surfaces()
    
    def _create_ui_surfaces(self):
        """Create UI surface elements."""
        # Top bar background
        self.top_bar = pygame.Surface((self.screen_width, 60), pygame.SRCALPHA)
        self.top_bar.fill(self.background_color)
        
        # Game over screen
        self.game_over_surface = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        self.game_over_surface.fill((0, 0, 0, 200))  # Dark semi-transparent background
    
    def render(self, screen, lap_count, remaining_time, best_lap_time):
        """
        Render UI elements to the screen.
        
        Args:
            screen: Pygame screen surface to render on
            lap_count: Current lap count
            remaining_time: Time remaining in seconds
            best_lap_time: Best lap time in seconds
        """
        # Draw top bar
        screen.blit(self.top_bar, (0, 0))
        
        # Format time remaining as MM:SS
        minutes = int(remaining_time) // 60
        seconds = int(remaining_time) % 60
        time_str = f"Time: {minutes:02d}:{seconds:02d}"
        
        # Format best lap time
        if best_lap_time == float('inf'):
            best_lap_str = "Best Lap: --:--"
        else:
            best_minutes = int(best_lap_time) // 60
            best_seconds = int(best_lap_time) % 60
            best_ms = int((best_lap_time - int(best_lap_time)) * 100)
            best_lap_str = f"Best Lap: {best_minutes:02d}:{best_seconds:02d}.{best_ms:02d}"
        
        # Render text
        lap_text = self.font_medium.render(f"Lap: {lap_count}", True, self.text_color)
        time_text = self.font_medium.render(time_str, True, self.text_color)
        best_lap_text = self.font_medium.render(best_lap_str, True, self.text_color)
        
        # Position text
        screen.blit(lap_text, (self.side_margin, self.top_margin))
        screen.blit(time_text, (self.screen_width // 2 - time_text.get_width() // 2, self.top_margin))
        screen.blit(best_lap_text, (self.screen_width - best_lap_text.get_width() - self.side_margin, self.top_margin))
        
        # If time is running out, flash the time
        if remaining_time < 10 and int(remaining_time * 2) % 2 == 0:
            time_text = self.font_medium.render(time_str, True, self.highlight_color)
            screen.blit(time_text, (self.screen_width // 2 - time_text.get_width() // 2, self.top_margin))
    
    def render_game_over(self, screen, lap_count, best_lap_time):
        """
        Render game over screen.
        
        Args:
            screen: Pygame screen surface to render on
            lap_count: Final lap count
            best_lap_time: Best lap time in seconds
        """
        # Draw game over background
        screen.blit(self.game_over_surface, (0, 0))
        
        # Render game over text
        game_over_text = self.font_large.render("GAME OVER", True, self.highlight_color)
        
        # Format best lap time
        if best_lap_time == float('inf'):
            best_lap_str = "Best Lap: --:--"
        else:
            best_minutes = int(best_lap_time) // 60
            best_seconds = int(best_lap_time) % 60
            best_ms = int((best_lap_time - int(best_lap_time)) * 100)
            best_lap_str = f"Best Lap: {best_minutes:02d}:{best_seconds:02d}.{best_ms:02d}"
        
        # Render stats text
        laps_text = self.font_medium.render(f"Laps Completed: {lap_count}", True, self.text_color)
        best_lap_text = self.font_medium.render(best_lap_str, True, self.text_color)
        restart_text = self.font_medium.render("Press SPACE to restart", True, self.text_color)
        
        # Position text
        center_x = self.screen_width // 2
        center_y = self.screen_height // 2
        
        screen.blit(game_over_text, (center_x - game_over_text.get_width() // 2, center_y - 100))
        screen.blit(laps_text, (center_x - laps_text.get_width() // 2, center_y - 20))
        screen.blit(best_lap_text, (center_x - best_lap_text.get_width() // 2, center_y + 20))
        screen.blit(restart_text, (center_x - restart_text.get_width() // 2, center_y + 100))
    
    def render_start_screen(self, screen):
        """
        Render start screen.
        
        Args:
            screen: Pygame screen surface to render on
        """
        # Draw start screen background
        screen.fill((0, 0, 0))  # Black background
        
        # Render title text
        title_text = self.font_large.render("RETRO RACING GAME", True, self.highlight_color)
        
        # Render instructions
        instructions1 = self.font_medium.render("Arrow Keys to Drive", True, self.text_color)
        instructions2 = self.font_medium.render("Complete as many laps as possible before time runs out!", True, self.text_color)
        start_text = self.font_medium.render("Press SPACE to start", True, self.text_color)
        
        # Position text
        center_x = self.screen_width // 2
        center_y = self.screen_height // 2
        
        screen.blit(title_text, (center_x - title_text.get_width() // 2, center_y - 100))
        screen.blit(instructions1, (center_x - instructions1.get_width() // 2, center_y - 20))
        screen.blit(instructions2, (center_x - instructions2.get_width() // 2, center_y + 20))
        screen.blit(start_text, (center_x - start_text.get_width() // 2, center_y + 100))
