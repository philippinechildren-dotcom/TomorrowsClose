# Tomorrow's Close Repository Architecture

## Repository Philosophy

The repository should mirror the Tomorrow's Close website.

A developer should be able to understand the project simply by reading the folder structure.

The website drives the repository.

The repository does **not** drive the website.

We ask:
1. Which strategy owns this?

2. Which folder does it belong in?
   - logic
   - website
   - settings
   - tests

3. What does it do?

4. Can I understand its purpose from the filename alone?

---

# Planned Repository Structure

EasyMode/

    RSI_PriceSolver/

        logic/

            calculate_signal.py

            calculate_performance.py

            build_webpage_data.py

        website/

            webpage.py

            webpage.html

        settings/

            defaults.py

            metadata.py

        tests/

            test_signal.py

            test_performance.py

```
Tomorrow's Close
│
├── EasyMode
│   │
│   ├── RSI PriceSolver
│   │   ├── engine
│   │   ├── performance
│   │   ├── website
│   │   ├── settings
│   │   └── tests
│   │
│   ├── UlcerShield
│   │   ├── engine
│   │   ├── performance
│   │   ├── website
│   │   ├── settings
│   │   └── tests
│   │
│   └── LowHigh
│       ├── engine
│       ├── performance
│       ├── website
│       ├── settings
│       └── tests
│
├── Other Strategies
│   │
│   ├── Mean Reversion
│   │   ├── Strategy A
│   │   ├── Strategy B
│   │   └── ...
│   │
│   ├── Momentum
│   │   ├── Strategy A
│   │   ├── Strategy B
│   │   └── ...
│   │
│   └── Trend Following
│       ├── Strategy A
│       ├── Strategy B
│       └── ...
│
├── Performance Rankings
│   ├── engine
│   ├── website
│   ├── cache
│   └── tests
│
├── Log
│   ├── website
│   ├── history
│   └── search
│
├── Library
│   │
│   ├── Indicators
│   ├── PriceSolvers
│   ├── Trading Concepts
│   ├── Tutorials
│   └── Glossary
│
├── Books
│
├── Pricing
│
├── About
│
├── Utilities
│   │
│   ├── Market Data
│   ├── Indicators
│   ├── Performance Metrics
│   ├── Trade Engine
│   ├── Formatting
│   ├── Order Rounding
│   └── Date Utilities
│
└── Tests
```

---

# Design Rules

- The repository should mirror the website.
- Every strategy should have the same internal organization.
- Every strategy should own its own calculations whenever practical.
- Performance Rankings gathers information from strategies but never owns them.
- Utilities contain only reusable tools.
- Folder names should describe Tomorrow's Close rather than Flask or Python concepts.
- Clarity is more important than minimizing duplicate code.
- A change to one strategy should rarely affect another strategy.
- Circular dependencies are never allowed.

• Every strategy is self-contained.
• Every strategy uses the same folder structure.
• Folder names describe WHAT something is.
• File names describe WHAT they do.
• Shared code belongs in Utilities only if it is truly reused by multiple strategies.
• Duplicate code is acceptable when it improves readability and keeps strategies independent.
• The website structure drives the repository structure.