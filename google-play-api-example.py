"""
Google Play API: A Quick Start Example
See more at: https://apify.com/johnvc/google-play-api?fpr=9n7kx3
Input schema: https://apify.com/johnvc/google-play-api/input-schema?fpr=9n7kx3

This script shows how to call the Google Play API on Apify from Python and
read its structured JSON output. The default run stays deliberately small so
your first call is inexpensive; the --example recipes mirror the API's main
use cases (see the README Recipes section).

Get your free Apify API key at: https://apify.com?fpr=9n7kx3

Examples:
  uv run python google-play-api-example.py
  uv run python google-play-api-example.py --example version_history
"""

from __future__ import annotations

import argparse
import os
from typing import Any

from apify_client import ApifyClient
from dotenv import load_dotenv

load_dotenv()

ACTOR_ID = "johnvc/google-play-api"


def _print_items(items: list[dict[str, Any]]) -> None:
    """Print a short summary of dataset items."""
    print(f"Returned {len(items)} item(s).\n")
    for item in items:
        print(item.get('title'), item.get('developer'), item.get('rating'), item.get('downloads'))


def run_default(client: ApifyClient) -> None:
    """Cheap general quick-start. Inputs stay small on purpose."""
    run_input: dict[str, Any] = {
        "search_mode": "search",
        "query": "fitness",
        "max_results": 3,  # small on purpose to keep the first run inexpensive
    }
    run = client.actor(ACTOR_ID).call(run_input=run_input)
    if run is None:
        raise SystemExit("The Actor run did not return a result.")
    items = list(client.dataset(run.default_dataset_id).iterate_items())
    _print_items(items)


def run_version_history(client: ApifyClient) -> None:
    """One release-cadence snapshot (mirrors the app-version-history use case).

    Schedule this and store version + updatedOn per run; the series is the
    version history Google Play never shows.
    """
    run_input: dict[str, Any] = {
        "search_mode": "product",
        "product_id": "homeworkout.homeworkouts.noequipment",
    }
    run = client.actor(ACTOR_ID).call(run_input=run_input)
    if run is None:
        raise SystemExit("The Actor run did not return a result.")
    for item in client.dataset(run.default_dataset_id).iterate_items():
        print(f"{item.get('title')}: version={item.get('version')} updated={item.get('updatedOn')} released={item.get('releasedOn')}")


def run_reviews_export(client: ApifyClient) -> None:
    """Export a few reviews (mirrors the google-play-reviews-exporter use case)."""
    run_input: dict[str, Any] = {
        "search_mode": "reviews",
        "product_id": "homeworkout.homeworkouts.noequipment",
        "max_results": 3,  # small on purpose; raise once you know your budget
    }
    run = client.actor(ACTOR_ID).call(run_input=run_input)
    if run is None:
        raise SystemExit("The Actor run did not return a result.")
    items = list(client.dataset(run.default_dataset_id).iterate_items())
    _print_items(items)


def main() -> None:
    """Dispatch a quick-start or use-case recipe."""
    parser = argparse.ArgumentParser(description="Google Play API examples")
    parser.add_argument(
        "--example",
        default="default",
        choices=['default', 'version_history', 'reviews_export'],
        help="Which recipe to run (see README Recipes).",
    )
    args = parser.parse_args()

    token = os.getenv("APIFY_API_TOKEN")
    if not token:
        raise SystemExit("Set APIFY_API_TOKEN in .env or the environment.")

    client = ApifyClient(token)
    dispatch = {
        "default": run_default,
        "version_history": run_version_history,
        "reviews_export": run_reviews_export,
    }
    dispatch[args.example](client)


if __name__ == "__main__":
    main()
