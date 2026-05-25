# base_watcher.py
# Base class for all watchers in Personal AI Employee Project

import time
import logging
from pathlib import Path
from abc import ABC, abstractmethod

class BaseWatcher(ABC):
    def __init__(self, vault_path: str, check_interval: int = 60):
        """
        vault_path: Path to your AI_Employee_Vault folder
        check_interval: Kitne seconds mein check kare (default 60)
        """
        self.vault_path = Path(vault_path)
        self.needs_action = self.vault_path / 'Needs_Action'
        self.check_interval = check_interval
        
        # Create Needs_Action folder if it doesn't exist
        self.needs_action.mkdir(exist_ok=True)
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(self.__class__.__name__)

    @abstractmethod
    def check_for_updates(self):
        """
        Yeh method har watcher ko implement karna hoga.
        Return: List of new items/messages to process
        """
        pass

    @abstractmethod
    def create_action_file(self, item):
        """
        New item ko Needs_Action folder mein .md file bana ke save karega.
        """
        pass

    def run(self):
        """Main loop - Watcher ko continuously chalata hai"""
        self.logger.info(f"🚀 {self.__class__.__name__} started. Checking every {self.check_interval} seconds.")
        self.logger.info(f"Monitoring folder: {self.needs_action}")

        while True:
            try:
                items = self.check_for_updates()
                
                for item in items:
                    try:
                        filepath = self.create_action_file(item)
                        self.logger.info(f"✅ New action file created: {filepath.name}")
                    except Exception as e:
                        self.logger.error(f"Failed to create action file for item: {e}")
                        
            except Exception as e:
                self.logger.error(f"Error in watcher loop: {e}")
            
            # Wait before next check
            time.sleep(self.check_interval)
