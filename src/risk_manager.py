"""
Risk management module for the arbitrage bot.

Provides features like maximum loss limits, position size limits, and daily trading limits.
"""

import logging
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional

logger = logging.getLogger(__name__)


@dataclass
class RiskLimits:
    """Risk management limits configuration."""
    max_daily_loss: Optional[float] = None  # Maximum loss per day in USDC
    max_position_size: Optional[float] = None  # Maximum position size in USDC
    max_trades_per_day: Optional[int] = None  # Maximum number of trades per day
    min_balance_required: float = 10.0  # Minimum balance required to continue trading
    max_balance_utilization: float = 0.8  # Maximum percentage of balance to use per trade


class RiskManager:
    """Manages risk limits and trading restrictions."""
    
    def __init__(self, limits: RiskLimits):
        """
        Initialize risk manager.
        
        Args:
            limits: Risk limits configuration
        """
        self.limits = limits
        self.daily_stats: dict = {
            "date": datetime.now().date().isoformat(),
            "trades_count": 0,
            "total_loss": 0.0,
            "total_profit": 0.0,
        }
    
    def _reset_daily_stats_if_needed(self):
        """Reset daily statistics if a new day has started."""
        today = datetime.now().date().isoformat()
        if self.daily_stats["date"] != today:
            self.daily_stats = {
                "date": today,
                "trades_count": 0,
                "total_loss": 0.0,
                "total_profit": 0.0,
            }
            logger.info("Daily risk limits reset for new day")
    
    def can_trade(self, trade_size: float, current_balance: float) -> tuple[bool, Optional[str]]:
        """
        Check if a trade is allowed based on risk limits.
        
        Args:
            trade_size: Size of the trade in USDC
            current_balance: Current account balance in USDC
            
        Returns:
            Tuple of (allowed, reason_if_not_allowed)
        """
        self._reset_daily_stats_if_needed()
        
        # Check minimum balance
        if current_balance < self.limits.min_balance_required:
            return False, f"Balance ${current_balance:.2f} below minimum ${self.limits.min_balance_required:.2f}"
        
        # Check maximum position size
        if self.limits.max_position_size and trade_size > self.limits.max_position_size:
            return False, f"Trade size ${trade_size:.2f} exceeds maximum ${self.limits.max_position_size:.2f}"
        
        # Check balance utilization
        max_trade_size = current_balance * self.limits.max_balance_utilization
        if trade_size > max_trade_size:
            return False, f"Trade size ${trade_size:.2f} exceeds {self.limits.max_balance_utilization*100:.0f}% of balance"
        
        # Check daily trade count
        if self.limits.max_trades_per_day:
            if self.daily_stats["trades_count"] >= self.limits.max_trades_per_day:
                return False, f"Daily trade limit ({self.limits.max_trades_per_day}) reached"
        
        # Check daily loss limit
        if self.limits.max_daily_loss:
            net_loss = self.daily_stats["total_loss"] - self.daily_stats["total_profit"]
            if net_loss >= self.limits.max_daily_loss:
                return False, f"Daily loss limit (${self.limits.max_daily_loss:.2f}) reached"
        
        return True, None
    
    def record_trade_result(self, profit: float):
        """
        Record the result of a trade for risk tracking.
        
        Args:
            profit: Profit/loss from the trade (negative for losses)
        """
        self._reset_daily_stats_if_needed()
        self.daily_stats["trades_count"] += 1
        
        if profit > 0:
            self.daily_stats["total_profit"] += profit
        else:
            self.daily_stats["total_loss"] += abs(profit)
    
    def get_daily_stats(self) -> dict:
        """Get current daily statistics."""
        self._reset_daily_stats_if_needed()
        net_pnl = self.daily_stats["total_profit"] - self.daily_stats["total_loss"]
        return {
            **self.daily_stats,
            "net_pnl": net_pnl,
        }
    
    def is_daily_loss_limit_reached(self) -> bool:
        """Check if daily loss limit has been reached."""
        if not self.limits.max_daily_loss:
            return False
        
        self._reset_daily_stats_if_needed()
        net_loss = self.daily_stats["total_loss"] - self.daily_stats["total_profit"]
        return net_loss >= self.limits.max_daily_loss

