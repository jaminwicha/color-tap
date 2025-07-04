import unittest
from unittest.mock import patch
from shape_factory import ShapeFactory
from shape_behaviors import Circle, Square, Triangle, Rectangle
from config import Color, AVAILABLE_COLORS

class TestShapeFactory(unittest.TestCase):
    
    def test_create_circle(self):
        circle = ShapeFactory.create_circle(100, 200, Color.RED, 25)
        
        self.assertIsInstance(circle, Circle)
        self.assertEqual(circle.x, 100)
        self.assertEqual(circle.y, 200)
        self.assertEqual(circle.color, Color.RED)
        self.assertEqual(circle.size, 25)
    
    def test_create_square(self):
        square = ShapeFactory.create_square(150, 250, Color.BLUE, 30)
        
        self.assertIsInstance(square, Square)
        self.assertEqual(square.x, 150)
        self.assertEqual(square.y, 250)
        self.assertEqual(square.color, Color.BLUE)
        self.assertEqual(square.size, 30)
    
    def test_create_triangle(self):
        triangle = ShapeFactory.create_triangle(200, 300, Color.GREEN, 35)
        
        self.assertIsInstance(triangle, Triangle)
        self.assertEqual(triangle.x, 200)
        self.assertEqual(triangle.y, 300)
        self.assertEqual(triangle.color, Color.GREEN)
        self.assertEqual(triangle.size, 35)
    
    def test_create_rectangle(self):
        rectangle = ShapeFactory.create_rectangle(250, 350, Color.YELLOW, 60, 40)
        
        self.assertIsInstance(rectangle, Rectangle)
        self.assertEqual(rectangle.x, 250)
        self.assertEqual(rectangle.y, 350)
        self.assertEqual(rectangle.color, Color.YELLOW)
        self.assertEqual(rectangle.width, 60)
        self.assertEqual(rectangle.height, 40)
    
    @patch('random.randint')
    def test_create_circle_with_random_size(self, mock_randint):
        mock_randint.return_value = 25
        
        circle = ShapeFactory.create_circle(100, 200, Color.RED)
        
        self.assertEqual(circle.size, 25)
        mock_randint.assert_called_once()
    
    @patch('random.randint')
    def test_create_rectangle_with_random_dimensions(self, mock_randint):
        # Mock returns different values for width and height calls
        mock_randint.side_effect = [60, 40]
        
        rectangle = ShapeFactory.create_rectangle(100, 200, Color.RED)
        
        self.assertEqual(rectangle.width, 60)
        self.assertEqual(rectangle.height, 40)
        self.assertEqual(mock_randint.call_count, 2)
    
    @patch('random.choice')
    def test_create_random_shape_with_provided_color(self, mock_choice):
        # Mock choice to always return the circle creator function
        mock_choice.return_value = ShapeFactory._create_circle
        
        shape = ShapeFactory.create_random_shape(100, 200, Color.PURPLE)
        
        self.assertIsInstance(shape, Circle)
        self.assertEqual(shape.color, Color.PURPLE)
    
    @patch('random.choice')
    def test_create_random_shape_with_random_color(self, mock_choice):
        # First call returns color, second returns shape creator
        mock_choice.side_effect = [Color.ORANGE, ShapeFactory._create_square]
        
        shape = ShapeFactory.create_random_shape(100, 200)
        
        self.assertIsInstance(shape, Square)
        self.assertEqual(shape.color, Color.ORANGE)
        self.assertEqual(mock_choice.call_count, 2)
    
    def test_all_shape_types_can_be_created(self):
        """Test that factory can create all shape types"""
        
        # Test each shape type directly
        circle = ShapeFactory.create_circle(0, 0, Color.RED)
        square = ShapeFactory.create_square(0, 0, Color.RED)
        triangle = ShapeFactory.create_triangle(0, 0, Color.RED)
        rectangle = ShapeFactory.create_rectangle(0, 0, Color.RED)
        
        self.assertIsInstance(circle, Circle)
        self.assertIsInstance(square, Square)
        self.assertIsInstance(triangle, Triangle)
        self.assertIsInstance(rectangle, Rectangle)
    
    def test_random_shape_creates_valid_shapes(self):
        """Test that random shape creation produces valid shape objects"""
        for _ in range(10):  # Test multiple random creations
            shape = ShapeFactory.create_random_shape(100, 200, Color.RED)
            
            # Should be one of the valid shape types
            self.assertIn(type(shape), [Circle, Square, Triangle, Rectangle])
            self.assertEqual(shape.x, 100)
            self.assertEqual(shape.y, 200)
            self.assertEqual(shape.color, Color.RED)
    
    def test_shape_size_ranges(self):
        """Test that shapes are created with sizes in expected ranges"""
        # Create multiple shapes to test size randomization
        shapes = [ShapeFactory.create_circle(0, 0, Color.RED) for _ in range(10)]
        
        for shape in shapes:
            self.assertGreaterEqual(shape.size, 20)  # min_shape_size
            self.assertLessEqual(shape.size, 40)     # max_shape_size
    
    def test_rectangle_dimension_ranges(self):
        """Test that rectangles have dimensions in expected ranges"""
        rectangles = [ShapeFactory.create_rectangle(0, 0, Color.RED) for _ in range(10)]
        
        for rect in rectangles:
            self.assertGreaterEqual(rect.width, 20)
            self.assertLessEqual(rect.width, 80)
            self.assertGreaterEqual(rect.height, 15)
            self.assertLessEqual(rect.height, 60)

if __name__ == '__main__':
    unittest.main()