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
        
        # Set up logging
        logging.basicConfig(
            filename=os.path.join(log_dir, f"cv_analyzer_{datetime.now().strftime('%Y%m%d')}.log"),
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger('cv_analyzer')
    
    def log_error(self, error, context=None):
        """Log an error with optional context."""
        error_info = {
            "timestamp": datetime.now().isoformat(),
            "type": type(error).__name__,
            "message": str(error),
            "context": context or "general"
        }
        
        self.errors.append(error_info)
        self.logger.error(f"Error in {context}: {str(error)}")
        
        # Also write to error log file
        with open(os.path.join(self.log_dir, "errors.json"), "a") as f:
            json.dump(error_info, f)
            f.write("\n")
    
    def log_performance_metric(self, metric, value):
        """Log a performance metric."""
        metric_info = {
            "timestamp": datetime.now().isoformat(),
            "metric": metric,
            "value": value
        }
        
        self.performance_metrics.append(metric_info)
        self.logger.info(f"Performance metric: {metric} = {value}")
        
        # Also write to performance log file
        with open(os.path.join(self.log_dir, "performance.json"), "a") as f:
            json.dump(metric_info, f)
            f.write("\n")
    
    def get_error_summary(self):
        """Get a summary of logged errors."""
        return [(e["timestamp"], e["type"], e["message"], e["context"]) for e in self.errors]
    
    def get_performance_metrics(self):
        """Get all logged performance metrics."""
        return self.performance_metrics
