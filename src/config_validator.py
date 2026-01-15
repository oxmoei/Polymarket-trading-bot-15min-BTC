"""
Configuration validation module.

Validates bot configuration and provides helpful error messages.
"""

import logging
from typing import List, Tuple

from .config import Settings

logger = logging.getLogger(__name__)


class ConfigValidator:
    """Validates bot configuration settings."""
    
    @staticmethod
    def validate(settings: Settings) -> Tuple[bool, List[str]]:
        """
        Validate configuration settings.
        
        Args:
            settings: Settings instance to validate
            
        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors = []
        
        # Required fields
        if not settings.private_key:
            errors.append("POLYMARKET_PRIVATE_KEY is required")
        elif not settings.private_key.startswith("0x"):
            errors.append("POLYMARKET_PRIVATE_KEY must start with '0x'")
        elif len(settings.private_key) < 64:
            errors.append("POLYMARKET_PRIVATE_KEY appears to be invalid (too short)")
        
        # Signature type validation
        if settings.signature_type not in [0, 1, 2]:
            errors.append("POLYMARKET_SIGNATURE_TYPE must be 0 (EOA), 1 (Magic.link), or 2 (Gnosis Safe)")
        
        # Magic.link requires funder
        if settings.signature_type == 1 and not settings.funder:
            errors.append("POLYMARKET_FUNDER is required when POLYMARKET_SIGNATURE_TYPE=1 (Magic.link)")
        
        # Trading parameters
        if settings.target_pair_cost <= 0 or settings.target_pair_cost >= 1.0:
            errors.append("TARGET_PAIR_COST must be between 0 and 1.0 (e.g., 0.99)")
        
        if settings.order_size < 5:
            errors.append("ORDER_SIZE must be at least 5 (minimum on Polymarket)")
        
        if settings.order_type not in ["FOK", "FAK", "GTC", "GTD"]:
            errors.append("ORDER_TYPE must be one of: FOK, FAK, GTC, GTD")
        
        if settings.cooldown_seconds < 0:
            errors.append("COOLDOWN_SECONDS must be >= 0")
        
        # Balance validation
        if settings.dry_run and settings.sim_balance < 0:
            errors.append("SIM_BALANCE must be >= 0 in simulation mode")
        
        return len(errors) == 0, errors
    
    @staticmethod
    def validate_and_print(settings: Settings) -> bool:
        """
        Validate configuration and print errors.
        
        Args:
            settings: Settings instance to validate
            
        Returns:
            True if valid, False otherwise
        """
        is_valid, errors = ConfigValidator.validate(settings)
        
        if not is_valid:
            logger.error("Configuration validation failed:")
            for error in errors:
                logger.error(f"  - {error}")
            logger.error("\nPlease fix the errors in your .env file and try again.")
        
        return is_valid

