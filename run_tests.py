import os
import sys
import unittest

if __name__ == "__main__":
    # Get the current directory
    current_directory = os.path.dirname(os.path.realpath(__file__))

    # Add the current directory to sys.path
    sys.path.append(current_directory)
    
    # Specify the start directory for test discovery
    test_directory = os.path.join(current_directory, 'test')

    # Run the test discovery
    unittest.main(module=None, argv=['', 'discover', '-s', test_directory], exit=False)
