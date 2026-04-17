"""WaFlow CLI — WhatsApp AI Assistant for small businesses in Morelia."""

from __future__ import annotations

import json
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from . import store, ai
from .demo_data import seed_demo_data

app = typer.Typer(
    name="waflow",
    help="WhatsApp AI Assistant platform for small service businesses in Morelia, Mexico",
    no_args_is_help=True,
)
console = Console()

CATEGORY_EMOJI = {
    "restaurant": "🍽️", "salon": "💇", "mechanic": "🔧", "clinic": "🏥",
    "dentist": "🦷", "gym": "💪", "veterinary": "🐾", "laundry": "👕",
    "tutoring": "📚", "other": "📋",
}

TIER_COLOR = {"free_trial": "yellow", "basic": "cyan", "pro": "green"}
STATUS_COLOR = {
    "active": "green", "paused": "yellow", "cancelled": "red",
    "pending": "yellow", "confirmed": "blue", "completed": "green",
    "no_show": "red", "paid": "green", "sent": "cyan", "failed": "red",
    "resolved": "dim", "escalated": "red",
}


# ─── Status ───

@app.command()
def status():
    """Show WaFlow platform dashboard."""
    stats = store.compute_stats()
    console.print(Panel(
        f"[bold]Negocios:[/] {stats['total_businesses']} ({stats['active_businesses']} activos)  |  "
        f"[bold]Clientes:[/] {stats['total_customers']}\n"
        f"[bold]Citas Hoy:[/] {stats['total_appointments_today']}  |  "
        f"[bold]Mensajes Hoy:[/] {stats['total_messages_today']}  |  "
        f"[bold]Conversaciones Activas:[/] {stats['active_conversations']}\n"
        f"[bold]Ingresos Cobros:[/] ${stats['monthly_revenue_mxn']:,.0f} MXN  |  "
        f"[bold]Suscripciones:[/] ${stats['subscription_revenue_mxn']:,.0f} MXN/mes  |  "
        f"[bold]Resp. Promedio:[/] {stats['avg_response_time_seconds']:.0f}s",
        title="[bold green]WaFlow Dashboard[/]",
        subtitle="WhatsApp AI para Negocios en Morelia",
        border_style="green",
    ))
    if stats["top_categories"]:
        console.print("\n[bold]Categorias Principales:[/]")
        for c in stats["top_categories"]:
            emoji = CATEGORY_EMOJI.get(c["category"], "📋")
            console.print(f"  {emoji} {c['category']}: {c['count']} negocios")


# ─── Demo ───

@app.command()
def demo():
    """Load demo data (15 businesses, 40 customers, 60 appointments, etc.)."""
    data = seed_demo_data()
    console.print(Panel(
        f"[green]Demo data loaded![/]\n\n"
        f"  🏪 Negocios: {len(data['businesses'])}\n"
        f"  👤 Clientes: {len(data['customers'])}\n"
        f"  📅 Citas: {len(data['appointments'])}\n"
        f"  💬 Conversaciones: {len(data['conversations'])}\n"
        f"  💰 Pagos: {len(data['payments'])}\n"
        f"  📝 Templates: {len(data['templates'])}\n"
        f"  📊 Analytics: {len(data['analytics'])}\n"
        f"  🔔 Webhook Events: {len(data['webhook_events'])}",
        title="[bold green]WaFlow Demo Data[/]",
        border_style="green",
    ))


# ─── Businesses ───

@app.command()
def businesses(
    category: Optional[str] = typer.Option(None, "--category", "-c", help="Filter by category"),
    city: Optional[str] = typer.Option(None, "--city", help="Filter by city"),
):
    """List all registered businesses."""
    items = store.get_collection("businesses")
    if category:
        items = [b for b in items if b.get("category") == category]
    if city:
        items = [b for b in items if b.get("city") == city]
    if not items:
        console.print("[yellow]No businesses found.[/]")
        return
    table = Table(title=f"Negocios ({len(items)})", border_style="green")
    table.add_column("Nombre", style="bold")
    table.add_column("Categoria")
    table.add_column("Dueno")
    table.add_column("WhatsApp")
    table.add_column("Plan")
    table.add_column("Status")
    for b in items:
        cat = b.get("category", "")
        emoji = CATEGORY_EMOJI.get(cat, "📋")
        tier = b.get("subscription_tier", "")
        tier_color = TIER_COLOR.get(tier, "white")
        st = b.get("status", "")
        st_color = STATUS_COLOR.get(st, "white")
        fee = b.get("monthly_fee_mxn", 0)
        tier_display = f"[{tier_color}]{tier}[/]" + (f" (${fee:.0f})" if fee > 0 else "")
        table.add_row(
            b["name"], f"{emoji} {cat}", b.get("owner_name", ""),
            b.get("phone_whatsapp", ""), tier_display, f"[{st_color}]{st}[/]",
        )
    console.print(table)


# ─── Customers ───

@app.command()
def customers(
    business: Optional[str] = typer.Option(None, "--business", "-b", help="Filter by business name"),
):
    """List customers."""
    items = store.get_collection("customers")
    if business:
        all_biz = store.get_collection("businesses")
        biz_id = None
        for b in all_biz:
            if business.lower() in b["name"].lower():
                biz_id = b["id"]
                break
        if biz_id:
            items = [c for c in items if biz_id in c.get("business_ids", [])]
    if not items:
        console.print("[yellow]No customers found.[/]")
        return
    table = Table(title=f"Clientes ({len(items)})", border_style="blue")
    table.add_column("Nombre", style="bold")
    table.add_column("Telefono")
    table.add_column("Idioma")
    table.add_column("Citas", justify="right")
    table.add_column("Ultimo Contacto")
    for c in items:
        table.add_row(
            c.get("name", ""), c.get("phone", ""),
            c.get("preferred_language", "es").upper(),
            str(c.get("total_appointments", 0)),
            str(c.get("last_contact", ""))[:10],
        )
    console.print(table)


# ─── Appointments ───

@app.command()
def appointments(
    business: Optional[str] = typer.Option(None, "--business", "-b", help="Filter by business name"),
    date: Optional[str] = typer.Option(None, "--date", "-d", help="Filter by date (YYYY-MM-DD)"),
):
    """List appointments."""
    items = store.get_collection("appointments")
    if business:
        all_biz = store.get_collection("businesses")
        for b in all_biz:
            if business.lower() in b["name"].lower():
                items = [a for a in items if a.get("business_id") == b["id"]]
                break
    if date:
        items = [a for a in items if a.get("date") == date]
    if not items:
        console.print("[yellow]No appointments found.[/]")
        return
    # Resolve business names
    biz_map = {b["id"]: b["name"] for b in store.get_collection("businesses")}
    table = Table(title=f"Citas ({len(items)})", border_style="cyan")
    table.add_column("Negocio")
    table.add_column("Cliente", style="bold")
    table.add_column("Servicio")
    table.add_column("Fecha")
    table.add_column("Hora")
    table.add_column("Status")
    table.add_column("Via")
    for a in sorted(items, key=lambda x: (x.get("date", ""), x.get("time", ""))):
        st = a.get("status", "")
        st_color = STATUS_COLOR.get(st, "white")
        table.add_row(
            biz_map.get(a.get("business_id", ""), "?")[:20],
            a.get("customer_name", ""),
            a.get("service_name", "")[:25],
            a.get("date", ""),
            a.get("time", ""),
            f"[{st_color}]{st}[/]",
            a.get("created_via", ""),
        )
    console.print(table)


# ─── Conversations ───

@app.command()
def conversations(
    business: Optional[str] = typer.Option(None, "--business", "-b", help="Filter by business name"),
    status_filter: Optional[str] = typer.Option(None, "--status", "-s", help="Filter by status"),
):
    """List active conversations."""
    items = store.get_collection("conversations")
    if business:
        all_biz = store.get_collection("businesses")
        for b in all_biz:
            if business.lower() in b["name"].lower():
                items = [c for c in items if c.get("business_id") == b["id"]]
                break
    if status_filter:
        items = [c for c in items if c.get("status") == status_filter]
    if not items:
        console.print("[yellow]No conversations found.[/]")
        return
    biz_map = {b["id"]: b["name"] for b in store.get_collection("businesses")}
    for c in items[:15]:
        biz_name = biz_map.get(c.get("business_id", ""), "?")
        st = c.get("status", "")
        st_color = STATUS_COLOR.get(st, "white")
        msgs = c.get("messages", [])
        msg_display = ""
        for m in msgs[-4:]:
            role = m.get("role", "")
            icon = "👤" if role == "customer" else "🤖" if role == "assistant" else "⚙️"
            content = m.get("content", "")[:80]
            msg_display += f"  {icon} {content}\n"
        console.print(Panel(
            msg_display.strip(),
            title=f"{biz_name} | {c.get('customer_phone', '')} | [{st_color}]{st}[/]",
            subtitle=f"Messages: {len(msgs)} | Started: {str(c.get('started_at', ''))[:16]}",
            border_style="green" if st == "active" else "dim",
        ))


# ─── Payments ───

@app.command()
def payments(
    status_filter: Optional[str] = typer.Option(None, "--status", "-s", help="Filter by status"),
):
    """Payment tracking."""
    items = store.get_collection("payments")
    if status_filter:
        items = [p for p in items if p.get("status") == status_filter]
    if not items:
        console.print("[yellow]No payments found.[/]")
        return
    biz_map = {b["id"]: b["name"] for b in store.get_collection("businesses")}
    table = Table(title=f"Pagos ({len(items)})", border_style="yellow")
    table.add_column("ID", style="dim")
    table.add_column("Negocio")
    table.add_column("Cliente")
    table.add_column("Monto", justify="right")
    table.add_column("Metodo")
    table.add_column("Status")
    table.add_column("Fecha")
    for p in items:
        st = p.get("status", "")
        st_color = STATUS_COLOR.get(st, "white")
        table.add_row(
            p["id"],
            biz_map.get(p.get("business_id", ""), "?")[:20],
            p.get("customer_phone", ""),
            f"${p.get('amount_mxn', 0):,.0f}",
            p.get("method", ""),
            f"[{st_color}]{st}[/]",
            str(p.get("created_at", ""))[:10],
        )
    console.print(table)


# ─── Templates ───

@app.command()
def templates(
    business: Optional[str] = typer.Option(None, "--business", "-b", help="Filter by business name"),
):
    """Message templates."""
    items = store.get_collection("templates")
    if business:
        all_biz = store.get_collection("businesses")
        for b in all_biz:
            if business.lower() in b["name"].lower():
                items = [t for t in items if t.get("business_id") == b["id"]]
                break
    if not items:
        console.print("[yellow]No templates found.[/]")
        return
    biz_map = {b["id"]: b["name"] for b in store.get_collection("businesses")}
    table = Table(title=f"Templates ({len(items)})", border_style="magenta")
    table.add_column("Negocio")
    table.add_column("Tipo", style="bold")
    table.add_column("Contenido (ES)")
    table.add_column("Variables")
    for t in items:
        table.add_row(
            biz_map.get(t.get("business_id", ""), "?")[:18],
            t.get("template_type", ""),
            t.get("content_es", "")[:60] + "..." if len(t.get("content_es", "")) > 60 else t.get("content_es", ""),
            ", ".join(t.get("variables", [])),
        )
    console.print(table)


# ─── Analytics ───

@app.command()
def analytics(
    business: Optional[str] = typer.Option(None, "--business", "-b", help="Filter by business name"),
    days: int = typer.Option(7, "--days", "-d", help="Number of days to show"),
):
    """Performance dashboard."""
    items = store.get_collection("analytics")
    biz_map = {b["id"]: b["name"] for b in store.get_collection("businesses")}

    if business:
        all_biz = store.get_collection("businesses")
        for b in all_biz:
            if business.lower() in b["name"].lower():
                items = [a for a in items if a.get("business_id") == b["id"]]
                break

    if not items:
        console.print("[yellow]No analytics found.[/]")
        return

    # Aggregate last N days
    from datetime import date as dt_date, timedelta
    today = dt_date.today()
    cutoff = (today - timedelta(days=days)).isoformat()
    recent = [a for a in items if a.get("date", "") >= cutoff]

    if not recent:
        console.print("[yellow]No recent analytics.[/]")
        return

    total_msgs_in = sum(a.get("messages_received", 0) for a in recent)
    total_msgs_out = sum(a.get("messages_sent", 0) for a in recent)
    total_booked = sum(a.get("appointments_booked", 0) for a in recent)
    total_completed = sum(a.get("appointments_completed", 0) for a in recent)
    total_no_shows = sum(a.get("no_shows", 0) for a in recent)
    total_revenue = sum(a.get("revenue_mxn", 0) for a in recent)
    avg_resp = sum(a.get("response_time_avg_seconds", 0) for a in recent) / len(recent) if recent else 0
    avg_sat = sum(a.get("customer_satisfaction", 0) for a in recent) / len(recent) if recent else 0

    console.print(Panel(
        f"[bold]Mensajes Recibidos:[/] {total_msgs_in:,}  |  [bold]Enviados:[/] {total_msgs_out:,}\n"
        f"[bold]Citas Agendadas:[/] {total_booked}  |  [bold]Completadas:[/] {total_completed}  |  "
        f"[bold]No Shows:[/] {total_no_shows}\n"
        f"[bold]Ingresos:[/] ${total_revenue:,.0f} MXN  |  "
        f"[bold]Tiempo Resp:[/] {avg_resp:.0f}s  |  "
        f"[bold]Satisfaccion:[/] {avg_sat:.1f}/5.0",
        title=f"[bold green]Analytics - Ultimos {days} dias[/]",
        border_style="green",
    ))


# ─── Simulate ───

@app.command()
def simulate():
    """Simulate a WhatsApp conversation (interactive demo)."""
    businesses_list = store.get_collection("businesses")
    if not businesses_list:
        console.print("[red]No businesses found. Run 'waflow demo' first.[/]")
        raise typer.Exit(1)

    console.print(Panel(
        "[bold]Selecciona un negocio para simular:[/]\n",
        title="[bold green]WaFlow Simulator[/]",
        border_style="green",
    ))
    for i, b in enumerate(businesses_list, 1):
        emoji = CATEGORY_EMOJI.get(b.get("category", ""), "📋")
        console.print(f"  {i}. {emoji} {b['name']} ({b.get('category', '')})")

    choice = typer.prompt("\nNumero del negocio", type=int, default=1)
    if choice < 1 or choice > len(businesses_list):
        console.print("[red]Opcion invalida.[/]")
        raise typer.Exit(1)

    business = businesses_list[choice - 1]
    console.print(f"\n[green]Conectado a {business['name']}![/]")
    console.print("[dim]Escribe como si fueras un cliente de WhatsApp. Escribe 'salir' para terminar.[/]\n")

    conversation = {"messages": []}

    while True:
        try:
            msg = typer.prompt("👤 Tu")
        except (KeyboardInterrupt, EOFError):
            break
        if msg.lower() in ("salir", "exit", "quit"):
            break

        conversation["messages"].append({
            "role": "customer",
            "content": msg,
            "message_type": "text",
        })

        with console.status("[green]WaFlow AI respondiendo..."):
            try:
                result = ai.process_customer_message(business, conversation, msg)
            except Exception as e:
                console.print(f"[red]Error AI: {e}[/]")
                # Fallback response
                result = {
                    "response": f"Hola! Gracias por escribir a {business['name']}. Un momento por favor, te comunico con el encargado.",
                    "action": "none",
                    "sentiment": "neutral",
                }

        response = result.get("response", "...")
        action = result.get("action", "none")
        conversation["messages"].append({
            "role": "assistant",
            "content": response,
            "message_type": action if action != "none" else "text",
        })

        action_badge = ""
        if action and action != "none":
            action_badge = f" [{TIER_COLOR.get(action, 'cyan')}][{action}][/]"

        console.print(f"🤖 {response}{action_badge}\n")

    console.print("\n[green]Simulacion terminada. Hasta luego![/]")


# ─── Setup ───

@app.command()
def setup(
    business_name: str = typer.Argument(..., help="Business name"),
    category: str = typer.Argument(..., help="Category (restaurant/salon/mechanic/clinic/dentist/gym/veterinary/laundry/tutoring/other)"),
):
    """AI-powered business onboarding."""
    console.print(f"[cyan]Configurando {business_name} ({category}) con AI...[/]\n")
    with console.status("[bold green]Generando configuracion..."):
        try:
            result = ai.generate_business_setup(category, business_name)
        except Exception as e:
            console.print(f"[red]Error: {e}[/]")
            raise typer.Exit(1)

    if "raw" in result:
        console.print(Panel(result["raw"], title="AI Response"))
        return

    # Show generated config
    if result.get("services"):
        console.print("[bold]Servicios sugeridos:[/]")
        for s in result["services"]:
            console.print(f"  - {s.get('name', '')}: ${s.get('price_mxn', 0):,.0f} MXN ({s.get('duration_min', 0)} min)")

    if result.get("templates"):
        console.print("\n[bold]Templates generados:[/]")
        for t in result["templates"]:
            console.print(f"  [{t.get('type', '')}] {t.get('content_es', '')[:70]}...")

    if result.get("suggested_greeting"):
        console.print(f"\n[bold]Saludo sugerido:[/] {result['suggested_greeting']}")

    console.print("\n[green]Configuracion generada exitosamente![/]")


# ─── Report ───

@app.command()
def report(
    business: Optional[str] = typer.Option(None, "--business", "-b", help="Business name"),
):
    """AI weekly report for a business."""
    all_biz = store.get_collection("businesses")
    if not all_biz:
        console.print("[red]No businesses found. Run 'waflow demo' first.[/]")
        raise typer.Exit(1)

    target_biz = all_biz[0]
    if business:
        for b in all_biz:
            if business.lower() in b["name"].lower():
                target_biz = b
                break

    ana = [a for a in store.get_collection("analytics") if a.get("business_id") == target_biz["id"]]

    console.print(f"[cyan]Generando reporte semanal para {target_biz['name']}...[/]\n")
    with console.status("[bold green]AI analizando..."):
        try:
            result = ai.generate_weekly_report(ana[:7], target_biz)
        except Exception as e:
            console.print(f"[red]Error: {e}[/]")
            raise typer.Exit(1)

    if "raw" in result:
        console.print(Panel(result["raw"], title="AI Response"))
        return

    console.print(Panel(
        result.get("summary_es", ""),
        title=f"Reporte Semanal — {target_biz['name']}",
        border_style="green",
    ))
    if result.get("highlights"):
        console.print("\n[bold green]Destacados:[/]")
        for h in result["highlights"]:
            console.print(f"  ✅ {h}")
    if result.get("concerns"):
        console.print("\n[bold yellow]Areas de Atencion:[/]")
        for c in result["concerns"]:
            console.print(f"  ⚠️ {c}")
    if result.get("recommendations_es"):
        console.print("\n[bold cyan]Recomendaciones:[/]")
        for r in result["recommendations_es"]:
            console.print(f"  💡 {r}")


# ─── Serve ───

@app.command()
def serve(
    host: str = typer.Option("0.0.0.0", "--host", "-h"),
    port: int = typer.Option(8000, "--port", "-p"),
):
    """Start the WaFlow API server."""
    import uvicorn
    console.print(Panel(
        f"[bold green]WaFlow API starting[/]\n"
        f"  Host: {host}\n"
        f"  Port: {port}\n"
        f"  Docs: http://{host}:{port}/docs",
        title="WaFlow Server",
        border_style="green",
    ))
    uvicorn.run("waflow.api:app", host=host, port=port, reload=True)


if __name__ == "__main__":
    app()
