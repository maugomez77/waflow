"""WaFlow demo data — realistic Morelia small business dataset."""

from __future__ import annotations

import random
from datetime import date, datetime, timedelta

from .store import save_store


def seed_demo_data() -> dict:
    """Generate and persist all demo data. Returns the full store dict."""

    # ─── 15 Businesses ───

    businesses = [
        {
            "id": "biz-tacos-guero",
            "name": "Tacos El Guero",
            "category": "restaurant",
            "owner_name": "Roberto Gutierrez",
            "phone_whatsapp": "+52 443 312 1001",
            "address": "Av. Madero 456, Centro",
            "city": "morelia",
            "working_hours": {
                "mon": {"open": "10:00", "close": "23:00"},
                "tue": {"open": "10:00", "close": "23:00"},
                "wed": {"open": "10:00", "close": "23:00"},
                "thu": {"open": "10:00", "close": "23:00"},
                "fri": {"open": "10:00", "close": "01:00"},
                "sat": {"open": "10:00", "close": "01:00"},
                "sun": {"open": "11:00", "close": "21:00"},
            },
            "services": [
                {"name": "Reservacion mesa 2-4", "price_mxn": 0, "duration_min": 60},
                {"name": "Reservacion mesa 5-8", "price_mxn": 0, "duration_min": 90},
                {"name": "Pedido para llevar", "price_mxn": 0, "duration_min": 20},
                {"name": "Catering evento", "price_mxn": 3000, "duration_min": 180},
            ],
            "subscription_tier": "basic",
            "monthly_fee_mxn": 299,
            "status": "active",
            "created_at": "2026-01-15T00:00:00",
        },
        {
            "id": "biz-carnitas-pepe",
            "name": "Carnitas Don Pepe",
            "category": "restaurant",
            "owner_name": "Jose Luis Perez",
            "phone_whatsapp": "+52 443 312 1002",
            "address": "Calzada Juarez 890, Chapultepec",
            "city": "morelia",
            "working_hours": {
                "mon": {"open": "08:00", "close": "17:00"},
                "tue": {"open": "08:00", "close": "17:00"},
                "wed": {"open": "08:00", "close": "17:00"},
                "thu": {"open": "08:00", "close": "17:00"},
                "fri": {"open": "08:00", "close": "17:00"},
                "sat": {"open": "07:00", "close": "16:00"},
                "sun": {"open": "07:00", "close": "15:00"},
            },
            "services": [
                {"name": "Orden de carnitas (1kg)", "price_mxn": 380, "duration_min": 15},
                {"name": "Orden de carnitas (1/2 kg)", "price_mxn": 200, "duration_min": 10},
                {"name": "Torta de carnitas", "price_mxn": 65, "duration_min": 5},
                {"name": "Pedido para evento (5kg+)", "price_mxn": 1800, "duration_min": 60},
            ],
            "subscription_tier": "free_trial",
            "monthly_fee_mxn": 0,
            "status": "active",
            "created_at": "2026-03-01T00:00:00",
        },
        {
            "id": "biz-sushi-morelia",
            "name": "Sushi Morelia",
            "category": "restaurant",
            "owner_name": "Akiko Tanaka de Ramirez",
            "phone_whatsapp": "+52 443 312 1003",
            "address": "Av. Camelinas 2345, Col. Felicitas del Rio",
            "city": "morelia",
            "working_hours": {
                "mon": {"open": "13:00", "close": "22:00"},
                "tue": {"open": "13:00", "close": "22:00"},
                "wed": {"open": "13:00", "close": "22:00"},
                "thu": {"open": "13:00", "close": "22:00"},
                "fri": {"open": "13:00", "close": "23:00"},
                "sat": {"open": "13:00", "close": "23:00"},
                "sun": {"open": "13:00", "close": "21:00"},
            },
            "services": [
                {"name": "Reservacion (2 personas)", "price_mxn": 0, "duration_min": 60},
                {"name": "Reservacion (4+ personas)", "price_mxn": 0, "duration_min": 90},
                {"name": "Sushi a domicilio", "price_mxn": 50, "duration_min": 40},
                {"name": "Paquete fiesta (20 rollos)", "price_mxn": 2500, "duration_min": 120},
            ],
            "subscription_tier": "pro",
            "monthly_fee_mxn": 599,
            "status": "active",
            "created_at": "2025-11-20T00:00:00",
        },
        {
            "id": "biz-estetica-diana",
            "name": "Estetica Diana",
            "category": "salon",
            "owner_name": "Diana Morales",
            "phone_whatsapp": "+52 443 315 2001",
            "address": "Calle Aquiles Serdan 123, Centro",
            "city": "morelia",
            "working_hours": {
                "mon": {"open": "09:00", "close": "19:00"},
                "tue": {"open": "09:00", "close": "19:00"},
                "wed": {"open": "09:00", "close": "19:00"},
                "thu": {"open": "09:00", "close": "19:00"},
                "fri": {"open": "09:00", "close": "20:00"},
                "sat": {"open": "09:00", "close": "18:00"},
                "sun": {"open": "", "close": ""},
            },
            "services": [
                {"name": "Corte de cabello dama", "price_mxn": 150, "duration_min": 45},
                {"name": "Corte de cabello caballero", "price_mxn": 80, "duration_min": 30},
                {"name": "Tinte completo", "price_mxn": 600, "duration_min": 120},
                {"name": "Mechas/Balayage", "price_mxn": 1200, "duration_min": 180},
                {"name": "Peinado para evento", "price_mxn": 350, "duration_min": 60},
                {"name": "Maquillaje profesional", "price_mxn": 500, "duration_min": 60},
                {"name": "Alisado keratina", "price_mxn": 1500, "duration_min": 150},
            ],
            "subscription_tier": "pro",
            "monthly_fee_mxn": 599,
            "status": "active",
            "created_at": "2025-10-01T00:00:00",
        },
        {
            "id": "biz-barberia-caballeros",
            "name": "Barberia Los Caballeros",
            "category": "salon",
            "owner_name": "Miguel Angel Torres",
            "phone_whatsapp": "+52 443 315 2002",
            "address": "Av. Lazaro Cardenas 567, Chapultepec Norte",
            "city": "morelia",
            "working_hours": {
                "mon": {"open": "10:00", "close": "20:00"},
                "tue": {"open": "10:00", "close": "20:00"},
                "wed": {"open": "10:00", "close": "20:00"},
                "thu": {"open": "10:00", "close": "20:00"},
                "fri": {"open": "10:00", "close": "21:00"},
                "sat": {"open": "09:00", "close": "19:00"},
                "sun": {"open": "", "close": ""},
            },
            "services": [
                {"name": "Corte clasico", "price_mxn": 100, "duration_min": 30},
                {"name": "Corte + barba", "price_mxn": 150, "duration_min": 45},
                {"name": "Afeitado clasico", "price_mxn": 80, "duration_min": 20},
                {"name": "Diseno de barba", "price_mxn": 120, "duration_min": 30},
                {"name": "Tratamiento capilar", "price_mxn": 250, "duration_min": 40},
            ],
            "subscription_tier": "basic",
            "monthly_fee_mxn": 299,
            "status": "active",
            "created_at": "2026-01-10T00:00:00",
        },
        {
            "id": "biz-nails-beauty",
            "name": "Nails & Beauty",
            "category": "salon",
            "owner_name": "Fernanda Rios",
            "phone_whatsapp": "+52 443 315 2003",
            "address": "Plaza Las Americas Local 45",
            "city": "morelia",
            "working_hours": {
                "mon": {"open": "10:00", "close": "20:00"},
                "tue": {"open": "10:00", "close": "20:00"},
                "wed": {"open": "10:00", "close": "20:00"},
                "thu": {"open": "10:00", "close": "20:00"},
                "fri": {"open": "10:00", "close": "21:00"},
                "sat": {"open": "10:00", "close": "20:00"},
                "sun": {"open": "11:00", "close": "17:00"},
            },
            "services": [
                {"name": "Manicure basico", "price_mxn": 120, "duration_min": 30},
                {"name": "Manicure gel/acrilico", "price_mxn": 350, "duration_min": 60},
                {"name": "Pedicure spa", "price_mxn": 200, "duration_min": 45},
                {"name": "Unas esculpidas", "price_mxn": 500, "duration_min": 90},
                {"name": "Depilacion facial", "price_mxn": 80, "duration_min": 15},
                {"name": "Depilacion pierna completa", "price_mxn": 300, "duration_min": 45},
            ],
            "subscription_tier": "basic",
            "monthly_fee_mxn": 299,
            "status": "active",
            "created_at": "2026-02-15T00:00:00",
        },
        {
            "id": "biz-taller-lopez",
            "name": "Taller Hermanos Lopez",
            "category": "mechanic",
            "owner_name": "Carlos y Juan Lopez",
            "phone_whatsapp": "+52 443 318 3001",
            "address": "Periferico Paseo de la Republica 1234",
            "city": "morelia",
            "working_hours": {
                "mon": {"open": "08:00", "close": "18:00"},
                "tue": {"open": "08:00", "close": "18:00"},
                "wed": {"open": "08:00", "close": "18:00"},
                "thu": {"open": "08:00", "close": "18:00"},
                "fri": {"open": "08:00", "close": "18:00"},
                "sat": {"open": "08:00", "close": "14:00"},
                "sun": {"open": "", "close": ""},
            },
            "services": [
                {"name": "Servicio menor (aceite+filtros)", "price_mxn": 1200, "duration_min": 60},
                {"name": "Servicio mayor", "price_mxn": 3500, "duration_min": 180},
                {"name": "Afinacion", "price_mxn": 2000, "duration_min": 120},
                {"name": "Frenos (cambio balatas)", "price_mxn": 1500, "duration_min": 90},
                {"name": "Diagnostico computarizado", "price_mxn": 500, "duration_min": 30},
                {"name": "Suspension", "price_mxn": 4000, "duration_min": 240},
            ],
            "subscription_tier": "basic",
            "monthly_fee_mxn": 299,
            "status": "active",
            "created_at": "2026-01-20T00:00:00",
        },
        {
            "id": "biz-autoservice",
            "name": "AutoService Morelia",
            "category": "mechanic",
            "owner_name": "Ricardo Hernandez",
            "phone_whatsapp": "+52 443 318 3002",
            "address": "Av. Solidaridad 890, Industrial",
            "city": "morelia",
            "working_hours": {
                "mon": {"open": "07:00", "close": "19:00"},
                "tue": {"open": "07:00", "close": "19:00"},
                "wed": {"open": "07:00", "close": "19:00"},
                "thu": {"open": "07:00", "close": "19:00"},
                "fri": {"open": "07:00", "close": "19:00"},
                "sat": {"open": "08:00", "close": "15:00"},
                "sun": {"open": "", "close": ""},
            },
            "services": [
                {"name": "Cambio de aceite", "price_mxn": 800, "duration_min": 30},
                {"name": "Lavado premium", "price_mxn": 250, "duration_min": 60},
                {"name": "Alineacion y balanceo", "price_mxn": 600, "duration_min": 45},
                {"name": "Cambio de llantas", "price_mxn": 200, "duration_min": 30},
                {"name": "Revision pre-viaje", "price_mxn": 350, "duration_min": 45},
            ],
            "subscription_tier": "free_trial",
            "monthly_fee_mxn": 0,
            "status": "active",
            "created_at": "2026-03-15T00:00:00",
        },
        {
            "id": "biz-dental-sonrisa",
            "name": "Clinica Dental Sonrisa",
            "category": "dentist",
            "owner_name": "Dra. Patricia Vega",
            "phone_whatsapp": "+52 443 320 4001",
            "address": "Av. Acueducto 345, Col. Lomas",
            "city": "morelia",
            "working_hours": {
                "mon": {"open": "09:00", "close": "18:00"},
                "tue": {"open": "09:00", "close": "18:00"},
                "wed": {"open": "09:00", "close": "18:00"},
                "thu": {"open": "09:00", "close": "18:00"},
                "fri": {"open": "09:00", "close": "17:00"},
                "sat": {"open": "09:00", "close": "14:00"},
                "sun": {"open": "", "close": ""},
            },
            "services": [
                {"name": "Limpieza dental", "price_mxn": 800, "duration_min": 45},
                {"name": "Consulta general", "price_mxn": 500, "duration_min": 30},
                {"name": "Blanqueamiento", "price_mxn": 3500, "duration_min": 60},
                {"name": "Resina (caries)", "price_mxn": 1200, "duration_min": 45},
                {"name": "Extraccion", "price_mxn": 1500, "duration_min": 30},
                {"name": "Ortodoncia (mensualidad)", "price_mxn": 2000, "duration_min": 30},
                {"name": "Corona dental", "price_mxn": 5000, "duration_min": 90},
            ],
            "subscription_tier": "pro",
            "monthly_fee_mxn": 599,
            "status": "active",
            "created_at": "2025-09-01T00:00:00",
        },
        {
            "id": "biz-pediatra-garcia",
            "name": "Dr. Garcia Pediatra",
            "category": "clinic",
            "owner_name": "Dr. Alejandro Garcia",
            "phone_whatsapp": "+52 443 320 4002",
            "address": "Calle Morelos Sur 678, Centro",
            "city": "morelia",
            "working_hours": {
                "mon": {"open": "08:00", "close": "14:00"},
                "tue": {"open": "08:00", "close": "14:00"},
                "wed": {"open": "08:00", "close": "14:00"},
                "thu": {"open": "16:00", "close": "20:00"},
                "fri": {"open": "08:00", "close": "14:00"},
                "sat": {"open": "09:00", "close": "13:00"},
                "sun": {"open": "", "close": ""},
            },
            "services": [
                {"name": "Consulta pediatrica", "price_mxn": 700, "duration_min": 30},
                {"name": "Control de nino sano", "price_mxn": 600, "duration_min": 45},
                {"name": "Vacunacion", "price_mxn": 400, "duration_min": 15},
                {"name": "Urgencia pediatrica", "price_mxn": 1000, "duration_min": 30},
            ],
            "subscription_tier": "basic",
            "monthly_fee_mxn": 299,
            "status": "active",
            "created_at": "2026-02-01T00:00:00",
        },
        {
            "id": "biz-crossfit-morelia",
            "name": "CrossFit Morelia",
            "category": "gym",
            "owner_name": "Enrique Zavala",
            "phone_whatsapp": "+52 443 322 5001",
            "address": "Blvd. Garcia de Leon 2100",
            "city": "morelia",
            "working_hours": {
                "mon": {"open": "06:00", "close": "21:00"},
                "tue": {"open": "06:00", "close": "21:00"},
                "wed": {"open": "06:00", "close": "21:00"},
                "thu": {"open": "06:00", "close": "21:00"},
                "fri": {"open": "06:00", "close": "21:00"},
                "sat": {"open": "07:00", "close": "14:00"},
                "sun": {"open": "08:00", "close": "12:00"},
            },
            "services": [
                {"name": "Membresia mensual", "price_mxn": 1200, "duration_min": 0},
                {"name": "Clase drop-in", "price_mxn": 150, "duration_min": 60},
                {"name": "Programa personal (mes)", "price_mxn": 3000, "duration_min": 60},
                {"name": "Clase de prueba gratis", "price_mxn": 0, "duration_min": 60},
            ],
            "subscription_tier": "basic",
            "monthly_fee_mxn": 299,
            "status": "active",
            "created_at": "2026-01-05T00:00:00",
        },
        {
            "id": "biz-vet-patitas",
            "name": "Veterinaria Patitas",
            "category": "veterinary",
            "owner_name": "Dra. Laura Mendez",
            "phone_whatsapp": "+52 443 325 6001",
            "address": "Calle Santiago Tapia 234",
            "city": "morelia",
            "working_hours": {
                "mon": {"open": "09:00", "close": "19:00"},
                "tue": {"open": "09:00", "close": "19:00"},
                "wed": {"open": "09:00", "close": "19:00"},
                "thu": {"open": "09:00", "close": "19:00"},
                "fri": {"open": "09:00", "close": "19:00"},
                "sat": {"open": "09:00", "close": "15:00"},
                "sun": {"open": "10:00", "close": "14:00"},
            },
            "services": [
                {"name": "Consulta general", "price_mxn": 400, "duration_min": 30},
                {"name": "Vacunacion", "price_mxn": 350, "duration_min": 15},
                {"name": "Bano y estetica canina", "price_mxn": 250, "duration_min": 60},
                {"name": "Esterilizacion", "price_mxn": 2500, "duration_min": 120},
                {"name": "Urgencia veterinaria", "price_mxn": 800, "duration_min": 45},
                {"name": "Desparasitacion", "price_mxn": 200, "duration_min": 15},
            ],
            "subscription_tier": "pro",
            "monthly_fee_mxn": 599,
            "status": "active",
            "created_at": "2025-12-10T00:00:00",
        },
        {
            "id": "biz-lavanquick",
            "name": "LavanQuick",
            "category": "laundry",
            "owner_name": "Martha Ortiz",
            "phone_whatsapp": "+52 443 328 7001",
            "address": "Av. Universidad 567",
            "city": "morelia",
            "working_hours": {
                "mon": {"open": "07:00", "close": "20:00"},
                "tue": {"open": "07:00", "close": "20:00"},
                "wed": {"open": "07:00", "close": "20:00"},
                "thu": {"open": "07:00", "close": "20:00"},
                "fri": {"open": "07:00", "close": "20:00"},
                "sat": {"open": "08:00", "close": "18:00"},
                "sun": {"open": "09:00", "close": "15:00"},
            },
            "services": [
                {"name": "Lavado por kilo", "price_mxn": 25, "duration_min": 120},
                {"name": "Lavado express (2hrs)", "price_mxn": 45, "duration_min": 120},
                {"name": "Planchado por pieza", "price_mxn": 20, "duration_min": 30},
                {"name": "Lavado en seco (pieza)", "price_mxn": 80, "duration_min": 1440},
                {"name": "Edredones/cobijas", "price_mxn": 120, "duration_min": 180},
            ],
            "subscription_tier": "free_trial",
            "monthly_fee_mxn": 0,
            "status": "active",
            "created_at": "2026-03-20T00:00:00",
        },
        {
            "id": "biz-tutorias-umsnh",
            "name": "Tutorias UMSNH",
            "category": "tutoring",
            "owner_name": "Prof. Ana Belen Castillo",
            "phone_whatsapp": "+52 443 330 8001",
            "address": "Calle Nigromante 89, Centro",
            "city": "morelia",
            "working_hours": {
                "mon": {"open": "15:00", "close": "21:00"},
                "tue": {"open": "15:00", "close": "21:00"},
                "wed": {"open": "15:00", "close": "21:00"},
                "thu": {"open": "15:00", "close": "21:00"},
                "fri": {"open": "15:00", "close": "21:00"},
                "sat": {"open": "09:00", "close": "15:00"},
                "sun": {"open": "", "close": ""},
            },
            "services": [
                {"name": "Tutoria matematicas (1hr)", "price_mxn": 200, "duration_min": 60},
                {"name": "Tutoria fisica/quimica (1hr)", "price_mxn": 200, "duration_min": 60},
                {"name": "Tutoria ingles (1hr)", "price_mxn": 180, "duration_min": 60},
                {"name": "Preparacion examen admision", "price_mxn": 250, "duration_min": 90},
                {"name": "Paquete 8 clases mensual", "price_mxn": 1400, "duration_min": 60},
            ],
            "subscription_tier": "basic",
            "monthly_fee_mxn": 299,
            "status": "active",
            "created_at": "2026-02-10T00:00:00",
        },
        {
            "id": "biz-foto-morelia",
            "name": "Fotografia Morelia",
            "category": "other",
            "owner_name": "Sebastian Ruiz",
            "phone_whatsapp": "+52 443 335 9001",
            "address": "Portal Hidalgo 12, Centro Historico",
            "city": "morelia",
            "working_hours": {
                "mon": {"open": "10:00", "close": "18:00"},
                "tue": {"open": "10:00", "close": "18:00"},
                "wed": {"open": "10:00", "close": "18:00"},
                "thu": {"open": "10:00", "close": "18:00"},
                "fri": {"open": "10:00", "close": "18:00"},
                "sat": {"open": "09:00", "close": "20:00"},
                "sun": {"open": "09:00", "close": "20:00"},
            },
            "services": [
                {"name": "Sesion retrato (1hr)", "price_mxn": 1500, "duration_min": 60},
                {"name": "Sesion familiar (2hr)", "price_mxn": 2500, "duration_min": 120},
                {"name": "Cobertura boda (8hr)", "price_mxn": 15000, "duration_min": 480},
                {"name": "Fotos de producto (10pz)", "price_mxn": 2000, "duration_min": 120},
                {"name": "Sesion XV anos", "price_mxn": 5000, "duration_min": 180},
                {"name": "Foto pasaporte/INE", "price_mxn": 100, "duration_min": 10},
            ],
            "subscription_tier": "basic",
            "monthly_fee_mxn": 299,
            "status": "active",
            "created_at": "2026-01-25T00:00:00",
        },
    ]

    # ─── 40 Customers ───

    _first_names = [
        "Maria", "Ana", "Guadalupe", "Rosa", "Carmen", "Lucia", "Elena",
        "Sofia", "Valentina", "Daniela", "Carlos", "Juan", "Miguel", "Pedro",
        "Fernando", "Ricardo", "Alejandro", "Francisco", "Arturo", "Eduardo",
        "Gabriela", "Mariana", "Isabella", "Camila", "Regina", "Diego",
        "Sebastian", "Mateo", "Leonardo", "Emiliano", "Josefina", "Teresa",
        "Adriana", "Claudia", "Veronica", "Leticia", "Jorge", "Alberto",
        "Oscar", "Raul",
    ]
    _last_names = [
        "Garcia", "Rodriguez", "Martinez", "Lopez", "Hernandez", "Gonzalez",
        "Perez", "Sanchez", "Ramirez", "Torres", "Flores", "Rivera",
        "Gomez", "Diaz", "Morales", "Reyes", "Cruz", "Ortiz",
        "Gutierrez", "Chavez",
    ]

    customers = []
    for i in range(40):
        fn = _first_names[i]
        ln = _last_names[i % len(_last_names)]
        phone_suffix = f"{100 + i:03d}"
        biz_count = random.randint(1, 3)
        biz_ids = random.sample([b["id"] for b in businesses], min(biz_count, len(businesses)))
        customers.append({
            "id": f"cust-{i+1:03d}",
            "phone": f"+52 443 {random.randint(100,999)} {phone_suffix}{random.randint(0,9)}",
            "name": f"{fn} {ln}",
            "preferred_language": "es" if random.random() < 0.92 else "en",
            "business_ids": biz_ids,
            "total_appointments": random.randint(0, 15),
            "last_contact": (datetime(2026, 4, 4) - timedelta(days=random.randint(0, 30))).isoformat(),
        })

    # ─── 60 Appointments (this week) ───

    today = date(2026, 4, 4)
    appointments = []
    _statuses = ["pending", "confirmed", "completed", "cancelled", "no_show"]
    _times = ["09:00", "09:30", "10:00", "10:30", "11:00", "11:30", "12:00",
              "13:00", "14:00", "15:00", "16:00", "17:00", "18:00", "19:00"]

    for i in range(60):
        biz = random.choice(businesses)
        cust = random.choice(customers)
        svc = random.choice(biz["services"]) if biz["services"] else {"name": "Consulta", "price_mxn": 0, "duration_min": 30}
        appt_date = today + timedelta(days=random.randint(-3, 4))
        status = random.choices(
            _statuses,
            weights=[15, 25, 30, 10, 5],
            k=1
        )[0]
        if appt_date > today:
            status = random.choice(["pending", "confirmed"])

        appointments.append({
            "id": f"appt-{i+1:03d}",
            "business_id": biz["id"],
            "customer_phone": cust["phone"],
            "customer_name": cust["name"],
            "service_name": svc["name"],
            "date": appt_date.isoformat(),
            "time": random.choice(_times),
            "duration_min": svc["duration_min"],
            "status": status,
            "reminder_sent": status in ("confirmed", "completed"),
            "created_via": random.choice(["whatsapp", "whatsapp", "whatsapp", "manual", "web"]),
            "notes": "",
        })

    # ─── 30 Conversations with realistic WhatsApp messages ───

    _conv_templates = [
        # Restaurant booking
        [
            {"role": "customer", "content": "Hola! Quisiera reservar una mesa para 4 personas este sabado", "message_type": "text"},
            {"role": "assistant", "content": "Hola! Con mucho gusto te ayudo. Para el sabado tenemos disponibilidad a las 14:00, 15:00 o 20:00. Cual te queda mejor?", "message_type": "text"},
            {"role": "customer", "content": "A las 20:00 por favor", "message_type": "text"},
            {"role": "assistant", "content": "Perfecto! Te reservo mesa para 4 personas el sabado a las 20:00. A nombre de quien sera la reserva?", "message_type": "booking"},
        ],
        # Salon appointment
        [
            {"role": "customer", "content": "Buenas tardes, cuanto cuesta el corte de cabello?", "message_type": "text"},
            {"role": "assistant", "content": "Buenas tardes! El corte de cabello para dama es de $150 y para caballero $80. Te gustaria agendar una cita?", "message_type": "text"},
            {"role": "customer", "content": "Si, para manana en la manana porfa", "message_type": "text"},
            {"role": "assistant", "content": "Claro! Tengo disponible a las 10:00 o 11:30. Cual prefieres?", "message_type": "booking"},
            {"role": "customer", "content": "10 am esta bien", "message_type": "text"},
            {"role": "assistant", "content": "Listo! Tu cita queda confirmada para manana a las 10:00 am. Te mandare un recordatorio. Que tengas bonita tarde!", "message_type": "confirmation"},
        ],
        # Mechanic inquiry
        [
            {"role": "customer", "content": "Buenas, mi carro esta haciendo un ruido raro. Cuando tienen espacio?", "message_type": "text"},
            {"role": "assistant", "content": "Hola! Que tipo de ruido y que carro es? Te puedo agendar para un diagnostico ($500). Tenemos espacio manana a las 9am o pasado a las 8am.", "message_type": "text"},
            {"role": "customer", "content": "Es un Nissan Versa 2019, suena como rechinido al frenar", "message_type": "text"},
            {"role": "assistant", "content": "Puede ser las balatas. El diagnostico nos confirmara. Cambio de balatas esta en $1,500 aprox. Te agendo manana a las 9am?", "message_type": "text"},
            {"role": "customer", "content": "Si dale, manana a las 9", "message_type": "text"},
            {"role": "assistant", "content": "Listo! Cita agendada para manana 9am, Nissan Versa 2019 - diagnostico de frenos. Trae tu carro en ayunas (sin lavar los frenos). Te espero!", "message_type": "confirmation"},
        ],
        # Dental
        [
            {"role": "customer", "content": "Hola doctora, necesito una limpieza dental", "message_type": "text"},
            {"role": "assistant", "content": "Hola! La limpieza dental tiene un costo de $800 y dura aprox 45 min. Tengo horarios disponibles esta semana. Que dia te acomoda?", "message_type": "text"},
            {"role": "customer", "content": "El jueves puede ser?", "message_type": "text"},
            {"role": "assistant", "content": "El jueves tengo a las 10:00am y 3:00pm. Cual prefieres?", "message_type": "booking"},
        ],
        # Vet
        [
            {"role": "customer", "content": "Hola, mi perrito necesita sus vacunas. Que horarios tienen?", "message_type": "text"},
            {"role": "assistant", "content": "Hola! Que gusto saludarte! Tenemos vacunacion todos los dias de 9am a 7pm. La vacuna tiene un costo de $350. Que raza y edad tiene tu lomito?", "message_type": "text"},
            {"role": "customer", "content": "Es un golden retriever de 3 meses", "message_type": "text"},
            {"role": "assistant", "content": "Que lindo! A esa edad le toca su primera vacuna polivalente. Te agendo para manana? Le hacemos su cartilla de vacunacion sin costo extra!", "message_type": "booking"},
        ],
        # Payment request
        [
            {"role": "customer", "content": "Hola ya quede con la cita de manana. Como puedo pagar?", "message_type": "text"},
            {"role": "assistant", "content": "Puedes pagar por transferencia a CLABE: 012180001234567890 (BBVA) o en efectivo cuando llegues. Si transfieres, mandame tu comprobante por aqui y te confirmo al instante!", "message_type": "payment"},
            {"role": "customer", "content": "Ya hice la transferencia, te mando el comprobante", "message_type": "text"},
            {"role": "assistant", "content": "Recibido! Pago confirmado. Tu cita esta lista para manana. Gracias por tu preferencia!", "message_type": "confirmation"},
        ],
        # Gym class
        [
            {"role": "customer", "content": "Que onda! Cuanto cuesta la membresia del crossfit?", "message_type": "text"},
            {"role": "assistant", "content": "Que onda! La membresia mensual esta en $1,200. Pero si quieres primero puedes tomar una clase de prueba GRATIS para que conozcas. Te animas?", "message_type": "text"},
            {"role": "customer", "content": "Orale! Si, cuando puedo ir?", "message_type": "text"},
            {"role": "assistant", "content": "Tenemos clases a las 6am, 7am, 5pm, 6pm y 7pm de lunes a viernes. Cual horario te late mas? Solo trae ropa comoda, tenis y agua!", "message_type": "booking"},
        ],
        # Laundry
        [
            {"role": "customer", "content": "Hola, cuanto me cobran por 5 kilos de ropa?", "message_type": "text"},
            {"role": "assistant", "content": "Hola! El lavado regular es $25/kg, serian $125 por 5kg. Si lo quieres express en 2hrs son $45/kg ($225). Incluye lavado, secado y doblado.", "message_type": "text"},
            {"role": "customer", "content": "El normal esta bien. Puedo llevarla ahorita?", "message_type": "text"},
            {"role": "assistant", "content": "Si, estamos abiertos hasta las 8pm. Tu ropa estaria lista manana antes del mediodia. Te mandamos mensaje cuando este lista!", "message_type": "confirmation"},
        ],
        # Photography
        [
            {"role": "customer", "content": "Hola! Cuanto cobran por fotos de XV anos?", "message_type": "text"},
            {"role": "assistant", "content": "Hola! La sesion de XV anos incluye 2-3 hrs de sesion, 50 fotos editadas y album digital por $5,000. Tambien tenemos paquete con video por $8,000. Cuando seria la fiesta?", "message_type": "text"},
            {"role": "customer", "content": "Es el 15 de mayo. Tienen disponible?", "message_type": "text"},
            {"role": "assistant", "content": "Dejame checar... Si! El 15 de mayo esta disponible. Para apartar la fecha necesitamos un anticipo de $1,500. Te parece si agendamos una llamada para ver los detalles?", "message_type": "booking"},
        ],
        # Tutoring
        [
            {"role": "customer", "content": "Buenas tardes, mi hijo necesita apoyo en matematicas para prepa", "message_type": "text"},
            {"role": "assistant", "content": "Buenas tardes! Tenemos tutorias de mate a $200/hr. Podemos evaluar el nivel de su hijo en la primera clase y armar un plan personalizado. Que semestre cursa?", "message_type": "text"},
            {"role": "customer", "content": "Va en tercer semestre, le cuestan las derivadas", "message_type": "text"},
            {"role": "assistant", "content": "Perfecto, eso es calculo diferencial. Nuestra profa Ana es especialista en eso. Puedo agendarle una clase de prueba esta semana?", "message_type": "booking"},
        ],
    ]

    conversations = []
    for i in range(30):
        biz = businesses[i % len(businesses)]
        cust = customers[i % len(customers)]
        template = _conv_templates[i % len(_conv_templates)]
        base_time = datetime(2026, 4, 4) - timedelta(hours=random.randint(1, 72))
        msgs = []
        for j, m in enumerate(template):
            msgs.append({
                **m,
                "timestamp": (base_time + timedelta(minutes=j * random.randint(1, 10))).isoformat(),
            })
        status = random.choice(["active", "active", "resolved", "escalated"])
        conversations.append({
            "id": f"conv-{i+1:03d}",
            "business_id": biz["id"],
            "customer_phone": cust["phone"],
            "messages": msgs,
            "status": status,
            "started_at": base_time.isoformat(),
            "resolved_at": (base_time + timedelta(hours=random.randint(1, 24))).isoformat() if status == "resolved" else None,
        })

    # ─── 20 Payments ───

    payments = []
    for i in range(20):
        biz = random.choice(businesses)
        cust = random.choice(customers)
        svc = random.choice(biz["services"]) if biz["services"] else {"price_mxn": 500}
        status = random.choice(["pending", "sent", "paid", "paid", "paid", "failed"])
        method = random.choice(["transfer", "transfer", "card", "cash", "cash"])
        payments.append({
            "id": f"pay-{i+1:03d}",
            "business_id": biz["id"],
            "customer_phone": cust["phone"],
            "appointment_id": f"appt-{random.randint(1, 60):03d}",
            "amount_mxn": svc["price_mxn"] if svc["price_mxn"] > 0 else random.choice([200, 500, 800, 1200]),
            "status": status,
            "payment_link": f"https://wa.flow/pay/{biz['id'][:8]}/{i+1}" if status in ("pending", "sent") else "",
            "method": method,
            "created_at": (datetime(2026, 4, 4) - timedelta(days=random.randint(0, 14))).isoformat(),
        })

    # ─── Templates (per business type) ───

    _type_templates = {
        "restaurant": [
            {"template_type": "greeting", "content_es": "Hola {nombre}! Bienvenido a {negocio}. En que te puedo ayudar hoy?", "content_en": "Hi {nombre}! Welcome to {negocio}. How can I help you today?", "variables": ["nombre", "negocio"]},
            {"template_type": "booking_confirm", "content_es": "Tu reservacion esta confirmada! Mesa para {personas} el {fecha} a las {hora}. Te esperamos!", "content_en": "Your reservation is confirmed! Table for {personas} on {fecha} at {hora}. See you there!", "variables": ["personas", "fecha", "hora"]},
            {"template_type": "reminder_24h", "content_es": "Hola {nombre}! Te recordamos que manana tienes reservacion a las {hora}. Sigues confirmado?", "content_en": "Hi {nombre}! Reminder: your reservation is tomorrow at {hora}. Still coming?", "variables": ["nombre", "hora"]},
            {"template_type": "thank_you", "content_es": "Gracias por visitarnos {nombre}! Esperamos que hayas disfrutado. Te esperamos pronto!", "content_en": "Thanks for visiting {nombre}! Hope you enjoyed it. See you soon!", "variables": ["nombre"]},
        ],
        "salon": [
            {"template_type": "greeting", "content_es": "Hola {nombre}! Bienvenida a {negocio}. Quieres agendar una cita?", "content_en": "Hi {nombre}! Welcome to {negocio}. Would you like to book an appointment?", "variables": ["nombre", "negocio"]},
            {"template_type": "booking_confirm", "content_es": "Cita confirmada! {servicio} el {fecha} a las {hora}. No olvides llegar 10 min antes.", "content_en": "Appointment confirmed! {servicio} on {fecha} at {hora}. Please arrive 10 min early.", "variables": ["servicio", "fecha", "hora"]},
            {"template_type": "reminder_1h", "content_es": "Hola {nombre}! Tu cita es en 1 hora ({hora}). Te esperamos!", "content_en": "Hi {nombre}! Your appointment is in 1 hour ({hora}). See you soon!", "variables": ["nombre", "hora"]},
            {"template_type": "payment_request", "content_es": "Hola {nombre}! El costo de tu {servicio} fue de ${monto}. Puedes pagar en efectivo o transferencia.", "content_en": "Hi {nombre}! Your {servicio} costs ${monto}. You can pay cash or transfer.", "variables": ["nombre", "servicio", "monto"]},
        ],
        "mechanic": [
            {"template_type": "greeting", "content_es": "Hola! Bienvenido a {negocio}. Tienes algun problema con tu vehiculo?", "content_en": "Hi! Welcome to {negocio}. Having issues with your vehicle?", "variables": ["negocio"]},
            {"template_type": "booking_confirm", "content_es": "Tu cita esta agendada: {servicio} el {fecha} a las {hora}. Recuerda traer tu tarjeta de circulacion.", "content_en": "Your appointment is set: {servicio} on {fecha} at {hora}.", "variables": ["servicio", "fecha", "hora"]},
            {"template_type": "payment_request", "content_es": "El diagnostico de tu vehiculo indica: {descripcion}. Costo total: ${monto}. Autorizas el trabajo?", "content_en": "Vehicle diagnosis: {descripcion}. Total cost: ${monto}. Shall we proceed?", "variables": ["descripcion", "monto"]},
        ],
        "default": [
            {"template_type": "greeting", "content_es": "Hola {nombre}! Gracias por contactar a {negocio}. Como te puedo ayudar?", "content_en": "Hi {nombre}! Thanks for contacting {negocio}. How can I help?", "variables": ["nombre", "negocio"]},
            {"template_type": "booking_confirm", "content_es": "Tu cita esta confirmada para el {fecha} a las {hora}. Te esperamos!", "content_en": "Your appointment is confirmed for {fecha} at {hora}. See you!", "variables": ["fecha", "hora"]},
            {"template_type": "reminder_24h", "content_es": "Hola {nombre}! Recordatorio: tu cita es manana a las {hora}.", "content_en": "Hi {nombre}! Reminder: your appointment is tomorrow at {hora}.", "variables": ["nombre", "hora"]},
            {"template_type": "closed", "content_es": "Gracias por tu mensaje! En este momento estamos cerrados. Nuestro horario es {horario}. Te respondemos manana!", "content_en": "Thanks for your message! We're currently closed. Our hours are {horario}. We'll reply tomorrow!", "variables": ["horario"]},
        ],
    }

    templates = []
    for biz in businesses:
        cat = biz["category"]
        tmpl_list = _type_templates.get(cat, _type_templates["default"])
        for t in tmpl_list:
            templates.append({
                "id": f"tmpl-{biz['id'][-8:]}-{t['template_type']}",
                "business_id": biz["id"],
                **t,
            })

    # ─── Analytics (past 30 days) ───

    analytics = []
    for biz in businesses:
        for day_offset in range(30):
            d = today - timedelta(days=day_offset)
            is_weekend = d.weekday() >= 5
            base_msgs = random.randint(5, 25) if not is_weekend else random.randint(8, 35)
            analytics.append({
                "id": f"ana-{biz['id'][-8:]}-{d.isoformat()}",
                "business_id": biz["id"],
                "period": "daily",
                "messages_received": base_msgs,
                "messages_sent": base_msgs + random.randint(0, 10),
                "appointments_booked": random.randint(0, 8),
                "appointments_completed": random.randint(0, 6),
                "no_shows": random.randint(0, 2),
                "revenue_mxn": random.randint(0, 5000) if biz["services"] else 0,
                "response_time_avg_seconds": random.randint(15, 120),
                "customer_satisfaction": round(random.uniform(3.5, 5.0), 1),
                "date": d.isoformat(),
            })

    # ─── Webhook Events (recent) ───

    webhook_events = []
    for i in range(15):
        biz = random.choice(businesses)
        evt_type = random.choice(["message_received", "message_sent", "status_update"])
        webhook_events.append({
            "id": f"wh-{i+1:03d}",
            "business_id": biz["id"],
            "event_type": evt_type,
            "payload": {"from": "+52 443 100 0000", "body": "test message"},
            "processed": random.choice([True, True, False]),
            "timestamp": (datetime(2026, 4, 4) - timedelta(minutes=random.randint(0, 1440))).isoformat(),
        })

    # ─── Save ───

    data = {
        "businesses": businesses,
        "customers": customers,
        "appointments": appointments,
        "conversations": conversations,
        "payments": payments,
        "templates": templates,
        "analytics": analytics,
        "webhook_events": webhook_events,
    }
    save_store(data)
    return data
