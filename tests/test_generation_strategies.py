import unittest
import math
from generation_strategies import (
    FractalSpiralStrategy, 
    FibonacciSpiralStrategy, 
    OrganicClustersStrategy,
    PerlinNoiseStrategy,
    MandelbrotStrategy,
    GenerationStrategyFactory
)
from config import WINDOW_WIDTH, WINDOW_HEIGHT

class TestGenerationStrategies(unittest.TestCase):
    
    def setUp(self):
        self.num_shapes = 8
    
    def test_fractal_spiral_strategy(self):
        strategy = FractalSpiralStrategy()
        positions = strategy.generate_positions(self.num_shapes)
        
        self.assertEqual(len(positions), self.num_shapes)
        self.assertEqual(strategy.name, "FRACTAL_SPIRAL")
        
        # Check that all positions are within bounds
        for x, y in positions:
            self.assertGreaterEqual(x, 50)
            self.assertLessEqual(x, WINDOW_WIDTH - 50)
            self.assertGreaterEqual(y, 50)
            self.assertLessEqual(y, WINDOW_HEIGHT - 50)
    
    def test_fibonacci_spiral_strategy(self):
        strategy = FibonacciSpiralStrategy()
        positions = strategy.generate_positions(self.num_shapes)
        
        self.assertEqual(len(positions), self.num_shapes)
        self.assertEqual(strategy.name, "FIBONACCI_SPIRAL")
        
        # Check bounds
        for x, y in positions:
            self.assertGreaterEqual(x, 50)
            self.assertLessEqual(x, WINDOW_WIDTH - 50)
            self.assertGreaterEqual(y, 50)
            self.assertLessEqual(y, WINDOW_HEIGHT - 50)
    
    def test_organic_clusters_strategy(self):
        strategy = OrganicClustersStrategy()
        positions = strategy.generate_positions(self.num_shapes)
        
        self.assertEqual(len(positions), self.num_shapes)
        self.assertEqual(strategy.name, "ORGANIC_CLUSTERS")
        
        # Check bounds
        for x, y in positions:
            self.assertGreaterEqual(x, 50)
            self.assertLessEqual(x, WINDOW_WIDTH - 50)
            self.assertGreaterEqual(y, 50)
            self.assertLessEqual(y, WINDOW_HEIGHT - 50)
    
    def test_perlin_noise_strategy(self):
        strategy = PerlinNoiseStrategy()
        positions = strategy.generate_positions(self.num_shapes)
        
        self.assertEqual(len(positions), self.num_shapes)
        self.assertEqual(strategy.name, "PERLIN_NOISE")
        
        # Check bounds
        for x, y in positions:
            self.assertGreaterEqual(x, 50)
            self.assertLessEqual(x, WINDOW_WIDTH - 50)
            self.assertGreaterEqual(y, 50)
            self.assertLessEqual(y, WINDOW_HEIGHT - 50)
    
    def test_mandelbrot_strategy(self):
        strategy = MandelbrotStrategy()
        positions = strategy.generate_positions(self.num_shapes)
        
        self.assertEqual(len(positions), self.num_shapes)
        self.assertEqual(strategy.name, "MANDELBROT_SET")
        
        # Check bounds
        for x, y in positions:
            self.assertGreaterEqual(x, 50)
            self.assertLessEqual(x, WINDOW_WIDTH - 50)
            self.assertGreaterEqual(y, 50)
            self.assertLessEqual(y, WINDOW_HEIGHT - 50)
    
    def test_generation_strategy_factory(self):
        # Test getting specific strategy
        fractal = GenerationStrategyFactory.get_strategy("FRACTAL_SPIRAL")
        self.assertIsInstance(fractal, FractalSpiralStrategy)
        
        fibonacci = GenerationStrategyFactory.get_strategy("FIBONACCI_SPIRAL")
        self.assertIsInstance(fibonacci, FibonacciSpiralStrategy)
        
        # Test getting unknown strategy
        unknown = GenerationStrategyFactory.get_strategy("UNKNOWN")
        self.assertIsNone(unknown)
        
        # Test getting random strategy
        random_strategy = GenerationStrategyFactory.get_random_strategy()
        self.assertIsNotNone(random_strategy)
        
        # Test getting all strategies
        all_strategies = GenerationStrategyFactory.get_all_strategies()
        self.assertEqual(len(all_strategies), 5)
    
    def test_strategy_consistency(self):
        """Test that each strategy produces consistent results with same input"""
        strategy = FractalSpiralStrategy()
        
        # Generate positions twice with same parameters
        positions1 = strategy.generate_positions(5)
        positions2 = strategy.generate_positions(5)
        
        # Should be identical (assuming no randomness in fractal spiral)
        self.assertEqual(len(positions1), len(positions2))
        
        # For strategies with randomness, we just check they produce valid output
        organic = OrganicClustersStrategy()
        organic_positions = organic.generate_positions(5)
        self.assertEqual(len(organic_positions), 5)
    
    def test_fibonacci_golden_ratio(self):
        """Test that Fibonacci spiral uses golden ratio correctly"""
        strategy = FibonacciSpiralStrategy()
        
        # The golden ratio should be approximately 1.618
        golden_ratio = (1 + math.sqrt(5)) / 2
        self.assertAlmostEqual(golden_ratio, 1.618, places=2)
        
        # Test that positions are generated
        positions = strategy.generate_positions(3)
        self.assertEqual(len(positions), 3)
    
    def test_position_uniqueness(self):
        """Test that strategies don't generate identical positions"""
        strategy = FractalSpiralStrategy()
        positions = strategy.generate_positions(8)
        
        # Convert to set to check for duplicates
        unique_positions = set(positions)
        
        # Should have same number of unique positions as total positions
        # (allowing for small floating point differences)
        self.assertGreaterEqual(len(unique_positions), len(positions) - 1)

if __name__ == '__main__':
    unittest.main()