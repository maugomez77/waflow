import { useParams } from 'react-router-dom';
import { useApi } from '../hooks/useApi';

const labels: Record<string, Record<string, string>> = {
  en: { services: 'Services', hours: 'Working Hours', templates: 'Templates', price: 'Price', duration: 'Duration', day: 'Day', open: 'Open', close: 'Close', type: 'Type', contentEs: 'Content (ES)' },
  es: { services: 'Servicios', hours: 'Horario', templates: 'Plantillas', price: 'Precio', duration: 'Duracion', day: 'Dia', open: 'Abre', close: 'Cierra', type: 'Tipo', contentEs: 'Contenido (ES)' },
};

const dayNames: Record<string, string> = { mon: 'Lunes', tue: 'Martes', wed: 'Miercoles', thu: 'Jueves', fri: 'Viernes', sat: 'Sabado', sun: 'Domingo' };

export default function BusinessDetail({ lang }: { lang: string }) {
  const { id } = useParams();
  const t = labels[lang] || labels.es;
  const { data: biz, loading } = useApi<any>(`/businesses/${id}`, null);
  const { data: tmplData } = useApi<{ templates: any[] }>(`/templates?business_id=${id}`, { templates: [] });

  if (loading || !biz) return <div className="page-header"><h1>Loading...</h1></div>;

  const hours = biz.working_hours || {};
  const services = biz.services || [];

  return (
    <div>
      <div className="page-header">
        <h1>{biz.name}</h1>
        <p>{biz.category} | {biz.city} | {biz.phone_whatsapp}</p>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 16, marginBottom: 16 }}>
        <div className="card">
          <h3 style={{ marginBottom: 12 }}>{t.services}</h3>
          <table className="data-table">
            <thead><tr><th>Servicio</th><th>{t.price}</th><th>{t.duration}</th></tr></thead>
            <tbody>
              {services.map((s: any, i: number) => (
                <tr key={i}>
                  <td>{s.name}</td>
                  <td>{s.price_mxn > 0 ? `$${s.price_mxn.toLocaleString()} MXN` : 'Gratis'}</td>
                  <td>{s.duration_min > 0 ? `${s.duration_min} min` : '-'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <div className="card">
          <h3 style={{ marginBottom: 12 }}>{t.hours}</h3>
          <table className="data-table">
            <thead><tr><th>{t.day}</th><th>{t.open}</th><th>{t.close}</th></tr></thead>
            <tbody>
              {Object.entries(hours).map(([day, h]: [string, any]) => (
                <tr key={day}>
                  <td>{dayNames[day] || day}</td>
                  <td>{h.open || '-'}</td>
                  <td>{h.close || '-'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      <div className="card">
        <h3 style={{ marginBottom: 12 }}>{t.templates} ({tmplData.templates.length})</h3>
        <table className="data-table">
          <thead><tr><th>{t.type}</th><th>{t.contentEs}</th></tr></thead>
          <tbody>
            {tmplData.templates.map((tp: any) => (
              <tr key={tp.id}>
                <td><span className="badge badge-active">{tp.template_type}</span></td>
                <td style={{ fontSize: '0.85rem' }}>{tp.content_es}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
