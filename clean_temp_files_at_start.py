import os
import sys
import tempfile
import glob
from shutil import rmtree
import atexit
from pathlib import Path

class AppSpecificTempCleanup:
    """
    Minimal cleanup manager that only handles temporary files created by the current application.
    - Cleans up only on application exit (not during runtime)
    - Handles multiple instances safely
    - Cleans MEI folders automatically if using PyInstaller
    - Minimal code footprint - can be embedded directly in your main application
    """
    
    def __init__(self, app_name="MyPySide6App"):
        self.app_name = app_name
        self.current_mei_path = getattr(sys, '_MEIPASS', None)
        self.temp_dir = tempfile.gettempdir()
        
        # Register cleanup to run on application exit
        atexit.register(self.cleanup_on_exit)
    
    def cleanup_mei_folders(self):
        """Clean up old MEI folders, but leave current one and any from other running instances."""
        if not self.current_mei_path:
            return  # Not running from PyInstaller
        
        try:
            # Get the parent directory of current MEI folder
            temp_path = os.path.dirname(self.current_mei_path)
            
            # Find all MEI folders in temp directory
            mei_pattern = os.path.join(temp_path, '_MEI*')
            mei_folders = glob.glob(mei_pattern)
            
            for mei_folder in mei_folders:
                # Skip current MEI folder
                if mei_folder == self.current_mei_path:
                    continue
                
                try:
                    # Try to remove the folder - if it fails, another instance is using it
                    rmtree(mei_folder)
                    print(f"Cleaned up old MEI folder: {os.path.basename(mei_folder)}")
                except (OSError, PermissionError):
                    # Folder is in use by another instance or system, skip it
                    pass
                    
        except Exception as e:
            # Silently handle any errors - cleanup shouldn't crash the app
            pass
    
    def cleanup_app_temp_files(self):
        """Clean up temporary files that might be created by your application."""
        try:
            # Define patterns for files your app might create
            # Customize these patterns based on your application's temp file naming
            app_temp_patterns = [
                f"{self.app_name}_*.tmp",
                f"{self.app_name}_temp_*",
                f"{self.app_name}*.log",  # If your app creates log files
                # Add more patterns specific to your app's temp file creation
            ]
            
            for pattern in app_temp_patterns:
                temp_pattern = os.path.join(self.temp_dir, pattern)
                for temp_file in glob.glob(temp_pattern):
                    try:
                        if os.path.isfile(temp_file):
                            os.remove(temp_file)
                            print(f"Cleaned up temp file: {os.path.basename(temp_file)}")
                        elif os.path.isdir(temp_file):
                            rmtree(temp_file)
                            print(f"Cleaned up temp directory: {os.path.basename(temp_file)}")
                    except (OSError, PermissionError):
                        # File might be in use, skip it
                        pass
                        
        except Exception:
            # Silently handle errors - cleanup should never crash the application
            pass
    
    def cleanup_on_exit(self):
        """Main cleanup function called on application exit."""
        # Clean up MEI folders (PyInstaller temp directories)
        self.cleanup_mei_folders()
        
        # Clean up application-specific temp files
        self.cleanup_app_temp_files()


# ===== INTEGRATION EXAMPLES =====

# Method 1: Full integration with your existing PySide6 application
class PySide6AppWithCleanup:
    """
    Example showing how to integrate with your existing PySide6 application.
    Just add the cleanup initialization to your existing code.
    """
    
    def __init__(self):
        from PySide6.QtWidgets import QApplication
        import sys
        
        # Your existing PySide6 app initialization
        self.app = QApplication(sys.argv)
        
        # Add just this one line to enable cleanup (customize the app name)
        self.temp_cleanup = AppSpecificTempCleanup("YourAppName")
        
        # Your existing window initialization
        # self.window = YourMainWindow()
    
    def run(self):
        # Your existing run code
        # self.window.show()
        # return self.app.exec()
        pass


# Method 2: Ultra-minimal integration - just add these lines to your existing main.py
"""
# Add these imports at the top of your existing main.py file:
import atexit
import os
import sys
import tempfile
import glob
from shutil import rmtree

# Add this function anywhere in your existing code:
def cleanup_mei_folders():
    '''Clean up old PyInstaller MEI folders on application exit'''
    current_mei = getattr(sys, '_MEIPASS', None)
    if not current_mei:
        return  # Not running from PyInstaller
    
    temp_path = os.path.dirname(current_mei)
    for mei_folder in glob.glob(os.path.join(temp_path, '_MEI*')):
        if mei_folder != current_mei:
            try:
                rmtree(mei_folder)
            except (OSError, PermissionError):
                pass  # Skip folders in use by other instances

# Add this single line right after your QApplication creation:
atexit.register(cleanup_mei_folders)

# That's it! Your app will now automatically clean up old MEI folders on exit.
"""

# Method 3: Integration with PySide6 closeEvent
"""
# If you want to hook into PySide6's window close event instead of atexit:

from PySide6.QtWidgets import QMainWindow

class YourMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Your existing window initialization
        self.temp_cleanup = AppSpecificTempCleanup("YourAppName")
    
    def closeEvent(self, event):
        '''Override closeEvent to perform cleanup when window is closed'''
        # Perform cleanup immediately when window closes
        self.temp_cleanup.cleanup_on_exit()
        
        # Call parent closeEvent to actually close the window
        event.accept()
"""
