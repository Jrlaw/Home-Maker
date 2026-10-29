// Whole-house map: every room of a house, floor by floor, from houses/<house>/web/house.js
// (built by lib/tools/house_map.py from house_layout.py). Two views of the same rooms:
//   Plan: top-down outlines with names and sizes; the listing plan can be shown underneath
//         to check the tracing.
//   3D:   a dollhouse with both floors stacked; drag to orbit, scroll to zoom, click a room.
// Modeled rooms link to their walkthrough; the rest are placeholders until they're started.
// Select a room by clicking it, from the list, or with #<room-id> in the address; add ?3d to
// open on the dollhouse, ?underlay to start with the listing plan showing.
(function () {
  const H = window.HOUSE;
  const NS = "http://www.w3.org/2000/svg";
  const $ = (id) => document.getElementById(id);
  const el = (tag, attrs, parent, ns) => {
    const e = ns ? document.createElementNS(NS, tag) : document.createElement(tag);
    for (const k in attrs || {}) e.setAttribute(k, attrs[k]);
    if (parent) parent.appendChild(e);
    return e;
  };
  const byId = Object.fromEntries(H.rooms.map((r) => [r.id, r]));
  const floorOf = Object.fromEntries(H.floors.map((f) => [f.id, f]));
  const ftin = (inches) => {
    const i = Math.round(inches);
    return `${Math.floor(i / 12)}'${i % 12}"`;
  };
  const bbox = (pts) => {
    const xs = pts.map((p) => p[0]), ys = pts.map((p) => p[1]);
    return { x0: Math.min(...xs), x1: Math.max(...xs), y0: Math.min(...ys), y1: Math.max(...ys) };
  };
  // label spot: the bbox center, or the centroid of the largest rectangle-ish part for odd shapes
  const center = (pts) => {
    const b = bbox(pts);
    let cx = (b.x0 + b.x1) / 2, cy = (b.y0 + b.y1) / 2;
    if (!inside(pts, cx, cy)) { cx = pts.reduce((s, p) => s + p[0], 0) / pts.length; cy = pts.reduce((s, p) => s + p[1], 0) / pts.length; }
    return [cx, cy];
  };
  const inside = (pts, x, y) => {
    let c = false;
    for (let i = 0, j = pts.length - 1; i < pts.length; j = i++) {
      const [xi, yi] = pts[i], [xj, yj] = pts[j];
      if ((yi > y) !== (yj > y) && x < ((xj - xi) * (y - yi)) / (yj - yi) + xi) c = !c;
    }
    return c;
  };
  const statusClass = (r) => (r.folder ? "modeled" : r.kind);

  let floor = "1st", selected = null, view = "plan";
  const listeners = [];

  // ---------------------------------------------------------------- plan view
  const all = H.rooms.flatMap((r) => r.outline);
  const B = bbox(all), pad = 30;
  const svg = el("svg", {
    viewBox: `${B.x0 - pad} ${-B.y1 - pad} ${B.x1 - B.x0 + 2 * pad} ${B.y1 - B.y0 + 2 * pad}`,
    role: "img", "aria-label": "Floor plan of the house",
  }, $("plan"), true);
  const defs = el("defs", {}, svg, true);
  const hatch = el("pattern", { id: "stairs-hatch", width: 10, height: 10, patternUnits: "userSpaceOnUse" }, defs, true);
  el("path", { d: "M0 0 V10", class: "hatch" }, hatch, true);
  const underlay = el("g", { class: "underlay" }, svg, true);
  const layers = {};
  H.floors.forEach((f) => {
    const p = H.plans[f.id];
    const g = el("g", { class: "plan-image", "data-floor": f.id }, underlay, true);
    if (p) el("image", { href: p.href, x: p.x, y: p.y, width: p.w, height: p.h, preserveAspectRatio: "none" }, g, true);
    layers[f.id] = el("g", { class: "floor", "data-floor": f.id }, svg, true);
  });
  const shapes = {};
  H.rooms.forEach((r) => {
    const g = el("g", { class: `room ${statusClass(r)}`, tabindex: 0, role: "button", "aria-label": r.name }, layers[r.floor], true);
    el("polygon", { points: r.outline.map(([x, y]) => `${x},${-y}`).join(" ") }, g, true);
    const b = bbox(r.outline), [cx, cy] = center(r.outline);
    const w = b.x1 - b.x0, h = b.y1 - b.y0;
    // as big as fits: the name's width is ~0.58 em per letter. Closets too small to fit
    // their name go unlabeled (they're in the list).
    const fit = Math.min(13, h / 3.2, (w * 0.92) / (0.58 * r.name.length));
    if (r.kind === "room" || fit >= 6) {
      const size = Math.max(6, fit);
      const t = el("text", { x: cx, y: -cy, class: "name", "font-size": size }, g, true);
      t.textContent = r.name;
      if (r.listed && r.kind === "room" && h > 50) {
        const s = el("text", { x: cx, y: -cy + size * 1.3, class: "size", "font-size": size * 0.8 }, g, true);
        s.textContent = r.listed;
      }
    }
    g.addEventListener("click", () => select(r.id));
    g.addEventListener("keydown", (e) => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); select(r.id); } });
    shapes[r.id] = g;
  });
  $("show-plan").addEventListener("change", (e) => svg.classList.toggle("with-plan", e.target.checked));

  // ---------------------------------------------------------------- side panel
  function renderList() {
    const list = $("room-list");
    list.innerHTML = "";
    H.floors.forEach((f) => {
      const rooms = H.rooms.filter((r) => r.floor === f.id);
      const sqft = rooms.filter((r) => r.kind !== "feature").reduce((s, r) => s + r.area, 0);
      const sec = el("section", {}, list);
      el("p", { class: "eyebrow" }, sec).textContent = `${f.name} · ${rooms.length} spaces · ~${sqft.toLocaleString()} sq ft`;
      const ul = el("ul", {}, sec);
      rooms.forEach((r) => {
        const li = el("li", {}, ul);
        const b = el("button", { "data-room": r.id }, li);
        el("span", { class: `dot ${statusClass(r)}` }, b);
        el("span", {}, b).textContent = r.name;
        b.addEventListener("click", () => select(r.id));
      });
    });
  }

  function renderDetail() {
    const d = $("detail");
    d.innerHTML = "";
    const modeled = H.rooms.filter((r) => r.folder).length;
    if (!selected) {
      el("p", { class: "eyebrow" }, d).textContent = "Whole house";
      el("h2", {}, d).textContent = `${H.rooms.length} spaces on ${H.floors.length} floors`;
      el("p", { class: "muted" }, d).textContent =
        `${modeled} modeled, the rest placeholders traced from the listing plan. Pick a room to see its size and what's next for it.`;
      return;
    }
    const r = byId[selected], b = bbox(r.outline);
    el("p", { class: "eyebrow" }, d).textContent = `${floorOf[r.floor].name} · ${r.kind === "room" ? "room" : r.kind}`;
    el("h2", {}, d).textContent = r.name;
    const chip = el("span", { class: `chip ${r.folder ? "on" : ""}` }, d);
    chip.textContent = r.folder ? r.status : "Placeholder";
    const dl = el("dl", {}, d);
    const row = (k, v) => { el("dt", {}, dl).textContent = k; el("dd", {}, dl).textContent = v; };
    if (r.listed) row("Listed size", r.listed);
    row("Traced", `${ftin(b.x1 - b.x0)} E–W × ${ftin(b.y1 - b.y0)} N–S`);
    row("Floor area", `~${r.area} sq ft`);
    row("Source", r.source);
    if (r.note) el("p", {}, d).textContent = r.note;
    if (r.links.length) {
      const nav = el("nav", { class: "links" }, d);
      r.links.forEach(([label, href]) => { const a = el("a", { href }, nav); a.textContent = label; });
    } else {
      const p = el("p", { class: "muted" }, d);
      p.append("Not modeled yet. To start it, say ");
      el("code", {}, p).textContent = `new room: ours, ${r.id}`;
      p.append(" in Claude Code.");
    }
    if (r.seen_in && byId[r.seen_in]) {
      const s = byId[r.seen_in];
      const p = el("p", { class: "muted" }, d);
      p.append("Shows up as a stand-in in the ");
      const a = el("a", { href: s.links[0] ? s.links[0][1] : "#" + s.id }, p);
      a.textContent = s.name.toLowerCase();
      p.append(" model.");
    }
    if (r.to && byId[r.to]) {
      const t = byId[r.to];
      const btn = el("button", { class: "go" }, d);
      btn.textContent = `Go to ${floorOf[t.floor].name.toLowerCase()} →`;
      btn.addEventListener("click", () => select(t.id));
    }
  }

  function select(id, fromHash) {
    selected = id && byId[id] ? id : null;
    if (selected) setFloor(byId[selected].floor);
    Object.entries(shapes).forEach(([k, g]) => g.classList.toggle("sel", k === selected));
    document.querySelectorAll("#room-list button").forEach((b) => b.setAttribute("aria-pressed", b.dataset.room === selected));
    renderDetail();
    listeners.forEach((f) => f());
    if (!fromHash) history.replaceState(null, "", selected ? "#" + selected : location.pathname + location.search);
  }

  function setFloor(f) {
    floor = f;
    document.querySelectorAll("#floors button").forEach((b) => b.setAttribute("aria-pressed", b.dataset.floor === f));
    svg.querySelectorAll("[data-floor]").forEach((g) => g.classList.toggle("hidden", g.dataset.floor !== f));
    listeners.forEach((fn) => fn());
  }

  // floor buttons (plan: one floor at a time; 3D: adds "Both")
  const floorsEl = $("floors");
  [...H.floors.map((f) => [f.id, f.name]), ["all", "Both"]].forEach(([id, name]) => {
    const b = el("button", { "data-floor": id, "aria-pressed": "false" }, floorsEl);
    b.textContent = name;
    b.addEventListener("click", () => setFloor(id));
  });

  // tabs
  document.querySelectorAll(".tabs button").forEach((b) => b.addEventListener("click", () => {
    view = b.dataset.tab;
    document.querySelectorAll(".tabs button").forEach((x) => x.setAttribute("aria-selected", x === b));
    $("plan").hidden = view !== "plan";
    $("dollhouse").hidden = view !== "3d";
    $("plan-tools").hidden = view !== "plan";
    document.body.dataset.view = view;
    if (view === "plan" && floor === "all") setFloor("1st");
    if (view === "3d") start3d();
    listeners.forEach((fn) => fn());
  }));

  // ---------------------------------------------------------------- 3D dollhouse
  let started = false;
  async function start3d() {
    if (started) return;
    started = true;
    const THREE = await import("three");
    const { OrbitControls } = await import("three/addons/controls/OrbitControls.js");
    const { CSS2DRenderer, CSS2DObject } = await import("three/addons/renderers/CSS2DRenderer.js");
    const box = $("dollhouse");
    const css = getComputedStyle(document.documentElement);
    const col = (v) => new THREE.Color(css.getPropertyValue(v).trim() || "#888");

    const renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
    box.appendChild(renderer.domElement);
    const labels = new CSS2DRenderer();
    labels.domElement.className = "labels";
    box.appendChild(labels.domElement);
    const scene = new THREE.Scene();
    scene.background = col("--chip");
    const camera = new THREE.PerspectiveCamera(40, 1, 10, 20000);
    const controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.maxPolarAngle = Math.PI * 0.49;
    scene.add(new THREE.HemisphereLight(0xffffff, 0x8a7f74, 2.2));
    const sun = new THREE.DirectionalLight(0xffffff, 1.6);
    sun.position.set(-400, 900, 600);
    scene.add(sun);

    // plan (x east, y north) -> three (x, y up, z south)
    const mats = {
      modeled: new THREE.MeshStandardMaterial({ color: col("--oak") }),
      room: new THREE.MeshStandardMaterial({ color: 0xd9d2c5 }),
      closet: new THREE.MeshStandardMaterial({ color: 0xc4bcae }),
      stairs: new THREE.MeshStandardMaterial({ color: 0x9c9284 }),
      feature: new THREE.MeshStandardMaterial({ color: 0x8b8178 }),
      sel: new THREE.MeshStandardMaterial({ color: col("--oak"), emissive: col("--oak"), emissiveIntensity: 0.35 }),
      wall: new THREE.MeshStandardMaterial({ color: 0xf4f0e8 }),
    };
    const WALL_H = 36;            // cut-away height, so you can see into the rooms
    const groups = {}, floorMeshes = {}, labelsOf = {};
    H.floors.forEach((f) => { groups[f.id] = new THREE.Group(); scene.add(groups[f.id]); labelsOf[f.id] = []; });
    H.rooms.forEach((r) => {
      const f = floorOf[r.floor], g = groups[r.floor];
      const shape = new THREE.Shape(r.outline.map(([x, y]) => new THREE.Vector2(x, y)));
      const geo = new THREE.ShapeGeometry(shape);
      geo.rotateX(-Math.PI / 2);     // shape y (north) -> -z
      const m = new THREE.Mesh(geo, mats[statusClass(r)]);
      m.position.y = f.z + 0.5;
      m.userData.room = r.id;
      g.add(m);
      floorMeshes[r.id] = m;
      const h = r.kind === "feature" ? f.ceiling * 0.6 : WALL_H;
      const n = r.outline.length;
      for (let i = 0; i < n; i++) {
        const [x0, y0] = r.outline[i], [x1, y1] = r.outline[(i + 1) % n];
        const len = Math.hypot(x1 - x0, y1 - y0);
        const w = new THREE.Mesh(new THREE.BoxGeometry(len + H.wall, h, H.wall), mats.wall);
        w.position.set((x0 + x1) / 2, f.z + h / 2, -(y0 + y1) / 2);
        w.rotation.y = Math.atan2(y1 - y0, x1 - x0);
        w.userData.room = r.id;
        g.add(w);
      }
      if (r.kind === "room" || r.kind === "stairs") {
        const div = el("div", { class: "label" });
        div.textContent = r.name;
        div.addEventListener("click", () => select(r.id));
        const [cx, cy] = center(r.outline);
        const lab = new CSS2DObject(div);
        lab.position.set(cx, f.z + WALL_H + 6, -cy);
        g.add(lab);
        labelsOf[r.floor].push(lab);
      }
    });

    const C = new THREE.Vector3((B.x0 + B.x1) / 2, -60, -(B.y0 + B.y1) / 2);
    camera.position.set(C.x - 120, 620, C.z + 560);
    controls.target.copy(C);

    function update() {
      // CSS2D labels don't inherit their group's visibility, so hide them too
      H.floors.forEach((f) => {
        const on = floor === "all" || floor === f.id;
        groups[f.id].visible = on;
        labelsOf[f.id].forEach((l) => { l.visible = on; });
      });
      Object.entries(floorMeshes).forEach(([id, m]) => {
        m.material = id === selected ? mats.sel : mats[statusClass(byId[id])];
      });
      // keep the active floor centered vertically
      const y = floor === "all" ? -60 : floorOf[floor].z;
      controls.target.y = y;
    }
    listeners.push(update);
    update();

    // click a room (ignore drags)
    const ray = new THREE.Raycaster(), ptr = new THREE.Vector2();
    let down = null;
    renderer.domElement.addEventListener("pointerdown", (e) => { down = [e.clientX, e.clientY]; });
    renderer.domElement.addEventListener("pointerup", (e) => {
      if (!down || Math.hypot(e.clientX - down[0], e.clientY - down[1]) > 5) return;
      const r = renderer.domElement.getBoundingClientRect();
      ptr.set(((e.clientX - r.left) / r.width) * 2 - 1, -((e.clientY - r.top) / r.height) * 2 + 1);
      ray.setFromCamera(ptr, camera);
      const hit = ray.intersectObjects(scene.children, true).find((h) => h.object.userData.room && h.object.parent.visible);
      if (hit) select(hit.object.userData.room);
    });

    function resize() {
      const w = box.clientWidth, h = box.clientHeight;
      renderer.setSize(w, h);
      labels.setSize(w, h);
      camera.aspect = w / h;
      camera.updateProjectionMatrix();
    }
    new ResizeObserver(resize).observe(box);
    resize();
    renderer.setAnimationLoop(() => {
      controls.update();
      renderer.render(scene, camera);
      labels.render(scene, camera);
    });
  }

  // ---------------------------------------------------------------- start
  renderList();
  setFloor("1st");
  select(decodeURIComponent(location.hash.slice(1)), true);
  addEventListener("hashchange", () => select(decodeURIComponent(location.hash.slice(1)), true));
  if (new URLSearchParams(location.search).has("underlay")) { $("show-plan").checked = true; svg.classList.add("with-plan"); }
  if (new URLSearchParams(location.search).has("3d")) document.querySelector('.tabs [data-tab="3d"]').click();
})();
