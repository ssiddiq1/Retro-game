"""
Track Module - Handles track generation, rendering, and collision detection
"""
import pygame
import numpy as np
import random
import math

class Track:
    """
    Track class that handles track generation, rendering, and collision detection.
    Implements procedural track generation with randomized turns.
    """
    
    def __init__(self, width=800, height=600, complexity=0.5):
        """
        Initialize the track with dimensions and properties.
        
        Args:
            width (int): Screen width
            height (int): Screen height
            complexity (float): Track complexity from 0.0 to 1.0
        """
        self.width = width
        self.height = height
        self.complexity = complexity
        
        # Track properties
        self.track_width = 100  # Width of the track
        self.border_color = (255, 255, 255)  # White borders
        self.road_color = (50, 50, 50)  # Dark gray road
        
        # Track points define the center line of the track
        self.track_points = []
        
        # Track boundaries (inner and outer)
        self.inner_boundary = []
        self.outer_boundary = []
        
        # Checkpoints for lap counting
        self.checkpoints = []
        
        # Start/finish line
        self.start_line = None
        
        # Generate the track
        self._generate_track()
        
        # Create track surface
        self.track_surface = self._create_track_surface()
    
    def _generate_track(self):
        """Generate a procedural track with randomized turns."""
        # For now, create a simple oval track
        # This will be replaced with procedural generation in step 004
        
        # Center of the screen
        center_x = self.width // 2
        center_y = self.height // 2
        
        # Oval dimensions
        oval_width = self.width * 0.7
        oval_height = self.height * 0.7
        
        # Generate points around an oval
        num_points = 20
        self.track_points = []
        
        for i in range(num_points):
            angle = 2 * math.pi * i / num_points
            x = center_x + (oval_width / 2) * math.cos(angle)
            y = center_y + (oval_height / 2) * math.sin(angle)
            self.track_points.append((x, y))
        
        # Generate inner and outer boundaries
        self._generate_boundaries()
        
        # Generate checkpoints
        self._generate_checkpoints()
        
        # Set start/finish line
        self.start_line = (self.track_points[0], self.track_points[-1])
    
    def _generate_boundaries(self):
        """Generate inner and outer track boundaries based on track points."""
        self.inner_boundary = []
        self.outer_boundary = []
        
        for i in range(len(self.track_points)):
            # Get current point and next point
            current = self.track_points[i]
            next_idx = (i + 1) % len(self.track_points)
            next_point = self.track_points[next_idx]
            
            # Calculate direction vector
            dx = next_point[0] - current[0]
            dy = next_point[1] - current[1]
            
            # Normalize direction vector
            length = math.sqrt(dx*dx + dy*dy)
            if length > 0:
                dx /= length
                dy /= length
            
            # Calculate perpendicular vector
            perpendicular_x = -dy
            perpendicular_y = dx
            
            # Calculate inner and outer points
            half_width = self.track_width / 2
            inner_x = current[0] - perpendicular_x * half_width
            inner_y = current[1] - perpendicular_y * half_width
            outer_x = current[0] + perpendicular_x * half_width
            outer_y = current[1] + perpendicular_y * half_width
            
            # Add to boundaries
            self.inner_boundary.append((inner_x, inner_y))
            self.outer_boundary.append((outer_x, outer_y))
    
    def _generate_checkpoints(self):
        """Generate checkpoints for lap counting."""
        # Use track points as checkpoints
        self.checkpoints = self.track_points.copy()
    
    def _create_track_surface(self):
        """Create a surface with the track drawn on it."""
        # Create a surface for the track
        track_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        
        # Draw the road
        if len(self.outer_boundary) > 2:
            pygame.draw.polygon(track_surface, self.road_color, self.outer_boundary + list(reversed(self.inner_boundary)))
        
        # Draw the borders
        if len(self.outer_boundary) > 1:
            pygame.draw.lines(track_surface, self.border_color, True, self.outer_boundary, 2)
            pygame.draw.lines(track_surface, self.border_color, True, self.inner_boundary, 2)
        
        # Draw start/finish line
        if self.start_line:
            pygame.draw.line(track_surface, (255, 0, 0), self.start_line[0], self.start_line[1], 3)
        
        return track_surface
    
    def render(self, screen):
        """
        Render the track to the screen.
        
        Args:
            screen: Pygame screen surface to render on
        """
        screen.blit(self.track_surface, (0, 0))
    
    def check_collision(self, car_rect):
        """
        Check if car collides with track boundaries.
        
        Args:
            car_rect: Rectangle representing car collision area
            
        Returns:
            bool: True if collision detected, False otherwise
        """
        # This will be implemented with proper collision detection in step 002
        # For now, return False (no collision)
        return False
    
    def get_checkpoint_index(self, position):
        """
        Get the index of the nearest checkpoint to the given position.
        
        Args:
            position: (x, y) position to check
            
        Returns:
            int: Index of the nearest checkpoint
        """
        # Find the nearest checkpoint
        min_distance = float('inf')
        nearest_idx = 0
        
        for i, checkpoint in enumerate(self.checkpoints):
            dx = position[0] - checkpoint[0]
            dy = position[1] - checkpoint[1]
            distance = math.sqrt(dx*dx + dy*dy)
            
            if distance < min_distance:
                min_distance = distance
                nearest_idx = i
        
        return nearest_idx
    
    def is_on_start_line(self, position, threshold=20):
        """
        Check if position is on the start/finish line.
        
        Args:
            position: (x, y) position to check
            threshold: Distance threshold
            
        Returns:
            bool: True if on start line, False otherwise
        """
        if not self.start_line:
            return False
        
        # Calculate distance to line segment
        x, y = position
        x1, y1 = self.start_line[0]
        x2, y2 = self.start_line[1]
        
        # Line segment length squared
        l2 = (x2 - x1)**2 + (y2 - y1)**2
        
        # If line segment is a point, calculate distance to that point
        if l2 == 0:
            return math.sqrt((x - x1)**2 + (y - y1)**2) <= threshold
        
        # Calculate projection of point onto line segment
        t = max(0, min(1, ((x - x1) * (x2 - x1) + (y - y1) * (y2 - y1)) / l2))
        
        # Calculate closest point on line segment
        px = x1 + t * (x2 - x1)
        py = y1 + t * (y2 - y1)
        
        # Calculate distance to closest point
        distance = math.sqrt((x - px)**2 + (y - py)**2)
        
        return distance <= threshold
