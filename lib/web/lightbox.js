// Click-to-enlarge for pictures: Lightbox.attach(selector) opens any matching <img> in a
// full-window viewer with its alt text as the caption. Arrow keys / buttons step through the
// other matches on the page, Esc or a click on the backdrop closes it.
(function () {
  const dlg = document.createElement("dialog");
  dlg.className = "lightbox";
  dlg.innerHTML = `<figure><img alt=""><figcaption></figcaption></figure>
    <button class="lb-close" aria-label="Close">×</button>
    <button class="lb-prev" aria-label="Previous picture">‹</button>
    <button class="lb-next" aria-label="Next picture">›</button>`;
  const img = dlg.querySelector("img"), cap = dlg.querySelector("figcaption");
  let list = [], i = 0;

  function show(k) {
    i = (k + list.length) % list.length;
    img.src = list[i].currentSrc || list[i].src;
    img.alt = cap.textContent = list[i].alt || "";
    dlg.querySelector(".lb-prev").hidden = dlg.querySelector(".lb-next").hidden = list.length < 2;
  }
  dlg.querySelector(".lb-close").addEventListener("click", () => dlg.close());
  dlg.querySelector(".lb-prev").addEventListener("click", () => show(i - 1));
  dlg.querySelector(".lb-next").addEventListener("click", () => show(i + 1));
  dlg.addEventListener("click", (e) => { if (e.target === dlg) dlg.close(); });
  dlg.addEventListener("keydown", (e) => {
    if (e.key === "ArrowLeft") show(i - 1);
    if (e.key === "ArrowRight") show(i + 1);
  });

  window.Lightbox = {
    attach(selector) {
      if (!dlg.isConnected) document.body.appendChild(dlg);
      document.addEventListener("click", (e) => {
        const t = e.target.closest(selector);
        if (!t) return;
        list = [...document.querySelectorAll(selector)].filter((x) => x.offsetParent);
        show(list.indexOf(t));
        dlg.showModal();
      });
    },
  };
})();
