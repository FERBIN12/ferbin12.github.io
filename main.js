/* Portfolio behaviour. No dependencies.
   - nav: highlight the section in view
   - video: load only near the viewport, play only while visible
   - simulation range: hover (or focus) to play on desktop, in-view on touch; filter chips */

(function () {
  "use strict";
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var canHover = window.matchMedia("(hover: hover) and (pointer: fine)").matches;
  var IO = "IntersectionObserver" in window;

  /* ---------- active nav ---------- */
  var links = $$('.nav nav a[href^="#"]');
  if (IO && links.length) {
    var map = {};
    links.forEach(function (a) { map[a.getAttribute("href").slice(1)] = a; });
    var navObs = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (!e.isIntersecting) return;
        links.forEach(function (a) { a.classList.toggle("on", a === map[e.target.id]); });
      });
    }, { rootMargin: "-45% 0px -50% 0px" });
    Object.keys(map).forEach(function (id) { var t = document.getElementById(id); if (t) navObs.observe(t); });
  }

  /* ---------- video ---------- */
  function load(v) {
    if (v.dataset.loaded) return;
    v.setAttribute("preload", "auto"); v.load(); v.dataset.loaded = "1";
  }
  function play(v) { load(v); var p = v.play(); if (p && p.catch) p.catch(function () {}); }

  var vids = $$("video.lazy");
  if (reduce) { vids.forEach(function (v) { v.removeAttribute("autoplay"); }); }
  else if (!IO) { vids.forEach(function (v) { v.setAttribute("preload", "metadata"); }); }
  else {
    var hoverVids = vids.filter(function (v) { return canHover && v.classList.contains("hover"); });
    var autoVids = vids.filter(function (v) { return hoverVids.indexOf(v) < 0; });

    var obs = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        var v = e.target;
        if (e.isIntersecting && !v.closest("[hidden]")) play(v);
        else if (!v.paused) v.pause();
      });
    }, { rootMargin: "150px 0px", threshold: 0.3 });
    autoVids.forEach(function (v) { obs.observe(v); });

    hoverVids.forEach(function (v) {
      var tile = v.closest(".rtile") || v;
      tile.addEventListener("mouseenter", function () { play(v); });
      tile.addEventListener("mouseleave", function () { v.pause(); });
      tile.addEventListener("focusin", function () { play(v); });
      tile.addEventListener("focusout", function () { v.pause(); });
    });
  }

  /* ---------- simulation range filters ---------- */
  var chips = $$(".fchip");
  var tiles = $$(".rtile");
  chips.forEach(function (c) {
    c.addEventListener("click", function () {
      var f = c.dataset.f;
      chips.forEach(function (x) { x.classList.toggle("on", x === c); x.setAttribute("aria-pressed", x === c ? "true" : "false"); });
      tiles.forEach(function (t) {
        var show = f === "all" || t.dataset.g === f;
        t.hidden = !show;
        var v = t.querySelector("video");
        if (!show && v && !v.paused) v.pause();
      });
    });
  });
})();
