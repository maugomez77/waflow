import { Routes, Route, NavLink } from 'react-router-dom';
import { useState } from 'react';
import Dashboard from './pages/Dashboard';
import Businesses from './pages/Businesses';
import BusinessDetail from './pages/BusinessDetail';
import Conversations from './pages/Conversations';
import Appointments from './pages/Appointments';
import Payments from './pages/Payments';
import Analytics from './pages/Analytics';
import Simulator from './pages/Simulator';
import Setup from './pages/Setup';
import PremiumTaxQA from './pages/PremiumTaxQA';

const navItems = [
  { path: '/', label: 'Dashboard', labelEs: 'Panel', icon: '📊', section: 'Overview' },
  { path: '/businesses', label: 'Businesses', labelEs: 'Negocios', icon: '🏢', section: 'Management' },
  { path: '/conversations', label: 'Conversations', labelEs: 'Conversaciones', icon: '💬', section: 'Management' },
  { path: '/appointments', label: 'Appointments', labelEs: 'Citas', icon: '📅', section: 'Operations' },
  { path: '/payments', label: 'Payments', labelEs: 'Pagos', icon: '💰', section: 'Operations' },
  { path: '/analytics', label: 'Analytics', labelEs: 'Analiticas', icon: '📈', section: 'Intelligence' },
  { path: '/simulator', label: 'AI Simulator', labelEs: 'Simulador AI', icon: '🤖', section: 'Intelligence' },
  { path: '/setup', label: 'Setup Wizard', labelEs: 'Configuracion', icon: '✨', section: 'Intelligence' },
  { path: '/tax-qa', label: 'Tax Q&A (Premium)', labelEs: 'Fiscal (Premium)', icon: '💸', section: 'Premium' },
];

export default function App() {
  const [lang, setLang] = useState<'en' | 'es'>('es');
  let lastSection = '';

  return (
    <div className="app-layout">
      <aside className="sidebar">
        <div className="sidebar-brand">
          WaFlow
          <small>{lang === 'en' ? 'WhatsApp AI for Business' : 'WhatsApp AI para Negocios'}</small>
        </div>
        <nav>
          {navItems.map((item) => {
            const showSection = item.section !== lastSection;
            lastSection = item.section;
            return (
              <div key={item.path}>
                {showSection && <div className="nav-section">{item.section}</div>}
                <NavLink to={item.path} end={item.path === '/'} className={({ isActive }) => isActive ? 'active' : ''}>
                  <span>{item.icon}</span> {lang === 'es' ? item.labelEs : item.label}
                </NavLink>
              </div>
            );
          })}
        </nav>
        <div className="sidebar-footer">
          <div className="lang-toggle">
            <button className={lang === 'en' ? 'active' : ''} onClick={() => setLang('en')}>EN</button>
            <button className={lang === 'es' ? 'active' : ''} onClick={() => setLang('es')}>ES</button>
          </div>
          <div style={{ marginTop: 8 }}>WaFlow v0.1.0 | Morelia, MX</div>
        </div>
      </aside>
      <main className="main-content">
        <Routes>
          <Route path="/" element={<Dashboard lang={lang} />} />
          <Route path="/businesses" element={<Businesses lang={lang} />} />
          <Route path="/businesses/:id" element={<BusinessDetail lang={lang} />} />
          <Route path="/conversations" element={<Conversations lang={lang} />} />
          <Route path="/appointments" element={<Appointments lang={lang} />} />
          <Route path="/payments" element={<Payments lang={lang} />} />
          <Route path="/analytics" element={<Analytics lang={lang} />} />
          <Route path="/simulator" element={<Simulator lang={lang} />} />
          <Route path="/setup" element={<Setup lang={lang} />} />
          <Route path="/tax-qa" element={<PremiumTaxQA lang={lang} />} />
        </Routes>
      </main>
    </div>
  );
}
