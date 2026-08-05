import os
import logging
from datetime import datetime

class ViolationLogger:
    def __init__(self, log_dir="logs"):
        """
        Initializes the logging system for wrong-way violations.
        """
        self.log_dir = log_dir
        
        # Ensure the logs directory exists
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
            
        # Create a new log file for the current day
        log_filename = datetime.now().strftime("violations_%Y-%m-%d.log")
        self.log_filepath = os.path.join(self.log_dir, log_filename)
        
        # Configure the Python logging module
        logging.basicConfig(
            filename=self.log_filepath,
            level=logging.INFO,
            format="%(asctime)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        
        # Set to keep track of vehicles we've already logged
        self.logged_ids = set()

    def log_violation(self, tracker_id):
        """
        Logs a wrong-way violation if it hasn't been recorded yet.
        """
        if tracker_id not in self.logged_ids:
            message = f"WRONG WAY VIOLATION DETECTED: Vehicle ID {tracker_id}"
            logging.info(message)
            print(f"[LOGGER SAVED] {message}")
            self.logged_ids.add(tracker_id)