import { useApi } from '../hooks/useApi';

interface Payment {
  id: string;
  business_id: string;
  customer_phone: string;
  amount_mxn: number;
  status: string;
  method: string;
  created_at: string;
}

interface Business { id: string; name: string; }

const labels: Record<string, Record<string, string>> = {
  en: { title: 'Payments', sub: 'Payment tracking across businesses', business: 'Business', customer: 'Customer', amount: 'Amount', method: 'Method', status: 'Status', date: 'Date' },
  es: { title: 'Pagos', sub: 'Seguimiento de pagos de todos los negocios', business: 'Negocio', customer: 'Cliente', amount: 'Monto', method: 'Metodo', status: 'Estado', date: 'Fecha' },
};

const methodLabel: Record<string, string> = { transfer: '\ud83c\udfe6 Transferencia', card: '\ud83d\udcb3 Tarjeta', cash: '\ud83d\udcb5 Efectivo' };

export default function Payments({ lang }: { lang: string }) {
  const t = labels[lang] || labels.es;
  const { data, loading } = useApi<{ payments: Payment[] }>('/payments', { payments: [] });
  const { data: bizData } = useApi<{ businesses: Business[] }>('/businesses', { businesses: [] });

  if (loading) return <div className="page-header"><h1>{t.title}</h1><p>Loading...</p></div>;

  const bizMap: Record<string, string> = {};
  bizData.businesses.forEach((b) => { bizMap[b.id] = b.name; });

  const totalPaid = data.payments.filter((p) => p.status === 'paid').reduce((s, p) => s + p.amount_mxn, 0);
  const totalPending = data.payments.filter((p) => p.status === 'pending' || p.status === 'sent').reduce((s, p) => s + p.amount_mxn, 0);

  return (
    <div>
      <div className="page-header">
        <h1>{t.title} ({data.payments.length})</h1>
        <p>{t.sub}</p>
      </div>

      <div className="stats-row" style={{ marginBottom: 20 }}>
        <div className="stat-card">
          <div className="stat-value" style={{ color: '#166534' }}>${totalPaid.toLocaleString()}</div>
          <div className="stat-label">{lang === 'es' ? 'Cobrado' : 'Collected'} (MXN)</div>
        </div>
        <div className="stat-card">
          <div className="stat-value" style={{ color: '#854d0e' }}>${totalPending.toLocaleString()}</div>
          <div className="stat-label">{lang === 'es' ? 'Pendiente' : 'Pending'} (MXN)</div>
        </div>
      </div>

      <table className="data-table">
        <thead>
          <tr><th>ID</th><th>{t.business}</th><th>{t.customer}</th><th>{t.amount}</th><th>{t.method}</th><th>{t.status}</th><th>{t.date}</th></tr>
        </thead>
        <tbody>
          {data.payments.map((p) => (
            <tr key={p.id}>
              <td style={{ fontSize: '0.8rem', color: 'var(--text-light)' }}>{p.id}</td>
              <td>{(bizMap[p.business_id] || '').slice(0, 20)}</td>
              <td style={{ fontSize: '0.85rem' }}>{p.customer_phone}</td>
              <td style={{ fontWeight: 600 }}>${p.amount_mxn.toLocaleString()} MXN</td>
              <td style={{ fontSize: '0.85rem' }}>{methodLabel[p.method] || p.method}</td>
              <td><span className={`badge badge-${p.status}`}>{p.status}</span></td>
              <td style={{ fontSize: '0.85rem' }}>{(p.created_at || '').slice(0, 10)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
