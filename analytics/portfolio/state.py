from dataclasses import dataclass, field


# ==========================================================
# Individual Sleeve
# ==========================================================

@dataclass
class Sleeve:
    """
    Represents one independent trading sleeve.

    Each sleeve receives a fixed allocation at the
    beginning of a campaign and trades independently.
    """

    sleeve_id: int
    allocation_pct: float

    active: bool = False

    entry_date: object = None
    entry_price: float = 0.0

    shares: float = 0.0

    current_price: float = 0.0
    market_value: float = 0.0

    realized_pnl: float = 0.0
    unrealized_pnl: float = 0.0


# ==========================================================
# Campaign State
# ==========================================================

@dataclass
class CampaignState:
    """
    Current campaign accounting.
    """

    active: bool = False

    start_date: object = None

    starting_equity: float = 100000.0

    current_equity: float = 100000.0

    closed_equity: float = 100000.0

    cash: float = 100000.0

    bars: int = 0


# ==========================================================
# Portfolio State
# ==========================================================

@dataclass
class PortfolioState:
    """
    Complete portfolio state.

    Contains campaign information plus
    all strategy sleeves.
    """

    campaign: CampaignState

    sleeves: list[Sleeve] = field(default_factory=list)

    equity_curve: list[float] = field(default_factory=list)

    daily_states: list[dict] = field(default_factory=list)