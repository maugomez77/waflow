import { useApi } from '../hooks/useApi';

interface Stats {
  total_businesses: number;
  active_businesses: number;
  total_appointments_today: number;
  total_messages_today: number;
  monthly_revenue_mxn: number;
  subscription_revenue_mxn: number;
  avg_response_time_seconds: number;
  top_categories: { category: string; count: number }[];
  total_customers: number;
  total_appointments: number;
  total_conversations: number;
  active_conversations: number;
}

const categoryEmoji: Record<string, string> = {
  restaurant: '\ud83c\udf7d\ufe0f', salon: '\ud83d\udc87', mechanic: '\ud83d\udd27', clinic: '\ud83c\udfe5',
  dentist: '\ud83e\uddb7', gym: '\ud83d\udcaa', veterinary: '\ud83d\udc3e', laundry: '\ud83d\udc55',
  tutoring: '\ud83d\udcda', other: '\ud83d\udccb',
};

const labels: Record<string, Record<string, string>> = {
  en: {
    title: 'Dashboard', sub: 'WaFlow platform overview for Morelia businesses',
    businesses: 'Businesses', customers: 'Customers', apptToday: 'Appointments Today',
    msgsToday: 'Messages Today', revenue: 'Payment Revenue', subscriptions: 'Subscriptions',
    respTime: 'Avg Response', activeConvos: 'Active Conversations',
    topCats: 'Top Categories', recentActivity: 'Platform Metrics',
  },
  es: {
    title: 'Panel', sub: 'Vista general de la plataforma WaFlow en Morelia',
    businesses: 'Negocios', customers: 'Clientes', apptToday: 'Citas Hoy',
    msgsToday: 'Mensajes Hoy', revenue: 'Ingresos Cobros', subscriptions: 'Suscripciones',
    respTime: 'Resp. Promedio', activeConvos: 'Conversaciones Activas',
    topCats: 'Categorias Top', recentActivity: 'Metricas de Plataforma',
  },
};

const defaultStats: Stats = {
  total_businesses: 0, active_businesses: 0, total_appointments_today: 0,
  total_messages_today: 0, monthly_revenue_mxn: 0, subscription_revenue_mxn: 0,
  avg_response_time_seconds: 0, top_categories: [], total_customers: 0,
  total_appointments: 0, total_conversations: 0, active_conversations: 0,
};

export default function Dashboard({ lang }: { lang: string }) {
  const t = labels[lang] || labels.es;
  const { data, loading } = useApi<Stats>('/stats', defaultStats);

  if (loading) return <div className="page-header"><h1>{t.title}</h1><p>Loading...</p></div>;

  return (
    <div>
      <div className="page-header">
        <h1>{t.title}</h1>
        <p>{t.sub}</p>
      </div>

      <div className="stats-row">
        <div className="stat-card">
          <div className="stat-value">{data.active_businesses}</div>
          <div className="stat-label">{t.businesses}</div>
        </div>
        <div className="stat-card">
          <div className="stat-value">{data.total_customers}</div>
          <div className="stat-label">{t.customers}</div>
        </div>
        <div className="stat-card">
          <div className="stat-value">{data.total_appointments_today}</div>
          <div className="stat-label">{t.apptToday}</div>
        </div>
        <div className="stat-card">
          <div className="stat-value">{data.total_messages_today}</div>
          <div className="stat-label">{t.msgsToday}</div>
        </div>
        <div className="stat-card">
          <div className="stat-value">${data.monthly_revenue_mxn.toLocaleString()}</div>
          <div className="stat-label">{t.revenue}</div>
        </div>
        <div className="stat-card">
          <div className="stat-value">${data.subscription_revenue_mxn.toLocaleString()}</div>
          <div className="stat-label">{t.subscriptions}</div>
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 16 }}>
        <div className="card">
          <h3 style={{ marginBottom: 12 }}>{t.topCats}</h3>
          {data.top_categories.map((c) => (
            <div key={c.category} style={{ display: 'flex', justifyContent: 'space-between', padding: '8px 0', borderBottom: '1px solid var(--border)' }}>
              <span className="category-icon">
                <span>{categoryEmoji[c.category] || '\ud83d\udccb'}</span>
                <span style={{ textTransform: 'capitalize' }}>{c.category}</span>
              </span>
              <strong>{c.count}</strong>
            </div>
          ))}
        </div>
        <div className="card">
          <h3 style={{ marginBottom: 12 }}>{t.recentActivity}</h3>
          <div className="activity-item">
            <div className="activity-dot green"></div>
            <div>
              <strong>{t.activeConvos}:</strong> {data.active_conversations}
            </div>
          </div>
          <div className="activity-item">
            <div className="activity-dot blue"></div>
            <div>
              <strong>{t.respTime}:</strong> {data.avg_response_time_seconds.toFixed(0)}s
            </div>
          </div>
          <div className="activity-item">
            <div className="activity-dot yellow"></div>
            <div>
              <strong>{lang === 'es' ? 'Total Citas' : 'Total Appointments'}:</strong> {data.total_appointments}
            </div>
          </div>
          <div className="activity-item">
            <div className="activity-dot green"></div>
            <div>
              <strong>{lang === 'es' ? 'Total Conversaciones' : 'Total Conversations'}:</strong> {data.total_conversations}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
