"""
Car Module - Handles car physics, controls, and rendering
"""
import pygame
import math
import numpy as np

class Car:
    """
    Car class that handles car physics, controls, and rendering.
    Implements simple physics for acceleration, deceleration, and steering.
    """
    
    def __init__(self, is_player=True, x=400, y=300):
        """
        Initialize the car with position and properties.
        
        Args:
            is_player (bool): Whether this car is controlled by the player
            x (int): Initial x position
            y (int): Initial y position
        """
        self.is_player = is_player
        self.x = x
        self.y = y
        self.angle = 0  # Angle in radians
        self.speed = 0
        self.acceleration = 0
        
        # Car properties
        self.max_speed = 10
        self.max_reverse_speed = -5
        self.acceleration_rate = 0.1
        self.deceleration_rate = 0.05
        self.steering_rate = 0.1
        self.friction = 0.02
        
        # Car dimensions
        self.width = 40
        self.height = 20
        
        # Car state
        self.is_accelerating = False
        self.is_braking = False
        self.is_turning_left = False
        self.is_turning_right = False
        
        # AI properties (if not player)
        if not is_player:
            self.ai_reaction_time = 0.5
            self.ai_accuracy = 0.8
            self.ai_last_decision_time = 0
        
        # Temporary car image (will be replaced with pixel art)
        self.image = self._create_temp_car_image()
        self.rect = self.image.get_rect(center=(self.x, self.y))
    
    def _create_temp_car_image(self):
        """Create a temporary car image for development."""
        car_image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        if self.is_player:
            color = (0, 0, 255)  # Blue for player
        else:
            color = (255, 0, 0)  # Red for AI
        
        # Draw car body
        pygame.draw.rect(car_image, color, (0, 0, self.width, self.height))
        # Draw car details
        pygame.draw.rect(car_image, (0, 0, 0), (self.width-10, 5, 5, 5))
        pygame.draw.rect(car_image, (0, 0, 0), (self.width-10, self.height-10, 5, 5))
        
        return car_image
    
    def update(self, keys, track, elapsed_time):
        """
        Update car state based on input, track, and elapsed time.
        
        Args:
            keys: Pressed keys for player input
            track: Track object for collision detection
            elapsed_time: Time elapsed since game start
        """
        if self.is_player:
            self._handle_player_input(keys)
        else:
            self._handle_ai_behavior(track, elapsed_time)
        
        # Apply physics
        self._apply_physics()
        
        # Update position
        self._update_position()
        
        # Update car image and rect
        self._update_image()
    
    def _handle_player_input(self, keys):
        """
        Handle player input from keyboard.
        
        Args:
            keys: Pressed keys
        """
        # Reset state
        self.is_accelerating = False
        self.is_braking = False
        self.is_turning_left = False
        self.is_turning_right = False
        
        # Check keys
        if keys[pygame.K_UP]:
            self.is_accelerating = True
        if keys[pygame.K_DOWN]:
            self.is_braking = True
        if keys[pygame.K_LEFT]:
            self.is_turning_left = True
        if keys[pygame.K_RIGHT]:
            self.is_turning_right = True
    
    def _handle_ai_behavior(self, track, elapsed_time):
        """
        Handle AI car behavior based on track and game state.
        
        Args:
            track: Track object for navigation
            elapsed_time: Time elapsed since game start
        """
        # This will be implemented with AI driving logic
        # For now, just make the AI car move forward
        self.is_accelerating = True
    
    def _apply_physics(self):
        """Apply physics to car movement including acceleration, friction, and steering."""
        # Handle acceleration and braking
        if self.is_accelerating:
            self.acceleration = self.acceleration_rate
        elif self.is_braking:
            self.acceleration = -self.deceleration_rate
        else:
            self.acceleration = 0
        
        # Apply acceleration to speed
        self.speed += self.acceleration
        
        # Apply friction
        if self.speed > 0:
            self.speed -= self.friction
            if self.speed < 0:
                self.speed = 0
        elif self.speed < 0:
            self.speed += self.friction
            if self.speed > 0:
                self.speed = 0
        
        # Clamp speed to limits
        self.speed = max(self.max_reverse_speed, min(self.max_speed, self.speed))
        
        # Handle steering (only when moving)
        if abs(self.speed) > 0.1:
            steering_factor = self.steering_rate * (self.speed / self.max_speed)
            if self.is_turning_left:
                self.angle -= steering_factor
            if self.is_turning_right:
                self.angle += steering_factor
    
    def _update_position(self):
        """Update car position based on speed and angle."""
        # Calculate movement vector
        dx = math.cos(self.angle) * self.speed
        dy = math.sin(self.angle) * self.speed
        
        # Update position
        self.x += dx
        self.y += dy
    
    def _update_image(self):
        """Update car image and rect based on current state."""
        # Rotate the original image
        rotated_image = pygame.transform.rotate(self.image, -math.degrees(self.angle))
        
        # Update the rect
        self.rect = rotated_image.get_rect(center=(self.x, self.y))
        
        # Store the rotated image for rendering
        self.rotated_image = rotated_image
    
    def render(self, screen):
        """
        Render the car to the screen.
        
        Args:
            screen: Pygame screen surface to render on
        """
        screen.blit(self.rotated_image, self.rect.topleft)
    
    def get_collision_rect(self):
        """Get the collision rectangle for the car."""
        return self.rect
    
    def get_position(self):
        """Get the current position of the car."""
        return (self.x, self.y)
    
    def get_speed(self):
        """Get the current speed of the car."""
        return self.speed
    
    def apply_boost(self, boost_factor=1.5, duration=2.0):
        """
        Apply a speed boost to the car.
        
        Args:
            boost_factor: Factor to multiply max_speed by
            duration: Duration of boost in seconds
        """
        # This will be implemented with the power-up system
        pass
