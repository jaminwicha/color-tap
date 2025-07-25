import unittest
from unittest.mock import Mock, patch, MagicMock
from collections import Counter
from level_generator import LevelGenerator
from shape_behaviors import Circle, Square
from config import Color, AVAILABLE_COLORS

class TestLevelGenerator(unittest.TestCase):
    
    def test_is_level_winnable_with_sufficient_target_shapes(self):
        """Test level is winnable when there are enough target color shapes"""
        target_color = Color.RED
        shapes = [
            Mock(color=Color.RED),
            Mock(color=Color.RED),
            Mock(color=Color.BLUE),
            Mock(color=Color.GREEN)
        ]
        
        result = LevelGenerator.is_level_winnable(shapes, target_color)
        self.assertTrue(result)
    
    def test_is_level_winnable_insufficient_target_shapes(self):
        """Test level is not winnable with insufficient target color shapes"""
        target_color = Color.RED
        shapes = [
            Mock(color=Color.RED),  # Only one red shape
            Mock(color=Color.BLUE),
            Mock(color=Color.GREEN)
        ]
        
        result = LevelGenerator.is_level_winnable(shapes, target_color)
        self.assertFalse(result)
    
    def test_is_level_winnable_no_target_shapes(self):
        """Test level is not winnable with no target color shapes"""
        target_color = Color.RED
        shapes = [
            Mock(color=Color.BLUE),
            Mock(color=Color.GREEN),
            Mock(color=Color.YELLOW)
        ]
        
        result = LevelGenerator.is_level_winnable(shapes, target_color)
        self.assertFalse(result)
    
    def test_is_level_winnable_complex_scenario(self):
        """Test level winnability with multiple color pairs"""
        target_color = Color.RED
        shapes = [
            Mock(color=Color.RED),
            Mock(color=Color.RED),
            Mock(color=Color.BLUE),
            Mock(color=Color.BLUE),
            Mock(color=Color.GREEN),
            Mock(color=Color.GREEN)
        ]
        
        # This should be winnable: 1 red pair, 1 blue pair, 1 green pair
        # Target red pair should be the last one remaining
        result = LevelGenerator.is_level_winnable(shapes, target_color)
        self.assertTrue(result)
    
    @patch('level_generator.GenerationStrategyFactory.get_random_strategy')
    @patch('level_generator.ShapeFactory.create_random_shape')
    @patch('random.choice')
    def test_create_level_success(self, mock_choice, mock_create_shape, mock_get_strategy):
        """Test successful level creation"""
        # Mock dependencies
        target_color = Color.RED
        mock_choice.return_value = target_color
        
        mock_strategy = Mock()
        mock_strategy.name = "TEST_STRATEGY"
        mock_strategy.generate_positions.return_value = [(100, 100), (200, 200)]
        mock_get_strategy.return_value = mock_strategy
        
        # Mock shape creation
        def create_mock_shape(x, y, color):
            mock_shape = Mock()
            mock_shape.color = color
            mock_shape.get_distance_to.return_value = 100  # Far apart
            mock_shape.get_collision_radius.return_value = 10
            mock_shape.get_max_dimension.return_value = 20
            mock_shape.x = x
            mock_shape.y = y
            return mock_shape
        
        mock_create_shape.side_effect = create_mock_shape
        
        # Mock is_level_winnable to return True
        with patch.object(LevelGenerator, 'is_level_winnable', return_value=True), \
             patch('level_generator.LevelValidator.validate_level', return_value=(True, [])), \
             patch('random.random', return_value=0.5):  # Skip fused shapes
            result = LevelGenerator.create_level()
        
        self.assertIsNotNone(result[0])  # shapes
        self.assertEqual(result[1], target_color)  # target_color
        self.assertEqual(result[2], "TEST_STRATEGY")  # algorithm
    
    @patch('level_generator.GenerationStrategyFactory.get_random_strategy')
    @patch('level_generator.ShapeFactory.create_random_shape')
    @patch('random.choice')
    def test_create_level_failure_after_max_attempts(self, mock_choice, mock_create_shape, mock_get_strategy):
        """Test level creation failure after max attempts"""
        # Mock dependencies
        target_color = Color.RED
        mock_choice.return_value = target_color
        
        mock_strategy = Mock()
        mock_strategy.name = "TEST_STRATEGY"
        mock_strategy.generate_positions.return_value = [(100, 100), (200, 200)]
        mock_get_strategy.return_value = mock_strategy
        
        # Mock shape creation
        def create_mock_shape(x, y, color):
            mock_shape = Mock()
            mock_shape.color = Color.BLUE  # Never winnable
            mock_shape.get_distance_to.return_value = 100  # Far apart
            mock_shape.get_collision_radius.return_value = 10
            mock_shape.get_max_dimension.return_value = 20
            mock_shape.x = x
            mock_shape.y = y
            return mock_shape
        
        mock_create_shape.side_effect = create_mock_shape
        
        # Mock is_level_winnable to always return False and force legacy generation
        with patch.object(LevelGenerator, 'is_level_winnable', return_value=False), \
             patch('level_generator.LevelValidator.validate_level', return_value=(False, [])), \
             patch('level_generator.LevelValidator.auto_fix_overlaps', return_value=[]), \
             patch('random.random', return_value=0.8):  # Force legacy generation (> 0.7)
            result = LevelGenerator.create_level()
        
        self.assertIsNone(result[0])  # shapes should be None
        self.assertEqual(result[1], target_color)  # target_color
        self.assertEqual(result[2], "legacy_generation")  # algorithm now returns this when failing
    
    def test_winnable_logic_with_real_shapes(self):
        """Test winnability logic with actual shape objects"""
        # Create shapes that should be winnable
        shapes = [
            Circle(100, 100, Color.RED, 30),
            Circle(200, 200, Color.RED, 30),
            Square(300, 300, Color.BLUE, 25),
            Square(400, 400, Color.BLUE, 25)
        ]
        
        # Should be winnable - target red shapes can be the final pair
        result = LevelGenerator.is_level_winnable(shapes, Color.RED)
        self.assertTrue(result)
        
        # Should not be winnable for a color that doesn't exist
        result = LevelGenerator.is_level_winnable(shapes, Color.GREEN)
        self.assertFalse(result)
    
    def test_color_counting_logic(self):
        """Test the color counting logic in is_level_winnable"""
        target_color = Color.RED
        shapes = [
            Mock(color=Color.RED),    # 1
            Mock(color=Color.RED),    # 2
            Mock(color=Color.RED),    # 3 - odd number
            Mock(color=Color.BLUE),   # 1
            Mock(color=Color.BLUE)    # 2 - even number
        ]
        
        result = LevelGenerator.is_level_winnable(shapes, target_color)
        
        # With 3 red shapes, we get 1 pair (leaving 1 remaining)
        # With 2 blue shapes, we get 1 pair
        # This should be winnable as the remaining red can potentially be the last
        self.assertTrue(result)
    
    @patch('level_generator.GAME_SETTINGS')
    def test_level_creation_uses_game_settings(self, mock_settings):
        """Test that level creation uses values from game settings"""
        mock_settings.__getitem__.side_effect = lambda key: {
            'num_shapes': 6,
            'max_level_attempts': 5
        }[key]
        
        with patch('level_generator.GenerationStrategyFactory.get_random_strategy') as mock_get_strategy, \
             patch('level_generator.ShapeFactory.create_random_shape') as mock_create_shape, \
             patch('random.choice') as mock_choice, \
             patch('random.random', return_value=0.8), \
             patch.object(LevelGenerator, 'is_level_winnable', return_value=False), \
             patch('level_generator.LevelValidator.validate_level', return_value=(False, [])), \
             patch('level_generator.LevelValidator.auto_fix_overlaps') as mock_auto_fix:
            
            mock_strategy = Mock()
            mock_strategy.name = "TEST"
            mock_strategy.generate_positions.return_value = [(i*50, i*50) for i in range(6)]
            mock_get_strategy.return_value = mock_strategy
            mock_choice.return_value = Color.RED
            
            # Create proper mock shape with required attributes
            def create_mock_shape(x, y, color):
                mock_shape = Mock()
                mock_shape.color = color
                mock_shape.size = 30  # Add size attribute for nested shape conversion
                mock_shape.get_distance_to.return_value = 100
                mock_shape.get_collision_radius.return_value = 10
                mock_shape.get_max_dimension.return_value = 20
                mock_shape.x = x
                mock_shape.y = y
                return mock_shape
            
            mock_create_shape.side_effect = create_mock_shape
            
            # Mock auto_fix_overlaps to return empty list
            mock_auto_fix.return_value = []
            
            LevelGenerator.create_level()
            
            # Should call generate_positions with num_shapes from settings
            mock_strategy.generate_positions.assert_called_with(6)

if __name__ == '__main__':
    unittest.main()