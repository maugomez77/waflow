"""WaFlow data models."""

from __future__ import annotations

import uuid
from datetime import date, datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


# --- Enums ---

class BusinessCategory(str, Enum):
    restaurant = "restaurant"
    salon = "salon"
    mechanic = "mechanic"
    clinic = "clinic"
    dentist = "dentist"
    gym = "gym"
    veterinary = "veterinary"
    laundry = "laundry"
    tutoring = "tutoring"
    other = "other"


class City(str, Enum):
    morelia = "morelia"
    patzcuaro = "patzcuaro"
    uruapan = "uruapan"
    zamora = "zamora"


class SubscriptionTier(str, Enum):
    free_trial = "free_trial"
    basic = "basic"
    pro = "pro"
    premium = "premium"


class BusinessStatus(str, Enum):
    active = "active"
    paused = "paused"
    cancelled = "cancelled"


class AppointmentStatus(str, Enum):
    pending = "pending"
    confirmed = "confirmed"
    completed = "completed"
    cancelled = "cancelled"
    no_show = "no_show"


class ConversationStatus(str, Enum):
    active = "active"
    resolved = "resolved"
    escalated = "escalated"


class MessageRole(str, Enum):
    customer = "customer"
    assistant = "assistant"
    system = "system"


class MessageType(str, Enum):
    text = "text"
    booking = "booking"
    confirmation = "confirmation"
    reminder = "reminder"
    payment = "payment"
    escalation = "escalation"


class PaymentStatus(str, Enum):
    pending = "pending"
    sent = "sent"
    paid = "paid"
    failed = "failed"


class PaymentMethod(str, Enum):
    transfer = "transfer"
    card = "card"
    cash = "cash"


class TemplateType(str, Enum):
    greeting = "greeting"
    booking_confirm = "booking_confirm"
    reminder_24h = "reminder_24h"
    reminder_1h = "reminder_1h"
    payment_request = "payment_request"
    thank_you = "thank_you"
    closed = "closed"
    busy = "busy"


class CreatedVia(str, Enum):
    whatsapp = "whatsapp"
    manual = "manual"
    web = "web"


class AnalyticsPeriod(str, Enum):
    daily = "daily"
    weekly = "weekly"
    monthly = "monthly"


class Language(str, Enum):
    es = "es"
    en = "en"


class WebhookEventType(str, Enum):
    message_received = "message_received"
    message_sent = "message_sent"
    status_update = "status_update"


# --- Helpers ---

def _uid() -> str:
    return uuid.uuid4().hex[:12]


# --- Models ---

class Business(BaseModel):
    id: str = Field(default_factory=_uid)
    name: str
    category: BusinessCategory
    owner_name: str = ""
    phone_whatsapp: str = ""
    address: str = ""
    city: City = City.morelia
    working_hours: dict = Field(default_factory=lambda: {
        "mon": {"open": "09:00", "close": "18:00"},
        "tue": {"open": "09:00", "close": "18:00"},
        "wed": {"open": "09:00", "close": "18:00"},
        "thu": {"open": "09:00", "close": "18:00"},
        "fri": {"open": "09:00", "close": "18:00"},
        "sat": {"open": "10:00", "close": "14:00"},
        "sun": {"open": "", "close": ""},
    })
    services: list[dict] = Field(default_factory=list)
    subscription_tier: SubscriptionTier = SubscriptionTier.free_trial
    monthly_fee_mxn: float = 0.0
    status: BusinessStatus = BusinessStatus.active
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Customer(BaseModel):
    id: str = Field(default_factory=_uid)
    phone: str
    name: str = ""
    preferred_language: Language = Language.es
    business_ids: list[str] = Field(default_factory=list)
    total_appointments: int = 0
    last_contact: datetime = Field(default_factory=datetime.utcnow)


class Message(BaseModel):
    role: MessageRole
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    message_type: MessageType = MessageType.text


class Appointment(BaseModel):
    id: str = Field(default_factory=_uid)
    business_id: str
    customer_phone: str
    customer_name: str = ""
    service_name: str = ""
    date: str = ""
    time: str = ""
    duration_min: int = 30
    status: AppointmentStatus = AppointmentStatus.pending
    reminder_sent: bool = False
    created_via: CreatedVia = CreatedVia.whatsapp
    notes: str = ""


class Conversation(BaseModel):
    id: str = Field(default_factory=_uid)
    business_id: str
    customer_phone: str
    messages: list[dict] = Field(default_factory=list)
    status: ConversationStatus = ConversationStatus.active
    started_at: datetime = Field(default_factory=datetime.utcnow)
    resolved_at: Optional[datetime] = None


class Payment(BaseModel):
    id: str = Field(default_factory=_uid)
    business_id: str
    customer_phone: str
    appointment_id: str = ""
    amount_mxn: float = 0.0
    status: PaymentStatus = PaymentStatus.pending
    payment_link: str = ""
    method: PaymentMethod = PaymentMethod.transfer
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Template(BaseModel):
    id: str = Field(default_factory=_uid)
    business_id: str
    template_type: TemplateType
    content_es: str = ""
    content_en: str = ""
    variables: list[str] = Field(default_factory=list)


class Analytics(BaseModel):
    id: str = Field(default_factory=_uid)
    business_id: str
    period: AnalyticsPeriod = AnalyticsPeriod.daily
    messages_received: int = 0
    messages_sent: int = 0
    appointments_booked: int = 0
    appointments_completed: int = 0
    no_shows: int = 0
    revenue_mxn: float = 0.0
    response_time_avg_seconds: float = 0.0
    customer_satisfaction: float = 0.0
    date: str = ""


class WebhookEvent(BaseModel):
    id: str = Field(default_factory=_uid)
    business_id: str
    event_type: WebhookEventType
    payload: dict = Field(default_factory=dict)
    processed: bool = False
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class WaFlowStats(BaseModel):
    total_businesses: int = 0
    active_businesses: int = 0
    total_appointments_today: int = 0
    total_messages_today: int = 0
    monthly_revenue_mxn: float = 0.0
    avg_response_time_seconds: float = 0.0
    top_categories: list[dict] = Field(default_factory=list)
