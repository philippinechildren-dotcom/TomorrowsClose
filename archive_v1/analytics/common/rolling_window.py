from datetime import datetime


def filter_complete_positions(
    positions: list,
    start_date: datetime,
    end_date: datetime,
) -> list:
    """
    Filters completed trades or campaigns using
    Tomorrow's Close reporting rules.

    Rules
    -----
    1. If the reporting window begins during an active
       position, include the entire position.

    2. If the reporting window ends during an active
       position, exclude that position entirely.

    3. Only completed positions are returned.
    """

    filtered = []

    for position in positions:

        entry = position["entry_date"]
        exit = position["exit_date"]

        # Ignore anything that finished before the window.
        if exit < start_date:
            continue

        # Ignore anything that starts after the window.
        if entry > end_date:
            continue

        # Window begins during this position.
        # Include the complete position.
        if entry < start_date <= exit:
            filtered.append(position)
            continue

        # Window ends during this position.
        # Exclude it entirely.
        if entry <= end_date < exit:
            continue

        # Position is completely inside the window.
        filtered.append(position)

    return filtered