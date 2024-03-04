function _e() {
}
function mt(n, t) {
  return n != n ? t == t : n !== t || n && typeof n == "object" || typeof n == "function";
}
const tt = typeof window < "u";
let je = tt ? () => window.performance.now() : () => Date.now(), lt = tt ? (n) => requestAnimationFrame(n) : _e;
const K = /* @__PURE__ */ new Set();
function nt(n) {
  K.forEach((t) => {
    t.c(n) || (K.delete(t), t.f());
  }), K.size !== 0 && lt(nt);
}
function bt(n) {
  let t;
  return K.size === 0 && lt(nt), {
    promise: new Promise((e) => {
      K.add(t = { c: n, f: e });
    }),
    abort() {
      K.delete(t);
    }
  };
}
const O = [];
function gt(n, t = _e) {
  let e;
  const l = /* @__PURE__ */ new Set();
  function i(o) {
    if (mt(n, o) && (n = o, e)) {
      const r = !O.length;
      for (const a of l)
        a[1](), O.push(a, n);
      if (r) {
        for (let a = 0; a < O.length; a += 2)
          O[a][0](O[a + 1]);
        O.length = 0;
      }
    }
  }
  function s(o) {
    i(o(n));
  }
  function f(o, r = _e) {
    const a = [o, r];
    return l.add(a), l.size === 1 && (e = t(i, s) || _e), o(n), () => {
      l.delete(a), l.size === 0 && e && (e(), e = null);
    };
  }
  return { set: i, update: s, subscribe: f };
}
function Se(n) {
  return Object.prototype.toString.call(n) === "[object Date]";
}
function we(n, t, e, l) {
  if (typeof e == "number" || Se(e)) {
    const i = l - e, s = (e - t) / (n.dt || 1 / 60), f = n.opts.stiffness * i, o = n.opts.damping * s, r = (f - o) * n.inv_mass, a = (s + r) * n.dt;
    return Math.abs(a) < n.opts.precision && Math.abs(i) < n.opts.precision ? l : (n.settled = !1, Se(e) ? new Date(e.getTime() + a) : e + a);
  } else {
    if (Array.isArray(e))
      return e.map(
        (i, s) => we(n, t[s], e[s], l[s])
      );
    if (typeof e == "object") {
      const i = {};
      for (const s in e)
        i[s] = we(n, t[s], e[s], l[s]);
      return i;
    } else
      throw new Error(`Cannot spring ${typeof e} values`);
  }
}
function Ve(n, t = {}) {
  const e = gt(n), { stiffness: l = 0.15, damping: i = 0.8, precision: s = 0.01 } = t;
  let f, o, r, a = n, c = n, d = 1, b = 0, m = !1;
  function u(q, L = {}) {
    c = q;
    const C = r = {};
    return n == null || L.hard || y.stiffness >= 1 && y.damping >= 1 ? (m = !0, f = je(), a = q, e.set(n = c), Promise.resolve()) : (L.soft && (b = 1 / ((L.soft === !0 ? 0.5 : +L.soft) * 60), d = 0), o || (f = je(), m = !1, o = bt((_) => {
      if (m)
        return m = !1, o = null, !1;
      d = Math.min(d + b, 1);
      const p = {
        inv_mass: d,
        opts: y,
        settled: !0,
        dt: (_ - f) * 60 / 1e3
      }, M = we(p, a, n, c);
      return f = _, a = n, e.set(n = M), p.settled && (o = null), !p.settled;
    })), new Promise((_) => {
      o.promise.then(() => {
        C === r && _();
      });
    }));
  }
  const y = {
    set: u,
    update: (q, L) => u(q(c, n), L),
    subscribe: e.subscribe,
    stiffness: l,
    damping: i,
    precision: s
  };
  return y;
}
const {
  SvelteComponent: ht,
  assign: wt,
  create_slot: kt,
  detach: yt,
  element: vt,
  get_all_dirty_from_scope: pt,
  get_slot_changes: qt,
  get_spread_update: Ct,
  init: Ft,
  insert: Lt,
  safe_not_equal: jt,
  set_dynamic_element_data: ze,
  set_style: j,
  toggle_class: A,
  transition_in: it,
  transition_out: st,
  update_slot_base: St
} = window.__gradio__svelte__internal;
function Vt(n) {
  let t, e, l;
  const i = (
    /*#slots*/
    n[18].default
  ), s = kt(
    i,
    n,
    /*$$scope*/
    n[17],
    null
  );
  let f = [
    { "data-testid": (
      /*test_id*/
      n[7]
    ) },
    { id: (
      /*elem_id*/
      n[2]
    ) },
    {
      class: e = "block " + /*elem_classes*/
      n[3].join(" ") + " svelte-1t38q2d"
    }
  ], o = {};
  for (let r = 0; r < f.length; r += 1)
    o = wt(o, f[r]);
  return {
    c() {
      t = vt(
        /*tag*/
        n[14]
      ), s && s.c(), ze(
        /*tag*/
        n[14]
      )(t, o), A(
        t,
        "hidden",
        /*visible*/
        n[10] === !1
      ), A(
        t,
        "padded",
        /*padding*/
        n[6]
      ), A(
        t,
        "border_focus",
        /*border_mode*/
        n[5] === "focus"
      ), A(t, "hide-container", !/*explicit_call*/
      n[8] && !/*container*/
      n[9]), j(
        t,
        "height",
        /*get_dimension*/
        n[15](
          /*height*/
          n[0]
        )
      ), j(t, "width", typeof /*width*/
      n[1] == "number" ? `calc(min(${/*width*/
      n[1]}px, 100%))` : (
        /*get_dimension*/
        n[15](
          /*width*/
          n[1]
        )
      )), j(
        t,
        "border-style",
        /*variant*/
        n[4]
      ), j(
        t,
        "overflow",
        /*allow_overflow*/
        n[11] ? "visible" : "hidden"
      ), j(
        t,
        "flex-grow",
        /*scale*/
        n[12]
      ), j(t, "min-width", `calc(min(${/*min_width*/
      n[13]}px, 100%))`), j(t, "border-width", "var(--block-border-width)");
    },
    m(r, a) {
      Lt(r, t, a), s && s.m(t, null), l = !0;
    },
    p(r, a) {
      s && s.p && (!l || a & /*$$scope*/
      131072) && St(
        s,
        i,
        r,
        /*$$scope*/
        r[17],
        l ? qt(
          i,
          /*$$scope*/
          r[17],
          a,
          null
        ) : pt(
          /*$$scope*/
          r[17]
        ),
        null
      ), ze(
        /*tag*/
        r[14]
      )(t, o = Ct(f, [
        (!l || a & /*test_id*/
        128) && { "data-testid": (
          /*test_id*/
          r[7]
        ) },
        (!l || a & /*elem_id*/
        4) && { id: (
          /*elem_id*/
          r[2]
        ) },
        (!l || a & /*elem_classes*/
        8 && e !== (e = "block " + /*elem_classes*/
        r[3].join(" ") + " svelte-1t38q2d")) && { class: e }
      ])), A(
        t,
        "hidden",
        /*visible*/
        r[10] === !1
      ), A(
        t,
        "padded",
        /*padding*/
        r[6]
      ), A(
        t,
        "border_focus",
        /*border_mode*/
        r[5] === "focus"
      ), A(t, "hide-container", !/*explicit_call*/
      r[8] && !/*container*/
      r[9]), a & /*height*/
      1 && j(
        t,
        "height",
        /*get_dimension*/
        r[15](
          /*height*/
          r[0]
        )
      ), a & /*width*/
      2 && j(t, "width", typeof /*width*/
      r[1] == "number" ? `calc(min(${/*width*/
      r[1]}px, 100%))` : (
        /*get_dimension*/
        r[15](
          /*width*/
          r[1]
        )
      )), a & /*variant*/
      16 && j(
        t,
        "border-style",
        /*variant*/
        r[4]
      ), a & /*allow_overflow*/
      2048 && j(
        t,
        "overflow",
        /*allow_overflow*/
        r[11] ? "visible" : "hidden"
      ), a & /*scale*/
      4096 && j(
        t,
        "flex-grow",
        /*scale*/
        r[12]
      ), a & /*min_width*/
      8192 && j(t, "min-width", `calc(min(${/*min_width*/
      r[13]}px, 100%))`);
    },
    i(r) {
      l || (it(s, r), l = !0);
    },
    o(r) {
      st(s, r), l = !1;
    },
    d(r) {
      r && yt(t), s && s.d(r);
    }
  };
}
function zt(n) {
  let t, e = (
    /*tag*/
    n[14] && Vt(n)
  );
  return {
    c() {
      e && e.c();
    },
    m(l, i) {
      e && e.m(l, i), t = !0;
    },
    p(l, [i]) {
      /*tag*/
      l[14] && e.p(l, i);
    },
    i(l) {
      t || (it(e, l), t = !0);
    },
    o(l) {
      st(e, l), t = !1;
    },
    d(l) {
      e && e.d(l);
    }
  };
}
function Mt(n, t, e) {
  let { $$slots: l = {}, $$scope: i } = t, { height: s = void 0 } = t, { width: f = void 0 } = t, { elem_id: o = "" } = t, { elem_classes: r = [] } = t, { variant: a = "solid" } = t, { border_mode: c = "base" } = t, { padding: d = !0 } = t, { type: b = "normal" } = t, { test_id: m = void 0 } = t, { explicit_call: u = !1 } = t, { container: y = !0 } = t, { visible: q = !0 } = t, { allow_overflow: L = !0 } = t, { scale: C = null } = t, { min_width: _ = 0 } = t, p = b === "fieldset" ? "fieldset" : "div";
  const M = (h) => {
    if (h !== void 0) {
      if (typeof h == "number")
        return h + "px";
      if (typeof h == "string")
        return h;
    }
  };
  return n.$$set = (h) => {
    "height" in h && e(0, s = h.height), "width" in h && e(1, f = h.width), "elem_id" in h && e(2, o = h.elem_id), "elem_classes" in h && e(3, r = h.elem_classes), "variant" in h && e(4, a = h.variant), "border_mode" in h && e(5, c = h.border_mode), "padding" in h && e(6, d = h.padding), "type" in h && e(16, b = h.type), "test_id" in h && e(7, m = h.test_id), "explicit_call" in h && e(8, u = h.explicit_call), "container" in h && e(9, y = h.container), "visible" in h && e(10, q = h.visible), "allow_overflow" in h && e(11, L = h.allow_overflow), "scale" in h && e(12, C = h.scale), "min_width" in h && e(13, _ = h.min_width), "$$scope" in h && e(17, i = h.$$scope);
  }, [
    s,
    f,
    o,
    r,
    a,
    c,
    d,
    m,
    u,
    y,
    q,
    L,
    C,
    _,
    p,
    M,
    b,
    i,
    l
  ];
}
class Tt extends ht {
  constructor(t) {
    super(), Ft(this, t, Mt, zt, jt, {
      height: 0,
      width: 1,
      elem_id: 2,
      elem_classes: 3,
      variant: 4,
      border_mode: 5,
      padding: 6,
      type: 16,
      test_id: 7,
      explicit_call: 8,
      container: 9,
      visible: 10,
      allow_overflow: 11,
      scale: 12,
      min_width: 13
    });
  }
}
const {
  SvelteComponent: Nt,
  attr: Pt,
  create_slot: Zt,
  detach: Bt,
  element: Et,
  get_all_dirty_from_scope: At,
  get_slot_changes: Dt,
  init: It,
  insert: Ut,
  safe_not_equal: Xt,
  transition_in: Yt,
  transition_out: Gt,
  update_slot_base: Ot
} = window.__gradio__svelte__internal;
function Rt(n) {
  let t, e;
  const l = (
    /*#slots*/
    n[1].default
  ), i = Zt(
    l,
    n,
    /*$$scope*/
    n[0],
    null
  );
  return {
    c() {
      t = Et("div"), i && i.c(), Pt(t, "class", "svelte-1hnfib2");
    },
    m(s, f) {
      Ut(s, t, f), i && i.m(t, null), e = !0;
    },
    p(s, [f]) {
      i && i.p && (!e || f & /*$$scope*/
      1) && Ot(
        i,
        l,
        s,
        /*$$scope*/
        s[0],
        e ? Dt(
          l,
          /*$$scope*/
          s[0],
          f,
          null
        ) : At(
          /*$$scope*/
          s[0]
        ),
        null
      );
    },
    i(s) {
      e || (Yt(i, s), e = !0);
    },
    o(s) {
      Gt(i, s), e = !1;
    },
    d(s) {
      s && Bt(t), i && i.d(s);
    }
  };
}
function Ht(n, t, e) {
  let { $$slots: l = {}, $$scope: i } = t;
  return n.$$set = (s) => {
    "$$scope" in s && e(0, i = s.$$scope);
  }, [i, l];
}
class Jt extends Nt {
  constructor(t) {
    super(), It(this, t, Ht, Rt, Xt, {});
  }
}
const Kt = [
  { color: "red", primary: 600, secondary: 100 },
  { color: "green", primary: 600, secondary: 100 },
  { color: "blue", primary: 600, secondary: 100 },
  { color: "yellow", primary: 500, secondary: 100 },
  { color: "purple", primary: 600, secondary: 100 },
  { color: "teal", primary: 600, secondary: 100 },
  { color: "orange", primary: 600, secondary: 100 },
  { color: "cyan", primary: 600, secondary: 100 },
  { color: "lime", primary: 500, secondary: 100 },
  { color: "pink", primary: 600, secondary: 100 }
], Me = {
  inherit: "inherit",
  current: "currentColor",
  transparent: "transparent",
  black: "#000",
  white: "#fff",
  slate: {
    50: "#f8fafc",
    100: "#f1f5f9",
    200: "#e2e8f0",
    300: "#cbd5e1",
    400: "#94a3b8",
    500: "#64748b",
    600: "#475569",
    700: "#334155",
    800: "#1e293b",
    900: "#0f172a",
    950: "#020617"
  },
  gray: {
    50: "#f9fafb",
    100: "#f3f4f6",
    200: "#e5e7eb",
    300: "#d1d5db",
    400: "#9ca3af",
    500: "#6b7280",
    600: "#4b5563",
    700: "#374151",
    800: "#1f2937",
    900: "#111827",
    950: "#030712"
  },
  zinc: {
    50: "#fafafa",
    100: "#f4f4f5",
    200: "#e4e4e7",
    300: "#d4d4d8",
    400: "#a1a1aa",
    500: "#71717a",
    600: "#52525b",
    700: "#3f3f46",
    800: "#27272a",
    900: "#18181b",
    950: "#09090b"
  },
  neutral: {
    50: "#fafafa",
    100: "#f5f5f5",
    200: "#e5e5e5",
    300: "#d4d4d4",
    400: "#a3a3a3",
    500: "#737373",
    600: "#525252",
    700: "#404040",
    800: "#262626",
    900: "#171717",
    950: "#0a0a0a"
  },
  stone: {
    50: "#fafaf9",
    100: "#f5f5f4",
    200: "#e7e5e4",
    300: "#d6d3d1",
    400: "#a8a29e",
    500: "#78716c",
    600: "#57534e",
    700: "#44403c",
    800: "#292524",
    900: "#1c1917",
    950: "#0c0a09"
  },
  red: {
    50: "#fef2f2",
    100: "#fee2e2",
    200: "#fecaca",
    300: "#fca5a5",
    400: "#f87171",
    500: "#ef4444",
    600: "#dc2626",
    700: "#b91c1c",
    800: "#991b1b",
    900: "#7f1d1d",
    950: "#450a0a"
  },
  orange: {
    50: "#fff7ed",
    100: "#ffedd5",
    200: "#fed7aa",
    300: "#fdba74",
    400: "#fb923c",
    500: "#f97316",
    600: "#ea580c",
    700: "#c2410c",
    800: "#9a3412",
    900: "#7c2d12",
    950: "#431407"
  },
  amber: {
    50: "#fffbeb",
    100: "#fef3c7",
    200: "#fde68a",
    300: "#fcd34d",
    400: "#fbbf24",
    500: "#f59e0b",
    600: "#d97706",
    700: "#b45309",
    800: "#92400e",
    900: "#78350f",
    950: "#451a03"
  },
  yellow: {
    50: "#fefce8",
    100: "#fef9c3",
    200: "#fef08a",
    300: "#fde047",
    400: "#facc15",
    500: "#eab308",
    600: "#ca8a04",
    700: "#a16207",
    800: "#854d0e",
    900: "#713f12",
    950: "#422006"
  },
  lime: {
    50: "#f7fee7",
    100: "#ecfccb",
    200: "#d9f99d",
    300: "#bef264",
    400: "#a3e635",
    500: "#84cc16",
    600: "#65a30d",
    700: "#4d7c0f",
    800: "#3f6212",
    900: "#365314",
    950: "#1a2e05"
  },
  green: {
    50: "#f0fdf4",
    100: "#dcfce7",
    200: "#bbf7d0",
    300: "#86efac",
    400: "#4ade80",
    500: "#22c55e",
    600: "#16a34a",
    700: "#15803d",
    800: "#166534",
    900: "#14532d",
    950: "#052e16"
  },
  emerald: {
    50: "#ecfdf5",
    100: "#d1fae5",
    200: "#a7f3d0",
    300: "#6ee7b7",
    400: "#34d399",
    500: "#10b981",
    600: "#059669",
    700: "#047857",
    800: "#065f46",
    900: "#064e3b",
    950: "#022c22"
  },
  teal: {
    50: "#f0fdfa",
    100: "#ccfbf1",
    200: "#99f6e4",
    300: "#5eead4",
    400: "#2dd4bf",
    500: "#14b8a6",
    600: "#0d9488",
    700: "#0f766e",
    800: "#115e59",
    900: "#134e4a",
    950: "#042f2e"
  },
  cyan: {
    50: "#ecfeff",
    100: "#cffafe",
    200: "#a5f3fc",
    300: "#67e8f9",
    400: "#22d3ee",
    500: "#06b6d4",
    600: "#0891b2",
    700: "#0e7490",
    800: "#155e75",
    900: "#164e63",
    950: "#083344"
  },
  sky: {
    50: "#f0f9ff",
    100: "#e0f2fe",
    200: "#bae6fd",
    300: "#7dd3fc",
    400: "#38bdf8",
    500: "#0ea5e9",
    600: "#0284c7",
    700: "#0369a1",
    800: "#075985",
    900: "#0c4a6e",
    950: "#082f49"
  },
  blue: {
    50: "#eff6ff",
    100: "#dbeafe",
    200: "#bfdbfe",
    300: "#93c5fd",
    400: "#60a5fa",
    500: "#3b82f6",
    600: "#2563eb",
    700: "#1d4ed8",
    800: "#1e40af",
    900: "#1e3a8a",
    950: "#172554"
  },
  indigo: {
    50: "#eef2ff",
    100: "#e0e7ff",
    200: "#c7d2fe",
    300: "#a5b4fc",
    400: "#818cf8",
    500: "#6366f1",
    600: "#4f46e5",
    700: "#4338ca",
    800: "#3730a3",
    900: "#312e81",
    950: "#1e1b4b"
  },
  violet: {
    50: "#f5f3ff",
    100: "#ede9fe",
    200: "#ddd6fe",
    300: "#c4b5fd",
    400: "#a78bfa",
    500: "#8b5cf6",
    600: "#7c3aed",
    700: "#6d28d9",
    800: "#5b21b6",
    900: "#4c1d95",
    950: "#2e1065"
  },
  purple: {
    50: "#faf5ff",
    100: "#f3e8ff",
    200: "#e9d5ff",
    300: "#d8b4fe",
    400: "#c084fc",
    500: "#a855f7",
    600: "#9333ea",
    700: "#7e22ce",
    800: "#6b21a8",
    900: "#581c87",
    950: "#3b0764"
  },
  fuchsia: {
    50: "#fdf4ff",
    100: "#fae8ff",
    200: "#f5d0fe",
    300: "#f0abfc",
    400: "#e879f9",
    500: "#d946ef",
    600: "#c026d3",
    700: "#a21caf",
    800: "#86198f",
    900: "#701a75",
    950: "#4a044e"
  },
  pink: {
    50: "#fdf2f8",
    100: "#fce7f3",
    200: "#fbcfe8",
    300: "#f9a8d4",
    400: "#f472b6",
    500: "#ec4899",
    600: "#db2777",
    700: "#be185d",
    800: "#9d174d",
    900: "#831843",
    950: "#500724"
  },
  rose: {
    50: "#fff1f2",
    100: "#ffe4e6",
    200: "#fecdd3",
    300: "#fda4af",
    400: "#fb7185",
    500: "#f43f5e",
    600: "#e11d48",
    700: "#be123c",
    800: "#9f1239",
    900: "#881337",
    950: "#4c0519"
  }
};
Kt.reduce(
  (n, { color: t, primary: e, secondary: l }) => ({
    ...n,
    [t]: {
      primary: Me[t][e],
      secondary: Me[t][l]
    }
  }),
  {}
);
function H(n) {
  let t = ["", "k", "M", "G", "T", "P", "E", "Z"], e = 0;
  for (; n > 1e3 && e < t.length - 1; )
    n /= 1e3, e++;
  let l = t[e];
  return (Number.isInteger(n) ? n : n.toFixed(1)) + l;
}
const {
  SvelteComponent: Qt,
  append: T,
  attr: v,
  component_subscribe: Te,
  detach: Wt,
  element: xt,
  init: $t,
  insert: el,
  noop: Ne,
  safe_not_equal: tl,
  set_style: fe,
  svg_element: N,
  toggle_class: Pe
} = window.__gradio__svelte__internal, { onMount: ll } = window.__gradio__svelte__internal;
function nl(n) {
  let t, e, l, i, s, f, o, r, a, c, d, b;
  return {
    c() {
      t = xt("div"), e = N("svg"), l = N("g"), i = N("path"), s = N("path"), f = N("path"), o = N("path"), r = N("g"), a = N("path"), c = N("path"), d = N("path"), b = N("path"), v(i, "d", "M255.926 0.754768L509.702 139.936V221.027L255.926 81.8465V0.754768Z"), v(i, "fill", "#FF7C00"), v(i, "fill-opacity", "0.4"), v(i, "class", "svelte-43sxxs"), v(s, "d", "M509.69 139.936L254.981 279.641V361.255L509.69 221.55V139.936Z"), v(s, "fill", "#FF7C00"), v(s, "class", "svelte-43sxxs"), v(f, "d", "M0.250138 139.937L254.981 279.641V361.255L0.250138 221.55V139.937Z"), v(f, "fill", "#FF7C00"), v(f, "fill-opacity", "0.4"), v(f, "class", "svelte-43sxxs"), v(o, "d", "M255.923 0.232622L0.236328 139.936V221.55L255.923 81.8469V0.232622Z"), v(o, "fill", "#FF7C00"), v(o, "class", "svelte-43sxxs"), fe(l, "transform", "translate(" + /*$top*/
      n[1][0] + "px, " + /*$top*/
      n[1][1] + "px)"), v(a, "d", "M255.926 141.5L509.702 280.681V361.773L255.926 222.592V141.5Z"), v(a, "fill", "#FF7C00"), v(a, "fill-opacity", "0.4"), v(a, "class", "svelte-43sxxs"), v(c, "d", "M509.69 280.679L254.981 420.384V501.998L509.69 362.293V280.679Z"), v(c, "fill", "#FF7C00"), v(c, "class", "svelte-43sxxs"), v(d, "d", "M0.250138 280.681L254.981 420.386V502L0.250138 362.295V280.681Z"), v(d, "fill", "#FF7C00"), v(d, "fill-opacity", "0.4"), v(d, "class", "svelte-43sxxs"), v(b, "d", "M255.923 140.977L0.236328 280.68V362.294L255.923 222.591V140.977Z"), v(b, "fill", "#FF7C00"), v(b, "class", "svelte-43sxxs"), fe(r, "transform", "translate(" + /*$bottom*/
      n[2][0] + "px, " + /*$bottom*/
      n[2][1] + "px)"), v(e, "viewBox", "-1200 -1200 3000 3000"), v(e, "fill", "none"), v(e, "xmlns", "http://www.w3.org/2000/svg"), v(e, "class", "svelte-43sxxs"), v(t, "class", "svelte-43sxxs"), Pe(
        t,
        "margin",
        /*margin*/
        n[0]
      );
    },
    m(m, u) {
      el(m, t, u), T(t, e), T(e, l), T(l, i), T(l, s), T(l, f), T(l, o), T(e, r), T(r, a), T(r, c), T(r, d), T(r, b);
    },
    p(m, [u]) {
      u & /*$top*/
      2 && fe(l, "transform", "translate(" + /*$top*/
      m[1][0] + "px, " + /*$top*/
      m[1][1] + "px)"), u & /*$bottom*/
      4 && fe(r, "transform", "translate(" + /*$bottom*/
      m[2][0] + "px, " + /*$bottom*/
      m[2][1] + "px)"), u & /*margin*/
      1 && Pe(
        t,
        "margin",
        /*margin*/
        m[0]
      );
    },
    i: Ne,
    o: Ne,
    d(m) {
      m && Wt(t);
    }
  };
}
function il(n, t, e) {
  let l, i, { margin: s = !0 } = t;
  const f = Ve([0, 0]);
  Te(n, f, (b) => e(1, l = b));
  const o = Ve([0, 0]);
  Te(n, o, (b) => e(2, i = b));
  let r;
  async function a() {
    await Promise.all([f.set([125, 140]), o.set([-125, -140])]), await Promise.all([f.set([-125, 140]), o.set([125, -140])]), await Promise.all([f.set([-125, 0]), o.set([125, -0])]), await Promise.all([f.set([125, 0]), o.set([-125, 0])]);
  }
  async function c() {
    await a(), r || c();
  }
  async function d() {
    await Promise.all([f.set([125, 0]), o.set([-125, 0])]), c();
  }
  return ll(() => (d(), () => r = !0)), n.$$set = (b) => {
    "margin" in b && e(0, s = b.margin);
  }, [s, l, i, f, o];
}
class sl extends Qt {
  constructor(t) {
    super(), $t(this, t, il, nl, tl, { margin: 0 });
  }
}
const {
  SvelteComponent: fl,
  append: X,
  attr: P,
  binding_callbacks: Ze,
  check_outros: ft,
  create_component: ol,
  create_slot: al,
  destroy_component: rl,
  destroy_each: ot,
  detach: w,
  element: B,
  empty: x,
  ensure_array_like: ue,
  get_all_dirty_from_scope: _l,
  get_slot_changes: cl,
  group_outros: at,
  init: ul,
  insert: k,
  mount_component: dl,
  noop: ke,
  safe_not_equal: ml,
  set_data: z,
  set_style: D,
  space: Z,
  text: F,
  toggle_class: V,
  transition_in: Q,
  transition_out: W,
  update_slot_base: bl
} = window.__gradio__svelte__internal, { tick: gl } = window.__gradio__svelte__internal, { onDestroy: hl } = window.__gradio__svelte__internal, wl = (n) => ({}), Be = (n) => ({});
function Ee(n, t, e) {
  const l = n.slice();
  return l[38] = t[e], l[40] = e, l;
}
function Ae(n, t, e) {
  const l = n.slice();
  return l[38] = t[e], l;
}
function kl(n) {
  let t, e = (
    /*i18n*/
    n[1]("common.error") + ""
  ), l, i, s;
  const f = (
    /*#slots*/
    n[29].error
  ), o = al(
    f,
    n,
    /*$$scope*/
    n[28],
    Be
  );
  return {
    c() {
      t = B("span"), l = F(e), i = Z(), o && o.c(), P(t, "class", "error svelte-1yserjw");
    },
    m(r, a) {
      k(r, t, a), X(t, l), k(r, i, a), o && o.m(r, a), s = !0;
    },
    p(r, a) {
      (!s || a[0] & /*i18n*/
      2) && e !== (e = /*i18n*/
      r[1]("common.error") + "") && z(l, e), o && o.p && (!s || a[0] & /*$$scope*/
      268435456) && bl(
        o,
        f,
        r,
        /*$$scope*/
        r[28],
        s ? cl(
          f,
          /*$$scope*/
          r[28],
          a,
          wl
        ) : _l(
          /*$$scope*/
          r[28]
        ),
        Be
      );
    },
    i(r) {
      s || (Q(o, r), s = !0);
    },
    o(r) {
      W(o, r), s = !1;
    },
    d(r) {
      r && (w(t), w(i)), o && o.d(r);
    }
  };
}
function yl(n) {
  let t, e, l, i, s, f, o, r, a, c = (
    /*variant*/
    n[8] === "default" && /*show_eta_bar*/
    n[18] && /*show_progress*/
    n[6] === "full" && De(n)
  );
  function d(_, p) {
    if (
      /*progress*/
      _[7]
    )
      return ql;
    if (
      /*queue_position*/
      _[2] !== null && /*queue_size*/
      _[3] !== void 0 && /*queue_position*/
      _[2] >= 0
    )
      return pl;
    if (
      /*queue_position*/
      _[2] === 0
    )
      return vl;
  }
  let b = d(n), m = b && b(n), u = (
    /*timer*/
    n[5] && Xe(n)
  );
  const y = [jl, Ll], q = [];
  function L(_, p) {
    return (
      /*last_progress_level*/
      _[15] != null ? 0 : (
        /*show_progress*/
        _[6] === "full" ? 1 : -1
      )
    );
  }
  ~(s = L(n)) && (f = q[s] = y[s](n));
  let C = !/*timer*/
  n[5] && Ke(n);
  return {
    c() {
      c && c.c(), t = Z(), e = B("div"), m && m.c(), l = Z(), u && u.c(), i = Z(), f && f.c(), o = Z(), C && C.c(), r = x(), P(e, "class", "progress-text svelte-1yserjw"), V(
        e,
        "meta-text-center",
        /*variant*/
        n[8] === "center"
      ), V(
        e,
        "meta-text",
        /*variant*/
        n[8] === "default"
      );
    },
    m(_, p) {
      c && c.m(_, p), k(_, t, p), k(_, e, p), m && m.m(e, null), X(e, l), u && u.m(e, null), k(_, i, p), ~s && q[s].m(_, p), k(_, o, p), C && C.m(_, p), k(_, r, p), a = !0;
    },
    p(_, p) {
      /*variant*/
      _[8] === "default" && /*show_eta_bar*/
      _[18] && /*show_progress*/
      _[6] === "full" ? c ? c.p(_, p) : (c = De(_), c.c(), c.m(t.parentNode, t)) : c && (c.d(1), c = null), b === (b = d(_)) && m ? m.p(_, p) : (m && m.d(1), m = b && b(_), m && (m.c(), m.m(e, l))), /*timer*/
      _[5] ? u ? u.p(_, p) : (u = Xe(_), u.c(), u.m(e, null)) : u && (u.d(1), u = null), (!a || p[0] & /*variant*/
      256) && V(
        e,
        "meta-text-center",
        /*variant*/
        _[8] === "center"
      ), (!a || p[0] & /*variant*/
      256) && V(
        e,
        "meta-text",
        /*variant*/
        _[8] === "default"
      );
      let M = s;
      s = L(_), s === M ? ~s && q[s].p(_, p) : (f && (at(), W(q[M], 1, 1, () => {
        q[M] = null;
      }), ft()), ~s ? (f = q[s], f ? f.p(_, p) : (f = q[s] = y[s](_), f.c()), Q(f, 1), f.m(o.parentNode, o)) : f = null), /*timer*/
      _[5] ? C && (C.d(1), C = null) : C ? C.p(_, p) : (C = Ke(_), C.c(), C.m(r.parentNode, r));
    },
    i(_) {
      a || (Q(f), a = !0);
    },
    o(_) {
      W(f), a = !1;
    },
    d(_) {
      _ && (w(t), w(e), w(i), w(o), w(r)), c && c.d(_), m && m.d(), u && u.d(), ~s && q[s].d(_), C && C.d(_);
    }
  };
}
function De(n) {
  let t, e = `translateX(${/*eta_level*/
  (n[17] || 0) * 100 - 100}%)`;
  return {
    c() {
      t = B("div"), P(t, "class", "eta-bar svelte-1yserjw"), D(t, "transform", e);
    },
    m(l, i) {
      k(l, t, i);
    },
    p(l, i) {
      i[0] & /*eta_level*/
      131072 && e !== (e = `translateX(${/*eta_level*/
      (l[17] || 0) * 100 - 100}%)`) && D(t, "transform", e);
    },
    d(l) {
      l && w(t);
    }
  };
}
function vl(n) {
  let t;
  return {
    c() {
      t = F("processing |");
    },
    m(e, l) {
      k(e, t, l);
    },
    p: ke,
    d(e) {
      e && w(t);
    }
  };
}
function pl(n) {
  let t, e = (
    /*queue_position*/
    n[2] + 1 + ""
  ), l, i, s, f;
  return {
    c() {
      t = F("queue: "), l = F(e), i = F("/"), s = F(
        /*queue_size*/
        n[3]
      ), f = F(" |");
    },
    m(o, r) {
      k(o, t, r), k(o, l, r), k(o, i, r), k(o, s, r), k(o, f, r);
    },
    p(o, r) {
      r[0] & /*queue_position*/
      4 && e !== (e = /*queue_position*/
      o[2] + 1 + "") && z(l, e), r[0] & /*queue_size*/
      8 && z(
        s,
        /*queue_size*/
        o[3]
      );
    },
    d(o) {
      o && (w(t), w(l), w(i), w(s), w(f));
    }
  };
}
function ql(n) {
  let t, e = ue(
    /*progress*/
    n[7]
  ), l = [];
  for (let i = 0; i < e.length; i += 1)
    l[i] = Ue(Ae(n, e, i));
  return {
    c() {
      for (let i = 0; i < l.length; i += 1)
        l[i].c();
      t = x();
    },
    m(i, s) {
      for (let f = 0; f < l.length; f += 1)
        l[f] && l[f].m(i, s);
      k(i, t, s);
    },
    p(i, s) {
      if (s[0] & /*progress*/
      128) {
        e = ue(
          /*progress*/
          i[7]
        );
        let f;
        for (f = 0; f < e.length; f += 1) {
          const o = Ae(i, e, f);
          l[f] ? l[f].p(o, s) : (l[f] = Ue(o), l[f].c(), l[f].m(t.parentNode, t));
        }
        for (; f < l.length; f += 1)
          l[f].d(1);
        l.length = e.length;
      }
    },
    d(i) {
      i && w(t), ot(l, i);
    }
  };
}
function Ie(n) {
  let t, e = (
    /*p*/
    n[38].unit + ""
  ), l, i, s = " ", f;
  function o(c, d) {
    return (
      /*p*/
      c[38].length != null ? Fl : Cl
    );
  }
  let r = o(n), a = r(n);
  return {
    c() {
      a.c(), t = Z(), l = F(e), i = F(" | "), f = F(s);
    },
    m(c, d) {
      a.m(c, d), k(c, t, d), k(c, l, d), k(c, i, d), k(c, f, d);
    },
    p(c, d) {
      r === (r = o(c)) && a ? a.p(c, d) : (a.d(1), a = r(c), a && (a.c(), a.m(t.parentNode, t))), d[0] & /*progress*/
      128 && e !== (e = /*p*/
      c[38].unit + "") && z(l, e);
    },
    d(c) {
      c && (w(t), w(l), w(i), w(f)), a.d(c);
    }
  };
}
function Cl(n) {
  let t = H(
    /*p*/
    n[38].index || 0
  ) + "", e;
  return {
    c() {
      e = F(t);
    },
    m(l, i) {
      k(l, e, i);
    },
    p(l, i) {
      i[0] & /*progress*/
      128 && t !== (t = H(
        /*p*/
        l[38].index || 0
      ) + "") && z(e, t);
    },
    d(l) {
      l && w(e);
    }
  };
}
function Fl(n) {
  let t = H(
    /*p*/
    n[38].index || 0
  ) + "", e, l, i = H(
    /*p*/
    n[38].length
  ) + "", s;
  return {
    c() {
      e = F(t), l = F("/"), s = F(i);
    },
    m(f, o) {
      k(f, e, o), k(f, l, o), k(f, s, o);
    },
    p(f, o) {
      o[0] & /*progress*/
      128 && t !== (t = H(
        /*p*/
        f[38].index || 0
      ) + "") && z(e, t), o[0] & /*progress*/
      128 && i !== (i = H(
        /*p*/
        f[38].length
      ) + "") && z(s, i);
    },
    d(f) {
      f && (w(e), w(l), w(s));
    }
  };
}
function Ue(n) {
  let t, e = (
    /*p*/
    n[38].index != null && Ie(n)
  );
  return {
    c() {
      e && e.c(), t = x();
    },
    m(l, i) {
      e && e.m(l, i), k(l, t, i);
    },
    p(l, i) {
      /*p*/
      l[38].index != null ? e ? e.p(l, i) : (e = Ie(l), e.c(), e.m(t.parentNode, t)) : e && (e.d(1), e = null);
    },
    d(l) {
      l && w(t), e && e.d(l);
    }
  };
}
function Xe(n) {
  let t, e = (
    /*eta*/
    n[0] ? `/${/*formatted_eta*/
    n[19]}` : ""
  ), l, i;
  return {
    c() {
      t = F(
        /*formatted_timer*/
        n[20]
      ), l = F(e), i = F("s");
    },
    m(s, f) {
      k(s, t, f), k(s, l, f), k(s, i, f);
    },
    p(s, f) {
      f[0] & /*formatted_timer*/
      1048576 && z(
        t,
        /*formatted_timer*/
        s[20]
      ), f[0] & /*eta, formatted_eta*/
      524289 && e !== (e = /*eta*/
      s[0] ? `/${/*formatted_eta*/
      s[19]}` : "") && z(l, e);
    },
    d(s) {
      s && (w(t), w(l), w(i));
    }
  };
}
function Ll(n) {
  let t, e;
  return t = new sl({
    props: { margin: (
      /*variant*/
      n[8] === "default"
    ) }
  }), {
    c() {
      ol(t.$$.fragment);
    },
    m(l, i) {
      dl(t, l, i), e = !0;
    },
    p(l, i) {
      const s = {};
      i[0] & /*variant*/
      256 && (s.margin = /*variant*/
      l[8] === "default"), t.$set(s);
    },
    i(l) {
      e || (Q(t.$$.fragment, l), e = !0);
    },
    o(l) {
      W(t.$$.fragment, l), e = !1;
    },
    d(l) {
      rl(t, l);
    }
  };
}
function jl(n) {
  let t, e, l, i, s, f = `${/*last_progress_level*/
  n[15] * 100}%`, o = (
    /*progress*/
    n[7] != null && Ye(n)
  );
  return {
    c() {
      t = B("div"), e = B("div"), o && o.c(), l = Z(), i = B("div"), s = B("div"), P(e, "class", "progress-level-inner svelte-1yserjw"), P(s, "class", "progress-bar svelte-1yserjw"), D(s, "width", f), P(i, "class", "progress-bar-wrap svelte-1yserjw"), P(t, "class", "progress-level svelte-1yserjw");
    },
    m(r, a) {
      k(r, t, a), X(t, e), o && o.m(e, null), X(t, l), X(t, i), X(i, s), n[30](s);
    },
    p(r, a) {
      /*progress*/
      r[7] != null ? o ? o.p(r, a) : (o = Ye(r), o.c(), o.m(e, null)) : o && (o.d(1), o = null), a[0] & /*last_progress_level*/
      32768 && f !== (f = `${/*last_progress_level*/
      r[15] * 100}%`) && D(s, "width", f);
    },
    i: ke,
    o: ke,
    d(r) {
      r && w(t), o && o.d(), n[30](null);
    }
  };
}
function Ye(n) {
  let t, e = ue(
    /*progress*/
    n[7]
  ), l = [];
  for (let i = 0; i < e.length; i += 1)
    l[i] = Je(Ee(n, e, i));
  return {
    c() {
      for (let i = 0; i < l.length; i += 1)
        l[i].c();
      t = x();
    },
    m(i, s) {
      for (let f = 0; f < l.length; f += 1)
        l[f] && l[f].m(i, s);
      k(i, t, s);
    },
    p(i, s) {
      if (s[0] & /*progress_level, progress*/
      16512) {
        e = ue(
          /*progress*/
          i[7]
        );
        let f;
        for (f = 0; f < e.length; f += 1) {
          const o = Ee(i, e, f);
          l[f] ? l[f].p(o, s) : (l[f] = Je(o), l[f].c(), l[f].m(t.parentNode, t));
        }
        for (; f < l.length; f += 1)
          l[f].d(1);
        l.length = e.length;
      }
    },
    d(i) {
      i && w(t), ot(l, i);
    }
  };
}
function Ge(n) {
  let t, e, l, i, s = (
    /*i*/
    n[40] !== 0 && Sl()
  ), f = (
    /*p*/
    n[38].desc != null && Oe(n)
  ), o = (
    /*p*/
    n[38].desc != null && /*progress_level*/
    n[14] && /*progress_level*/
    n[14][
      /*i*/
      n[40]
    ] != null && Re()
  ), r = (
    /*progress_level*/
    n[14] != null && He(n)
  );
  return {
    c() {
      s && s.c(), t = Z(), f && f.c(), e = Z(), o && o.c(), l = Z(), r && r.c(), i = x();
    },
    m(a, c) {
      s && s.m(a, c), k(a, t, c), f && f.m(a, c), k(a, e, c), o && o.m(a, c), k(a, l, c), r && r.m(a, c), k(a, i, c);
    },
    p(a, c) {
      /*p*/
      a[38].desc != null ? f ? f.p(a, c) : (f = Oe(a), f.c(), f.m(e.parentNode, e)) : f && (f.d(1), f = null), /*p*/
      a[38].desc != null && /*progress_level*/
      a[14] && /*progress_level*/
      a[14][
        /*i*/
        a[40]
      ] != null ? o || (o = Re(), o.c(), o.m(l.parentNode, l)) : o && (o.d(1), o = null), /*progress_level*/
      a[14] != null ? r ? r.p(a, c) : (r = He(a), r.c(), r.m(i.parentNode, i)) : r && (r.d(1), r = null);
    },
    d(a) {
      a && (w(t), w(e), w(l), w(i)), s && s.d(a), f && f.d(a), o && o.d(a), r && r.d(a);
    }
  };
}
function Sl(n) {
  let t;
  return {
    c() {
      t = F(" /");
    },
    m(e, l) {
      k(e, t, l);
    },
    d(e) {
      e && w(t);
    }
  };
}
function Oe(n) {
  let t = (
    /*p*/
    n[38].desc + ""
  ), e;
  return {
    c() {
      e = F(t);
    },
    m(l, i) {
      k(l, e, i);
    },
    p(l, i) {
      i[0] & /*progress*/
      128 && t !== (t = /*p*/
      l[38].desc + "") && z(e, t);
    },
    d(l) {
      l && w(e);
    }
  };
}
function Re(n) {
  let t;
  return {
    c() {
      t = F("-");
    },
    m(e, l) {
      k(e, t, l);
    },
    d(e) {
      e && w(t);
    }
  };
}
function He(n) {
  let t = (100 * /*progress_level*/
  (n[14][
    /*i*/
    n[40]
  ] || 0)).toFixed(1) + "", e, l;
  return {
    c() {
      e = F(t), l = F("%");
    },
    m(i, s) {
      k(i, e, s), k(i, l, s);
    },
    p(i, s) {
      s[0] & /*progress_level*/
      16384 && t !== (t = (100 * /*progress_level*/
      (i[14][
        /*i*/
        i[40]
      ] || 0)).toFixed(1) + "") && z(e, t);
    },
    d(i) {
      i && (w(e), w(l));
    }
  };
}
function Je(n) {
  let t, e = (
    /*p*/
    (n[38].desc != null || /*progress_level*/
    n[14] && /*progress_level*/
    n[14][
      /*i*/
      n[40]
    ] != null) && Ge(n)
  );
  return {
    c() {
      e && e.c(), t = x();
    },
    m(l, i) {
      e && e.m(l, i), k(l, t, i);
    },
    p(l, i) {
      /*p*/
      l[38].desc != null || /*progress_level*/
      l[14] && /*progress_level*/
      l[14][
        /*i*/
        l[40]
      ] != null ? e ? e.p(l, i) : (e = Ge(l), e.c(), e.m(t.parentNode, t)) : e && (e.d(1), e = null);
    },
    d(l) {
      l && w(t), e && e.d(l);
    }
  };
}
function Ke(n) {
  let t, e;
  return {
    c() {
      t = B("p"), e = F(
        /*loading_text*/
        n[9]
      ), P(t, "class", "loading svelte-1yserjw");
    },
    m(l, i) {
      k(l, t, i), X(t, e);
    },
    p(l, i) {
      i[0] & /*loading_text*/
      512 && z(
        e,
        /*loading_text*/
        l[9]
      );
    },
    d(l) {
      l && w(t);
    }
  };
}
function Vl(n) {
  let t, e, l, i, s;
  const f = [yl, kl], o = [];
  function r(a, c) {
    return (
      /*status*/
      a[4] === "pending" ? 0 : (
        /*status*/
        a[4] === "error" ? 1 : -1
      )
    );
  }
  return ~(e = r(n)) && (l = o[e] = f[e](n)), {
    c() {
      t = B("div"), l && l.c(), P(t, "class", i = "wrap " + /*variant*/
      n[8] + " " + /*show_progress*/
      n[6] + " svelte-1yserjw"), V(t, "hide", !/*status*/
      n[4] || /*status*/
      n[4] === "complete" || /*show_progress*/
      n[6] === "hidden"), V(
        t,
        "translucent",
        /*variant*/
        n[8] === "center" && /*status*/
        (n[4] === "pending" || /*status*/
        n[4] === "error") || /*translucent*/
        n[11] || /*show_progress*/
        n[6] === "minimal"
      ), V(
        t,
        "generating",
        /*status*/
        n[4] === "generating"
      ), V(
        t,
        "border",
        /*border*/
        n[12]
      ), D(
        t,
        "position",
        /*absolute*/
        n[10] ? "absolute" : "static"
      ), D(
        t,
        "padding",
        /*absolute*/
        n[10] ? "0" : "var(--size-8) 0"
      );
    },
    m(a, c) {
      k(a, t, c), ~e && o[e].m(t, null), n[31](t), s = !0;
    },
    p(a, c) {
      let d = e;
      e = r(a), e === d ? ~e && o[e].p(a, c) : (l && (at(), W(o[d], 1, 1, () => {
        o[d] = null;
      }), ft()), ~e ? (l = o[e], l ? l.p(a, c) : (l = o[e] = f[e](a), l.c()), Q(l, 1), l.m(t, null)) : l = null), (!s || c[0] & /*variant, show_progress*/
      320 && i !== (i = "wrap " + /*variant*/
      a[8] + " " + /*show_progress*/
      a[6] + " svelte-1yserjw")) && P(t, "class", i), (!s || c[0] & /*variant, show_progress, status, show_progress*/
      336) && V(t, "hide", !/*status*/
      a[4] || /*status*/
      a[4] === "complete" || /*show_progress*/
      a[6] === "hidden"), (!s || c[0] & /*variant, show_progress, variant, status, translucent, show_progress*/
      2384) && V(
        t,
        "translucent",
        /*variant*/
        a[8] === "center" && /*status*/
        (a[4] === "pending" || /*status*/
        a[4] === "error") || /*translucent*/
        a[11] || /*show_progress*/
        a[6] === "minimal"
      ), (!s || c[0] & /*variant, show_progress, status*/
      336) && V(
        t,
        "generating",
        /*status*/
        a[4] === "generating"
      ), (!s || c[0] & /*variant, show_progress, border*/
      4416) && V(
        t,
        "border",
        /*border*/
        a[12]
      ), c[0] & /*absolute*/
      1024 && D(
        t,
        "position",
        /*absolute*/
        a[10] ? "absolute" : "static"
      ), c[0] & /*absolute*/
      1024 && D(
        t,
        "padding",
        /*absolute*/
        a[10] ? "0" : "var(--size-8) 0"
      );
    },
    i(a) {
      s || (Q(l), s = !0);
    },
    o(a) {
      W(l), s = !1;
    },
    d(a) {
      a && w(t), ~e && o[e].d(), n[31](null);
    }
  };
}
let oe = [], me = !1;
async function zl(n, t = !0) {
  if (!(window.__gradio_mode__ === "website" || window.__gradio_mode__ !== "app" && t !== !0)) {
    if (oe.push(n), !me)
      me = !0;
    else
      return;
    await gl(), requestAnimationFrame(() => {
      let e = [0, 0];
      for (let l = 0; l < oe.length; l++) {
        const s = oe[l].getBoundingClientRect();
        (l === 0 || s.top + window.scrollY <= e[0]) && (e[0] = s.top + window.scrollY, e[1] = l);
      }
      window.scrollTo({ top: e[0] - 20, behavior: "smooth" }), me = !1, oe = [];
    });
  }
}
function Ml(n, t, e) {
  let l, { $$slots: i = {}, $$scope: s } = t, { i18n: f } = t, { eta: o = null } = t, { queue_position: r } = t, { queue_size: a } = t, { status: c } = t, { scroll_to_output: d = !1 } = t, { timer: b = !0 } = t, { show_progress: m = "full" } = t, { message: u = null } = t, { progress: y = null } = t, { variant: q = "default" } = t, { loading_text: L = "Loading..." } = t, { absolute: C = !0 } = t, { translucent: _ = !1 } = t, { border: p = !1 } = t, { autoscroll: M } = t, h, $ = !1, ie = 0, I = 0, Y = null, G = null, qe = 0, U = null, ee, E = null, Ce = !0;
  const ct = () => {
    e(0, o = e(26, Y = e(19, se = null))), e(24, ie = performance.now()), e(25, I = 0), $ = !0, Fe();
  };
  function Fe() {
    requestAnimationFrame(() => {
      e(25, I = (performance.now() - ie) / 1e3), $ && Fe();
    });
  }
  function Le() {
    e(25, I = 0), e(0, o = e(26, Y = e(19, se = null))), $ && ($ = !1);
  }
  hl(() => {
    $ && Le();
  });
  let se = null;
  function ut(g) {
    Ze[g ? "unshift" : "push"](() => {
      E = g, e(16, E), e(7, y), e(14, U), e(15, ee);
    });
  }
  function dt(g) {
    Ze[g ? "unshift" : "push"](() => {
      h = g, e(13, h);
    });
  }
  return n.$$set = (g) => {
    "i18n" in g && e(1, f = g.i18n), "eta" in g && e(0, o = g.eta), "queue_position" in g && e(2, r = g.queue_position), "queue_size" in g && e(3, a = g.queue_size), "status" in g && e(4, c = g.status), "scroll_to_output" in g && e(21, d = g.scroll_to_output), "timer" in g && e(5, b = g.timer), "show_progress" in g && e(6, m = g.show_progress), "message" in g && e(22, u = g.message), "progress" in g && e(7, y = g.progress), "variant" in g && e(8, q = g.variant), "loading_text" in g && e(9, L = g.loading_text), "absolute" in g && e(10, C = g.absolute), "translucent" in g && e(11, _ = g.translucent), "border" in g && e(12, p = g.border), "autoscroll" in g && e(23, M = g.autoscroll), "$$scope" in g && e(28, s = g.$$scope);
  }, n.$$.update = () => {
    n.$$.dirty[0] & /*eta, old_eta, timer_start, eta_from_start*/
    218103809 && (o === null && e(0, o = Y), o != null && Y !== o && (e(27, G = (performance.now() - ie) / 1e3 + o), e(19, se = G.toFixed(1)), e(26, Y = o))), n.$$.dirty[0] & /*eta_from_start, timer_diff*/
    167772160 && e(17, qe = G === null || G <= 0 || !I ? null : Math.min(I / G, 1)), n.$$.dirty[0] & /*progress*/
    128 && y != null && e(18, Ce = !1), n.$$.dirty[0] & /*progress, progress_level, progress_bar, last_progress_level*/
    114816 && (y != null ? e(14, U = y.map((g) => {
      if (g.index != null && g.length != null)
        return g.index / g.length;
      if (g.progress != null)
        return g.progress;
    })) : e(14, U = null), U ? (e(15, ee = U[U.length - 1]), E && (ee === 0 ? e(16, E.style.transition = "0", E) : e(16, E.style.transition = "150ms", E))) : e(15, ee = void 0)), n.$$.dirty[0] & /*status*/
    16 && (c === "pending" ? ct() : Le()), n.$$.dirty[0] & /*el, scroll_to_output, status, autoscroll*/
    10493968 && h && d && (c === "pending" || c === "complete") && zl(h, M), n.$$.dirty[0] & /*status, message*/
    4194320, n.$$.dirty[0] & /*timer_diff*/
    33554432 && e(20, l = I.toFixed(1));
  }, [
    o,
    f,
    r,
    a,
    c,
    b,
    m,
    y,
    q,
    L,
    C,
    _,
    p,
    h,
    U,
    ee,
    E,
    qe,
    Ce,
    se,
    l,
    d,
    u,
    M,
    ie,
    I,
    Y,
    G,
    s,
    i,
    ut,
    dt
  ];
}
class Tl extends fl {
  constructor(t) {
    super(), ul(
      this,
      t,
      Ml,
      Vl,
      ml,
      {
        i18n: 1,
        eta: 0,
        queue_position: 2,
        queue_size: 3,
        status: 4,
        scroll_to_output: 21,
        timer: 5,
        show_progress: 6,
        message: 22,
        progress: 7,
        variant: 8,
        loading_text: 9,
        absolute: 10,
        translucent: 11,
        border: 12,
        autoscroll: 23
      },
      null,
      [-1, -1]
    );
  }
}
const {
  SvelteComponent: Nl,
  append: ae,
  attr: R,
  detach: Pl,
  element: be,
  init: Zl,
  insert: Bl,
  listen: ge,
  noop: Qe,
  run_all: El,
  safe_not_equal: Al,
  set_data: Dl,
  space: Il,
  text: Ul,
  toggle_class: We
} = window.__gradio__svelte__internal, { createEventDispatcher: Xl } = window.__gradio__svelte__internal;
function Yl(n) {
  let t, e, l, i, s, f, o;
  return {
    c() {
      t = be("label"), e = be("input"), l = Il(), i = be("span"), s = Ul(
        /*label*/
        n[1]
      ), e.disabled = /*disabled*/
      n[2], R(e, "type", "checkbox"), R(e, "name", "test"), R(e, "data-testid", "checkbox"), R(e, "class", "svelte-15y2hcz"), R(i, "class", "ml-2 svelte-15y2hcz"), R(t, "class", "svelte-15y2hcz"), We(
        t,
        "disabled",
        /*disabled*/
        n[2]
      );
    },
    m(r, a) {
      Bl(r, t, a), ae(t, e), e.checked = /*value*/
      n[0], ae(t, l), ae(t, i), ae(i, s), f || (o = [
        ge(
          e,
          "change",
          /*input_change_handler*/
          n[6]
        ),
        ge(
          e,
          "keydown",
          /*handle_enter*/
          n[3]
        ),
        ge(
          e,
          "input",
          /*handle_input*/
          n[4]
        )
      ], f = !0);
    },
    p(r, [a]) {
      a & /*disabled*/
      4 && (e.disabled = /*disabled*/
      r[2]), a & /*value*/
      1 && (e.checked = /*value*/
      r[0]), a & /*label*/
      2 && Dl(
        s,
        /*label*/
        r[1]
      ), a & /*disabled*/
      4 && We(
        t,
        "disabled",
        /*disabled*/
        r[2]
      );
    },
    i: Qe,
    o: Qe,
    d(r) {
      r && Pl(t), f = !1, El(o);
    }
  };
}
function Gl(n, t, e) {
  let l, { value: i = !1 } = t, { label: s = "Checkbox" } = t, { interactive: f } = t;
  const o = Xl();
  async function r(d) {
    d.key === "Enter" && (e(0, i = !i), o("select", {
      index: 0,
      value: d.currentTarget.checked,
      selected: d.currentTarget.checked
    }));
  }
  async function a(d) {
    e(0, i = d.currentTarget.checked), o("select", {
      index: 0,
      value: d.currentTarget.checked,
      selected: d.currentTarget.checked
    });
  }
  function c() {
    i = this.checked, e(0, i);
  }
  return n.$$set = (d) => {
    "value" in d && e(0, i = d.value), "label" in d && e(1, s = d.label), "interactive" in d && e(5, f = d.interactive);
  }, n.$$.update = () => {
    n.$$.dirty & /*value*/
    1 && o("change", i), n.$$.dirty & /*interactive*/
    32 && e(2, l = !f);
  }, [
    i,
    s,
    l,
    r,
    a,
    f,
    c
  ];
}
class fn extends Nl {
  constructor(t) {
    super(), Zl(this, t, Gl, Yl, Al, { value: 0, label: 1, interactive: 5 });
  }
}
const {
  SvelteComponent: Ol,
  append: ce,
  assign: Rl,
  attr: S,
  check_outros: Hl,
  create_component: ye,
  destroy_component: ve,
  detach: le,
  element: de,
  get_spread_object: Jl,
  get_spread_update: Kl,
  group_outros: Ql,
  init: Wl,
  insert: ne,
  listen: xe,
  mount_component: pe,
  run_all: xl,
  safe_not_equal: $l,
  set_data: rt,
  space: he,
  text: _t,
  toggle_class: re,
  transition_in: J,
  transition_out: te
} = window.__gradio__svelte__internal, { afterUpdate: en } = window.__gradio__svelte__internal;
function $e(n) {
  let t, e;
  return {
    c() {
      t = de("span"), e = _t(
        /*label*/
        n[4]
      ), S(t, "class", "toggle-label svelte-47wo9l"), S(t, "aria-hidden", "true");
    },
    m(l, i) {
      ne(l, t, i), ce(t, e);
    },
    p(l, i) {
      i & /*label*/
      16 && rt(
        e,
        /*label*/
        l[4]
      );
    },
    d(l) {
      l && le(t);
    }
  };
}
function et(n) {
  let t, e, l;
  return e = new Jt({
    props: {
      $$slots: { default: [tn] },
      $$scope: { ctx: n }
    }
  }), {
    c() {
      t = de("div"), ye(e.$$.fragment), S(t, "class", "toggle-info svelte-47wo9l");
    },
    m(i, s) {
      ne(i, t, s), pe(e, t, null), l = !0;
    },
    p(i, s) {
      const f = {};
      s & /*$$scope, info*/
      65600 && (f.$$scope = { dirty: s, ctx: i }), e.$set(f);
    },
    i(i) {
      l || (J(e.$$.fragment, i), l = !0);
    },
    o(i) {
      te(e.$$.fragment, i), l = !1;
    },
    d(i) {
      i && le(t), ve(e);
    }
  };
}
function tn(n) {
  let t;
  return {
    c() {
      t = _t(
        /*info*/
        n[6]
      );
    },
    m(e, l) {
      ne(e, t, l);
    },
    p(e, l) {
      l & /*info*/
      64 && rt(
        t,
        /*info*/
        e[6]
      );
    },
    d(e) {
      e && le(t);
    }
  };
}
function ln(n) {
  let t, e, l, i, s, f, o, r, a;
  const c = [
    {
      autoscroll: (
        /*gradio*/
        n[11].autoscroll
      )
    },
    { i18n: (
      /*gradio*/
      n[11].i18n
    ) },
    /*loading_status*/
    n[10]
  ];
  let d = {};
  for (let u = 0; u < c.length; u += 1)
    d = Rl(d, c[u]);
  t = new Tl({ props: d });
  let b = (
    /*show_label*/
    n[5] && $e(n)
  ), m = (
    /*info*/
    n[6] && et(n)
  );
  return {
    c() {
      ye(t.$$.fragment), e = he(), l = de("div"), b && b.c(), i = he(), s = de("div"), f = he(), m && m.c(), S(s, "class", "toggle-switch svelte-47wo9l"), S(s, "tabindex", "0"), S(s, "type", "button"), S(s, "role", "switch"), S(
        s,
        "aria-checked",
        /*value*/
        n[0]
      ), S(
        s,
        "aria-label",
        /*label*/
        n[4]
      ), re(
        s,
        "active",
        /*value*/
        n[0]
      ), re(s, "non-interactive", !/*interactive*/
      n[12]), S(l, "class", "toggle-container");
    },
    m(u, y) {
      pe(t, u, y), ne(u, e, y), ne(u, l, y), b && b.m(l, null), ce(l, i), ce(l, s), ce(l, f), m && m.m(l, null), o = !0, r || (a = [
        xe(
          s,
          "click",
          /*handle_change*/
          n[14]
        ),
        xe(
          s,
          "keydown",
          /*handle_keydown*/
          n[13]
        )
      ], r = !0);
    },
    p(u, y) {
      const q = y & /*gradio, loading_status*/
      3072 ? Kl(c, [
        y & /*gradio*/
        2048 && {
          autoscroll: (
            /*gradio*/
            u[11].autoscroll
          )
        },
        y & /*gradio*/
        2048 && { i18n: (
          /*gradio*/
          u[11].i18n
        ) },
        y & /*loading_status*/
        1024 && Jl(
          /*loading_status*/
          u[10]
        )
      ]) : {};
      t.$set(q), /*show_label*/
      u[5] ? b ? b.p(u, y) : (b = $e(u), b.c(), b.m(l, i)) : b && (b.d(1), b = null), (!o || y & /*value*/
      1) && S(
        s,
        "aria-checked",
        /*value*/
        u[0]
      ), (!o || y & /*label*/
      16) && S(
        s,
        "aria-label",
        /*label*/
        u[4]
      ), (!o || y & /*value*/
      1) && re(
        s,
        "active",
        /*value*/
        u[0]
      ), (!o || y & /*interactive*/
      4096) && re(s, "non-interactive", !/*interactive*/
      u[12]), /*info*/
      u[6] ? m ? (m.p(u, y), y & /*info*/
      64 && J(m, 1)) : (m = et(u), m.c(), J(m, 1), m.m(l, null)) : m && (Ql(), te(m, 1, 1, () => {
        m = null;
      }), Hl());
    },
    i(u) {
      o || (J(t.$$.fragment, u), J(m), o = !0);
    },
    o(u) {
      te(t.$$.fragment, u), te(m), o = !1;
    },
    d(u) {
      u && (le(e), le(l)), ve(t, u), b && b.d(), m && m.d(), r = !1, xl(a);
    }
  };
}
function nn(n) {
  let t, e;
  return t = new Tt({
    props: {
      visible: (
        /*visible*/
        n[3]
      ),
      elem_id: (
        /*elem_id*/
        n[1]
      ),
      elem_classes: (
        /*elem_classes*/
        n[2]
      ),
      container: (
        /*container*/
        n[7]
      ),
      scale: (
        /*scale*/
        n[8]
      ),
      min_width: (
        /*min_width*/
        n[9]
      ),
      $$slots: { default: [ln] },
      $$scope: { ctx: n }
    }
  }), {
    c() {
      ye(t.$$.fragment);
    },
    m(l, i) {
      pe(t, l, i), e = !0;
    },
    p(l, [i]) {
      const s = {};
      i & /*visible*/
      8 && (s.visible = /*visible*/
      l[3]), i & /*elem_id*/
      2 && (s.elem_id = /*elem_id*/
      l[1]), i & /*elem_classes*/
      4 && (s.elem_classes = /*elem_classes*/
      l[2]), i & /*container*/
      128 && (s.container = /*container*/
      l[7]), i & /*scale*/
      256 && (s.scale = /*scale*/
      l[8]), i & /*min_width*/
      512 && (s.min_width = /*min_width*/
      l[9]), i & /*$$scope, info, value, label, interactive, show_label, gradio, loading_status*/
      72817 && (s.$$scope = { dirty: i, ctx: l }), t.$set(s);
    },
    i(l) {
      e || (J(t.$$.fragment, l), e = !0);
    },
    o(l) {
      te(t.$$.fragment, l), e = !1;
    },
    d(l) {
      ve(t, l);
    }
  };
}
function sn(n, t, e) {
  let { elem_id: l = "" } = t, { elem_classes: i = [] } = t, { visible: s = !0 } = t, { value: f = !1 } = t, { value_is_output: o = !1 } = t, { label: r = "Toggle" } = t, { show_label: a = !0 } = t, { info: c = void 0 } = t, { container: d = !0 } = t, { scale: b = null } = t, { min_width: m = void 0 } = t, { loading_status: u } = t, { gradio: y } = t, { interactive: q = !0 } = t;
  function L(_) {
    (_.key === "Enter" || _.key === " ") && C();
  }
  function C() {
    q && (e(0, f = !f), y.dispatch("change"), o || y.dispatch("input"));
  }
  return en(() => {
    e(15, o = !1);
  }), n.$$set = (_) => {
    "elem_id" in _ && e(1, l = _.elem_id), "elem_classes" in _ && e(2, i = _.elem_classes), "visible" in _ && e(3, s = _.visible), "value" in _ && e(0, f = _.value), "value_is_output" in _ && e(15, o = _.value_is_output), "label" in _ && e(4, r = _.label), "show_label" in _ && e(5, a = _.show_label), "info" in _ && e(6, c = _.info), "container" in _ && e(7, d = _.container), "scale" in _ && e(8, b = _.scale), "min_width" in _ && e(9, m = _.min_width), "loading_status" in _ && e(10, u = _.loading_status), "gradio" in _ && e(11, y = _.gradio), "interactive" in _ && e(12, q = _.interactive);
  }, [
    f,
    l,
    i,
    s,
    r,
    a,
    c,
    d,
    b,
    m,
    u,
    y,
    q,
    L,
    C,
    o
  ];
}
class on extends Ol {
  constructor(t) {
    super(), Wl(this, t, sn, nn, $l, {
      elem_id: 1,
      elem_classes: 2,
      visible: 3,
      value: 0,
      value_is_output: 15,
      label: 4,
      show_label: 5,
      info: 6,
      container: 7,
      scale: 8,
      min_width: 9,
      loading_status: 10,
      gradio: 11,
      interactive: 12
    });
  }
}
export {
  fn as BaseCheckbox,
  on as default
};
