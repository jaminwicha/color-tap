import unittest
import math
import pygame
from unittest.mock import Mock, patch
from shape_behaviors import Circle, Square, Triangle, Rectangle
from config import Color

class TestShapeBehaviors(unittest.TestCase):
    
    def setUp(self):
        self.circle = Circle(100, 100, Color.RED, 30)
        self.square = Square(200, 200, Color.BLUE, 25)
        self.triangle = Triangle(300, 300, Color.GREEN, 35)
        self.rectangle = Rectangle(400, 400, Color.YELLOW, 60, 40)
    
    def test_circle_creation(self):
        self.assertEqual(self.circle.x, 100)
        self.assertEqual(self.circle.y, 100)
        self.assertEqual(self.circle.color, Color.RED)
        self.assertEqual(self.circle.size, 30)
    
    def test_rectangle_creation(self):
        self.assertEqual(self.rectangle.x, 400)
        self.assertEqual(self.rectangle.y, 400)
        self.assertEqual(self.rectangle.color, Color.YELLOW)
        self.assertEqual(self.rectangle.width, 60)
        self.assertEqual(self.rectangle.height, 40)
    
    def test_circle_contains_point(self):
        # Point inside circle
        self.assertTrue(self.circle.contains_point(110, 110))
        # Point outside circle
        self.assertFalse(self.circle.contains_point(150, 150))
        # Point on edge (approximately)
        self.assertTrue(self.circle.contains_point(129, 100))
    
    def test_square_contains_point(self):
        # Point inside square
        self.assertTrue(self.square.contains_point(210, 210))
        # Point outside square
        self.assertFalse(self.square.contains_point(250, 250))
    
    def test_rectangle_contains_point(self):
        # Point inside rectangle
        self.assertTrue(self.rectangle.contains_point(420, 410))
        # Point outside rectangle
        self.assertFalse(self.rectangle.contains_point(470, 430))
    
    def test_collision_detection(self):
        # Create two circles that should collide
        circle1 = Circle(100, 100, Color.RED, 30)
        circle2 = Circle(140, 100, Color.BLUE, 30)  # 40 pixels apart, radii sum to 60
        self.assertTrue(circle1.is_colliding_with(circle2))
        
        # Create two circles that shouldn't collide
        circle3 = Circle(100, 100, Color.RED, 30)
        circle4 = Circle(200, 100, Color.BLUE, 30)  # 100 pixels apart, radii sum to 60
        self.assertFalse(circle3.is_colliding_with(circle4))
    
    def test_get_distance_between_shapes(self):
        circle1 = Circle(0, 0, Color.RED, 10)
        circle2 = Circle(3, 4, Color.BLUE, 10)  # 3-4-5 triangle
        distance = circle1.get_distance_to(circle2)
        self.assertAlmostEqual(distance, 5.0, places=1)
    
    def test_collision_radius(self):
        self.assertEqual(self.circle.get_collision_radius(), 30)
        self.assertEqual(self.square.get_collision_radius(), 25)
        self.assertEqual(self.rectangle.get_collision_radius(), 30)  # max(60, 40) // 2
    
    def test_max_dimension(self):
        self.assertEqual(self.circle.get_max_dimension(), 30)
        self.assertEqual(self.square.get_max_dimension(), 25)
        self.assertEqual(self.rectangle.get_max_dimension(), 60)  # max(60, 40)
    
    @patch('pygame.draw.circle')
    def test_circle_draw(self, mock_draw_circle):
        mock_screen = Mock()
        self.circle.draw(mock_screen)
        # New drawing method calls circle multiple times for bevel effect
        self.assertGreater(mock_draw_circle.call_count, 1)
        # Check that the main circle call is made
        mock_draw_circle.assert_any_call(mock_screen, Color.RED, (100, 100), 30)
    
    @patch('pygame.draw.rect')
    def test_square_draw(self, mock_draw_rect):
        mock_screen = Mock()
        self.square.draw(mock_screen)
        # Check that draw was called with the square
        self.assertGreater(mock_draw_rect.call_count, 0)
        # Check that the main rect call is made
        mock_draw_rect.assert_any_call(mock_screen, Color.BLUE, pygame.Rect(175, 175, 50, 50))
    
    @patch('pygame.draw.rect')
    def test_rectangle_draw(self, mock_draw_rect):
        mock_screen = Mock()
        self.rectangle.draw(mock_screen)
        # Check that draw was called with the rectangle
        self.assertGreater(mock_draw_rect.call_count, 0)
        # Check that the main rect call is made
        mock_draw_rect.assert_any_call(mock_screen, Color.YELLOW, pygame.Rect(370, 380, 60, 40))
    
    def test_bounce_physics(self):
        circle1 = Circle(100, 100, Color.RED, 30)
        circle2 = Circle(150, 100, Color.BLUE, 30)
        
        # Set initial velocities
        circle1.velocity_x = 5
        circle1.velocity_y = 0
        circle2.velocity_x = -5
        circle2.velocity_y = 0
        
        # Store initial velocities
        initial_v1x = circle1.velocity_x
        initial_v2x = circle2.velocity_x
        
        # Apply bounce
        circle1.bounce_off(circle2)
        
        # Velocities should change due to bounce
        self.assertNotEqual(circle1.velocity_x, initial_v1x)
        self.assertNotEqual(circle2.velocity_x, initial_v2x)
    
    def test_shape_update_physics(self):
        circle = Circle(100, 100, Color.RED, 30)
        circle.velocity_x = 10
        circle.velocity_y = 5
        
        initial_x = circle.x
        initial_y = circle.y
        
        circle.update()
        
        # Position should change based on velocity
        self.assertGreater(circle.x, initial_x)
        self.assertGreater(circle.y, initial_y)
        
        # Velocity should be reduced by friction
        self.assertLess(abs(circle.velocity_x), 10)
        self.assertLess(abs(circle.velocity_y), 5)

if __name__ == '__main__':
    unittest.main()