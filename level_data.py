import json
import os
from datetime import datetime
from shape_factory import ShapeFactory
from nested_shapes import NestedShape, NestedShapeFactory

class LevelData:
    def __init__(self, level_id, shapes, target_color, algorithm_used):
        self.level_id = level_id
        self.shapes = shapes
        self.target_color = target_color
        self.algorithm_used = algorithm_used
        self.created_at = datetime.now().isoformat()
        self.original_shapes = [self.shape_to_dict(shape) for shape in shapes]
    
    def shape_to_dict(self, shape):
        shape_data = {
            'x': shape.x,
            'y': shape.y,
            'shape_type': shape.__class__.__name__,
            'color': list(shape.color),  # Convert tuple to list for JSON
            'size': getattr(shape, 'size', None)
        }
        
        if hasattr(shape, 'width'):
            shape_data['width'] = shape.width
        if hasattr(shape, 'height'):
            shape_data['height'] = shape.height
        
        # Handle NestedShape serialization
        if isinstance(shape, NestedShape):
            shape_data['stack_pattern'] = shape.stack_pattern
            shape_data['component_shapes'] = [self.shape_to_dict(component) for component in shape.component_shapes]
            shape_data['total_width'] = shape.total_width
            shape_data['total_height'] = shape.total_height
            
        return shape_data
    
    def dict_to_shape(self, shape_dict):
        shape_type = shape_dict['shape_type']
        x, y = shape_dict['x'], shape_dict['y']
        color = tuple(shape_dict['color'])  # Convert list back to tuple
        
        if shape_type == 'NestedShape':
            # Reconstruct component shapes first
            component_shapes = [self.dict_to_shape(component_dict) for component_dict in shape_dict['component_shapes']]
            return NestedShape(x, y, color, component_shapes, shape_dict['stack_pattern'])
        elif shape_type == 'Circle':
            return ShapeFactory.create_circle(x, y, color, shape_dict.get('size'))
        elif shape_type == 'Square':
            return ShapeFactory.create_square(x, y, color, shape_dict.get('size'))
        elif shape_type == 'Triangle':
            return ShapeFactory.create_triangle(x, y, color, shape_dict.get('size'))
        elif shape_type == 'Rectangle':
            return ShapeFactory.create_rectangle(x, y, color, 
                                               shape_dict.get('width'), 
                                               shape_dict.get('height'))
        else:
            raise ValueError(f"Unknown shape type: {shape_type}")
    
    def to_dict(self):
        return {
            'level_id': self.level_id,
            'target_color': list(self.target_color),  # Convert tuple to list for JSON
            'algorithm_used': self.algorithm_used,
            'created_at': self.created_at,
            'original_shapes': self.original_shapes
        }
    
    @classmethod
    def from_dict(cls, data):
        level_data = cls.__new__(cls)
        level_data.level_id = data['level_id']
        level_data.target_color = tuple(data['target_color'])  # Convert list back to tuple
        level_data.algorithm_used = data['algorithm_used']
        level_data.created_at = data['created_at']
        level_data.original_shapes = data['original_shapes']
        return level_data
    
    def get_fresh_shapes(self):
        return [self.dict_to_shape(shape_dict) for shape_dict in self.original_shapes]

class LevelPersistence:
    def __init__(self, data_dir="level_data"):
        self.data_dir = data_dir
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
    
    def save_level(self, level_data):
        filename = f"{self.data_dir}/level_{level_data.level_id}.json"
        with open(filename, 'w') as f:
            json.dump(level_data.to_dict(), f, indent=2)
    
    def load_level(self, level_id):
        filename = f"{self.data_dir}/level_{level_id}.json"
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                data = json.load(f)
                return LevelData.from_dict(data)
        return None
    
    def list_levels(self):
        levels = []
        for filename in os.listdir(self.data_dir):
            if filename.startswith("level_") and filename.endswith(".json"):
                level_id = filename[6:-5]
                levels.append(level_id)
        return sorted(levels)
    
    def get_current_level_file(self):
        return f"{self.data_dir}/current_level.json"
    
    def save_current_level(self, level_data):
        with open(self.get_current_level_file(), 'w') as f:
            json.dump(level_data.to_dict(), f, indent=2)
    
    def load_current_level(self):
        filename = self.get_current_level_file()
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                data = json.load(f)
                return LevelData.from_dict(data)
        return None