/* Lazy, in-view sim clips. No dependencies, no theme toggle:
   the page is one dark surface now, so there is nothing to switch. */

(function () {
  "use strict";

  /* ---------- active nav ---------- */

  var links = Array.prototype.slice.call(document.querySelectorAll('.nav nav a[href^="#"]'));
  var targets = links
    .map(function (a) { return document.getElementById(a.getAttribute("href").slice(1)); })
    .filter(Boolean);

  if (targets.length && "IntersectionObserver" in window) {
    var navObs = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (!e.isIntersecting) return;
        links.forEach(function (a) {
          var on = a.getAttribute("href") === "#" + e.target.id;
          a.style.color = on ? "var(--ink)" : "";
          a.style.borderBottomColor = on ? "var(--ink)" : "";
        });
      });
    }, { rootMargin: "-45% 0px -50% 0px" });
    targets.forEach(function (t) { navObs.observe(t); });
  }

  /* ---------- lazy video ----------
     Clips load only when scrolled near, and stay paused entirely
     when the visitor has asked for reduced motion. */

  var videos = Array.prototype.slice.call(
    document.querySelectorAll(".morph-media video, .proj-media video"));
  if (!videos.length) return;
  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;

  if (!("IntersectionObserver" in window)) {
    videos.forEach(function (v) { v.setAttribute("preload", "metadata"); });
    return;
  }

  var vidObs = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      var v = entry.target;
      if (entry.isIntersecting) {
        if (!v.dataset.loaded) {
          v.setAttribute("preload", "auto");
          v.load();
          v.dataset.loaded = "1";
        }
        var p = v.play();
        if (p && p.catch) p.catch(function () { /* autoplay blocked, poster stands */ });
      } else if (!v.paused) {
        v.pause();
      }
    });
  }, { rootMargin: "200px 0px", threshold: 0.25 });

  videos.forEach(function (v) { vidObs.observe(v); });
})();
