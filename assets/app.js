/* Devre Analizi I — Vize Rehberi · etkileşimler */
(function () {
  'use strict';
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => Array.from(r.querySelectorAll(s));
  const store = {
    get(k, d) { try { const v = localStorage.getItem(k); return v === null ? d : JSON.parse(v); } catch (e) { return d; } },
    set(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) { } }
  };

  /* ---------------- math ---------------- */
  function renderMath(root) {
    if (!window.renderMathInElement) return;
    window.renderMathInElement(root || document.body, {
      delimiters: [
        { left: '\\[', right: '\\]', display: true },
        { left: '$$', right: '$$', display: true },
        { left: '\\(', right: '\\)', display: false },
        { left: '$', right: '$', display: false }
      ],
      throwOnError: false,
      ignoredTags: ['script', 'noscript', 'style', 'textarea', 'pre', 'code', 'input']
    });
  }

  /* ---------------- theme ---------------- */
  function setTheme(t) {
    document.documentElement.dataset.theme = t;
    try { localStorage.setItem('da1-theme', t); } catch (e) { }
    const b = $('#themeBtn');
    if (b) b.setAttribute('aria-label', t === 'dark' ? 'Gündüz moduna geç' : 'Gece moduna geç');
  }

  /* ---------------- toast ---------------- */
  let toastTimer;
  function toast(msg, ms = 2600) {
    const el = $('#toast'); if (!el) return;
    el.textContent = msg; el.classList.add('is-show');
    clearTimeout(toastTimer); toastTimer = setTimeout(() => el.classList.remove('is-show'), ms);
  }

  /* ---------------- confetti ---------------- */
  function confetti() {
    const c = $('#confetti'); if (!c) return;
    const ctx = c.getContext('2d');
    const dpr = window.devicePixelRatio || 1;
    c.width = innerWidth * dpr; c.height = innerHeight * dpr; ctx.scale(dpr, dpr);
    const colors = ['#38BDF8', '#10B981', '#F59E0B', '#6366F1', '#F472B6', '#FDE047'];
    const parts = Array.from({ length: 180 }, () => ({
      x: innerWidth / 2 + (Math.random() - .5) * 200, y: innerHeight * .35,
      vx: (Math.random() - .5) * 16, vy: -Math.random() * 14 - 4,
      w: 6 + Math.random() * 6, h: 8 + Math.random() * 8, r: Math.random() * 6.28,
      vr: (Math.random() - .5) * .3, c: colors[(Math.random() * colors.length) | 0]
    }));
    let t = 0;
    (function frame() {
      ctx.clearRect(0, 0, innerWidth, innerHeight);
      parts.forEach(p => {
        p.vy += .35; p.vx *= .99; p.x += p.vx; p.y += p.vy; p.r += p.vr;
        ctx.save(); ctx.translate(p.x, p.y); ctx.rotate(p.r); ctx.fillStyle = p.c;
        ctx.fillRect(-p.w / 2, -p.h / 2, p.w, p.h); ctx.restore();
      });
      if (++t < 220) requestAnimationFrame(frame); else ctx.clearRect(0, 0, innerWidth, innerHeight);
    })();
  }

  /* ---------------- progress (done set) ---------------- */
  const DONE_KEY = 'da1-done-v5';
  let done = new Set(store.get(DONE_KEY, []));
  function allIds() { return $$('.problem').map(p => p.dataset.pid); }

  function paintProgress() {
    const ids = allIds();
    const total = ids.length;
    const n = ids.filter(id => done.has(id)).length;
    $$('.problem').forEach(p => {
      const on = done.has(p.dataset.pid);
      p.classList.toggle('is-done', on);
      $$('[data-done]', p).forEach(b => b.setAttribute('aria-pressed', on ? 'true' : 'false'));
    });
    $$('.side-link[data-pid]').forEach(a => a.classList.toggle('is-done', done.has(a.dataset.pid)));
    // ring
    const fg = $('#ringFg');
    if (fg) {
      const C = 2 * Math.PI * 12;
      fg.style.strokeDasharray = C;
      fg.style.strokeDashoffset = total ? C * (1 - n / total) : C;
    }
    const pct = total ? Math.round(100 * n / total) : 0;
    $$('[data-progress-text]').forEach(el => el.textContent = `%${pct}`);
    $$('[data-progress-count]').forEach(el => el.textContent = `${n}/${total}`);
    // per topic
    [1, 2, 3, 4].forEach(t => {
      const tids = $$(`.problem[data-topic="${t}"]`).map(p => p.dataset.pid);
      const k = tids.filter(id => done.has(id)).length;
      $$(`[data-topic-bar="${t}"]`).forEach(b => b.style.width = tids.length ? (100 * k / tids.length) + '%' : '0');
      $$(`[data-topic-count="${t}"]`).forEach(b => b.textContent = `${k}/${tids.length}`);
    });
    return { n, total };
  }

  function toggleDone(id) {
    const was = done.has(id);
    if (was) done.delete(id); else done.add(id);
    store.set(DONE_KEY, Array.from(done));
    const { n, total } = paintProgress();
    if (!was) {
      if (n === total && total > 0) { confetti(); toast('Hepsi tamam! Vizeye %100 hazırsın. 🎉', 4200); }
      else toast(`Harika — ${n}/${total} soru tamamlandı.`);
    }
  }

  /* ---------------- problem card behaviour ---------------- */
  function setupProblem(card) {
    // figure tabs
    $$('.fig-tabs .seg-btn', card).forEach(btn => btn.addEventListener('click', () => {
      $$('.fig-tabs .seg-btn', card).forEach(b => b.classList.toggle('is-active', b === btn));
      $$('.fig-pane', card).forEach(p => p.hidden = p.dataset.pane !== btn.dataset.fig);
    }));
    // view modes
    const steps = $$('.step', card);
    const stepper = $('.stepper', card);
    let shown = steps.length;
    function paintSteps() {
      steps.forEach((s, i) => {
        const vis = i < shown;
        if (vis && s.hidden) s.classList.add('is-revealed');
        s.hidden = !vis;
      });
      const cnt = $('.stepper-count', card);
      if (cnt) cnt.textContent = `Adım ${Math.min(shown, steps.length)} / ${steps.length}`;
      const next = $('[data-stepper="next"]', card);
      if (next) next.disabled = shown >= steps.length;
    }
    $$('[data-view-btn]', card).forEach(btn => btn.addEventListener('click', () => {
      const mode = btn.dataset.viewBtn;
      $$('[data-view-btn]', card).forEach(b => b.classList.toggle('is-active', b === btn));
      card.dataset.mode = mode;
      const detail = $('[data-view="detail"]', card), exam = $('[data-view="exam"]', card);
      if (mode === 'exam') { detail.hidden = true; if (exam) exam.hidden = false; }
      else {
        detail.hidden = false; if (exam) exam.hidden = true;
        if (mode === 'step') { shown = 1; stepper.hidden = false; }
        else { shown = steps.length; stepper.hidden = true; }
        paintSteps();
      }
    }));
    $$('[data-stepper]', card).forEach(btn => btn.addEventListener('click', () => {
      const a = btn.dataset.stepper;
      if (a === 'next') shown = Math.min(steps.length, shown + 1);
      if (a === 'prev') shown = Math.max(1, shown - 1);
      if (a === 'all') shown = steps.length;
      paintSteps();
      if (a === 'next') steps[shown - 1].scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }));
    $$('[data-done]', card).forEach(btn => btn.addEventListener('click', () => toggleDone(btn.dataset.done)));
  }

  /* ---------------- lightbox ---------------- */
  function openLightbox(src, cap) {
    const ov = $('#lightbox'); if (!ov) return;
    $('#lightboxImg').src = src;
    $('#lightboxCap').textContent = cap || '';
    ov.classList.add('is-open');
  }
  function closeOverlays() { $$('.overlay.is-open').forEach(o => o.classList.remove('is-open')); document.body.style.overflow = ''; }

  /* ---------------- sidebar current + reading progress ---------------- */
  function setupScrollSpy() {
    const links = $$('.side-link[href^="#"]');
    const map = new Map(links.map(a => [a.getAttribute('href').slice(1), a]));
    const targets = Array.from(map.keys()).map(id => document.getElementById(id)).filter(Boolean);
    if (!('IntersectionObserver' in window) || !targets.length) return;
    let current = null;
    const io = new IntersectionObserver(entries => {
      entries.forEach(e => { if (e.isIntersecting) current = e.target.id; });
      if (current) links.forEach(a => a.classList.toggle('is-current', a === map.get(current)));
    }, { rootMargin: '-20% 0px -70% 0px' });
    targets.forEach(t => io.observe(t));
  }
  function setupReadProgress() {
    const bar = $('#readBar'); if (!bar) return;
    const upd = () => {
      const h = document.documentElement;
      const max = h.scrollHeight - h.clientHeight;
      bar.style.width = (max > 0 ? (h.scrollTop / max) * 100 : 0) + '%';
    };
    addEventListener('scroll', upd, { passive: true }); upd();
  }

  /* ---------------- search & level filter & topic order ---------------- */
  let currentLevelFilter = 'all';
  function applyFilters() {
    const input = $('#search');
    const norm = s => s.toLocaleLowerCase('tr').normalize('NFD').replace(/[\u0300-\u036f]/g, '');
    const q = input ? norm(input.value.trim()) : '';
    $$('.problem').forEach(p => {
      const matchQ = !q || norm(p.dataset.search).includes(q);
      const matchLvl = currentLevelFilter === 'all' || p.dataset.level === currentLevelFilter;
      p.classList.toggle('is-hidden', !(matchQ && matchLvl));
    });
    $$('[data-tier-banner]').forEach(b => {
      b.hidden = currentLevelFilter !== 'all' && b.dataset.tierBanner !== currentLevelFilter;
    });
    $$('.side-link[data-pid]').forEach(a => {
      const matchQ = !q || norm(a.dataset.search || '').includes(q);
      const matchLvl = currentLevelFilter === 'all' || a.dataset.level === currentLevelFilter;
      a.hidden = !(matchQ && matchLvl);
    });
  }

  function setupSearch() {
    const input = $('#search');
    if (input) {
      input.addEventListener('input', applyFilters);
      input.addEventListener('keydown', e => {
        if (e.key === 'Enter') { const f = $$('.problem').find(p => !p.classList.contains('is-hidden')); if (f) f.scrollIntoView({ behavior: 'smooth' }); }
        if (e.key === 'Escape') { input.value = ''; applyFilters(); input.blur(); }
      });
      addEventListener('keydown', e => {
        if (e.key === '/' && document.activeElement.tagName !== 'INPUT') { e.preventDefault(); input.focus(); }
      });
    }
    $$('#levelFilter [data-filter-level]').forEach(btn => btn.addEventListener('click', () => {
      currentLevelFilter = btn.dataset.filterLevel;
      $$('#levelFilter [data-filter-level]').forEach(b => b.classList.toggle('is-active', b === btn));
      applyFilters();
    }));
    $$('#orderToggle [data-order]').forEach(btn => btn.addEventListener('click', () => {
      const mode = btn.dataset.order;
      $$('#orderToggle [data-order]').forEach(b => b.classList.toggle('is-active', b === btn));
      const container = $('#topicsContainer');
      const sideContainer = $('#sidebarTopics');
      const key = mode === 'exam' ? 'examOrder' : 'stageOrder';
      if (container) {
        const secs = $$('.topic-section', container).sort((a, b) => (+a.dataset[key]) - (+b.dataset[key]));
        secs.forEach(s => container.appendChild(s));
        let num = 1;
        $$('.problem .pnum', container).forEach(el => { el.textContent = `${num++}.`; });
      }
      if (sideContainer) {
        const grps = $$('[data-side-topic]', sideContainer).sort((a, b) => (+a.dataset[key]) - (+b.dataset[key]));
        grps.forEach(g => sideContainer.appendChild(g));
      }
      toast(mode === 'exam' ? 'Tahtadaki soru sırasına (Soru 1 → 4) geçildi.' : 'Kolaydan zora önerilen öğrenme sırasına geçildi.');
    }));
  }

  /* ---------------- mock exams ---------------- */
  function setupMock() {
    const root = $('#mock'); if (!root || !window.MOCKS) return;
    const tabs = $('#mockTabs'), shell = $('#mockShell');
    let timer = null, left = 0, cur = 0;
    function fmt(s) { const m = Math.floor(s / 60), r = s % 60; return `${String(m).padStart(2, '0')}:${String(r).padStart(2, '0')}`; }
    function stop() { clearInterval(timer); timer = null; }
    function load(i) {
      stop(); cur = i; left = 90 * 60;
      tabs.querySelectorAll('.seg-btn').forEach((b, k) => b.classList.toggle('is-active', k === i));
      const m = window.MOCKS[i];
      const qs = m.items.map((id, k) => {
        const src = document.getElementById(id);
        if (!src) return '';
        const code = src.querySelector('.pcode').textContent;
        const title = src.querySelector('.problem-title').innerHTML.replace(/<span class="pnum">.*?<\/span>/, '');
        const q = src.querySelector('.question > div').innerHTML;
        const img = src.querySelector('.fig-pane[data-pane="orig"] img');
        const ans = src.querySelector('.answer-chips');
        return `<div class="mock-q">
          <div class="mock-q-head"><span class="pcode">${code}</span><strong>Soru ${k + 1}</strong><span class="pts">25 puan</span></div>
          <div class="mock-q-title" style="font-weight:650;margin-bottom:6px">${title}</div>
          ${img ? `<img class="zoomable" src="${img.getAttribute('src')}" alt="${code}">` : ''}
          <div>${q}</div>
          <div class="mock-sol" hidden><div class="answer"><div class="answer-label">Cevap</div>${ans ? ans.outerHTML : ''}</div>
            <p style="margin:10px 0 0;font-size:.9rem"><a href="#${id}">Tam çözüme git →</a></p></div>
          <div class="mock-grade"><button class="btn btn-ghost" data-reveal>Cevabı göster</button>
            <label>Kendi puanın: <input type="number" min="0" max="25" step="1" data-score placeholder="0–25"></label></div>
        </div>`;
      }).join('');
      shell.innerHTML = `<div class="mock-top"><div><div class="mock-title">${m.title}</div><div style="font-size:.85rem;color:var(--muted)">${m.desc}</div></div>
        <div style="display:flex;gap:8px;align-items:center"><span class="timer" id="timer">${fmt(left)}</span>
        <button class="btn btn-primary" id="timerBtn">Süreyi başlat</button></div></div>${qs}
        <div class="mock-score"><span>Toplam (kendi değerlendirmen)</span><b id="mockTotal">0 / 100</b></div>`;
      $('#timerBtn').addEventListener('click', e => {
        if (timer) { stop(); e.target.textContent = 'Devam et'; return; }
        e.target.textContent = 'Duraklat';
        timer = setInterval(() => {
          left = Math.max(0, left - 1);
          const t = $('#timer'); t.textContent = fmt(left); t.classList.toggle('is-low', left < 600);
          if (!left) { stop(); toast('Süre doldu! Kalemleri bırak. ⏰', 4000); }
        }, 1000);
      });
      $$('[data-reveal]', shell).forEach(b => b.addEventListener('click', () => {
        const sol = b.closest('.mock-q').querySelector('.mock-sol'); sol.hidden = !sol.hidden;
        b.textContent = sol.hidden ? 'Cevabı göster' : 'Cevabı gizle';
      }));
      $$('[data-score]', shell).forEach(inp => inp.addEventListener('input', () => {
        const s = $$('[data-score]', shell).reduce((a, x) => a + Math.max(0, Math.min(25, +x.value || 0)), 0);
        $('#mockTotal').textContent = `${s} / 100`;
      }));
      renderMath(shell);
    }
    tabs.innerHTML = window.MOCKS.map((m, i) => `<button class="seg-btn" data-i="${i}">Deneme ${i + 1}</button>`).join('');
    tabs.querySelectorAll('.seg-btn').forEach(b => b.addEventListener('click', () => load(+b.dataset.i)));
    load(0);
  }

  /* ---------------- init ---------------- */
  function init() {
    renderMath(document.body);
    $$('.problem').forEach(setupProblem);
    paintProgress();
    setupScrollSpy(); setupReadProgress(); setupSearch(); setupMock();

    const tb = $('#themeBtn');
    if (tb) tb.addEventListener('click', () => setTheme(document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark'));

    const cs = $('#cheatBtn');
    if (cs) cs.addEventListener('click', () => { $('#cheat').classList.add('is-open'); document.body.style.overflow = 'hidden'; });
    $$('[data-close]').forEach(b => b.addEventListener('click', closeOverlays));
    $$('.overlay').forEach(o => o.addEventListener('click', e => { if (e.target === o || e.target.closest('[data-lb-close]')) closeOverlays(); }));
    addEventListener('keydown', e => { if (e.key === 'Escape') closeOverlays(); });

    document.addEventListener('click', e => {
      const img = e.target.closest('img.zoomable');
      if (img) { const cap = img.closest('figure')?.querySelector('figcaption')?.textContent || img.alt; openLightbox(img.src, cap); }
    });

    const mb = $('#menuBtn');
    if (mb) mb.addEventListener('click', () => document.body.classList.toggle('nav-open'));
    $$('.sidebar a').forEach(a => a.addEventListener('click', () => document.body.classList.remove('nav-open')));

    const reset = $('#resetProgress');
    if (reset) reset.addEventListener('click', () => { if (confirm('İlerlemeyi sıfırlamak istiyor musun?')) { done = new Set(); store.set(DONE_KEY, []); paintProgress(); } });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
