# Tomorrow's Close - Development Standards

## Core Rule

Build slowly. Keep every step working.

Every change should follow:

1. Build one component.
2. Test it.
3. Commit it.
4. Move forward.

Never commit broken code.

---

# Architecture Rules

## Market Data

The market_data folder is the only place allowed to communicate with external data providers.

Examples:
- Yahoo Finance
- Polygon
- Other APIs

Indicators and strategies never retrieve their own data.

---

## Engine

The engine coordinates the application.

The engine:
- Receives requests.
- Calls market data.
- Calls indicators.
- Calls strategies.
- Returns results.

The engine does not contain trading logic.

---

## Indicators

Every indicator has its own module.

Indicators:
- Calculate mathematical values.
- Accept parameters.
- Return standardized results.

Indicators do not:
- Fetch data.
- Decide trades.
- Handle website output.

---

## Strategies

Strategies interpret indicators.

Strategies:
- Define trading rules.
- Determine buy/sell direction.
- Format signal meaning.

Strategies do not:
- Download prices.
- Duplicate indicator calculations.

---

# Coding Rules

## Keep Files Modular

Avoid large files.

Prefer:
- One purpose per file.
- Clear names.
- Simple functions.

---

## Testing

Every major module requires a test.

Before adding new features:
- Existing tests must pass.

---

## Data Handling

Daily strategies use locked closing prices.

Phase 1 and Phase 2:
- No intraday updates.
- Closing price finalized after settlement period.

Future intraday strategies may use live prices.

---

# Git Rules

Before committing:

1. Test the code.
2. Confirm output.
3. Commit a working version.

Commit messages should describe the change.

Example:

"Added Yahoo Finance market data provider"

---

# Naming Rules

Use descriptive names.

Good:
- rsi_solver.py
- market_provider.py
- donchian_channel.py

Avoid:
- stuff.py
- test2.py
- new_code.py

---

# Development Philosophy

Avoid premature complexity.

Build the foundation first.

A simple working system is better than a complex unfinished system.