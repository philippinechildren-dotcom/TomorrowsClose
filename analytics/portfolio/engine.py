from copy import deepcopy
from analytics.portfolio.state import Sleeve, CampaignState, PortfolioState


class PortfolioEngine:

    def __init__(
        self,
        sleeve_count=5,
        allocation_pct=0.20,
        starting_equity=100000.0
    ):

        campaign = CampaignState(
            active=False,
            starting_equity=starting_equity,
            current_equity=starting_equity,
            closed_equity=starting_equity,
            cash=starting_equity
        )

        sleeves = [
            Sleeve(
                sleeve_id=i,
                allocation_pct=allocation_pct
            )
            for i in range(sleeve_count)
        ]

        self.state = PortfolioState(
            campaign=campaign,
            sleeves=sleeves
        )

    # -------------------------------------------------
    # Helpers
    # -------------------------------------------------

    def campaign_active(self):
        return self.state.campaign.active

    def active_sleeves(self):
        return sum(
            1
            for s in self.state.sleeves
            if s.active
        )

    def sleeve(self, sleeve_id):
        return self.state.sleeves[sleeve_id]

    # -------------------------------------------------
    # Campaign Control
    # -------------------------------------------------

    def start_campaign(self, date):

        if self.state.campaign.active:
            return

        c = self.state.campaign

        c.active = True
        c.start_date = date
        c.bars = 0

        c.starting_equity = c.closed_equity
        c.current_equity = c.closed_equity
        c.cash = c.closed_equity

        for sleeve in self.state.sleeves:

            sleeve.active = False
            sleeve.entry_date = None
            sleeve.entry_price = 0.0
            sleeve.current_price = 0.0

            sleeve.shares = 0.0

            sleeve.market_value = 0.0

            sleeve.realized_pnl = 0.0
            sleeve.unrealized_pnl = 0.0

    def end_campaign(self):

        if not self.state.campaign.active:
            return

        c = self.state.campaign

        c.closed_equity = c.current_equity
        c.cash = c.current_equity
        c.active = False

    # -------------------------------------------------
    # Orders
    # -------------------------------------------------

    def buy(
        self,
        sleeve_id,
        date,
        price
    ):

        sleeve = self.sleeve(sleeve_id)

        if sleeve.active:
            return

        if not self.campaign_active():
            self.start_campaign(date)

        allocation = (
            self.state.campaign.starting_equity
            *
            sleeve.allocation_pct
        )

        shares = allocation / price

        sleeve.active = True
        sleeve.entry_date = date
        sleeve.entry_price = price

        sleeve.current_price = price
        sleeve.shares = shares

        sleeve.market_value = shares * price

        self.state.campaign.cash -= allocation

    def sell(
        self,
        sleeve_id,
        price
    ):

        sleeve = self.sleeve(sleeve_id)

        if not sleeve.active:
            return

        value = sleeve.shares * price

        pnl = value - (
            sleeve.shares
            * sleeve.entry_price
        )

        sleeve.realized_pnl += pnl

        self.state.campaign.cash += value

        sleeve.active = False
        sleeve.current_price = price
        sleeve.market_value = 0.0

        sleeve.shares = 0.0
        sleeve.entry_price = 0.0
        sleeve.entry_date = None

        if self.active_sleeves() == 0:
            self.state.campaign.current_equity = self.state.campaign.cash
            self.state.campaign.closed_equity = self.state.campaign.current_equity
            self.end_campaign()

    # -------------------------------------------------
    # Daily Mark-to-Market
    # -------------------------------------------------

    def mark_to_market(self, close):

        total_value = self.state.campaign.cash

        for sleeve in self.state.sleeves:

            if sleeve.active:

                sleeve.current_price = close

                sleeve.market_value = (
                    sleeve.shares * close
                )

                sleeve.unrealized_pnl = (
                    sleeve.market_value
                    -
                    (
                        sleeve.shares
                        * sleeve.entry_price
                    )
                )

                total_value += sleeve.market_value

        self.state.campaign.current_equity = total_value

    # -------------------------------------------------
    # Advance One Trading Day
    # -------------------------------------------------

    def update_day(
        self,
        date,
        close
    ):

        if self.state.campaign.active:
            self.state.campaign.bars += 1

        self.mark_to_market(close)

        self.state.equity_curve.append(
            self.state.campaign.current_equity
        )

        snapshot = {
            "date": date,
            "equity": self.state.campaign.current_equity,
            "closed_equity": self.state.campaign.closed_equity,
            "cash": self.state.campaign.cash,
            "campaign_active": self.state.campaign.active,
            "active_sleeves": self.active_sleeves(),
            "sleeves": []
        }

        for sleeve in self.state.sleeves:

            snapshot["sleeves"].append({
                "sleeve_id": sleeve.sleeve_id,
                "active": sleeve.active,
                "shares": sleeve.shares,
                "entry_price": sleeve.entry_price,
                "current_price": sleeve.current_price,
                "market_value": sleeve.market_value,
                "realized_pnl": sleeve.realized_pnl,
                "unrealized_pnl": sleeve.unrealized_pnl
            })

        self.state.daily_states.append(snapshot)

    # -------------------------------------------------
    # Results
    # -------------------------------------------------

    def results(self):

        ending_equity = (
            self.state.campaign.current_equity
        )

        return {
            "starting_equity":
                self.state.campaign.starting_equity,

            "ending_equity":
                ending_equity,

            "equity_curve":
                self.state.equity_curve,

            "daily_states":
                deepcopy(
                    self.state.daily_states
                ),

            "campaign":
                deepcopy(
                    self.state.campaign
                ),

            "sleeves":
                deepcopy(
                    self.state.sleeves
                )
        }