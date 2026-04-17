import { useApi } from '../hooks/useApi';

interface Appointment {
  id: string;
  business_id: string;
  customer_phone: string;
  customer_name: string;
  service_name: string;
  date: string;
  time: string;
  duration_min: number;
  status: string;
  created_via: string;
}

interface Business { id: string; name: string; }

const labels: Record<string, Record<string, string>> = {
  en: { title: 'Appointments', sub: 'All scheduled appointments', business: 'Business', customer: 'Customer', service: 'Service', date: 'Date', time: 'Time', status: 'Status', via: 'Via' },
  es: { title: 'Citas', sub: 'Todas las citas agendadas', business: 'Negocio', customer: 'Cliente', service: 'Servicio', date: 'Fecha', time: 'Hora', status: 'Estado', via: 'Via' },
};

export default function Appointments({ lang }: { lang: string }) {
  const t = labels[lang] || labels.es;
  const { data, loading } = useApi<{ appointments: Appointment[] }>('/appointments', { appointments: [] });
  const { data: bizData } = useApi<{ businesses: Business[] }>('/businesses', { businesses: [] });

  if (loading) return <div className="page-header"><h1>{t.title}</h1><p>Loading...</p></div>;

  const bizMap: Record<string, string> = {};
  bizData.businesses.forEach((b) => { bizMap[b.id] = b.name; });

  const sorted = [...data.appointments].sort((a, b) => {
    const da = `${a.date} ${a.time}`;
    const db = `${b.date} ${b.time}`;
    return da.localeCompare(db);
  });

  return (
    <div>
      <div className="page-header">
        <h1>{t.title} ({data.appointments.length})</h1>
        <p>{t.sub}</p>
      </div>

      <table className="data-table">
        <thead>
          <tr>
            <th>{t.business}</th>
            <th>{t.customer}</th>
            <th>{t.service}</th>
            <th>{t.date}</th>
            <th>{t.time}</th>
            <th>{t.status}</th>
            <th>{t.via}</th>
          </tr>
        </thead>
        <tbody>
          {sorted.map((a) => (
            <tr key={a.id}>
              <td>{(bizMap[a.business_id] || a.business_id).slice(0, 22)}</td>
              <td>
                <div style={{ fontWeight: 500 }}>{a.customer_name}</div>
                <div style={{ fontSize: '0.75rem', color: 'var(--text-light)' }}>{a.customer_phone}</div>
              </td>
              <td>{a.service_name.slice(0, 25)}</td>
              <td>{a.date}</td>
              <td>{a.time}</td>
              <td><span className={`badge badge-${a.status}`}>{a.status}</span></td>
              <td style={{ fontSize: '0.8rem' }}>{a.created_via === 'whatsapp' ? '\ud83d\udcf1 WhatsApp' : a.created_via}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
