# Tomorrow's Close - Project Specification

## Purpose

Tomorrow's Close is a platform that reverse-calculates trading indicator trigger prices so traders know the exact closing price required to generate a signal before the market close.

The core concept:

Instead of asking:
"Did my indicator trigger today?"

Tomorrow's Close answers:
"What closing price would trigger my indicator?"

The system is designed around close-based trading strategies using Limit-On-Close (LOC) execution.

---

# Core Architecture

The system is divided into four major layers:

## 1. Market Data Layer

Responsible only for obtaining and validating market data.

Responsibilities:
- Retrieve OHLCV data.
- Track data source.
- Support validation against multiple providers.
- Provide historical data for calculations.

The market data layer does not calculate indicators or signals.

---

## 2. Engine Layer

The engine coordinates the system.

Responsibilities:
- Receive user inputs.
- Request market data.
- Call the appropriate indicator solver.
- Return standardized results.

The engine does not contain indicator calculations.

---

## 3. Indicator Layer

Each indicator has its own module.

Examples:
- RSI
- Donchian Channels
- SMA
- Moving Average Crossovers

Each indicator module:
- Receives market data.
- Receives user parameters.
- Calculates required values.
- Returns standardized output.

---

## 4. Strategy Layer

Strategies combine indicators and determine trade interpretation.

Examples:
- LowHigh
- RSI PriceSolver
- RSI UlcerShield
- Donchian Breakout
- Moving Average Crossover

Strategies determine whether the output represents:
- Mean reversion.
- Momentum.
- Breakout.
- Trend following.

---

# Phase 1 Goals

The first version focuses on end-of-day strategies.

Requirements:

- Daily closing data only.
- Prices locked after market close.
- No intraday updating.
- Results represent the next trading decision.

Initial strategies:

1. RSI PriceSolver
2. RSI UlcerShield
3. LowHigh
4. Moving Average Crossover
5. Donchian Breakout

---

# Initial Indicators

Phase 1 indicators:

- RSI
- Donchian
- SMA
- Moving Average relationships
- Price change calculations

Future indicators can be added without changing the engine.

---

# User Experience

Each major indicator and strategy has its own SEO-friendly page.

Example:

tomorrowsclose.com/rsi

tomorrowsclose.com/lowhigh

Pages contain:

1. Calculator/results section at the top.
2. Explanation below.
3. Strategy education.
4. Implementation details.

Users should be able to:
- Use default parameters.
- Change parameters.
- Save preferences locally.

---

# Results Format

Outputs should clearly describe the order type.

Examples:

"Buy on close below 695.25"

"Sell on close above 710.50"

"Break above 720.00"

"Break below 680.00"

"Between 690.00 and 700.00"

The wording should explain how the trader should interpret the value.

---

# Free vs Paid Model

Free version:
- Limited ETFs.
- Selected major indexes.
- Includes at least one free UlcerShield implementation.

Possible free ETFs:
- SPY
- DIA
- QQQ
- VOO
- International index ETF

Paid version:
- Expanded ETF support.
- Full strategy access.
- User-selected tickers.

---

# Future Features

- Data Confidence Index.
- Multiple data source comparison.
- User indicator suggestions.
- Additional PriceSolver algorithms.
- Intraday adaptive indicators.
