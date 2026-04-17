import { useApi } from '../hooks/useApi';
import { Link } from 'react-router-dom';

interface Business {
  id: string;
  name: string;
  category: string;
  owner_name: string;
  phone_whatsapp: string;
  city: string;
  subscription_tier: string;
  monthly_fee_mxn: number;
  status: string;
}

const categoryEmoji: Record<string, string> = {
  restaurant: '\ud83c\udf7d\ufe0f', salon: '\ud83d\udc87', mechanic: '\ud83d\udd27', clinic: '\ud83c\udfe5',
  dentist: '\ud83e\uddb7', gym: '\ud83d\udcaa', veterinary: '\ud83d\udc3e', laundry: '\ud83d\udc55',
  tutoring: '\ud83d\udcda', other: '\ud83d\udccb',
};

const labels: Record<string, Record<string, string>> = {
  en: { title: 'Businesses', sub: 'All registered businesses on WaFlow', name: 'Name', category: 'Category', owner: 'Owner', phone: 'WhatsApp', plan: 'Plan', status: 'Status' },
  es: { title: 'Negocios', sub: 'Todos los negocios registrados en WaFlow', name: 'Nombre', category: 'Categoria', owner: 'Dueno', phone: 'WhatsApp', plan: 'Plan', status: 'Estado' },
};

export default function Businesses({ lang }: { lang: string }) {
  const t = labels[lang] || labels.es;
  const { data, loading } = useApi<{ businesses: Business[]; total: number }>('/businesses', { businesses: [], total: 0 });

  if (loading) return <div className="page-header"><h1>{t.title}</h1><p>Loading...</p></div>;

  return (
    <div>
      <div className="page-header">
        <h1>{t.title} ({data.total})</h1>
        <p>{t.sub}</p>
      </div>

      <div className="card-grid">
        {data.businesses.map((b) => (
          <Link to={`/businesses/${b.id}`} key={b.id} style={{ textDecoration: 'none', color: 'inherit' }}>
            <div className="card" style={{ cursor: 'pointer', transition: 'transform 0.1s' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 12 }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                  <span style={{ fontSize: '1.5rem' }}>{categoryEmoji[b.category] || '\ud83d\udccb'}</span>
                  <div>
                    <h3 style={{ fontSize: '1rem', margin: 0 }}>{b.name}</h3>
                    <span style={{ fontSize: '0.8rem', color: 'var(--text-light)', textTransform: 'capitalize' }}>{b.category}</span>
                  </div>
                </div>
                <span className={`badge badge-${b.status}`}>{b.status}</span>
              </div>
              <div style={{ fontSize: '0.85rem', color: 'var(--text-light)' }}>
                <div>{b.owner_name}</div>
                <div>{b.phone_whatsapp}</div>
                <div style={{ marginTop: 8, display: 'flex', justifyContent: 'space-between' }}>
                  <span className={`badge badge-${b.subscription_tier}`}>{b.subscription_tier}</span>
                  {b.monthly_fee_mxn > 0 && <span>${b.monthly_fee_mxn}/mes</span>}
                </div>
              </div>
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
}
