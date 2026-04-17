"""WaFlow AI features — Claude-powered WhatsApp business intelligence."""

from __future__ import annotations

import json
import os
from typing import Any

from dotenv import load_dotenv

load_dotenv()

_client = None


def _get_client():
    global _client
    if _client is None:
        from anthropic import Anthropic
        _client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY", ""))
    return _client


def _ask(system: str, prompt: str, max_tokens: int = 2048) -> str:
    client = _get_client()
    resp = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=max_tokens,
        system=system,
        messages=[{"role": "user", "content": prompt}],
    )
    return resp.content[0].text


def process_customer_message(business: dict, conversation: dict, message: str) -> dict:
    """AI generates a WhatsApp response to a customer message."""
    system = (
        "Eres el asistente de WhatsApp AI de WaFlow para negocios en Morelia, Mexico. "
        "Tu trabajo es responder mensajes de clientes de forma amable, natural y eficiente. "
        "Usa un tono informal pero profesional, como un mexicano amigable. Usa emojis naturalmente. "
        "Puedes: agendar citas, dar informacion de servicios/precios, confirmar reservas, "
        "enviar recordatorios, cobrar, o escalar al dueno si no sabes algo.\n\n"
        "IMPORTANTE: Lee TODA la conversacion anterior para mantener el contexto. "
        "Si el cliente ya pidio algo o ya se acordo un precio/fecha/hora, NO lo olvides. "
        "Si el cliente dice 'confirmado' o 'si', confirma lo que se estaba discutiendo. "
        "NO saludes de nuevo si ya llevas conversando. Continua la conversacion naturalmente.\n\n"
        "Responde SIEMPRE en JSON:\n"
        '{"response": str (el mensaje para el cliente en espanol), '
        '"action": str (none/booking/confirmation/payment/escalation), '
        '"booking_details": null | {"service": str, "date": str, "time": str}, '
        '"payment_amount": null | float, '
        '"escalate_reason": null | str, '
        '"sentiment": str (positive/neutral/negative)}'
    )
    services_str = json.dumps(business.get("services", []), ensure_ascii=False)
    hours_str = json.dumps(business.get("working_hours", {}), ensure_ascii=False)
    msgs_str = json.dumps(conversation.get("messages", [])[-20:], default=str, ensure_ascii=False)

    prompt = (
        f"Negocio: {business.get('name', '')} ({business.get('category', '')})\n"
        f"Servicios: {services_str}\n"
        f"Horario: {hours_str}\n"
        f"Conversacion reciente:\n{msgs_str}\n\n"
        f"Nuevo mensaje del cliente: {message}"
    )
    raw = _ask(system, prompt)
    # Strip markdown code blocks if present
    text = raw
    if "```json" in text:
        text = text.split("```json")[1].split("```")[0]
    elif "```" in text:
        text = text.split("```")[1].split("```")[0]
    try:
        return json.loads(text.strip())
    except json.JSONDecodeError:
        # If still can't parse, return the raw text as the response
        return {"response": raw.replace("```json", "").replace("```", "").strip(), "action": "none", "sentiment": "neutral"}


def generate_business_setup(category: str, business_name: str) -> dict:
    """Auto-generate templates, services, and working hours for a business."""
    system = (
        "Eres WaFlow AI, plataforma de WhatsApp para negocios en Morelia, Mexico. "
        "Genera la configuracion completa para un negocio nuevo. "
        "Incluye servicios con precios reales en MXN para Morelia, plantillas de mensajes en espanol, "
        "y horarios tipicos.\n\n"
        "Responde en JSON:\n"
        '{"services": [{"name": str, "price_mxn": float, "duration_min": int}], '
        '"working_hours": {"mon": {"open": str, "close": str}, ...}, '
        '"templates": [{"type": str, "content_es": str, "content_en": str, "variables": [str]}], '
        '"suggested_greeting": str}'
    )
    prompt = f"Categoria: {category}\nNombre del negocio: {business_name}\nCiudad: Morelia, Michoacan"
    raw = _ask(system, prompt, max_tokens=3000)
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {"raw": raw}


def analyze_conversations(conversations: list[dict]) -> dict:
    """Sentiment analysis, common requests, improvement suggestions."""
    system = (
        "Eres WaFlow AI analista de conversaciones de WhatsApp para negocios en Morelia. "
        "Analiza las conversaciones y proporciona insights.\n\n"
        "Responde en JSON:\n"
        '{"overall_sentiment": str, "common_requests": [str], '
        '"peak_hours": [str], "improvement_suggestions_es": [str], '
        '"improvement_suggestions_en": [str], '
        '"customer_satisfaction_score": float (1-10), '
        '"summary_es": str, "summary_en": str}'
    )
    prompt = f"Conversaciones:\n{json.dumps(conversations[:20], default=str, ensure_ascii=False)}"
    raw = _ask(system, prompt)
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {"raw": raw}


def optimize_schedule(appointments: list[dict], working_hours: dict) -> dict:
    """Scheduling optimization suggestions."""
    system = (
        "Eres WaFlow AI optimizador de agenda para negocios en Morelia. "
        "Analiza las citas y sugiere mejoras en la programacion.\n\n"
        "Responde en JSON:\n"
        '{"utilization_pct": float, "peak_slots": [str], "empty_slots": [str], '
        '"suggestions_es": [str], "suggestions_en": [str], '
        '"estimated_revenue_increase_pct": float}'
    )
    prompt = (
        f"Citas:\n{json.dumps(appointments[:30], default=str, ensure_ascii=False)}\n"
        f"Horario:\n{json.dumps(working_hours, ensure_ascii=False)}"
    )
    raw = _ask(system, prompt)
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {"raw": raw}


def generate_weekly_report(analytics: list[dict], business: dict) -> dict:
    """Business owner weekly summary."""
    system = (
        "Eres WaFlow AI, generador de reportes semanales para duenos de negocios en Morelia. "
        "Crea un resumen ejecutivo amigable y accionable.\n\n"
        "Responde en JSON:\n"
        '{"summary_es": str, "summary_en": str, '
        '"highlights": [str], "concerns": [str], '
        '"recommendations_es": [str], "recommendations_en": [str], '
        '"revenue_trend": str (up/stable/down), '
        '"customer_trend": str (growing/stable/declining)}'
    )
    prompt = (
        f"Negocio: {business.get('name', '')} ({business.get('category', '')})\n"
        f"Analytics:\n{json.dumps(analytics[:7], default=str, ensure_ascii=False)}"
    )
    raw = _ask(system, prompt)
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {"raw": raw}


def suggest_upsells(business: dict, customer_history: list[dict]) -> dict:
    """Revenue optimization suggestions based on customer patterns."""
    system = (
        "Eres WaFlow AI consultor de ventas para negocios en Morelia. "
        "Sugiere oportunidades de upsell basadas en el historial del cliente.\n\n"
        "Responde en JSON:\n"
        '{"suggestions": [{"service": str, "reason_es": str, "reason_en": str, '
        '"estimated_revenue_mxn": float, "message_template": str}], '
        '"total_opportunity_mxn": float}'
    )
    prompt = (
        f"Negocio: {json.dumps(business, default=str, ensure_ascii=False)}\n"
        f"Historial del cliente:\n{json.dumps(customer_history[:10], default=str, ensure_ascii=False)}"
    )
    raw = _ask(system, prompt)
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {"raw": raw}
