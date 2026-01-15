"""
Utility functions for the arbitrage bot.
"""

import signal
import sys
from typing import Callable, Optional


class GracefulShutdown:
    """Handles graceful shutdown on SIGINT/SIGTERM signals."""
    
    def __init__(self):
        self.shutdown_requested = False
        self.shutdown_callbacks: list[Callable] = []
        
        # Register signal handlers
        signal.signal(signal.SIGINT, self._signal_handler)
        if hasattr(signal, 'SIGTERM'):
            signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals."""
        if not self.shutdown_requested:
            self.shutdown_requested = True
            print("\n🛑 Shutdown requested. Finishing current operations...")
            # Run shutdown callbacks
            for callback in self.shutdown_callbacks:
                try:
                    callback()
                except Exception as e:
                    print(f"Error in shutdown callback: {e}")
        else:
            # Force exit on second signal
            print("\n⚠️ Force exit requested.")
            sys.exit(1)
    
    def register_callback(self, callback: Callable):
        """Register a callback to run on shutdown."""
        self.shutdown_callbacks.append(callback)
    
    def is_shutdown_requested(self) -> bool:
        """Check if shutdown has been requested."""
        return self.shutdown_requested

