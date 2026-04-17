import { useState, useRef, useEffect } from 'react';
import { useApi, postApi } from '../hooks/useApi';

interface Business { id: string; name: string; category: string; }
interface ChatMsg { role: 'customer' | 'assistant'; content: string; time: string; action?: string; }

const categoryEmoji: Record<string, string> = {
  restaurant: '\ud83c\udf7d\ufe0f', salon: '\ud83d\udc87', mechanic: '\ud83d\udd27', clinic: '\ud83c\udfe5',
  dentist: '\ud83e\uddb7', gym: '\ud83d\udcaa', veterinary: '\ud83d\udc3e', laundry: '\ud83d\udc55',
  tutoring: '\ud83d\udcda', other: '\ud83d\udccb',
};

const labels: Record<string, Record<string, string>> = {
  en: {
    title: 'AI Simulator', sub: 'Test the WhatsApp AI assistant in real-time',
    selectBiz: 'Select a business to chat with', placeholder: 'Type a message as a customer...',
    send: 'Send', typing: 'WaFlow AI is typing...',
    hint: 'Try: "Hola, quiero agendar una cita" or "Cuanto cuesta el corte?"',
  },
  es: {
    title: 'Simulador AI', sub: 'Prueba el asistente de WhatsApp AI en tiempo real',
    selectBiz: 'Selecciona un negocio para chatear', placeholder: 'Escribe como cliente de WhatsApp...',
    send: 'Enviar', typing: 'WaFlow AI esta escribiendo...',
    hint: 'Prueba: "Hola, quiero agendar una cita" o "Cuanto cuesta el corte?"',
  },
};

export default function Simulator({ lang }: { lang: string }) {
  const t = labels[lang] || labels.es;
  const { data: bizData, loading } = useApi<{ businesses: Business[] }>('/businesses', { businesses: [] });
  const [selectedBiz, setSelectedBiz] = useState<Business | null>(null);
  const [messages, setMessages] = useState<ChatMsg[]>([]);
  const [input, setInput] = useState('');
  const [sending, setSending] = useState(false);
  const msgsEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    msgsEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const selectBusiness = (biz: Business) => {
    setSelectedBiz(biz);
    setMessages([{
      role: 'assistant',
      content: `Hola! Bienvenido a ${biz.name}. En que te puedo ayudar hoy?`,
      time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    }]);
  };

  const sendMessage = async () => {
    if (!input.trim() || !selectedBiz || sending) return;
    const userMsg: ChatMsg = {
      role: 'customer',
      content: input.trim(),
      time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    };
    setMessages((prev) => [...prev, userMsg]);
    setInput('');
    setSending(true);

    try {
      const result = await postApi('/ai/process-message', {
        business_id: selectedBiz.id,
        customer_phone: '+52 443 100 0000',
        message: userMsg.content,
      });
      // Extract clean response text — handle JSON strings or plain text
      let responseText = result.response || '';
      if (!responseText && typeof result === 'string') {
        try {
          const parsed = JSON.parse(result);
          responseText = parsed.response || result;
        } catch { responseText = result; }
      }
      // Clean any remaining JSON artifacts
      responseText = responseText.replace(/```json\s*/g, '').replace(/```/g, '').trim();
      if (responseText.startsWith('{') && responseText.includes('"response"')) {
        try { responseText = JSON.parse(responseText).response; } catch { /* keep as is */ }
      }
      const aiMsg: ChatMsg = {
        role: 'assistant',
        content: responseText || 'Gracias por tu mensaje. Un momento por favor. 😊',
        time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        action: result.action !== 'none' ? result.action : undefined,
      };
      setMessages((prev) => [...prev, aiMsg]);
    } catch {
      setMessages((prev) => [...prev, {
        role: 'assistant',
        content: `Hola! Gracias por escribir a ${selectedBiz.name}. En un momento te atendemos.`,
        time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      }]);
    } finally {
      setSending(false);
    }
  };

  if (loading) return <div className="page-header"><h1>{t.title}</h1><p>Loading...</p></div>;

  if (!selectedBiz) {
    return (
      <div>
        <div className="page-header">
          <h1>{t.title}</h1>
          <p>{t.sub}</p>
        </div>
        <p style={{ marginBottom: 16, color: 'var(--text-light)' }}>{t.selectBiz}:</p>
        <div className="card-grid">
          {bizData.businesses.map((b) => (
            <div key={b.id} className="card" style={{ cursor: 'pointer' }} onClick={() => selectBusiness(b)}>
              <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
                <span style={{ fontSize: '2rem' }}>{categoryEmoji[b.category] || '\ud83c\udfe2'}</span>
                <div>
                  <h3 style={{ margin: 0, fontSize: '1rem' }}>{b.name}</h3>
                  <span style={{ color: 'var(--text-light)', textTransform: 'capitalize', fontSize: '0.85rem' }}>{b.category}</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    );
  }

  return (
    <div>
      <div className="page-header">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <div>
            <h1>{t.title}</h1>
            <p>{t.hint}</p>
          </div>
          <button className="btn btn-primary" onClick={() => { setSelectedBiz(null); setMessages([]); }}>
            {lang === 'es' ? 'Cambiar negocio' : 'Change business'}
          </button>
        </div>
      </div>

      <div className="chat-container">
        <div className="chat-header">
          <div className="avatar">{categoryEmoji[selectedBiz.category] || '\ud83c\udfe2'}</div>
          <div>
            <div style={{ fontWeight: 600 }}>{selectedBiz.name}</div>
            <div style={{ fontSize: '0.8rem', opacity: 0.8 }}>
              {sending ? t.typing : (lang === 'es' ? 'En linea' : 'Online')}
            </div>
          </div>
        </div>

        <div className="chat-messages">
          {messages.map((m, i) => (
            <div key={i} className={`chat-bubble ${m.role}`}>
              {m.content}
              <div className="bubble-time">
                {m.time}
                {m.action && <span style={{ marginLeft: 8, fontStyle: 'italic' }}>[{m.action}]</span>}
              </div>
            </div>
          ))}
          {sending && (
            <div className="chat-bubble assistant" style={{ opacity: 0.6 }}>
              <em>{t.typing}</em>
            </div>
          )}
          <div ref={msgsEndRef} />
        </div>

        <div className="chat-input">
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && sendMessage()}
            placeholder={t.placeholder}
            disabled={sending}
          />
          <button onClick={sendMessage} disabled={sending}>{'\u27a4'}</button>
        </div>
      </div>
    </div>
  );
}
