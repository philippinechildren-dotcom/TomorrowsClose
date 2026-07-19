# Tomorrow's Close

Tomorrow's Close is an open-source platform for calculating **Signal Zones**: the market prices at which technical indicators and trading strategies become true.

Instead of asking:

> "What is my indicator value?"

Tomorrow's Close answers:

> "At what price will my indicator generate a signal?"

The platform is designed for systematic traders who want to know important trigger prices before the market closes.

## Goals

* Calculate Signal Zones for technical indicators.
* Support complete trading strategies built on those indicators.
* Provide transparent, validated market data.
* Separate calculation logic from presentation.
* Build a modular architecture that can easily support new indicators and strategies.

## Initial Version

The first release will focus on:

* RSI
* Donchian Channels
* Simple Moving Averages
* LowHigh Strategy
* RSI PriceSolver
* UlcerShield

Additional indicators and strategies will be added over time.

## Architecture

Tomorrow's Close is built around a modular design:

Website

↓

Presentation Layer

↓

Tomorrow's Close Engine

↓

Indicator Solver / Strategy Solver

↓

Market Data Layer

↓

Market Data Provider

Each component has a single responsibility, making the platform easy to maintain and extend.

## License

This project is under active development.
