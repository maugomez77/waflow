import { useState } from 'react';
import { useApi } from '../hooks/useApi';

interface Business {
  id: string;
  name: string;
  category?: string;
  city?: string;
  subscription_tier?: string;
}

interface TaxAnswer {
  answer_es?: string;
  answer_en?: string;
  citations?: string[];
  confidence?: string;
  recommend_accountant?: boolean;
}

const labels: Record<string, Record<string, string>> = {
  en: {
    title: 'Premium: Tax Compliance Q&A',
    sub: 'Ask CFDI 5.0, RESICO, IVA, ISR, IMSS, NOM-035 questions — grounded in your business context',
    pickBusiness: 'Select a business',
    noPremium: 'This business is not on premium. Upgrade to use the tax assistant.',
    upgrade: 'Upgrade to Premium',
    placeholder: 'e.g. "¿Necesito factura CFDI 5.0 para pagos de proveedor en efectivo de $4,000?"',
    ask: 'Ask',
    asking: 'Thinking…',
    empty: 'Ask a question to get started.',
    answer: 'Answer',
    refs: 'References',
    confidence: 'Confidence',
    accountant: 'Recommend contacting an accountant for your specific case.',
    emptyState: 'No businesses yet — create one first to use the tax assistant.',
  },
  es: {
    title: 'Premium: Asistente Fiscal',
    sub: 'Preguntas sobre CFDI 5.0, RESICO, IVA, ISR, IMSS, NOM-035 — adaptadas a tu negocio',
    pickBusiness: 'Selecciona un negocio',
    noPremium: 'Este negocio no tiene plan Premium. Actualiza para usar el asistente fiscal.',
    upgrade: 'Actualizar a Premium',
    placeholder: 'ej. "¿Necesito factura CFDI 5.0 para pagos de proveedor en efectivo de $4,000?"',
    ask: 'Preguntar',
    asking: 'Pensando…',
    empty: 'Haz una pregunta para empezar.',
    answer: 'Respuesta',
    refs: 'Referencias',
    confidence: 'Confianza',
    accountant: 'Recomienda consultar con un contador para tu caso específico.',
    emptyState: 'No hay negocios todavía — crea uno primero para usar el asistente fiscal.',
  },
};

const API_BASE = (import.meta.env.VITE_API_URL || '') + '/api/v1';
const PREMIUM_TIERS = new Set(['premium', 'pro']);

export default function PremiumTaxQA({ lang }: { lang: 'en' | 'es' }) {
  const t = labels[lang];
  const { data, loading, refetch } = useApi<{ businesses: Business[] }>('/businesses', { businesses: [] });
  const [selected, setSelected] = useState<string>('');
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState<TaxAnswer | null>(null);
  const [loadingAnswer, setLoadingAnswer] = useState(false);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  const businesses = data.businesses ?? [];
  const current = businesses.find((b) => b.id === selected);
  const isPremium = current && PREMIUM_TIERS.has(current.subscription_tier ?? '');

  async function ask() {
    if (!selected || !question.trim()) return;
    setLoadingAnswer(true);
    setErrorMsg(null);
    setAnswer(null);
    try {
      const res = await fetch(`${API_BASE}/premium/tax-qa`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ business_id: selected, question: question.trim() }),
      });
      if (res.status === 402) {
        const payload = await res.json();
        setErrorMsg(payload?.detail?.[`message_${lang}`] ?? t.noPremium);
        return;
      }
      if (!res.ok) throw new Error(`${res.status} ${res.statusText}`);
      const payload = (await res.json()) as TaxAnswer;
      setAnswer(payload);
    } catch (e: any) {
      setErrorMsg(e?.message ?? 'error');
    } finally {
      setLoadingAnswer(false);
    }
  }

  async function upgradeToPremium() {
    if (!selected) return;
    try {
      const res = await fetch(`${API_BASE}/businesses/${selected}/tier?tier=premium`, { method: 'PUT' });
      if (!res.ok) throw new Error(`${res.status} ${res.statusText}`);
      await refetch();
    } catch (e: any) {
      setErrorMsg(e?.message ?? 'error');
    }
  }

  if (loading) return <div className="page"><p>{lang === 'es' ? 'Cargando…' : 'Loading…'}</p></div>;

  return (
    <div className="page">
      <header>
        <h1>{t.title}</h1>
        <p>{t.sub}</p>
      </header>

      {businesses.length === 0 ? (
        <p className="empty">{t.emptyState}</p>
      ) : (
        <>
          <label className="field">
            <span>{t.pickBusiness}</span>
            <select value={selected} onChange={(e) => { setSelected(e.target.value); setAnswer(null); setErrorMsg(null); }}>
              <option value="">—</option>
              {businesses.map((b) => (
                <option key={b.id} value={b.id}>
                  {b.name} · {b.subscription_tier ?? 'free_trial'}
                </option>
              ))}
            </select>
          </label>

          {current && !isPremium && (
            <div className="notice">
              <p>{t.noPremium}</p>
              <button onClick={upgradeToPremium}>{t.upgrade}</button>
            </div>
          )}

          {current && isPremium && (
            <div className="field">
              <textarea
                placeholder={t.placeholder}
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                rows={4}
              />
              <button onClick={ask} disabled={loadingAnswer || !question.trim()}>
                {loadingAnswer ? t.asking : t.ask}
              </button>
            </div>
          )}

          {errorMsg && <p className="error">{errorMsg}</p>}

          {answer && (
            <section className="answer">
              <h2>{t.answer}</h2>
              <p style={{ whiteSpace: 'pre-wrap' }}>{lang === 'es' ? answer.answer_es : (answer.answer_en || answer.answer_es)}</p>

              {answer.citations && answer.citations.length > 0 && (
                <>
                  <h3>{t.refs}</h3>
                  <ul>
                    {answer.citations.map((c, i) => <li key={i}>{c}</li>)}
                  </ul>
                </>
              )}

              <p className="meta">
                {t.confidence}: <strong>{answer.confidence ?? '—'}</strong>
              </p>
              {answer.recommend_accountant && <p className="warning">{t.accountant}</p>}
            </section>
          )}
        </>
      )}
    </div>
  );
}
