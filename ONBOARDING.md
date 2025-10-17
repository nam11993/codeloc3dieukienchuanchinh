# Onboarding Guide

Welcome to the Stock Scanner Vietnam project! This document gives you a high-level map of the repository, highlights the most important modules, and suggests next steps for diving deeper.

## Repository Layout

| Path | Purpose |
| ---- | ------- |
| `app.py` | Telegram bot plus all shared scanning logic (data fetch, indicators, filters). |
| `webapp_simple.py` | Production Streamlit UI that wraps the scanner for the web. |
| `streamlit_app.py` | Experimental Streamlit UI with richer components (charts, CafeF fallback). |
| `demo_signals.py` | CLI demo that prints sample signal classifications. |
| `clear_bot.py` | Utility for clearing Telegram bot updates. |
| `symbols.json` / `symbols_clean.json` | Cached symbol lists used when APIs are slow. |
| `requirements.txt` / `requirements_webapp.txt` | Dependency pins for the bot and web app. |
| `README.md`, `README_WEBAPP.md`, etc. | Product-level docs written in Vietnamese. |

There is no `scanner_core.py` in this repo—the functionality described in some docs lives inside `app.py`.

## Core Scanning Pipeline

All scanning logic is orchestrated from `app.py`:

1. **Load symbol metadata** via `fetch_all_symbols()`, which reads from `symbols.json` for 200+ Vietnamese tickers. 【F:app.py†L86-L116】
2. **Pull market data** with `fetch_symbol_bundle*` helpers. They call the VNDIRECT REST endpoints to retrieve 1-minute intraday candles and ~120 days of daily bars and compute the latest price and percentage change. 【F:app.py†L118-L257】【F:app.py†L560-L577】
3. **Apply filters**:
   * `apply_filters()` encodes the original “MUA 1” rule set (Buy Break, Buy Normal, Sell, Short, Cover, Sideway) using moving averages, rolling highs/lows, RSI, and liquidity checks. 【F:app.py†L268-L332】
   * `apply_filters_sin()` and `apply_filters_sin2()` cover the stricter “MUA SỊN” variations. 【F:app.py†L334-L427】
4. **Parallel scanning** happens in `scan_symbols*()` which fan out requests with a `ThreadPoolExecutor`, collect bundles, run the filters, and return only tickers that triggered signals. 【F:app.py†L560-L664】
5. **Surface results** either in Telegram (handlers build inline keyboards, chunk results, and add summary stats) or via Streamlit UIs that call the same scanning helpers.

Because the filters work on Pandas DataFrames, most enhancements boil down to manipulating those frames before the boolean checks.

## Telegram Bot Overview

The bot logic (also in `app.py`) uses `python-telegram-bot` v21’s async API. Key entry points:

- `cmd_start()` registers reply buttons for the scan commands. 【F:app.py†L666-L696】
- `handle_text()` inspects user input and launches `run_scan()` or `run_scan_sin()` coroutines to trigger scans and format HTML responses (chunked per 100 tickers, grouped by signal type, and annotated with stats and timestamps). 【F:app.py†L699-L917】
- `main()` wires everything together by reading `TELEGRAM_BOT_TOKEN` from `.env` and starting the event loop. 【F:app.py†L951-L1021】

If you need to debug the bot, run `python clear_bot.py` to flush stale updates. 【F:clear_bot.py†L1-L62】

## Streamlit Web Apps

Two Streamlit entry points exist:

- `webapp_simple.py` is the polished UI that mirrors the product spec screenshot—styled headers, sidebar filter descriptions, metrics, results grid, and CSV export. It loads ticker codes, calls `scan_symbols*()`, and renders metrics per filter. 【F:webapp_simple.py†L1-L211】【F:webapp_simple.py†L220-L312】
- `streamlit_app.py` is an in-progress rewrite mixing advanced features (CafeF backup data, Plotly charts, custom components). Review before using—it currently contains duplicated imports from merge work and needs cleanup. 【F:streamlit_app.py†L1-L120】

Run either app with `streamlit run webapp_simple.py` after installing `requirements_webapp.txt`. 【F:README_WEBAPP.md†L1-L26】

## Working With Data

- The scanner relies on VNDIRECT’s public endpoints. Network hiccups are common, so the code retries and falls back to local JSON.
- Intraday price uses the most recent 1-minute candle; percent change is relative to the previous close. 【F:app.py†L208-L257】【F:app.py†L560-L577】
- Local symbol JSONs should be updated manually if the market listing changes.

## Suggested Next Steps

1. **Run the Telegram bot**: create a `.env` with `TELEGRAM_BOT_TOKEN`, install `requirements.txt`, and execute `python app.py` to watch real scan output.
2. **Experiment with filters**: tweak thresholds inside `apply_filters*()` and rerun `demo_signals.py` or the Streamlit app to see how classifications shift.
3. **Stabilize `streamlit_app.py`**: if you need charts or CafeF data, clean up the file and ensure it reuses the shared scanner helpers.
4. **Add tests or logging**: the project currently lacks automated tests—consider adding unit tests for the filter functions or structured logging around API calls.
5. **Monitor performance**: adjust `MAX_WORKERS` or API timeouts in `app.py` if you observe throttling. 【F:app.py†L60-L101】

Welcome aboard, and happy scanning!
