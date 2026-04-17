import { useState } from 'react';
import { postApi } from '../hooks/useApi';

const categories = [
  { value: 'restaurant', label: 'Restaurante', emoji: '\ud83c\udf7d\ufe0f' },
  { value: 'salon', label: 'Estetica / Salon', emoji: '\ud83d\udc87' },
  { value: 'mechanic', label: 'Mecanico / Taller', emoji: '\ud83d\udd27' },
  { value: 'clinic', label: 'Clinica / Consultorio', emoji: '\ud83c\udfe5' },
  { value: 'dentist', label: 'Dentista', emoji: '\ud83e\uddb7' },
  { value: 'gym', label: 'Gimnasio', emoji: '\ud83d\udcaa' },
  { value: 'veterinary', label: 'Veterinaria', emoji: '\ud83d\udc3e' },
  { value: 'laundry', label: 'Lavanderia', emoji: '\ud83d\udc55' },
  { value: 'tutoring', label: 'Tutorias / Clases', emoji: '\ud83d\udcda' },
  { value: 'other', label: 'Otro', emoji: '\ud83d\udccb' },
];

const labels: Record<string, Record<string, string>> = {
  en: {
    title: 'Setup Wizard', sub: 'AI-powered business onboarding',
    name: 'Business Name', category: 'Category', generate: 'Generate with AI',
    generating: 'AI is generating configuration...', services: 'Suggested Services',
    templates: 'Generated Templates', greeting: 'Suggested Greeting',
    step1: 'Step 1: Enter your business info', step2: 'Step 2: AI generates your config',
  },
  es: {
    title: 'Configuracion', sub: 'Onboarding de negocios con AI',
    name: 'Nombre del Negocio', category: 'Categoria', generate: 'Generar con AI',
    generating: 'AI esta generando la configuracion...', services: 'Servicios Sugeridos',
    templates: 'Plantillas Generadas', greeting: 'Saludo Sugerido',
    step1: 'Paso 1: Ingresa la informacion de tu negocio', step2: 'Paso 2: AI genera tu configuracion',
  },
};

export default function Setup({ lang }: { lang: string }) {
  const t = labels[lang] || labels.es;
  const [name, setName] = useState('');
  const [category, setCategory] = useState('salon');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState('');

  const generate = async () => {
    if (!name.trim()) return;
    setLoading(true);
    setError('');
    setResult(null);
    try {
      const data = await postApi('/ai/setup', { category, business_name: name });
      setResult(data);
    } catch (e: any) {
      setError(e.message || 'Error generating configuration');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <div className="page-header">
        <h1>{t.title}</h1>
        <p>{t.sub}</p>
      </div>

      <div className="card" style={{ maxWidth: 600 }}>
        <h3 style={{ marginBottom: 16 }}>{t.step1}</h3>

        <div style={{ marginBottom: 16 }}>
          <label style={{ display: 'block', fontSize: '0.85rem', fontWeight: 500, marginBottom: 4 }}>{t.name}</label>
          <input
            value={name}
            onChange={(e) => setName(e.target.value)}
            placeholder="Ej: Estetica Diana"
            style={{ width: '100%', padding: '10px 14px', border: '1px solid var(--border)', borderRadius: 8, fontSize: '0.9rem' }}
          />
        </div>

        <div style={{ marginBottom: 16 }}>
          <label style={{ display: 'block', fontSize: '0.85rem', fontWeight: 500, marginBottom: 4 }}>{t.category}</label>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(150px, 1fr))', gap: 8 }}>
            {categories.map((c) => (
              <div
                key={c.value}
                onClick={() => setCategory(c.value)}
                style={{
                  padding: '10px 12px', borderRadius: 8, cursor: 'pointer', textAlign: 'center',
                  border: category === c.value ? '2px solid var(--wa-green)' : '1px solid var(--border)',
                  background: category === c.value ? '#dcf8c6' : 'white',
                  fontSize: '0.85rem',
                }}
              >
                <div style={{ fontSize: '1.3rem' }}>{c.emoji}</div>
                {c.label}
              </div>
            ))}
          </div>
        </div>

        <button
          className="btn btn-wa"
          onClick={generate}
          disabled={loading || !name.trim()}
          style={{ width: '100%', justifyContent: 'center', padding: '12px 16px', fontSize: '1rem' }}
        >
          {loading ? t.generating : `\u2728 ${t.generate}`}
        </button>

        {error && <p style={{ color: 'var(--danger)', marginTop: 12 }}>{error}</p>}
      </div>

      {result && (
        <div style={{ marginTop: 24 }}>
          <h3 style={{ marginBottom: 16 }}>{t.step2}</h3>

          {result.raw ? (
            <div className="card"><pre style={{ whiteSpace: 'pre-wrap', fontSize: '0.85rem' }}>{result.raw}</pre></div>
          ) : (
            <>
              {result.services && (
                <div className="card" style={{ marginBottom: 16 }}>
                  <h3 style={{ marginBottom: 12 }}>{t.services}</h3>
                  <table className="data-table">
                    <thead><tr><th>Servicio</th><th>Precio (MXN)</th><th>Duracion</th></tr></thead>
                    <tbody>
                      {result.services.map((s: any, i: number) => (
                        <tr key={i}>
                          <td>{s.name}</td>
                          <td style={{ fontWeight: 500 }}>${s.price_mxn?.toLocaleString()}</td>
                          <td>{s.duration_min} min</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}

              {result.templates && (
                <div className="card" style={{ marginBottom: 16 }}>
                  <h3 style={{ marginBottom: 12 }}>{t.templates}</h3>
                  {result.templates.map((tp: any, i: number) => (
                    <div key={i} style={{ padding: '8px 0', borderBottom: '1px solid var(--border)' }}>
                      <span className="badge badge-active" style={{ marginRight: 8 }}>{tp.type}</span>
                      <span style={{ fontSize: '0.9rem' }}>{tp.content_es}</span>
                    </div>
                  ))}
                </div>
              )}

              {result.suggested_greeting && (
                <div className="card">
                  <h3 style={{ marginBottom: 8 }}>{t.greeting}</h3>
                  <div className="chat-bubble assistant" style={{ maxWidth: '100%' }}>
                    {result.suggested_greeting}
                  </div>
                </div>
              )}
            </>
          )}
        </div>
      )}
    </div>
  );
}
