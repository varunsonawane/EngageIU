/* EngageIU — Shared JavaScript. Vanilla JS only, no framework. */

// Auto-detect origin so it works on any host/port
const BASE_URL = window.location.origin;

// ── Auth helpers ──────────────────────────────────────────────────────────────

function getToken() {
  return localStorage.getItem('engageiu_token');
}

function setToken(token) {
  localStorage.setItem('engageiu_token', token);
}

function clearToken() {
  localStorage.removeItem('engageiu_token');
}

function isAdmin() {
  return !!getToken();
}

function authHeaders() {
  const token = getToken();
  const h = { 'Content-Type': 'application/json' };
  if (token) h['Authorization'] = `Bearer ${token}`;
  return h;
}

// ── API fetch wrapper ─────────────────────────────────────────────────────────

async function api(method, path, body = null, requiresAuth = false) {
  const opts = {
    method,
    headers: requiresAuth ? authHeaders() : { 'Content-Type': 'application/json' },
  };
  if (body) opts.body = JSON.stringify(body);
  const res = await fetch(BASE_URL + path, opts);
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: 'Unknown error' }));
    throw new Error(err.detail || `HTTP ${res.status}`);
  }
  return res.json();
}

// ── Date / time helpers ───────────────────────────────────────────────────────

function formatDate(isoStr) {
  if (!isoStr) return '';
  const d = new Date(isoStr);
  return d.toLocaleDateString('en-US', {
    weekday: 'short', month: 'short', day: 'numeric', year: 'numeric'
  });
}

function formatDateTime(isoStr) {
  if (!isoStr) return '';
  const d = new Date(isoStr);
  return d.toLocaleString('en-US', {
    month: 'short', day: 'numeric', hour: 'numeric', minute: '2-digit'
  });
}

// Week label: "Apr 13 – Apr 19, 2025"
function formatWeekRange(startIso, endIso) {
  if (!startIso || !endIso) return '';
  const s = new Date(startIso);
  const e = new Date(endIso);
  const fmt = (d) => d.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
  return `${fmt(s)} – ${fmt(e)}, ${e.getFullYear()}`;
}

// ── Campus list ───────────────────────────────────────────────────────────────

const CAMPUSES = [
  'IU Bloomington',
  'IU Indianapolis',
  'IU East',
  'IU Kokomo',
  'IU Northwest',
  'IU South Bend',
  'IU Southeast',
  'IU Columbus',
  'IU Fort Wayne',
];

function campusOptions(includeAll = true, selectedValue = '') {
  let html = includeAll ? `<option value="">All Campuses</option>` : '';
  CAMPUSES.forEach(c => {
    const sel = c === selectedValue ? 'selected' : '';
    html += `<option value="${c}" ${sel}>${c}</option>`;
  });
  return html;
}

// ── Modal helpers ─────────────────────────────────────────────────────────────

function openModal(id) {
  document.getElementById(id).classList.add('open');
  document.body.style.overflow = 'hidden';
}

function closeModal(id) {
  document.getElementById(id).classList.remove('open');
  document.body.style.overflow = '';
}

// Close modal when clicking the overlay backdrop
document.addEventListener('click', e => {
  if (e.target.classList.contains('modal-overlay')) {
    e.target.classList.remove('open');
    document.body.style.overflow = '';
  }
});

// ── Show alert inside a container ────────────────────────────────────────────

function showAlert(containerId, message, type = 'error') {
  const el = document.getElementById(containerId);
  if (!el) return;
  el.className = `alert alert-${type}`;
  el.textContent = message;
  el.classList.remove('hidden');
}

function hideAlert(containerId) {
  const el = document.getElementById(containerId);
  if (el) el.classList.add('hidden');
}

// ── Admin state ───────────────────────────────────────────────────────────────

function applyAdminState() {
  const adminLinks = document.querySelectorAll('.admin-nav-link');
  if (isAdmin()) {
    document.body.classList.add('admin-logged');
    const loginBtn = document.getElementById('btn-admin-login');
    const logoutBtn = document.getElementById('btn-admin-logout');
    if (loginBtn) loginBtn.classList.add('hidden');
    if (logoutBtn) logoutBtn.classList.remove('hidden');
    adminLinks.forEach(el => el.classList.remove('hidden'));
  } else {
    document.body.classList.remove('admin-logged');
    const loginBtn = document.getElementById('btn-admin-login');
    const logoutBtn = document.getElementById('btn-admin-logout');
    if (loginBtn) loginBtn.classList.remove('hidden');
    if (logoutBtn) logoutBtn.classList.add('hidden');
    adminLinks.forEach(el => el.classList.add('hidden'));
  }
}

// ── Admin login modal (shared across all pages) ────────────────────────────

async function handleAdminLogin(e) {
  e.preventDefault();
  const username = document.getElementById('admin-username').value.trim();
  const password = document.getElementById('admin-password').value;
  hideAlert('admin-login-alert');

  try {
    const data = await api('POST', '/auth/login', { username, password });
    setToken(data.access_token);
    closeModal('admin-login-modal');
    applyAdminState();
    // Reload page to reveal admin UI elements
    window.location.reload();
  } catch (err) {
    showAlert('admin-login-alert', err.message);
  }
}

function handleAdminLogout() {
  clearToken();
  applyAdminState();
  window.location.reload();
}

// ── Rank badge ────────────────────────────────────────────────────────────────

function rankBadge(rank) {
  const classes = rank === 1 ? 'gold' : rank === 2 ? 'silver' : rank === 3 ? 'bronze' : '';
  return `<span class="rank-num ${classes}">${rank}</span>`;
}

// ── Rank number with medal emoji ──────────────────────────────────────────────

function rankLabel(rank) {
  const medals = { 1: '🥇', 2: '🥈', 3: '🥉' };
  return medals[rank] ? `${medals[rank]} ${rank}` : rank;
}

// ── Init shared nav elements once DOM ready ───────────────────────────────────

document.addEventListener('DOMContentLoaded', () => {
  applyAdminState();

  // Admin login form
  const loginForm = document.getElementById('admin-login-form');
  if (loginForm) loginForm.addEventListener('submit', handleAdminLogin);

  // Admin login/logout buttons
  const loginBtn = document.getElementById('btn-admin-login');
  if (loginBtn) loginBtn.addEventListener('click', () => openModal('admin-login-modal'));

  const logoutBtn = document.getElementById('btn-admin-logout');
  if (logoutBtn) logoutBtn.addEventListener('click', handleAdminLogout);

  // Modal close buttons
  document.querySelectorAll('[data-close-modal]').forEach(btn => {
    btn.addEventListener('click', () => closeModal(btn.dataset.closeModal));
  });
});
