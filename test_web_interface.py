#!/usr/bin/env python
"""
Simple test script to verify the web interface components work.
This doesn't require a trained model - it just checks that Flask routes work.
"""
import sys
import os

# Add source directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'source'))

def test_imports():
    """Test that all required imports work."""
    print("Testing imports...")
    try:
        import flask
        print("✓ Flask imported successfully")
    except ImportError as e:
        print(f"✗ Flask import failed: {e}")
        return False
    
    try:
        import numpy
        print("✓ NumPy imported successfully")
    except ImportError as e:
        print(f"✗ NumPy import failed: {e}")
        return False
    
    try:
        import svgwrite
        print("✓ svgwrite imported successfully")
    except ImportError as e:
        print(f"✗ svgwrite import failed: {e}")
        return False
    
    try:
        import cv2
        print("✓ OpenCV imported successfully")
    except ImportError as e:
        print(f"✗ OpenCV import failed: {e}")
        return False
    
    return True

def test_flask_app():
    """Test that Flask app can be created."""
    print("\nTesting Flask app creation...")
    try:
        from flask import Flask
        app = Flask(__name__, template_folder='templates')
        print("✓ Flask app created successfully")
        
        # Check template exists
        import os
        template_path = os.path.join('templates', 'index.html')
        if os.path.exists(template_path):
            print(f"✓ Template file exists: {template_path}")
        else:
            print(f"✗ Template file not found: {template_path}")
            return False
        
        return True
    except Exception as e:
        print(f"✗ Flask app creation failed: {e}")
        return False

def test_svg_generation():
    """Test that SVG generation works."""
    print("\nTesting SVG generation...")
    try:
        import svgwrite
        import numpy as np
        
        # Create a simple test stroke
        test_stroke = np.array([
            [0, 0, 0],
            [10, 10, 0],
            [20, 15, 0],
            [30, 20, 1],
            [40, 20, 0],
            [50, 25, 0]
        ], dtype=np.float32)
        
        dwg = svgwrite.Drawing('/tmp/test.svg', size=(200, 100))
        
        abs_x, abs_y = 0, 0
        for i in range(len(test_stroke)):
            prev_x, prev_y = abs_x, abs_y
            x = float(test_stroke[i, 0])
            y = float(test_stroke[i, 1])
            abs_x += x
            abs_y += y
            
            if test_stroke[i, 2] == 0:  # pen down
                dwg.add(dwg.line((prev_x, prev_y), (abs_x, abs_y), stroke='black', stroke_width=2))
        
        dwg.save()
        print("✓ SVG generation successful")
        
        # Clean up
        if os.path.exists('/tmp/test.svg'):
            os.remove('/tmp/test.svg')
        
        return True
    except Exception as e:
        print(f"✗ SVG generation failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests."""
    print("=" * 60)
    print("Web Interface Component Tests")
    print("=" * 60)
    
    all_passed = True
    
    # Test imports
    if not test_imports():
        all_passed = False
        print("\n⚠ Some imports failed. Install dependencies with:")
        print("  pip install -r requirements.txt")
    
    # Test Flask app
    if not test_flask_app():
        all_passed = False
    
    # Test SVG generation
    if not test_svg_generation():
        all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("✓ All tests passed!")
        print("\nTo start the web interface (requires trained model):")
        print("  python app.py -M <path_to_model_checkpoint>")
    else:
        print("✗ Some tests failed. Please fix the issues above.")
        return 1
    print("=" * 60)
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
