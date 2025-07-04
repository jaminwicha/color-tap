import unittest
from unittest.mock import Mock, patch, MagicMock
import pygame
from game import Game
from shape_behaviors import Circle, Square
from nested_shapes import NestedShape
from config import Color
from collections import Counter

class TestEnhancedGameLogic(unittest.TestCase):
    
    def setUp(self):
        # Mock pygame to avoid actual window creation during tests
        pygame.init = Mock()
        pygame.display.set_mode = Mock()
        pygame.display.set_caption = Mock()
        pygame.time.Clock = Mock()
        
        with patch('game.LevelPersistence'), \
             patch.object(Game, 'load_or_create_level'):
            self.game = Game()
    
    def test_same_color_mass_elimination(self):
        """Test that ALL same-colored shapes are eliminated when two collide"""
        # Create multiple shapes of the same color
        red_shapes = [
            Mock(color=Color.RED, x=100, y=100),
            Mock(color=Color.RED, x=200, y=200), 
            Mock(color=Color.RED, x=300, y=300),
            Mock(color=Color.RED, x=400, y=400)
        ]
        
        # Create shapes of different colors
        blue_shape = Mock(color=Color.BLUE, x=500, y=500)
        green_shape = Mock(color=Color.GREEN, x=600, y=600)
        
        # Set up collision between first two red shapes
        red_shapes[0].is_colliding_with.return_value = True
        red_shapes[1].is_colliding_with.return_value = True
        
        # Set up non-colliding for other combinations
        for shape in red_shapes[2:] + [blue_shape, green_shape]:
            shape.is_colliding_with.return_value = False
        
        self.game.shapes = red_shapes + [blue_shape, green_shape]
        self.game.target_color = Color.RED
        
        # Trigger collision
        self.game.handle_same_color_collision(red_shapes[0], red_shapes[1])
        
        # All red shapes should be removed
        remaining_colors = [shape.color for shape in self.game.shapes]
        self.assertNotIn(Color.RED, remaining_colors)
        self.assertIn(Color.BLUE, remaining_colors)
        self.assertIn(Color.GREEN, remaining_colors)
        self.assertEqual(len(self.game.shapes), 2)
    
    def test_nested_shape_shell_removal(self):
        """Test that only outer shell is removed from nested shapes"""
        # Create a nested shape with multiple shells
        shells = [(Color.RED, 30), (Color.BLUE, 22), (Color.GREEN, 14)]
        nested_shape = NestedShape(200, 200, shells)
        regular_red_shape = Mock(color=Color.RED, x=100, y=100)
        blue_shape = Mock(color=Color.BLUE, x=300, y=300)
        
        self.game.shapes = [nested_shape, regular_red_shape, blue_shape]
        self.game.target_color = Color.RED
        
        # Trigger collision with red color
        self.game.handle_same_color_collision(regular_red_shape, blue_shape)
        
        # Nested shape should still exist but with one fewer shell
        self.assertIn(nested_shape, self.game.shapes)
        self.assertEqual(nested_shape.get_shell_count(), 2)  # Should have 2 shells left
        self.assertEqual(nested_shape.color, Color.BLUE)  # New outer shell should be blue
        
        # Regular red shape should be removed
        self.assertNotIn(regular_red_shape, self.game.shapes)
        
        # Blue shape should remain
        self.assertIn(blue_shape, self.game.shapes)
    
    def test_nested_shape_complete_removal(self):
        """Test that nested shape is completely removed when it has only one shell"""
        # Create a nested shape with only one shell
        shells = [(Color.RED, 25)]
        nested_shape = NestedShape(200, 200, shells)
        regular_red_shape = Mock(color=Color.RED, x=100, y=100)
        
        self.game.shapes = [nested_shape, regular_red_shape]
        self.game.target_color = Color.RED
        
        # Trigger collision with red color
        self.game.handle_same_color_collision(regular_red_shape, nested_shape)
        
        # Both shapes should be removed since nested shape had only one shell
        self.assertEqual(len(self.game.shapes), 0)
    
    def test_level_completion_validation(self):
        """Test proper level completion validation"""
        # Test case 1: All shapes eliminated with correct final color
        self.game.shapes = []
        self.game.last_merged_color = Color.RED
        self.game.target_color = Color.RED
        self.game.level_complete = False
        
        self.game.check_level_completion()
        self.assertTrue(self.game.level_complete)
        
        # Test case 2: All shapes eliminated with wrong final color
        self.game.shapes = []
        self.game.last_merged_color = Color.BLUE
        self.game.target_color = Color.RED
        self.game.level_complete = False
        self.game.show_impossible_popup = False
        
        self.game.check_level_completion()
        self.assertFalse(self.game.level_complete)
        self.assertTrue(self.game.show_impossible_popup)
        
        # Test case 3: Single shape remaining of target color
        target_shape = Mock(color=Color.RED)
        self.game.shapes = [target_shape]
        self.game.target_color = Color.RED
        self.game.level_complete = False
        
        self.game.check_level_completion()
        self.assertTrue(self.game.level_complete)
        
        # Test case 4: No target color shapes remaining
        blue_shape = Mock(color=Color.BLUE)
        self.game.shapes = [blue_shape]
        self.game.target_color = Color.RED
        self.game.level_complete = False
        self.game.show_impossible_popup = False
        
        self.game.check_level_completion()
        self.assertFalse(self.game.level_complete)
        self.assertTrue(self.game.show_impossible_popup)
    
    def test_collision_with_different_colors_bounces(self):
        """Test that different colored shapes bounce without elimination"""
        red_shape = Mock(color=Color.RED, x=100, y=100)
        blue_shape = Mock(color=Color.BLUE, x=120, y=120)
        
        red_shape.is_colliding_with.return_value = True
        blue_shape.is_colliding_with.return_value = True
        
        self.game.shapes = [red_shape, blue_shape]
        
        # Trigger collision check
        self.game.check_collisions()
        
        # Both shapes should remain
        self.assertEqual(len(self.game.shapes), 2)
        self.assertIn(red_shape, self.game.shapes)
        self.assertIn(blue_shape, self.game.shapes)
        
        # Bounce should have been called
        red_shape.bounce_off.assert_called_once_with(blue_shape)
    
    def test_impossibility_detection_during_gameplay(self):
        """Test that impossibility is detected during gameplay"""
        # Create a scenario where target color no longer exists
        blue_shape = Mock(color=Color.BLUE)
        green_shape = Mock(color=Color.GREEN)
        
        self.game.shapes = [blue_shape, green_shape]
        self.game.target_color = Color.RED
        self.game.show_impossible_popup = False
        
        self.game.check_level_possibility()
        self.assertTrue(self.game.show_impossible_popup)

if __name__ == '__main__':
    unittest.main()