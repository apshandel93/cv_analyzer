import os
import logging
import json
from datetime import datetime

class Debugger:
    """A utility class for debugging and logging in the CV Analyzer application."""
    
    def __init__(self, log_dir="logs"):
        """Initialize the debugger with a log directory."""
        self.log_dir = log_dir
        self.errors = []
        self.performance_metrics = []
        
        # Create log directory if it doesn't exist
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        # Set up
