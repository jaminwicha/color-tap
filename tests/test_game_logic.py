import unittest
from unittest.mock import Mock, patch, MagicMock
import pygame
from game import Game
from shape_behaviors import Circle, Square
from config import Color

class TestGameLogic(unittest.TestCase):
    
    def setUp(self):
        # Mock pygame to avoid actual window creation during tests
        pygame.init = Mock()
        pygame.display.set_mode = Mock()
        pygame.display.set_caption = Mock()
        pygame.time.Clock = Mock()
        
        with patch('game.LevelPersistence'), \
             patch.object(Game, 'load_or_create_level'):
            self.game = Game()
    
    def test_game_initialization(self):
        """Test that game initializes with correct default values"""
        # Background color is now based on aesthetic palette
        self.assertIsNotNone(self.game.background_color)
        self.assertFalse(self.game.level_complete)
        self.assertFalse(self.game.show_impossible_popup)
        self.assertIsNone(self.game.dragging_shape)
        self.assertEqual(self.game.shapes, [])
        # Test that the palette system is working
        self.assertIsNotNone(self.game.current_palette)
    
    def test_handle_mouse_down_selects_shape(self):
        """Test that mouse down selects a shape under cursor"""
        circle = Mock()
        circle.contains_point.return_value = True
        circle.x = 80
        circle.y = 80
        self.game.shapes = [circle]
        
        self.game.handle_mouse_down((100, 100))
        
        self.assertEqual(self.game.dragging_shape, circle)
        self.assertTrue(circle.being_dragged)
        circle.contains_point.assert_called_with(100, 100)
    
    def test_handle_mouse_down_no_shape_selected(self):
        """Test that mouse down with no shape under cursor selects nothing"""
        circle = Mock()
        circle.contains_point.return_value = False
        circle.being_dragged = False
        self.game.shapes = [circle]
        
        self.game.handle_mouse_down((100, 100))
        
        self.assertIsNone(self.game.dragging_shape)
        self.assertFalse(circle.being_dragged)
    
    def test_handle_mouse_up_releases_shape(self):
        """Test that mouse up releases the dragged shape"""
        circle = Mock()
        circle.being_dragged = True
        self.game.dragging_shape = circle
        
        self.game.handle_mouse_up()
        
        self.assertIsNone(self.game.dragging_shape)
        self.assertFalse(circle.being_dragged)
    
    def test_handle_mouse_motion_moves_dragged_shape(self):
        """Test that mouse motion moves the dragged shape"""
        circle = Mock()
        circle.x = 100
        circle.y = 100
        circle.drag_offset_x = 10
        circle.drag_offset_y = 15
        self.game.dragging_shape = circle
        
        self.game.handle_mouse_motion((150, 200))
        
        self.assertEqual(circle.x, 140)  # 150 - 10
        self.assertEqual(circle.y, 185)  # 200 - 15
    
    def test_check_collisions_same_color_merge(self):
        """Test that same color shapes merge and disappear"""
        shape1 = Mock()
        shape1.color = Color.RED
        shape1.is_colliding_with.return_value = True
        shape1.x = 100
        shape1.y = 100
        
        shape2 = Mock()
        shape2.color = Color.RED
        shape2.x = 120
        shape2.y = 120
        
        self.game.shapes = [shape1, shape2]
        
        with patch.object(self.game, 'check_level_possibility'):
            self.game.check_collisions()
        
        # Shapes should be removed
        self.assertEqual(len(self.game.shapes), 0)
        self.assertEqual(self.game.last_merged_color, Color.RED)
    
    def test_check_collisions_different_color_bounce(self):
        """Test that different color shapes bounce off each other"""
        shape1 = Mock()
        shape1.color = Color.RED
        shape1.is_colliding_with.return_value = True
        shape1.x = 100
        shape1.y = 100
        
        shape2 = Mock()
        shape2.color = Color.BLUE
        shape2.x = 120
        shape2.y = 120
        
        self.game.shapes = [shape1, shape2]
        
        self.game.check_collisions()
        
        # Shapes should still exist
        self.assertEqual(len(self.game.shapes), 2)
        shape1.bounce_off.assert_called_with(shape2)
    
    def test_level_complete_condition(self):
        """Test that level completes when no shapes remain and target color matches"""
        self.game.shapes = []
        self.game.last_merged_color = Color.RED
        self.game.target_color = Color.RED
        
        self.game.check_collisions()
        
        self.assertTrue(self.game.level_complete)
    
    def test_level_not_complete_wrong_color(self):
        """Test that level doesn't complete with wrong final color"""
        self.game.shapes = []
        self.game.last_merged_color = Color.BLUE
        self.game.target_color = Color.RED
        
        self.game.check_collisions()
        
        self.assertFalse(self.game.level_complete)
    
    def test_level_not_complete_shapes_remaining(self):
        """Test that level doesn't complete with shapes remaining"""
        shape = Mock()
        self.game.shapes = [shape]
        self.game.last_merged_color = Color.RED
        self.game.target_color = Color.RED
        
        self.game.check_collisions()
        
        self.assertFalse(self.game.level_complete)
    
    @patch('game.LevelGenerator.is_level_winnable')
    def test_check_level_possibility_impossible(self, mock_is_winnable):
        """Test that impossible popup shows when level becomes unwinnable"""
        mock_is_winnable.return_value = False
        
        shape = Mock()
        self.game.shapes = [shape]
        self.game.target_color = Color.RED
        
        self.game.check_level_possibility()
        
        self.assertTrue(self.game.show_impossible_popup)
        mock_is_winnable.assert_called_with([shape], Color.RED)
    
    @patch('game.LevelGenerator.is_level_winnable')
    def test_check_level_possibility_still_possible(self, mock_is_winnable):
        """Test that popup doesn't show when level is still winnable"""
        mock_is_winnable.return_value = True
        
        shape = Mock()
        self.game.shapes = [shape]
        self.game.target_color = Color.RED
        
        self.game.check_level_possibility()
        
        self.assertFalse(self.game.show_impossible_popup)
    
    def test_reset_to_original_level(self):
        """Test that reset restores original level state"""
        mock_level_data = Mock()
        mock_level_data.get_fresh_shapes.return_value = [Mock(), Mock()]
        mock_level_data.target_color = Color.GREEN
        
        self.game.current_level_data = mock_level_data
        
        self.game.reset_to_original_level()
        
        self.assertEqual(len(self.game.shapes), 2)
        self.assertEqual(self.game.target_color, Color.GREEN)
        self.assertEqual(self.game.border_color, Color.GREEN)
        self.assertFalse(self.game.level_complete)
        self.assertFalse(self.game.show_impossible_popup)
        self.assertIsNone(self.game.last_merged_color)
        self.assertEqual(self.game.background_color, Color.WHITE)
    
    @patch('game.LevelGenerator.create_level')
    @patch('game.uuid.uuid4')
    def test_create_new_level_success(self, mock_uuid, mock_create_level):
        """Test successful new level creation"""
        # Mock UUID generation
        mock_uuid.return_value.hex = "12345678abcdef"
        
        # Mock level generation with proper color attributes
        mock_shape1 = Mock()
        mock_shape1.color = Color.RED
        mock_shape2 = Mock()
        mock_shape2.color = Color.BLUE
        mock_shapes = [mock_shape1, mock_shape2]
        mock_create_level.return_value = (mock_shapes, Color.BLUE, "TEST_ALGORITHM")
        
        # Mock persistence
        self.game.level_persistence = Mock()
        
        with patch.object(self.game, 'load_level_from_data') as mock_load:
            self.game.create_new_level()
        
        # Should create and save level data
        self.game.level_persistence.save_level.assert_called_once()
        self.game.level_persistence.save_current_level.assert_called_once()
        mock_load.assert_called_once()
    
    @patch('game.LevelGenerator.create_level')
    def test_create_new_level_failure(self, mock_create_level):
        """Test new level creation failure"""
        # Mock level generation failure
        mock_create_level.return_value = (None, Color.RED, "TEST_ALGORITHM")
        
        self.game.create_new_level()
        
        self.assertTrue(self.game.show_impossible_popup)
    
    def test_load_level_from_data(self):
        """Test loading level from level data object"""
        mock_shapes = [Mock(), Mock()]
        mock_level_data = Mock()
        mock_level_data.get_fresh_shapes.return_value = mock_shapes
        mock_level_data.target_color = Color.PURPLE
        
        self.game.load_level_from_data(mock_level_data)
        
        self.assertEqual(self.game.current_level_data, mock_level_data)
        self.assertEqual(self.game.shapes, mock_shapes)
        self.assertEqual(self.game.target_color, Color.PURPLE)
        self.assertEqual(self.game.border_color, Color.PURPLE)
        self.assertFalse(self.game.level_complete)
        self.assertFalse(self.game.show_impossible_popup)

if __name__ == '__main__':
    unittest.main()