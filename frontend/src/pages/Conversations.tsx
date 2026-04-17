import { useState } from 'react';
import { useApi } from '../hooks/useApi';

interface Message {
  role: string;
  content: string;
  timestamp: string;
  message_type: string;
}

interface Conversation {
  id: string;
  business_id: string;
  customer_phone: string;
  messages: Message[];
  status: string;
  started_at: string;
}

interface Business {
  id: string;
  name: string;
  category: string;
}

const categoryEmoji: Record<string, string> = {
  restaurant: '\ud83c\udf7d\ufe0f', salon: '\ud83d\udc87', mechanic: '\ud83d\udd27', clinic: '\ud83c\udfe5',
  dentist: '\ud83e\uddb7', gym: '\ud83d\udcaa', veterinary: '\ud83d\udc3e', laundry: '\ud83d\udc55',
  tutoring: '\ud83d\udcda', other: '\ud83d\udccb',
};

const labels: Record<string, Record<string, string>> = {
  en: { title: 'Conversations', sub: 'WhatsApp conversations across all businesses', select: 'Select a conversation to view' },
  es: { title: 'Conversaciones', sub: 'Conversaciones de WhatsApp de todos los negocios', select: 'Selecciona una conversacion para ver' },
};

export default function Conversations({ lang }: { lang: string }) {
  const t = labels[lang] || labels.es;
  const { data: convData, loading } = useApi<{ conversations: Conversation[] }>('/conversations', { conversations: [] });
  const { data: bizData } = useApi<{ businesses: Business[] }>('/businesses', { businesses: [] });
  const [selected, setSelected] = useState<string | null>(null);

  if (loading) return <div className="page-header"><h1>{t.title}</h1><p>Loading...</p></div>;

  const bizMap: Record<string, Business> = {};
  bizData.businesses.forEach((b) => { bizMap[b.id] = b; });

  const selectedConv = convData.conversations.find((c) => c.id === selected);

  return (
    <div>
      <div className="page-header">
        <h1>{t.title} ({convData.conversations.length})</h1>
        <p>{t.sub}</p>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '350px 1fr', gap: 16 }}>
        {/* Conversation list */}
        <div style={{ maxHeight: 650, overflowY: 'auto' }}>
          {convData.conversations.map((c) => {
            const biz = bizMap[c.business_id];
            const lastMsg = c.messages[c.messages.length - 1];
            return (
              <div
                key={c.id}
                onClick={() => setSelected(c.id)}
                style={{
                  padding: '12px 16px', cursor: 'pointer',
                  background: selected === c.id ? '#dcf8c6' : 'white',
                  borderBottom: '1px solid var(--border)',
                  transition: 'background 0.1s',
                }}
              >
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <strong style={{ fontSize: '0.9rem' }}>
                    {biz ? `${categoryEmoji[biz.category] || ''} ${biz.name}` : c.business_id}
                  </strong>
                  <span className={`badge badge-${c.status}`} style={{ fontSize: '0.65rem' }}>{c.status}</span>
                </div>
                <div style={{ fontSize: '0.8rem', color: 'var(--text-light)', marginTop: 2 }}>{c.customer_phone}</div>
                {lastMsg && (
                  <div style={{ fontSize: '0.8rem', color: 'var(--text-light)', marginTop: 4, whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                    {lastMsg.role === 'customer' ? '\ud83d\udc64' : '\ud83e\udd16'} {lastMsg.content}
                  </div>
                )}
              </div>
            );
          })}
        </div>

        {/* Chat view */}
        {selectedConv ? (
          <div className="chat-container">
            <div className="chat-header">
              <div className="avatar">
                {categoryEmoji[bizMap[selectedConv.business_id]?.category] || '\ud83c\udfe2'}
              </div>
              <div>
                <div style={{ fontWeight: 600 }}>{bizMap[selectedConv.business_id]?.name || 'Business'}</div>
                <div style={{ fontSize: '0.8rem', opacity: 0.8 }}>{selectedConv.customer_phone}</div>
              </div>
            </div>
            <div className="chat-messages">
              {selectedConv.messages.map((m, i) => (
                <div key={i} className={`chat-bubble ${m.role}`}>
                  {m.content}
                  <div className="bubble-time">
                    {m.timestamp ? new Date(m.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) : ''}
                    {m.message_type !== 'text' && ` [${m.message_type}]`}
                  </div>
                </div>
              ))}
            </div>
          </div>
        ) : (
          <div className="card" style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: 600, color: 'var(--text-light)' }}>
            <div style={{ textAlign: 'center' }}>
              <div style={{ fontSize: '3rem', marginBottom: 12 }}>\ud83d\udcac</div>
              <p>{t.select}</p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
