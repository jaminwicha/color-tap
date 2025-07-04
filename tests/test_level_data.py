import unittest
import os
import tempfile
import json
from unittest.mock import Mock, patch
from level_data import LevelData, LevelPersistence
from shape_behaviors import Circle, Square, Rectangle
from config import Color

class TestLevelData(unittest.TestCase):
    
    def setUp(self):
        self.shapes = [
            Circle(100, 100, Color.RED, 30),
            Square(200, 200, Color.BLUE, 25),
            Rectangle(300, 300, Color.GREEN, 60, 40)
        ]
        self.level_data = LevelData("test123", self.shapes, Color.RED, "FRACTAL_SPIRAL")
    
    def test_level_data_creation(self):
        self.assertEqual(self.level_data.level_id, "test123")
        self.assertEqual(self.level_data.target_color, Color.RED)
        self.assertEqual(self.level_data.algorithm_used, "FRACTAL_SPIRAL")
        self.assertEqual(len(self.level_data.shapes), 3)
        self.assertIsNotNone(self.level_data.created_at)
    
    def test_shape_to_dict_circle(self):
        circle = Circle(100, 100, Color.RED, 30)
        shape_dict = self.level_data.shape_to_dict(circle)
        
        expected = {
            'x': 100,
            'y': 100,
            'shape_type': 'Circle',
            'color': list(Color.RED),
            'size': 30
        }
        self.assertEqual(shape_dict, expected)
    
    def test_shape_to_dict_rectangle(self):
        rectangle = Rectangle(200, 200, Color.BLUE, 60, 40)
        shape_dict = self.level_data.shape_to_dict(rectangle)
        
        expected = {
            'x': 200,
            'y': 200,
            'shape_type': 'Rectangle',
            'color': list(Color.BLUE),
            'size': 30,  # Rectangle inherits default size from parent
            'width': 60,
            'height': 40
        }
        self.assertEqual(shape_dict, expected)
    
    def test_dict_to_shape_circle(self):
        shape_dict = {
            'x': 150,
            'y': 150,
            'shape_type': 'Circle',
            'color': list(Color.GREEN),
            'size': 25
        }
        
        shape = self.level_data.dict_to_shape(shape_dict)
        
        self.assertIsInstance(shape, Circle)
        self.assertEqual(shape.x, 150)
        self.assertEqual(shape.y, 150)
        self.assertEqual(shape.color, Color.GREEN)
        self.assertEqual(shape.size, 25)
    
    def test_dict_to_shape_rectangle(self):
        shape_dict = {
            'x': 250,
            'y': 250,
            'shape_type': 'Rectangle',
            'color': list(Color.YELLOW),
            'width': 50,
            'height': 30
        }
        
        shape = self.level_data.dict_to_shape(shape_dict)
        
        self.assertIsInstance(shape, Rectangle)
        self.assertEqual(shape.x, 250)
        self.assertEqual(shape.y, 250)
        self.assertEqual(shape.color, Color.YELLOW)
        self.assertEqual(shape.width, 50)
        self.assertEqual(shape.height, 30)
    
    def test_dict_to_shape_unknown_type(self):
        shape_dict = {
            'x': 100,
            'y': 100,
            'shape_type': 'Unknown',
            'color': list(Color.RED)
        }
        
        with self.assertRaises(ValueError):
            self.level_data.dict_to_shape(shape_dict)
    
    def test_to_dict(self):
        data_dict = self.level_data.to_dict()
        
        self.assertEqual(data_dict['level_id'], "test123")
        self.assertEqual(data_dict['target_color'], list(Color.RED))
        self.assertEqual(data_dict['algorithm_used'], "FRACTAL_SPIRAL")
        self.assertIn('created_at', data_dict)
        self.assertIn('original_shapes', data_dict)
        self.assertEqual(len(data_dict['original_shapes']), 3)
    
    def test_from_dict(self):
        data_dict = {
            'level_id': 'restored123',
            'target_color': Color.BLUE,
            'algorithm_used': 'FIBONACCI_SPIRAL',
            'created_at': '2023-01-01T00:00:00',
            'original_shapes': [
                {
                    'x': 100,
                    'y': 100,
                    'shape_type': 'Circle',
                    'color': Color.RED,
                    'size': 30
                }
            ]
        }
        
        level_data = LevelData.from_dict(data_dict)
        
        self.assertEqual(level_data.level_id, 'restored123')
        self.assertEqual(level_data.target_color, Color.BLUE)
        self.assertEqual(level_data.algorithm_used, 'FIBONACCI_SPIRAL')
        self.assertEqual(level_data.created_at, '2023-01-01T00:00:00')
        self.assertEqual(len(level_data.original_shapes), 1)
    
    def test_get_fresh_shapes(self):
        fresh_shapes = self.level_data.get_fresh_shapes()
        
        self.assertEqual(len(fresh_shapes), 3)
        self.assertIsInstance(fresh_shapes[0], Circle)
        self.assertIsInstance(fresh_shapes[1], Square)
        self.assertIsInstance(fresh_shapes[2], Rectangle)
        
        # Should be new instances, not the same objects
        self.assertIsNot(fresh_shapes[0], self.shapes[0])


class TestLevelPersistence(unittest.TestCase):
    
    def setUp(self):
        # Use temporary directory for testing
        self.temp_dir = tempfile.mkdtemp()
        self.persistence = LevelPersistence(self.temp_dir)
        
        self.shapes = [
            Circle(100, 100, Color.RED, 30),
            Square(200, 200, Color.BLUE, 25)
        ]
        self.level_data = LevelData("test123", self.shapes, Color.RED, "FRACTAL_SPIRAL")
    
    def tearDown(self):
        # Clean up temporary directory
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_save_and_load_level(self):
        # Save level
        self.persistence.save_level(self.level_data)
        
        # Check file was created
        filename = f"{self.temp_dir}/level_test123.json"
        self.assertTrue(os.path.exists(filename))
        
        # Load level
        loaded_level = self.persistence.load_level("test123")
        
        self.assertIsNotNone(loaded_level)
        self.assertEqual(loaded_level.level_id, "test123")
        self.assertEqual(loaded_level.target_color, Color.RED)
        self.assertEqual(loaded_level.algorithm_used, "FRACTAL_SPIRAL")
    
    def test_load_nonexistent_level(self):
        loaded_level = self.persistence.load_level("nonexistent")
        self.assertIsNone(loaded_level)
    
    def test_list_levels(self):
        # Save multiple levels
        level1 = LevelData("level1", self.shapes, Color.RED, "STRATEGY1")
        level2 = LevelData("level2", self.shapes, Color.BLUE, "STRATEGY2")
        
        self.persistence.save_level(level1)
        self.persistence.save_level(level2)
        
        # List levels
        levels = self.persistence.list_levels()
        
        self.assertIn("level1", levels)
        self.assertIn("level2", levels)
        self.assertEqual(len(levels), 2)
    
    def test_save_and_load_current_level(self):
        # Save current level
        self.persistence.save_current_level(self.level_data)
        
        # Check file was created
        filename = self.persistence.get_current_level_file()
        self.assertTrue(os.path.exists(filename))
        
        # Load current level
        loaded_level = self.persistence.load_current_level()
        
        self.assertIsNotNone(loaded_level)
        self.assertEqual(loaded_level.level_id, "test123")
    
    def test_load_current_level_when_none_exists(self):
        loaded_level = self.persistence.load_current_level()
        self.assertIsNone(loaded_level)
    
    def test_data_directory_creation(self):
        # Test that directory is created if it doesn't exist
        new_dir = os.path.join(self.temp_dir, "new_subdir")
        self.assertFalse(os.path.exists(new_dir))
        
        persistence = LevelPersistence(new_dir)
        self.assertTrue(os.path.exists(new_dir))
    
    def test_json_file_format(self):
        # Save level and check JSON format
        self.persistence.save_level(self.level_data)
        
        filename = f"{self.temp_dir}/level_test123.json"
        with open(filename, 'r') as f:
            data = json.load(f)
        
        # Check required fields
        self.assertIn('level_id', data)
        self.assertIn('target_color', data)
        self.assertIn('algorithm_used', data)
        self.assertIn('created_at', data)
        self.assertIn('original_shapes', data)
        
        # Check shapes format
        self.assertIsInstance(data['original_shapes'], list)
        self.assertGreater(len(data['original_shapes']), 0)
    
    def test_roundtrip_serialization(self):
        """Test that save/load preserves all data correctly"""
        # Save and load
        self.persistence.save_level(self.level_data)
        loaded_level = self.persistence.load_level("test123")
        
        # Check all data is preserved
        self.assertEqual(loaded_level.level_id, self.level_data.level_id)
        self.assertEqual(loaded_level.target_color, self.level_data.target_color)
        self.assertEqual(loaded_level.algorithm_used, self.level_data.algorithm_used)
        self.assertEqual(len(loaded_level.original_shapes), len(self.level_data.original_shapes))
        
        # Check that shapes can be reconstructed
        fresh_shapes = loaded_level.get_fresh_shapes()
        self.assertEqual(len(fresh_shapes), 2)
        self.assertIsInstance(fresh_shapes[0], Circle)
        self.assertIsInstance(fresh_shapes[1], Square)

if __name__ == '__main__':
    unittest.main()