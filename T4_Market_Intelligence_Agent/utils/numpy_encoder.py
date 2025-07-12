"""
JSON Encoder for NumPy types
Handles serialization of NumPy arrays and data types
"""

import json
import numpy as np
from datetime import datetime, date
from decimal import Decimal


class NumpyEncoder(json.JSONEncoder):
    """Custom JSON encoder that handles NumPy types and other special types"""
    
    def default(self, obj):
        # NumPy arrays
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        
        # NumPy scalars
        if isinstance(obj, (np.integer, np.int_, np.intc, np.intp, 
                          np.int8, np.int16, np.int32, np.int64,
                          np.uint8, np.uint16, np.uint32, np.uint64)):
            return int(obj)
        
        if isinstance(obj, (np.floating, np.float_, np.float16, 
                          np.float32, np.float64)):
            return float(obj)
        
        if isinstance(obj, (np.complex_, np.complex64, np.complex128)):
            return {'real': obj.real, 'imag': obj.imag}
        
        if isinstance(obj, np.bool_):
            return bool(obj)
        
        if isinstance(obj, np.void):
            return None
        
        # Datetime types
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        
        # Decimal type
        if isinstance(obj, Decimal):
            return float(obj)
        
        # Sets
        if isinstance(obj, set):
            return list(obj)
        
        # Let the base class default method raise the TypeError
        return super().default(obj)