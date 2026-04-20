"""WaFlow FastAPI application."""

from __future__ import annotations

import asyncio
from contextlib import asynccontextmanager
from datetime import datetime

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from . import ai, store
from .database import init_db
from .models import (
    Appointment, Business, Conversation, Customer, Payment, Template,
)


async def _load_demo_if_empty():
    try:
        if not store.get_collection("businesses"):
            from . import demo_data
            demo_data.seed_demo_data()
    except Exception:
        import traceback
        traceback.print_exc()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create Postgres table if DATABASE_URL is set; no-op otherwise.
    try:
        init_db()
    except Exception:
        import traceback
        traceback.print_exc()
    asyncio.create_task(_load_demo_if_empty())
    yield


app = FastAPI(
    title="WaFlow API",
    description="WhatsApp AI Assistant platform for small service businesses in Morelia, Mexico",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Request models ---

class WhatsAppMessage(BaseModel):
    from_phone: str
    to_business_id: str
    body: str


class AIProcessMessage(BaseModel):
    business_id: str
    customer_phone: str
    message: str


class AISetupRequest(BaseModel):
    category: str
    business_name: str


class AIReportRequest(BaseModel):
    business_id: str


class AIOptimizeRequest(BaseModel):
    business_id: str


# --- Health ---

@app.get("/api/health")
def health():
    return {"status": "ok", "service": "waflow", "region": "morelia"}


# --- Dashboard ---

@app.get("/api/v1/stats")
def get_stats():
    return store.compute_stats()


# --- Businesses ---

@app.get("/api/v1/businesses")
def list_businesses(category: str | None = None, city: str | None = None, status: str | None = None):
    items = store.get_collection("businesses")
    if category:
        items = [b for b in items if b.get("category") == category]
    if city:
        items = [b for b in items if b.get("city") == city]
    if status:
        items = [b for b in items if b.get("status") == status]
    return {"businesses": items, "total": len(items)}


@app.get("/api/v1/businesses/{business_id}")
def get_business(business_id: str):
    item = store.get_item("businesses", business_id)
    if not item:
        raise HTTPException(404, "Business not found")
    return item


@app.post("/api/v1/businesses")
def create_business(data: Business):
    return store.add_item("businesses", data.model_dump())


@app.put("/api/v1/businesses/{business_id}")
def update_business(business_id: str, updates: dict):
    item = store.update_item("businesses", business_id, updates)
    if not item:
        raise HTTPException(404, "Business not found")
    return item


# --- WhatsApp Webhook (simulated) ---

@app.post("/api/v1/webhook/whatsapp")
def webhook_whatsapp(msg: WhatsAppMessage):
    """Receive incoming WhatsApp message (simulated)."""
    business = store.get_item("businesses", msg.to_business_id)
    if not business:
        raise HTTPException(404, "Business not found")

    # Find or create conversation
    convos = store.get_collection("conversations")
    conv = None
    for c in convos:
        if c.get("business_id") == msg.to_business_id and c.get("customer_phone") == msg.from_phone and c.get("status") == "active":
            conv = c
            break

    if not conv:
        conv = {
            "id": f"conv-auto-{datetime.utcnow().strftime('%H%M%S')}",
            "business_id": msg.to_business_id,
            "customer_phone": msg.from_phone,
            "messages": [],
            "status": "active",
            "started_at": datetime.utcnow().isoformat(),
            "resolved_at": None,
        }
        store.add_item("conversations", conv)

    # Add customer message
    customer_msg = {
        "role": "customer",
        "content": msg.body,
        "timestamp": datetime.utcnow().isoformat(),
        "message_type": "text",
    }
    conv.setdefault("messages", []).append(customer_msg)

    # Log webhook event
    store.add_item("webhook_events", {
        "id": f"wh-auto-{datetime.utcnow().strftime('%H%M%S')}",
        "business_id": msg.to_business_id,
        "event_type": "message_received",
        "payload": {"from": msg.from_phone, "body": msg.body},
        "processed": True,
        "timestamp": datetime.utcnow().isoformat(),
    })

    # AI response
    try:
        result = ai.process_customer_message(business, conv, msg.body)
    except Exception:
        result = {
            "response": f"Hola! Gracias por escribir a {business['name']}. En un momento te atendemos.",
            "action": "none",
            "sentiment": "neutral",
        }

    # Add AI response to conversation
    ai_msg = {
        "role": "assistant",
        "content": result.get("response", ""),
        "timestamp": datetime.utcnow().isoformat(),
        "message_type": result.get("action", "text"),
    }
    conv["messages"].append(ai_msg)

    # Update conversation in store
    store.update_item("conversations", conv["id"], {"messages": conv["messages"]})

    return {
        "response": result.get("response", ""),
        "action": result.get("action", "none"),
        "booking_details": result.get("booking_details"),
        "sentiment": result.get("sentiment", "neutral"),
    }


@app.post("/api/v1/webhook/status")
def webhook_status(payload: dict):
    """Message status updates (simulated)."""
    store.add_item("webhook_events", {
        "id": f"wh-st-{datetime.utcnow().strftime('%H%M%S')}",
        "business_id": payload.get("business_id", ""),
        "event_type": "status_update",
        "payload": payload,
        "processed": True,
        "timestamp": datetime.utcnow().isoformat(),
    })
    return {"ok": True}


# --- Conversations ---

@app.get("/api/v1/conversations")
def list_conversations(business_id: str | None = None, status: str | None = None):
    items = store.get_collection("conversations")
    if business_id:
        items = [c for c in items if c.get("business_id") == business_id]
    if status:
        items = [c for c in items if c.get("status") == status]
    return {"conversations": items, "total": len(items)}


@app.get("/api/v1/conversations/{conv_id}")
def get_conversation(conv_id: str):
    item = store.get_item("conversations", conv_id)
    if not item:
        raise HTTPException(404, "Conversation not found")
    return item


@app.post("/api/v1/conversations/{conv_id}/reply")
def reply_conversation(conv_id: str, body: dict):
    """Manual reply to a conversation."""
    conv = store.get_item("conversations", conv_id)
    if not conv:
        raise HTTPException(404, "Conversation not found")
    msg = {
        "role": "assistant",
        "content": body.get("message", ""),
        "timestamp": datetime.utcnow().isoformat(),
        "message_type": "text",
    }
    conv.setdefault("messages", []).append(msg)
    store.update_item("conversations", conv_id, {"messages": conv["messages"]})
    return {"ok": True, "message": msg}


# --- Appointments ---

@app.get("/api/v1/appointments")
def list_appointments(business_id: str | None = None, date: str | None = None, status: str | None = None):
    items = store.get_collection("appointments")
    if business_id:
        items = [a for a in items if a.get("business_id") == business_id]
    if date:
        items = [a for a in items if a.get("date") == date]
    if status:
        items = [a for a in items if a.get("status") == status]
    return {"appointments": items, "total": len(items)}


@app.post("/api/v1/appointments")
def create_appointment(data: Appointment):
    return store.add_item("appointments", data.model_dump())


@app.put("/api/v1/appointments/{appt_id}")
def update_appointment(appt_id: str, updates: dict):
    item = store.update_item("appointments", appt_id, updates)
    if not item:
        raise HTTPException(404, "Appointment not found")
    return item


# --- Customers ---

@app.get("/api/v1/customers")
def list_customers(business_id: str | None = None):
    items = store.get_collection("customers")
    if business_id:
        items = [c for c in items if business_id in c.get("business_ids", [])]
    return {"customers": items, "total": len(items)}


# --- Payments ---

@app.get("/api/v1/payments")
def list_payments(business_id: str | None = None, status: str | None = None):
    items = store.get_collection("payments")
    if business_id:
        items = [p for p in items if p.get("business_id") == business_id]
    if status:
        items = [p for p in items if p.get("status") == status]
    return {"payments": items, "total": len(items)}


@app.post("/api/v1/payments")
def create_payment(data: Payment):
    return store.add_item("payments", data.model_dump())


@app.put("/api/v1/payments/{payment_id}")
def update_payment(payment_id: str, updates: dict):
    item = store.update_item("payments", payment_id, updates)
    if not item:
        raise HTTPException(404, "Payment not found")
    return item


# --- Templates ---

@app.get("/api/v1/templates")
def list_templates(business_id: str | None = None):
    items = store.get_collection("templates")
    if business_id:
        items = [t for t in items if t.get("business_id") == business_id]
    return {"templates": items, "total": len(items)}


@app.put("/api/v1/templates/{template_id}")
def update_template(template_id: str, updates: dict):
    item = store.update_item("templates", template_id, updates)
    if not item:
        raise HTTPException(404, "Template not found")
    return item


# --- Analytics ---

@app.get("/api/v1/analytics")
def list_analytics(business_id: str | None = None, period: str | None = None, days: int = 7):
    items = store.get_collection("analytics")
    if business_id:
        items = [a for a in items if a.get("business_id") == business_id]
    if period:
        items = [a for a in items if a.get("period") == period]
    # Sort by date descending and limit
    items.sort(key=lambda x: x.get("date", ""), reverse=True)
    return {"analytics": items[:days * 15], "total": len(items)}


# --- AI Endpoints ---

@app.post("/api/v1/ai/process-message")
def ai_process_message(req: AIProcessMessage):
    """Simulate AI response to a customer message — maintains full conversation history."""
    from datetime import datetime as dt

    business = store.get_item("businesses", req.business_id)
    if not business:
        raise HTTPException(404, "Business not found")

    # Find or create conversation for this business+customer pair
    convos = store.get_collection("conversations")
    conv = None
    for c in convos:
        if c.get("business_id") == req.business_id and c.get("customer_phone") == req.customer_phone:
            conv = c
            break

    if conv is None:
        conv = {
            "id": f"conv-sim-{req.business_id}-{req.customer_phone.replace(' ','').replace('+','')}",
            "business_id": req.business_id,
            "customer_phone": req.customer_phone,
            "messages": [],
            "status": "active",
            "started_at": dt.utcnow().isoformat(),
        }
        store.add_item("conversations", conv)

    # Add customer message to conversation history BEFORE calling AI
    conv["messages"].append({
        "role": "customer",
        "content": req.message,
        "timestamp": dt.utcnow().isoformat(),
        "message_type": "text",
    })

    try:
        result = ai.process_customer_message(business, conv, req.message)
    except Exception as e:
        result = {
            "response": f"Hola! Gracias por escribir a {business['name']}. En un momento te atendemos. 😊",
            "action": "none",
            "sentiment": "neutral",
        }

    # Add AI response to conversation history AFTER getting response
    conv["messages"].append({
        "role": "assistant",
        "content": result.get("response", ""),
        "timestamp": dt.utcnow().isoformat(),
        "message_type": result.get("action", "text"),
    })

    # Persist full conversation so next message has context
    store.update_item("conversations", conv["id"], {"messages": conv["messages"]})

    return result


@app.post("/api/v1/ai/setup")
def ai_setup(req: AISetupRequest):
    """Auto-generate business configuration."""
    try:
        return ai.generate_business_setup(req.category, req.business_name)
    except Exception as e:
        raise HTTPException(500, str(e))


@app.post("/api/v1/ai/report")
def ai_report(req: AIReportRequest):
    """Generate weekly report for a business."""
    business = store.get_item("businesses", req.business_id)
    if not business:
        raise HTTPException(404, "Business not found")
    analytics_data = [a for a in store.get_collection("analytics") if a.get("business_id") == req.business_id]
    try:
        return ai.generate_weekly_report(analytics_data[:7], business)
    except Exception as e:
        raise HTTPException(500, str(e))


@app.post("/api/v1/ai/optimize-schedule")
def ai_optimize_schedule(req: AIReportRequest):
    """Scheduling optimization."""
    business = store.get_item("businesses", req.business_id)
    if not business:
        raise HTTPException(404, "Business not found")
    appts = [a for a in store.get_collection("appointments") if a.get("business_id") == req.business_id]
    try:
        return ai.optimize_schedule(appts, business.get("working_hours", {}))
    except Exception as e:
        raise HTTPException(500, str(e))
