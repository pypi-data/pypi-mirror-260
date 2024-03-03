const {
  SvelteComponent: c,
  append: f,
  attr: o,
  detach: g,
  element: d,
  init: r,
  insert: v,
  noop: u,
  safe_not_equal: y,
  set_data: m,
  text: b,
  toggle_class: _
} = window.__gradio__svelte__internal;
function w(a) {
  let e, n = (
    /*value*/
    (a[0] !== null ? (
      /*value*/
      a[0].toLocaleString()
    ) : "") + ""
  ), s;
  return {
    c() {
      e = d("div"), s = b(n), o(e, "class", "svelte-1gecy8w"), _(
        e,
        "table",
        /*type*/
        a[1] === "table"
      ), _(
        e,
        "gallery",
        /*type*/
        a[1] === "gallery"
      ), _(
        e,
        "selected",
        /*selected*/
        a[2]
      );
    },
    m(l, t) {
      v(l, e, t), f(e, s);
    },
    p(l, [t]) {
      t & /*value*/
      1 && n !== (n = /*value*/
      (l[0] !== null ? (
        /*value*/
        l[0].toLocaleString()
      ) : "") + "") && m(s, n), t & /*type*/
      2 && _(
        e,
        "table",
        /*type*/
        l[1] === "table"
      ), t & /*type*/
      2 && _(
        e,
        "gallery",
        /*type*/
        l[1] === "gallery"
      ), t & /*selected*/
      4 && _(
        e,
        "selected",
        /*selected*/
        l[2]
      );
    },
    i: u,
    o: u,
    d(l) {
      l && g(e);
    }
  };
}
function S(a, e, n) {
  let { value: s } = e, { type: l } = e, { selected: t = !1 } = e;
  return a.$$set = (i) => {
    "value" in i && n(0, s = i.value), "type" in i && n(1, l = i.type), "selected" in i && n(2, t = i.selected);
  }, [s, l, t];
}
class h extends c {
  constructor(e) {
    super(), r(this, e, S, w, y, { value: 0, type: 1, selected: 2 });
  }
}
export {
  h as default
};
