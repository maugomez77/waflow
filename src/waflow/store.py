"""WaFlow JSON store — hybrid persistence layer."""

from __future__ import annotations

import json
from datetime import date, datetime
from pathlib import Path
from typing import Any

STORE_DIR = Path.home() / ".waflow"
STORE_FILE = STORE_DIR / "store.json"

COLLECTIONS = [
    "businesses", "customers", "appointments", "conversations",
    "payments", "templates", "analytics", "webhook_events",
]


def _ensure_dir() -> None:
    STORE_DIR.mkdir(parents=True, exist_ok=True)


def load_store() -> dict[str, list[dict]]:
    _ensure_dir()
    if STORE_FILE.exists():
        return json.loads(STORE_FILE.read_text())
    return {k: [] for k in COLLECTIONS}


def save_store(data: dict[str, list[dict]]) -> None:
    _ensure_dir()
    STORE_FILE.write_text(json.dumps(data, indent=2, default=str))


def get_collection(name: str) -> list[dict]:
    return load_store().get(name, [])


def add_item(collection: str, item: dict) -> dict:
    store = load_store()
    store.setdefault(collection, []).append(item)
    save_store(store)
    return item


def update_item(collection: str, item_id: str, updates: dict) -> dict | None:
    store = load_store()
    for item in store.get(collection, []):
        if item.get("id") == item_id:
            item.update(updates)
            save_store(store)
            return item
    return None


def delete_item(collection: str, item_id: str) -> bool:
    store = load_store()
    items = store.get(collection, [])
    before = len(items)
    store[collection] = [i for i in items if i.get("id") != item_id]
    if len(store[collection]) < before:
        save_store(store)
        return True
    return False


def get_item(collection: str, item_id: str) -> dict | None:
    for item in get_collection(collection):
        if item.get("id") == item_id:
            return item
    return None


def count_collection(collection: str) -> int:
    return len(get_collection(collection))


def compute_stats() -> dict[str, Any]:
    store = load_store()
    businesses = store.get("businesses", [])
    appointments = store.get("appointments", [])
    conversations = store.get("conversations", [])
    payments = store.get("payments", [])
    analytics = store.get("analytics", [])

    active_biz = [b for b in businesses if b.get("status") == "active"]

    today_str = date.today().isoformat()
    today_appts = [a for a in appointments if a.get("date") == today_str]

    # Count today's messages from conversations
    today_msgs = 0
    for c in conversations:
        for m in c.get("messages", []):
            ts = m.get("timestamp", "")
            if isinstance(ts, str) and ts.startswith(today_str):
                today_msgs += 1

    # Monthly revenue from paid payments
    paid = [p for p in payments if p.get("status") in ("paid", "sent")]
    monthly_rev = sum(p.get("amount_mxn", 0) for p in paid)

    # Subscription revenue
    sub_rev = sum(b.get("monthly_fee_mxn", 0) for b in active_biz)

    # Avg response time from analytics
    response_times = [a.get("response_time_avg_seconds", 0) for a in analytics if a.get("response_time_avg_seconds", 0) > 0]
    avg_resp = sum(response_times) / len(response_times) if response_times else 0

    # Top categories
    cat_counts: dict[str, int] = {}
    for b in businesses:
        cat = b.get("category", "other")
        cat_counts[cat] = cat_counts.get(cat, 0) + 1
    top_cats = sorted(cat_counts.items(), key=lambda x: x[1], reverse=True)[:5]

    return {
        "total_businesses": len(businesses),
        "active_businesses": len(active_biz),
        "total_appointments_today": len(today_appts),
        "total_messages_today": today_msgs,
        "monthly_revenue_mxn": round(monthly_rev, 2),
        "subscription_revenue_mxn": round(sub_rev, 2),
        "avg_response_time_seconds": round(avg_resp, 1),
        "top_categories": [{"category": c, "count": n} for c, n in top_cats],
        "total_customers": len(store.get("customers", [])),
        "total_appointments": len(appointments),
        "total_conversations": len(conversations),
        "active_conversations": len([c for c in conversations if c.get("status") == "active"]),
    }
