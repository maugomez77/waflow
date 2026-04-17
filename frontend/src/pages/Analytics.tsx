import { useState } from 'react';
import { useApi } from '../hooks/useApi';

interface AnalyticsEntry {
  business_id: string;
  messages_received: number;
  messages_sent: number;
  appointments_booked: number;
  appointments_completed: number;
  no_shows: number;
  revenue_mxn: number;
  response_time_avg_seconds: number;
  customer_satisfaction: number;
  date: string;
}

interface Business { id: string; name: string; category: string; }

const labels: Record<string, Record<string, string>> = {
  en: {
    title: 'Analytics', sub: 'Performance metrics across businesses',
    msgsIn: 'Messages In', msgsOut: 'Messages Out', booked: 'Booked', completed: 'Completed',
    noShows: 'No Shows', revenue: 'Revenue', respTime: 'Resp Time', satisfaction: 'Satisfaction',
    allBusinesses: 'All Businesses', last7: 'Last 7 days', last30: 'Last 30 days',
  },
  es: {
    title: 'Analiticas', sub: 'Metricas de desempeno de todos los negocios',
    msgsIn: 'Mensajes Rec.', msgsOut: 'Mensajes Env.', booked: 'Agendadas', completed: 'Completadas',
    noShows: 'No Shows', revenue: 'Ingresos', respTime: 'T. Resp', satisfaction: 'Satisfaccion',
    allBusinesses: 'Todos los Negocios', last7: 'Ultimos 7 dias', last30: 'Ultimos 30 dias',
  },
};

export default function Analytics({ lang }: { lang: string }) {
  const t = labels[lang] || labels.es;
  const [selectedBiz, setSelectedBiz] = useState<string>('');
  const { data: bizData } = useApi<{ businesses: Business[] }>('/businesses', { businesses: [] });

  const queryBiz = selectedBiz ? `&business_id=${selectedBiz}` : '';
  const { data, loading } = useApi<{ analytics: AnalyticsEntry[] }>(`/analytics?days=30${queryBiz}`, { analytics: [] });

  if (loading) return <div className="page-header"><h1>{t.title}</h1><p>Loading...</p></div>;

  const entries = data.analytics;

  // Aggregate by date (last 7 days)
  const dateMap: Record<string, { msgs_in: number; msgs_out: number; booked: number; completed: number; no_shows: number; revenue: number; resp: number[]; sat: number[] }> = {};
  entries.forEach((e) => {
    if (!dateMap[e.date]) dateMap[e.date] = { msgs_in: 0, msgs_out: 0, booked: 0, completed: 0, no_shows: 0, revenue: 0, resp: [], sat: [] };
    const d = dateMap[e.date];
    d.msgs_in += e.messages_received;
    d.msgs_out += e.messages_sent;
    d.booked += e.appointments_booked;
    d.completed += e.appointments_completed;
    d.no_shows += e.no_shows;
    d.revenue += e.revenue_mxn;
    if (e.response_time_avg_seconds > 0) d.resp.push(e.response_time_avg_seconds);
    if (e.customer_satisfaction > 0) d.sat.push(e.customer_satisfaction);
  });

  const dates = Object.keys(dateMap).sort().slice(-7);
  const totalMsgsIn = dates.reduce((s, d) => s + dateMap[d].msgs_in, 0);
  const totalMsgsOut = dates.reduce((s, d) => s + dateMap[d].msgs_out, 0);
  const totalBooked = dates.reduce((s, d) => s + dateMap[d].booked, 0);
  const totalCompleted = dates.reduce((s, d) => s + dateMap[d].completed, 0);
  const totalRevenue = dates.reduce((s, d) => s + dateMap[d].revenue, 0);

  // Simple bar chart using CSS
  const maxMsgs = Math.max(...dates.map((d) => dateMap[d].msgs_in + dateMap[d].msgs_out), 1);
  const maxRev = Math.max(...dates.map((d) => dateMap[d].revenue), 1);

  return (
    <div>
      <div className="page-header">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <div>
            <h1>{t.title}</h1>
            <p>{t.sub}</p>
          </div>
          <select
            value={selectedBiz}
            onChange={(e) => setSelectedBiz(e.target.value)}
            style={{ padding: '8px 12px', borderRadius: 8, border: '1px solid var(--border)', fontSize: '0.9rem' }}
          >
            <option value="">{t.allBusinesses}</option>
            {bizData.businesses.map((b) => (
              <option key={b.id} value={b.id}>{b.name}</option>
            ))}
          </select>
        </div>
      </div>

      <div className="stats-row">
        <div className="stat-card"><div className="stat-value">{totalMsgsIn.toLocaleString()}</div><div className="stat-label">{t.msgsIn}</div></div>
        <div className="stat-card"><div className="stat-value">{totalMsgsOut.toLocaleString()}</div><div className="stat-label">{t.msgsOut}</div></div>
        <div className="stat-card"><div className="stat-value">{totalBooked}</div><div className="stat-label">{t.booked}</div></div>
        <div className="stat-card"><div className="stat-value">{totalCompleted}</div><div className="stat-label">{t.completed}</div></div>
        <div className="stat-card"><div className="stat-value">${totalRevenue.toLocaleString()}</div><div className="stat-label">{t.revenue} (MXN)</div></div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 16 }}>
        {/* Messages chart */}
        <div className="card">
          <h3 style={{ marginBottom: 16 }}>{lang === 'es' ? 'Mensajes / Dia' : 'Messages / Day'}</h3>
          <div style={{ display: 'flex', alignItems: 'flex-end', gap: 8, height: 200 }}>
            {dates.map((d) => {
              const total = dateMap[d].msgs_in + dateMap[d].msgs_out;
              const pct = (total / maxMsgs) * 100;
              return (
                <div key={d} style={{ flex: 1, display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
                  <div style={{ fontSize: '0.7rem', marginBottom: 4 }}>{total}</div>
                  <div style={{ width: '100%', height: `${pct}%`, background: 'var(--wa-green)', borderRadius: '4px 4px 0 0', minHeight: 4 }}></div>
                  <div style={{ fontSize: '0.65rem', color: 'var(--text-light)', marginTop: 4 }}>{d.slice(5)}</div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Revenue chart */}
        <div className="card">
          <h3 style={{ marginBottom: 16 }}>{lang === 'es' ? 'Ingresos / Dia (MXN)' : 'Revenue / Day (MXN)'}</h3>
          <div style={{ display: 'flex', alignItems: 'flex-end', gap: 8, height: 200 }}>
            {dates.map((d) => {
              const pct = (dateMap[d].revenue / maxRev) * 100;
              return (
                <div key={d} style={{ flex: 1, display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
                  <div style={{ fontSize: '0.7rem', marginBottom: 4 }}>${(dateMap[d].revenue / 1000).toFixed(1)}k</div>
                  <div style={{ width: '100%', height: `${pct}%`, background: 'var(--wa-dark)', borderRadius: '4px 4px 0 0', minHeight: 4 }}></div>
                  <div style={{ fontSize: '0.65rem', color: 'var(--text-light)', marginTop: 4 }}>{d.slice(5)}</div>
                </div>
              );
            })}
          </div>
        </div>
      </div>

      {/* Daily breakdown table */}
      <div className="card" style={{ marginTop: 16 }}>
        <h3 style={{ marginBottom: 12 }}>{lang === 'es' ? 'Desglose Diario' : 'Daily Breakdown'}</h3>
        <table className="data-table">
          <thead>
            <tr><th>{lang === 'es' ? 'Fecha' : 'Date'}</th><th>{t.msgsIn}</th><th>{t.msgsOut}</th><th>{t.booked}</th><th>{t.completed}</th><th>{t.noShows}</th><th>{t.revenue}</th></tr>
          </thead>
          <tbody>
            {dates.reverse().map((d) => (
              <tr key={d}>
                <td>{d}</td>
                <td>{dateMap[d].msgs_in}</td>
                <td>{dateMap[d].msgs_out}</td>
                <td>{dateMap[d].booked}</td>
                <td>{dateMap[d].completed}</td>
                <td style={{ color: dateMap[d].no_shows > 0 ? 'var(--danger)' : undefined }}>{dateMap[d].no_shows}</td>
                <td style={{ fontWeight: 500 }}>${dateMap[d].revenue.toLocaleString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
