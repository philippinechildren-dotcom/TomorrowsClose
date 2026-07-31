# Tomorrow's Close System Architecture

## Purpose

Tomorrow's Close consists of independent systems, each responsible for one specific job.

The architecture is intentionally modular so that each system can evolve independently without requiring major changes to the others.

---

# System Overview

```
Visitor
    │
    ▼
Cloudflare
    │
    ├────────────► Ghost Website
    │                  │
    │                  ▼
    │          Membership & Navigation
    │                  │
    │                  ▼
    │          JavaScript API Requests
    │                  │
    ▼                  ▼
Render (Flask API & Scheduler)
    │
    ▼
Python Calculation Engine
    │
    ▼
PriceSolver / Strategy Logic
```

---

# Responsibilities

## Cloudflare

Responsibilities

* Domain registration
* DNS management
* SSL (HTTPS)
* Direct traffic to services

Examples

```
tomorrowsclose.com
```

→ Ghost

```
api.tomorrowsclose.com
```

→ Render

Cloudflare performs no calculations.

---

## Ghost

Ghost is responsible for everything the visitor sees.

Responsibilities

* Website
* Marketing pages
* Articles
* Navigation
* Membership
* Stripe subscriptions
* Login
* Email newsletters
* Restricting Free vs Paid pages

Ghost does **not** calculate trading signals.

---

## Render

Render hosts the Python application.

Responsibilities

* Flask API
* Daily scheduler
* Execute calculations
* Return JSON responses

Render does **not** manage subscriptions.

Render assumes Ghost has already determined what page the visitor is allowed to access.

---

## Python Calculation Engine

Responsibilities

* RSI PriceSolver
* LowHigh
* UlcerShield
* Future Strategy Lab
* Indicator calculations
* Trading logic

The calculation engine contains **no website code**.

---

# Scheduler

Runs once each trading day after market close.

Responsibilities

* Download market data
* Calculate all EasyMode systems
* Generate daily outputs
* Save precomputed daily results

Interactive user calculations are **not** stored.

---

# Interactive Requests

When a visitor changes parameters:

```
Ghost Page

↓

JavaScript

↓

Render API

↓

Python

↓

Return JSON

↓

Update Page
```

Nothing is written to disk.

Each request is independent.

---

# Daily Static Pages

The scheduler creates precomputed results once each trading day.

Ghost displays those results on the appropriate pages.

Examples

* Free Dashboard
* Paid Dashboard
* Daily Signal Pages

---

# Membership Model

Ghost determines membership status.

Guest

↓

Marketing pages only

Free Member

↓

Free system pages

Paid Member

↓

Paid system pages

The Python backend does not manage authentication.

---

# Design Principles

1. One responsibility per system.
2. Trading logic never contains website code.
3. Website code never contains trading logic.
4. Ghost manages users.
5. Render manages calculations.
6. Cloudflare routes traffic.
7. The scheduler generates precomputed daily outputs for pages and emails. Interactive pages calculate on demand and do not use stored JSON results.
8. Interactive requests calculate on demand.
9. Build once, reuse everywhere.

---

# Long-Term Goal

Ghost becomes the complete customer-facing website.

Render becomes the calculation engine behind every interactive feature.

The trading algorithms remain completely independent of the website and can be reused by future products without modification.
