/* Olvasónézet: az eredeti szöveg a felolvasással szinkronban, kattintásra onnan szól. */
(() => {
  "use strict";
  const root = document.querySelector("[data-reader]");
  if (!root) return;

  const projectId = root.dataset.project;
  const textEl = document.getElementById("reader-text");
  const listEl = document.getElementById("reader-chapters");
  const audio = document.getElementById("reader-audio");
  const titleEl = document.getElementById("player-title");
  const statusEl = document.getElementById("reader-status");
  const speedEl = document.getElementById("reader-speed");
  const followEl = document.getElementById("reader-follow");
  const toggleBtn = document.querySelector('[data-act="toggle"]');
  const reduceMotion = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const storeKey = `felolvaso.reader.${projectId}`;

  let chapters = [];
  let current = null;       // aktuális fejezet objektum
  let currentSeg = null;    // kiemelt szegmens elem
  let userScrollUntil = 0;  // kézi görgetés után egy ideig nem görget automatikusan
  let pendingSeek = null;

  const store = {
    get() { try { return JSON.parse(localStorage.getItem(storeKey) || "null"); } catch { return null; } },
    set(v) { try { localStorage.setItem(storeKey, JSON.stringify(v)); } catch { /* privát mód */ } },
  };

  function announce(msg) { statusEl.textContent = msg; }

  // --- nézet: a feltöltött eredeti PDF, vagy a forgatókönyv szövege kiemeléssel ---
  const viewBtns = document.querySelectorAll("[data-view]:is(button)");
  const viewKey = "felolvaso.reader.view";
  function setView(view) {
    root.dataset.view = view;
    for (const b of viewBtns) b.setAttribute("aria-pressed", String(b.dataset.view === view));
    try { localStorage.setItem(viewKey, view); } catch { /* privát mód */ }
  }
  if (viewBtns.length) {
    for (const b of viewBtns) b.addEventListener("click", () => setView(b.dataset.view));
    let saved = null;
    try { saved = localStorage.getItem(viewKey); } catch { /* privát mód */ }
    setView(saved === "text" ? "text" : "pdf");
  }

  function fmt(sec) {
    if (sec == null || !isFinite(sec)) return "";
    const s = Math.round(sec), h = Math.floor(s / 3600), m = Math.floor((s % 3600) / 60), r = s % 60;
    return (h ? `${h}:${String(m).padStart(2, "0")}` : `${m}`) + `:${String(r).padStart(2, "0")}`;
  }

  function chapterState(ch) {
    if (!ch.audio) return "még nincs hang";
    if (!ch.synced) return `${fmt(ch.duration)} · szöveg nincs szinkronban`;
    return fmt(ch.duration);
  }

  // --- megjelenítés ---
  function render(data) {
    chapters = data.chapters;
    listEl.innerHTML = "";
    textEl.innerHTML = "";
    for (const ch of chapters) {
      const li = document.createElement("li");
      const btn = document.createElement("button");
      btn.type = "button";
      btn.dataset.ch = ch.index;
      btn.innerHTML = `<span></span><span class="ch-state num"></span>`;
      btn.firstChild.textContent = ch.title;
      btn.lastChild.textContent = chapterState(ch);
      btn.addEventListener("click", () => goChapter(ch, 0, true));
      li.append(btn);
      listEl.append(li);
      ch.btn = btn;

      const sec = document.createElement("section");
      sec.id = `ch-${ch.index}`;
      sec.setAttribute("aria-label", ch.title);
      if (ch.audio && !ch.synced) {
        const note = document.createElement("p");
        note.className = "reader-note";
        note.textContent = "A szöveg az utolsó generálás óta változott, ezért a kiemelés ennél a fejezetnél ki van kapcsolva. Generáld újra a fejezetet.";
        sec.append(note);
      }
      ch.segs = [];
      for (const g of ch.groups) {
        const div = document.createElement("div");
        div.className = "seg" + (ch.audio && ch.synced && g.start != null ? "" : " no-audio");
        div.tabIndex = -1;
        div.innerHTML = g.html;
        div._ch = ch;
        div._g = g;
        sec.append(div);
        ch.segs.push(div);
      }
      ch.section = sec;
      textEl.append(sec);
    }
    textEl.setAttribute("aria-busy", "false");
    renderMath();
  }

  function renderMath() {
    if (!window.katex || !window.renderMathInElement) { setTimeout(renderMath, 100); return; }
    for (const el of textEl.querySelectorAll(".math-display[data-tex]")) {
      try { katex.render(el.dataset.tex, el, { displayMode: true, throwOnError: false }); }
      catch { /* a nyers TeX marad látható */ }
    }
    // szövegközi képletek: $…$, \(…\), $$…$$, \[…\]
    renderMathInElement(textEl, {
      delimiters: [
        { left: "$$", right: "$$", display: true }, { left: "\\[", right: "\\]", display: true },
        { left: "$", right: "$", display: false }, { left: "\\(", right: "\\)", display: false },
      ],
      ignoredClasses: ["math-display"], throwOnError: false,
    });
  }

  // --- lejátszás ---
  function setCurrentChapter(ch) {
    if (current === ch) return;
    current?.btn.removeAttribute("aria-current");
    current = ch;
    ch.btn.setAttribute("aria-current", "true");
    titleEl.textContent = ch.title;
    if (ch.audio_url) {
      audio.src = ch.audio_url;
      audio.playbackRate = Number(speedEl.value);
    } else {
      audio.removeAttribute("src");
      audio.load();
    }
  }

  function goChapter(ch, time, play) {
    if (!ch.audio_url) {
      setCurrentChapter(ch);
      scrollTo(ch.section, true);
      announce("Ennek a fejezetnek még nincs hangja.");
      return;
    }
    const sameSrc = current === ch;
    setCurrentChapter(ch);
    if (sameSrc && audio.readyState > 0) {
      audio.currentTime = time;
    } else {
      pendingSeek = time;
    }
    if (play) audio.play().catch(() => {});
    if (time === 0) scrollTo(ch.section, true);
  }

  function seekSeg(seg) {
    const ch = seg._ch, g = seg._g;
    if (!ch.audio_url) { announce("Ennek a fejezetnek még nincs hangja."); return; }
    if (!ch.synced || g.start == null) { goChapter(ch, 0, true); return; }
    userScrollUntil = 0;
    goChapter(ch, g.start + 0.01, true);
    highlight(seg, false);
  }

  audio.addEventListener("loadedmetadata", () => {
    if (pendingSeek != null) { audio.currentTime = pendingSeek; pendingSeek = null; }
  });

  function findSeg(ch, t) {
    // az utolsó szegmens, amelynek kezdete <= t (bináris keresés)
    const segs = ch.segs.filter((s) => s._g.start != null);
    let lo = 0, hi = segs.length - 1, ans = null;
    while (lo <= hi) {
      const mid = (lo + hi) >> 1;
      if (segs[mid]._g.start <= t) { ans = segs[mid]; lo = mid + 1; } else hi = mid - 1;
    }
    return ans;
  }

  function highlight(seg, autoScroll) {
    if (seg === currentSeg) return;
    currentSeg?.classList.remove("is-current");
    currentSeg = seg;
    if (!seg) return;
    seg.classList.add("is-current");
    if (autoScroll && followEl.checked && Date.now() > userScrollUntil) scrollTo(seg, false);
  }

  function scrollTo(el, top, instant) {
    el.scrollIntoView({ block: top ? "start" : "center", behavior: reduceMotion || instant ? "auto" : "smooth" });
  }

  let raf = 0;
  function tick() {
    raf = 0;
    if (current?.synced) highlight(findSeg(current, audio.currentTime), true);
    if (!audio.paused) raf = requestAnimationFrame(tick);
  }
  audio.addEventListener("play", () => { setToggle(true); if (!raf) raf = requestAnimationFrame(tick); });
  audio.addEventListener("pause", () => { setToggle(false); savePos(); });
  audio.addEventListener("seeked", () => { tick(); savePos(); });
  audio.addEventListener("ended", () => {
    const next = chapters.find((c) => c.index > current.index && c.audio_url);
    if (next) goChapter(next, 0, true);
  });

  function setToggle(playing) {
    const tpl = document.getElementById(playing ? "icon-pause" : "icon-play");
    toggleBtn.replaceChildren(tpl.content.cloneNode(true));
    toggleBtn.setAttribute("aria-label", playing ? "Szünet" : "Lejátszás");
  }

  function savePos() {
    if (current) store.set({ ch: current.index, t: audio.currentTime || 0, speed: speedEl.value });
  }
  setInterval(() => { if (!audio.paused) savePos(); }, 3000);

  function stepSeg(dir) {
    if (!current) { const first = chapters.find((c) => c.audio_url); if (first) goChapter(first, 0, true); return; }
    const segs = current.segs.filter((s) => s._g.start != null);
    if (!current.synced || !segs.length) { audio.currentTime = Math.max(0, audio.currentTime + dir * 10); return; }
    const i = currentSeg ? segs.indexOf(currentSeg) : -1;
    const target = segs[i + dir];
    if (target) seekSeg(target);
    else if (dir > 0) {
      const next = chapters.find((c) => c.index > current.index && c.audio_url);
      if (next) goChapter(next, 0, true);
    } else audio.currentTime = 0;
  }

  // --- vezérlők ---
  toggleBtn.addEventListener("click", () => {
    if (!current) { const first = chapters.find((c) => c.audio_url); if (first) goChapter(first, 0, true); return; }
    if (audio.paused) audio.play().catch(() => {}); else audio.pause();
  });
  document.querySelector('[data-act="prev"]').addEventListener("click", () => stepSeg(-1));
  document.querySelector('[data-act="next"]').addEventListener("click", () => stepSeg(1));
  speedEl.addEventListener("change", () => { audio.playbackRate = Number(speedEl.value); savePos(); });

  textEl.addEventListener("click", (e) => {
    if (window.getSelection()?.toString()) return;  // szövegkijelölés ne indítson lejátszást
    const seg = e.target.closest(".seg");
    if (seg) seekSeg(seg);
  });

  for (const ev of ["wheel", "touchmove"]) {
    addEventListener(ev, () => { userScrollUntil = Date.now() + 5000; }, { passive: true });
  }

  document.addEventListener("keydown", (e) => {
    const t = e.target;
    if (e.ctrlKey || e.metaKey || e.altKey) return;
    if (t.closest("input, select, textarea, audio, [contenteditable]")) return;
    if (e.key === " ") {
      if (t.closest("button")) return;  // a gomb szóközre magától kattint
      e.preventDefault(); toggleBtn.click();
    }
    else if (e.key === "ArrowRight") { e.preventDefault(); stepSeg(1); }
    else if (e.key === "ArrowLeft") { e.preventDefault(); stepSeg(-1); }
  });

  // --- betöltés ---
  fetch(`/api/projects/${projectId}/reader`)
    .then((r) => { if (!r.ok) throw new Error(r.status); return r.json(); })
    .then((data) => {
      render(data);
      const saved = store.get();
      if (saved?.speed) speedEl.value = saved.speed;
      const ch = saved && chapters.find((c) => c.index === saved.ch);
      if (ch) {
        goChapter(ch, saved.t || 0, false);
        const seg = ch.synced ? findSeg(ch, saved.t || 0) : null;
        if (seg) highlight(seg, false);
        // a képletek szedése után, hogy a végleges elrendezésben ugorjon a helyére
        setTimeout(() => scrollTo(seg || ch.section, !seg, true), 300);
        announce(`Folytatás: ${ch.title}`);
      }
    })
    .catch(() => {
      textEl.innerHTML = '<p class="banner banner-error" role="alert">Az olvasó adatait nem sikerült betölteni.</p>';
    });
})();
