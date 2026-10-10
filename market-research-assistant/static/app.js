/**
 * app.js — Frontend logic for the Intelligent Market Research Assistant
 * Handles form submission, Q&A chat, tab navigation, and report rendering.
 */

'use strict';

// ─── Constants ────────────────────────────────────────────────────────────────
const API = {
  health:   '/api/health',
  research: '/api/research',
  query:    '/api/query',
};

const AGENT_STEPS = [
  { tool: 'MarketTrendAnalyzer',   label: '📈 Analyzing market trends…',          icon: '📈' },
  { tool: 'CompetitorAnalyzer',    label: '⚔️  Scanning competitors…',            icon: '⚔️' },
  { tool: 'CustomerInsightEngine', label: '👥 Building customer insights…',        icon: '👥' },
  { tool: 'OpportunityFinder',     label: '💡 Finding opportunities…',            icon: '💡' },
  { tool: 'ReportGenerator',       label: '📄 Synthesizing executive report…',    icon: '📄' },
];

// ─── Startup ──────────────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  checkHealth();
  setupForm();
  setupQAInput();
  setupTabs();
});

// ─── Health Check ─────────────────────────────────────────────────────────────
async function checkHealth() {
  const badge = document.getElementById('mode-badge');
  try {
    const res = await fetch(API.health);
    const data = await res.json();
    if (data.mode === 'live') {
      badge.textContent = '🟢 IBM Granite Live';
      badge.className = 'badge badge-live';
    } else {
      badge.textContent = '🟡 Demo Mode';
      badge.className = 'badge badge-demo';
    }
  } catch {
    badge.textContent = '🔴 Offline';
    badge.className = 'badge badge-demo';
  }
}

// ─── Research Form ────────────────────────────────────────────────────────────
function setupForm() {
  const form = document.getElementById('research-form');
  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    if (!validateForm()) return;
    await runResearch();
  });
}

function validateForm() {
  const required = ['industry', 'product', 'target_audience', 'location'];
  let valid = true;
  required.forEach(id => {
    const el = document.getElementById(id);
    if (!el.value.trim()) {
      el.classList.add('error');
      el.addEventListener('input', () => el.classList.remove('error'), { once: true });
      valid = false;
    }
  });
  return valid;
}

async function runResearch() {
  const payload = {
    industry:        document.getElementById('industry').value.trim(),
    product:         document.getElementById('product').value.trim(),
    target_audience: document.getElementById('target_audience').value.trim(),
    location:        document.getElementById('location').value.trim(),
    competitors:     document.getElementById('competitors').value.trim(),
  };

  // Show loading state
  showLoading(payload);
  setFormBusy(true);

  try {
    const res = await fetch(API.research, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    const data = await res.json();

    if (!res.ok || data.status === 'error') {
      showError(data.message || 'An error occurred. Please try again.');
      return;
    }

    renderReport(data, payload);

  } catch (err) {
    showError('Could not reach the server. Please check that the application is running.');
  } finally {
    setFormBusy(false);
  }
}

function setFormBusy(busy) {
  const btn = document.getElementById('research-btn');
  btn.disabled = busy;
  btn.querySelector('.btn-label').textContent = busy ? 'Analyzing…' : 'Generate Market Report';
}

// ─── Loading State ────────────────────────────────────────────────────────────
function showLoading(payload) {
  document.getElementById('empty-state').classList.add('hidden');
  document.getElementById('report-output').classList.add('hidden');
  document.getElementById('loading-state').classList.remove('hidden');

  document.getElementById('loading-title').textContent = `Researching: ${payload.industry}`;
  document.getElementById('loading-subtitle').textContent =
    `Analyzing ${payload.product} for ${payload.target_audience} in ${payload.location}`;

  // Animate agent steps sequentially
  const container = document.getElementById('agent-steps-live');
  container.innerHTML = '';
  AGENT_STEPS.forEach((s, i) => {
    const el = document.createElement('div');
    el.className = 'agent-step';
    el.id = `live-step-${i}`;
    el.innerHTML = `<span class="step-icon">${s.icon}</span><span>${s.label}</span>`;
    container.appendChild(el);
  });

  animateLoadingSteps();
}

function animateLoadingSteps() {
  let current = 0;
  const total = AGENT_STEPS.length;

  function advance() {
    if (current > 0) {
      const prev = document.getElementById(`live-step-${current - 1}`);
      if (prev) prev.className = 'agent-step done';
    }
    const cur = document.getElementById(`live-step-${current}`);
    if (cur) cur.className = 'agent-step active';
    current++;
    if (current < total) {
      setTimeout(advance, 4500 / total);
    }
  }
  advance();
}

// ─── Report Rendering ─────────────────────────────────────────────────────────
function renderReport(data, payload) {
  document.getElementById('loading-state').classList.add('hidden');
  document.getElementById('report-output').classList.remove('hidden');

  // Title & meta
  document.getElementById('report-title').textContent =
    `${payload.industry} Market Research Report`;
  document.getElementById('report-subtitle').textContent =
    `${payload.product} · ${payload.target_audience} · ${payload.location}`;

  const modeBadge = document.getElementById('report-mode-badge');
  modeBadge.textContent = data.mode === 'live' ? '🟢 IBM Granite Live' : '🟡 Demo Mode';
  modeBadge.className = `badge ${data.mode === 'live' ? 'badge-live' : 'badge-demo'}`;

  document.getElementById('report-time-badge').textContent =
    `⏱ ${data.elapsed_seconds}s`;

  // Render each section
  setContent('content-summary', data.report.executive_summary);
  setContent('content-trends', data.report.market_trends);
  setContent('content-competitors', data.report.competitor_analysis);
  setContent('content-customers', data.report.customer_insights);
  setContent('content-opportunities', data.report.opportunities);

  // Render reasoning steps
  renderReasoning(data.reasoning_steps);

  // Render ethics
  renderEthics(data.ethics_check);

  // Warnings
  renderWarnings(data.warnings);

  // Activate summary tab
  activateTab('summary');
}

function setContent(id, markdown) {
  document.getElementById(id).innerHTML = markdownToHtml(markdown || '');
}

/**
 * Lightweight Markdown → HTML renderer.
 * Handles: headers (##, ###, ####), **bold**, *italic*, bullet lists, horizontal rules, line breaks.
 */
function markdownToHtml(md) {
  if (!md) return '<p><em>No content available.</em></p>';

  let html = md
    // Escape HTML entities
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')

    // Headers
    .replace(/^####\s+(.+)$/gm, '<h4>$1</h4>')
    .replace(/^###\s+(.+)$/gm, '<h3>$1</h3>')
    .replace(/^##\s+(.+)$/gm, '<h2>$1</h2>')
    .replace(/^#\s+(.+)$/gm, '<h1>$1</h1>')

    // Bold and italic
    .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
    .replace(/\*([^*]+)\*/g, '<em>$1</em>')

    // Horizontal rules
    .replace(/^---+$/gm, '<hr/>')

    // Bullet lists — convert consecutive bullet lines into <ul>
    .replace(/((?:^[-*]\s+.+\n?)+)/gm, (block) => {
      const items = block.trim().split('\n').map(line =>
        `<li>${line.replace(/^[-*]\s+/, '')}</li>`
      ).join('');
      return `<ul>${items}</ul>`;
    })

    // Numbered lists
    .replace(/((?:^\d+\.\s+.+\n?)+)/gm, (block) => {
      const items = block.trim().split('\n').map(line =>
        `<li>${line.replace(/^\d+\.\s+/, '')}</li>`
      ).join('');
      return `<ol>${items}</ol>`;
    })

    // Paragraphs — wrap double-newline separated blocks
    .split(/\n{2,}/)
    .map(para => {
      para = para.trim();
      if (!para) return '';
      if (/^<(h[1-4]|ul|ol|hr|li)/.test(para)) return para;
      return `<p>${para.replace(/\n/g, '<br/>')}</p>`;
    })
    .join('\n');

  return html;
}

function renderReasoning(steps) {
  const container = document.getElementById('content-reasoning');
  if (!steps || steps.length === 0) {
    container.innerHTML = '<p>No reasoning steps available.</p>';
    return;
  }
  container.innerHTML = steps.map(s => `
    <div class="reasoning-step">
      <div class="r-step-num">${s.step}</div>
      <div class="r-step-content">
        <div class="r-step-tool">${escHtml(s.tool)}</div>
        <div class="r-step-action">${escHtml(s.action)}</div>
      </div>
    </div>
  `).join('');
}

function renderEthics(ethics) {
  const container = document.getElementById('content-ethics');
  if (!ethics) { container.innerHTML = ''; return; }

  const passed = ethics.passed;
  const keys = Object.keys(ethics).filter(k => k !== 'passed');

  const labelMap = {
    data_privacy:    'Data Privacy',
    bias_reduction:  'Bias Reduction',
    transparency:    'Transparency',
    content_safety:  'Content Safety',
    fairness:        'Fairness',
    ham_tone:        'HAM Tone',
  };

  const rows = keys.map(k => `
    <tr>
      <td><strong>${labelMap[k] || k}</strong></td>
      <td>${escHtml(ethics[k])}</td>
    </tr>
  `).join('');

  container.innerHTML = `
    <div class="ethics-check-badge">✅ Ethics Guardrails: ${passed ? 'All checks passed' : 'Review required'}</div>
    <table class="ethics-table">
      <thead><tr><th>Principle</th><th>Implementation</th></tr></thead>
      <tbody>${rows}</tbody>
    </table>
  `;
}

function renderWarnings(warnings) {
  const panel = document.getElementById('warnings-panel');
  const list = document.getElementById('warnings-list');
  if (!warnings || warnings.length === 0) {
    panel.classList.add('hidden');
    return;
  }
  list.innerHTML = warnings.map(w => `<li>${escHtml(w)}</li>`).join('');
  panel.classList.remove('hidden');
}

function showError(message) {
  document.getElementById('loading-state').classList.add('hidden');
  document.getElementById('empty-state').classList.remove('hidden');

  // Inject error into empty state temporarily
  const es = document.getElementById('empty-state');
  const existing = es.querySelector('.error-alert');
  if (existing) existing.remove();

  const alert = document.createElement('div');
  alert.className = 'error-alert';
  alert.style.cssText = `
    background:#ffebe9;border:1px solid #f85149;border-radius:6px;
    padding:12px 16px;font-size:13px;color:#cf222e;margin-top:16px;text-align:left;
  `;
  alert.innerHTML = `<strong>⚠️ Error:</strong> ${escHtml(message)}`;
  es.appendChild(alert);
}

// ─── Tab Navigation ───────────────────────────────────────────────────────────
function setupTabs() {
  document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', () => activateTab(btn.dataset.tab));
  });
}

function activateTab(tabId) {
  document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
  document.querySelectorAll('.tab-pane').forEach(p => p.classList.add('hidden'));

  const btn = document.querySelector(`.tab-btn[data-tab="${tabId}"]`);
  const pane = document.getElementById(`tab-${tabId}`);
  if (btn) btn.classList.add('active');
  if (pane) pane.classList.remove('hidden');
}

// ─── Q&A Chat ─────────────────────────────────────────────────────────────────
function setupQAInput() {
  const input = document.getElementById('qa-input');
  input.addEventListener('keydown', e => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendQuery();
    }
  });
}

function setSampleQ(text) {
  document.getElementById('qa-input').value = text;
  document.getElementById('qa-input').focus();
}

async function sendQuery() {
  const input = document.getElementById('qa-input');
  const question = input.value.trim();
  if (!question) return;

  const btn = document.getElementById('qa-btn');
  const chatWindow = document.getElementById('chat-window');

  // Clear welcome state on first message
  const welcome = chatWindow.querySelector('.chat-welcome');
  if (welcome) welcome.remove();

  // Add user message
  appendChatMsg(chatWindow, 'user', question);
  input.value = '';
  btn.disabled = true;
  btn.textContent = '…';

  // Add thinking indicator
  const thinkingId = 'thinking-' + Date.now();
  const thinking = document.createElement('div');
  thinking.id = thinkingId;
  thinking.className = 'chat-msg chat-msg-thinking';
  thinking.textContent = 'IMRA is thinking…';
  chatWindow.appendChild(thinking);
  chatWindow.scrollTop = chatWindow.scrollHeight;

  try {
    const res = await fetch(API.query, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question }),
    });
    const data = await res.json();

    document.getElementById(thinkingId)?.remove();

    if (!res.ok || data.status === 'error') {
      appendChatMsg(chatWindow, 'error', data.message || 'An error occurred.');
    } else {
      appendChatMsg(chatWindow, 'bot', data.answer);
    }

  } catch {
    document.getElementById(thinkingId)?.remove();
    appendChatMsg(chatWindow, 'error', 'Could not reach the server.');
  } finally {
    btn.disabled = false;
    btn.textContent = 'Ask';
    chatWindow.scrollTop = chatWindow.scrollHeight;
  }
}

function appendChatMsg(container, type, text) {
  const div = document.createElement('div');
  div.className = `chat-msg chat-msg-${type === 'error' ? 'bot chat-msg-error' : type}`;
  div.innerHTML = markdownToHtml(text);
  container.appendChild(div);
  container.scrollTop = container.scrollHeight;
}

// ─── Utilities ────────────────────────────────────────────────────────────────
function escHtml(str) {
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}
