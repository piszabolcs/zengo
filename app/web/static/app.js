// Felolvasó felület: a htmx által nem lefedett, kis kliensoldali viselkedések.
"use strict";

(() => {
  const $ = (sel, root = document) => root.querySelector(sel);

  // --- téma: tábla (alapértelmezés) vagy papír ---
  const themeBtn = $("[data-theme-toggle]");
  if (themeBtn) {
    const sync = () => {
      const light = document.documentElement.dataset.theme === "light";
      themeBtn.setAttribute("aria-pressed", String(light));
      themeBtn.textContent = light ? "Tábla téma" : "Papír téma";
    };
    themeBtn.addEventListener("click", () => {
      const light = document.documentElement.dataset.theme !== "light";
      if (light) document.documentElement.dataset.theme = "light";
      else delete document.documentElement.dataset.theme;
      try { localStorage.setItem("felolvaso.theme", light ? "light" : "dark"); } catch { /* privát mód */ }
      sync();
    });
    sync();
  }

  // --- kapcsolat és hibák (9.8) ---
  const connLost = $("#conn-lost");
  document.addEventListener("htmx:sendError", () => { if (connLost) connLost.hidden = false; });
  document.addEventListener("htmx:afterRequest", (e) => {
    if (e.detail.successful && connLost) connLost.hidden = true;
  });
  document.addEventListener("htmx:responseError", (e) => {
    const target = e.detail.target;
    if (!target) return;
    const p = document.createElement("p");
    p.className = "banner banner-error";
    p.setAttribute("role", "alert");
    p.textContent = `Hiba (${e.detail.xhr.status}): ${e.detail.xhr.responseText.slice(0, 300)}`;
    target.replaceChildren(p);
  });

  // --- hang lejátszása egy POST/GET válaszból ---
  async function playFrom(url, audio, statusEl, body) {
    if (statusEl) statusEl.textContent = "Generálás…";
    try {
      const opts = body === undefined ? {} : {
        method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body),
      };
      const resp = await fetch(url, opts);
      if (!resp.ok) {
        let msg = resp.statusText;
        try { msg = (await resp.json()).detail || msg; } catch { /* nem JSON */ }
        throw new Error(msg);
      }
      const blob = await resp.blob();
      if (audio.dataset.url) URL.revokeObjectURL(audio.dataset.url);
      audio.dataset.url = URL.createObjectURL(blob);
      audio.src = audio.dataset.url;
      audio.hidden = false;
      await audio.play().catch(() => {});
      if (statusEl) statusEl.textContent = "Lejátszás.";
    } catch (err) {
      if (statusEl) statusEl.textContent = `Nem sikerült: ${err.message}`;
      else alert(`Nem sikerült: ${err.message}`);
    }
  }

  let sharedAudio;
  function audioEl() {
    if (!sharedAudio) { sharedAudio = new Audio(); }
    return sharedAudio;
  }

  document.addEventListener("click", (e) => {
    const play = e.target.closest("[data-play]");
    if (play) {
      const a = audioEl();
      a.src = play.dataset.play;
      a.play().catch((err) => alert(`Nem játszható le: ${err.message}`));
      return;
    }
    const test = e.target.closest("[data-voice-test]");
    if (test) {
      playFrom(`/api/voices/${encodeURIComponent(test.dataset.voiceTest)}/test`, $("#voice-audio"), $("#voice-status"), {});
      return;
    }
    const say = e.target.closest("[data-say]");
    if (say) {
      const voice = $("#l-voice")?.value;
      playFrom(`/api/voices/${encodeURIComponent(voice)}/test`, $("#voice-audio"), $("#voice-status"),
        { text: say.dataset.say });
    }
  });

  // --- aláírás: alkalmazásinfó ablak (Esc és a háttérre kattintás bezárja) ---
  const info = $("#app-info");
  if (info) {
    $("[data-signature]")?.addEventListener("click", () => info.showModal());
    $("[data-signature-close]", info)?.addEventListener("click", () => info.close());
    info.addEventListener("click", (e) => { if (e.target === info) info.close(); });
  }

  // --- fájl behúzás (9.1, 9.2): eredeti jegyzet és forgatókönyv, külön mezőben ---
  document.querySelectorAll("[data-dropzone]").forEach((drop) => {
    const input = $("[data-file-input]", drop);
    const name = $("[data-file-name]", drop);
    const show = () => { name.textContent = input.files[0] ? input.files[0].name : ""; };
    input.addEventListener("change", show);
    ["dragenter", "dragover"].forEach((t) => drop.addEventListener(t, (e) => {
      e.preventDefault(); drop.classList.add("is-over");
    }));
    ["dragleave", "drop"].forEach((t) => drop.addEventListener(t, () => drop.classList.remove("is-over")));
    drop.addEventListener("drop", (e) => {
      e.preventDefault();
      if (!e.dataTransfer.files.length) return;
      input.files = e.dataTransfer.files;
      show();
    });
  });

  // --- szerkesztő (9.3) ---
  const editor = $("[data-editor]");
  if (!editor) return;
  const ta = $("[data-script]");
  const gutter = $("#gutter");
  const status = $("#editor-status");
  const pos = $("#cursor-pos");
  const projectId = editor.dataset.project;
  let dirty = false;

  function renderGutter() {
    const n = ta.value.split("\n").length;
    let out = "";
    for (let i = 1; i <= n; i++) out += i + "\n";
    gutter.textContent = out;
    gutter.scrollTop = ta.scrollTop;
  }
  function currentLine() {
    return ta.value.slice(0, ta.selectionStart).split("\n").length;
  }
  function updatePos() { pos.textContent = `${currentLine()}. sor`; }

  function gotoLine(line) {
    const lines = ta.value.split("\n");
    const target = Math.max(1, Math.min(line, lines.length));
    let offset = 0;
    for (let i = 0; i < target - 1; i++) offset += lines[i].length + 1;
    ta.focus();
    ta.setSelectionRange(offset, offset + lines[target - 1].length);
    const lineHeight = parseFloat(getComputedStyle(ta).lineHeight) || 20;
    ta.scrollTop = Math.max(0, (target - 4) * lineHeight);
    updatePos();
  }

  // a kurzor alatti blokk: üres sorokkal határolt bekezdés vagy cím
  function currentBlock() {
    const lines = ta.value.split("\n");
    let i = currentLine() - 1;
    if (!lines[i] || !lines[i].trim()) return "";
    if (/^#{1,3}\s/.test(lines[i])) return lines[i].replace(/^#+\s*/, "");
    let start = i, end = i;
    while (start > 0 && lines[start - 1].trim() && !/^#{1,3}\s/.test(lines[start - 1])) start--;
    while (end < lines.length - 1 && lines[end + 1].trim() && !/^#{1,3}\s/.test(lines[end + 1])) end++;
    return lines.slice(start, end + 1).join("\n");
  }

  async function preview() {
    const text = currentBlock();
    if (!text || text.trim() === "---") { status.textContent = "Állj egy bekezdésre vagy címre az előhallgatáshoz."; return; }
    await playFrom(`/api/projects/${projectId}/preview`, $("#preview-audio"), status, { text });
  }

  ta.addEventListener("input", () => { renderGutter(); dirty = true; status.textContent = "Nem mentett módosítás."; });
  ta.addEventListener("scroll", () => { gutter.scrollTop = ta.scrollTop; });
  ta.addEventListener("keyup", updatePos);
  ta.addEventListener("click", updatePos);
  ta.addEventListener("keydown", (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "s") { e.preventDefault(); $("#script-form").requestSubmit(); }
    if ((e.ctrlKey || e.metaKey) && e.key === "Enter") { e.preventDefault(); preview(); }
    if (e.key === "Tab" && !e.shiftKey && !e.ctrlKey) {
      // a Tab elhagyja a mezőt (billentyűzetes bejárhatóság), behúzás nincs a formátumban
    }
  });
  $("[data-preview]").addEventListener("click", preview);
  editor.addEventListener("click", (e) => {
    const btn = e.target.closest("[data-goto-line]");
    if (btn) gotoLine(parseInt(btn.dataset.gotoLine, 10));
  });
  document.addEventListener("htmx:afterSwap", (e) => {
    if (e.detail.target.id === "issues") { dirty = false; status.textContent = ""; }
  });
  window.addEventListener("beforeunload", (e) => { if (dirty) { e.preventDefault(); e.returnValue = ""; } });
  renderGutter();
  updatePos();
})();
