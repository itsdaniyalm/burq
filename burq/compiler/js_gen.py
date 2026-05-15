from ..app import App


def generate_js(app: App) -> str:
    api_base = app.api_base
    api_key  = app.api_key

    main_js = f"""/* ⚡ Burq Runtime — https://burq.dev */

const Burq = {{
  apiBase: "{api_base}",
  apiKey:  "{api_key}",

  // ── FETCH ──
  async fetch(method, endpoint, data = null) {{
      let resolvedEndpoint = endpoint;
      if (window.__burqParams) {{
        resolvedEndpoint = endpoint.replace(/\\{{(\\w+)\\}}/g, (_, key) => window.__burqParams[key] || "");
      }}
      const url = this.apiBase + resolvedEndpoint;
      const opts = {{
        method,
        headers: {{
          "Content-Type": "application/json",
          ...(this.apiKey ? {{ "Authorization": `Bearer ${{this.apiKey}}` }} : {{}})
        }},
      }};
      if (data && method !== "GET") opts.body = JSON.stringify(data);
      const res = await fetch(url, opts);
      if (!res.ok) throw new Error(`Burq fetch error: ${{res.status}} ${{res.statusText}}`);
      return res.json();
  }},

  // ── NAVIGATE ──
  navigate(href) {{
    window.location.href = href;
  }},

  // ── RELOAD ──
  reload() {{
    window.location.reload();
  }},
}};

// ── TOAST MANAGER ──
const ToastManager = {{
  container: null,

  init() {{
    this.container = document.createElement("div");
    this.container.className = "toast-container";
    document.body.appendChild(this.container);
  }},

  show({{ title, message = "", type = "info", duration = 3000 }}) {{
    const icons = {{
      success: "circle-check",
      error:   "circle-x",
      warning: "triangle-alert",
      info:    "info"
    }};
    const toast = document.createElement("div");
    toast.className = `toast toast--${{type}}`;
    toast.innerHTML = `
      <i data-lucide="${{icons[type]}}" class="toast__icon"></i>
      <div class="toast__body">
        <div class="toast__title">${{title}}</div>
        ${{message ? `<div class="toast__message">${{message}}</div>` : ""}}
      </div>
      <button class="toast__close">
        <i data-lucide="x" style="width:12px;height:12px;"></i>
      </button>
    `;
    this.container.appendChild(toast);
    lucide.createIcons();

    const dismiss = () => {{
      toast.classList.add("toast--dismissing");
      setTimeout(() => toast.remove(), 200);
    }};

    toast.querySelector(".toast__close").addEventListener("click", dismiss);
    if (duration > 0) setTimeout(dismiss, duration);
  }}
}};

// ── MODAL MANAGER ──
const ModalManager = {{
  open(id) {{
    const overlay = document.getElementById(id);
    if (!overlay) return;
    overlay.style.display = "flex";
    requestAnimationFrame(() => overlay.classList.add("overlay--open"));
    document.body.style.overflow = "hidden";
  }},

  close(id) {{
    const overlay = document.getElementById(id);
    if (!overlay) return;
    overlay.classList.remove("overlay--open");
    setTimeout(() => {{
      overlay.style.display = "none";
      document.body.style.overflow = "";
    }}, 150);
  }},

  init() {{
    document.querySelectorAll(".overlay").forEach(overlay => {{
      overlay.style.display = "none";
      overlay.addEventListener("click", e => {{
        if (e.target === overlay) this.close(overlay.id);
      }});
    }});
    document.addEventListener("keydown", e => {{
      if (e.key === "Escape") {{
        const open = document.querySelector(".overlay--open");
        if (open) this.close(open.id);
      }}
    }});
  }}
}};

// ── TABS ──
function initTabs() {{
  document.querySelectorAll(".tabs").forEach(tabs => {{
    const triggers = tabs.querySelectorAll(".tabs__trigger");
    const panels   = tabs.querySelectorAll(".tabs__panel");
    triggers.forEach((trigger, i) => {{
      trigger.addEventListener("click", () => {{
        triggers.forEach(t => t.classList.remove("tabs__trigger--active"));
        panels.forEach(p => p.classList.remove("tabs__panel--active"));
        trigger.classList.add("tabs__trigger--active");
        if (panels[i]) panels[i].classList.add("tabs__panel--active");
      }});
    }});
    if (triggers.length) {{
      triggers[0].classList.add("tabs__trigger--active");
      if (panels[0]) panels[0].classList.add("tabs__panel--active");
    }}
  }});
}}

// ── DROPDOWNS ──
function initDropdowns() {{
  document.querySelectorAll(".dropdown").forEach(dropdown => {{
    const trigger = dropdown.querySelector("[data-dropdown-trigger]");
    const menu    = dropdown.querySelector(".dropdown__menu");
    if (!trigger || !menu) return;

    trigger.addEventListener("click", e => {{
      e.stopPropagation();
      const isOpen = menu.classList.contains("dropdown__menu--open");
      document.querySelectorAll(".dropdown__menu--open")
        .forEach(m => m.classList.remove("dropdown__menu--open"));
      if (!isOpen) menu.classList.add("dropdown__menu--open");
    }});

    menu.addEventListener("keydown", e => {{
      const items = [...menu.querySelectorAll(".dropdown__item:not(.dropdown__item--disabled)")];
      const idx   = items.indexOf(document.activeElement);
      if (e.key === "ArrowDown") {{ e.preventDefault(); items[Math.min(idx+1, items.length-1)]?.focus(); }}
      if (e.key === "ArrowUp")   {{ e.preventDefault(); items[Math.max(idx-1, 0)]?.focus(); }}
      if (e.key === "Escape")    {{ menu.classList.remove("dropdown__menu--open"); trigger.focus(); }}
    }});
  }});

  document.addEventListener("click", () => {{
    document.querySelectorAll(".dropdown__menu--open")
      .forEach(m => m.classList.remove("dropdown__menu--open"));
  }});
}}

// ── CUSTOM SELECTS ──
function initCustomSelects() {{
  document.querySelectorAll(".custom-select").forEach(select => {{
    const trigger     = select.querySelector(".custom-select__trigger");
    const dropdown    = select.querySelector(".custom-select__dropdown");
    const searchInput = select.querySelector(".custom-select__search-input");
    const optionsList = select.querySelector(".custom-select__options");
    const placeholder = select.querySelector(".custom-select__placeholder");
    const valueEl     = select.querySelector(".custom-select__value");
    const clearBtn    = select.querySelector(".custom-select__clear");
    const options     = Array.from(select.querySelectorAll(".custom-select__option"));
    let focusedIndex  = -1;

    function open() {{
      trigger.classList.add("custom-select__trigger--open");
      dropdown.classList.add("custom-select__dropdown--open");
      searchInput.value = "";
      filterOptions("");
      searchInput.focus();
      focusedIndex = -1;
    }}

    function close() {{
      trigger.classList.remove("custom-select__trigger--open");
      dropdown.classList.remove("custom-select__dropdown--open");
    }}

    function selectOption(option) {{
      options.forEach(o => {{
        o.classList.remove("custom-select__option--selected");
        o.querySelector(".custom-select__option-check").style.display = "none";
      }});
      option.classList.add("custom-select__option--selected");
      option.querySelector(".custom-select__option-check").style.display = "";
      placeholder.style.display = "none";
      valueEl.textContent = option.dataset.label || option.textContent.trim();
      valueEl.style.display = "";
      clearBtn.style.display = "";
      close();
    }}

    function clearSelection() {{
      options.forEach(o => {{
        o.classList.remove("custom-select__option--selected");
        o.querySelector(".custom-select__option-check").style.display = "none";
      }});
      placeholder.style.display = "";
      valueEl.style.display = "none";
      clearBtn.style.display = "none";
    }}

    function filterOptions(query) {{
      let visible = [];
      options.forEach(o => {{
        const match = o.textContent.toLowerCase().includes(query.toLowerCase());
        o.style.display = match ? "" : "none";
        if (match) visible.push(o);
      }});
      const empty = optionsList.querySelector(".custom-select__empty");
      if (empty) empty.style.display = visible.length ? "none" : "";
      focusedIndex = -1;
    }}

    function setFocus(index) {{
      const visible = options.filter(o => o.style.display !== "none");
      visible.forEach(o => o.classList.remove("custom-select__option--focused"));
      if (index >= 0 && index < visible.length) {{
        visible[index].classList.add("custom-select__option--focused");
        visible[index].scrollIntoView({{ block: "nearest" }});
        focusedIndex = index;
      }}
    }}

    valueEl.style.display  = "none";
    clearBtn.style.display = "none";
    options.forEach(o => {{
      o.querySelector(".custom-select__option-check").style.display = "none";
    }});

    trigger.addEventListener("click", () => {{
      dropdown.classList.contains("custom-select__dropdown--open") ? close() : open();
    }});

    clearBtn.addEventListener("click", e => {{ e.stopPropagation(); clearSelection(); }});
    searchInput.addEventListener("input", e => filterOptions(e.target.value));

    searchInput.addEventListener("keydown", e => {{
      const visible = options.filter(o => o.style.display !== "none");
      if (e.key === "ArrowDown") {{ e.preventDefault(); setFocus(Math.min(focusedIndex+1, visible.length-1)); }}
      if (e.key === "ArrowUp")   {{ e.preventDefault(); setFocus(Math.max(focusedIndex-1, 0)); }}
      if (e.key === "Enter" && focusedIndex >= 0) {{ selectOption(visible[focusedIndex]); }}
      if (e.key === "Escape") close();
    }});

    options.forEach(o => o.addEventListener("click", () => selectOption(o)));
    document.addEventListener("click", e => {{ if (!select.contains(e.target)) close(); }});
  }});
}}

// ── TABLE HYDRATION ──
async function initTables() {{
  const tables = document.querySelectorAll(".table-wrapper[data-fetch-endpoint]");
  for (const wrapper of tables) {{
    const method       = wrapper.dataset.fetchMethod   || "GET";
    const endpoint     = wrapper.dataset.fetchEndpoint || "";
    const columns      = (wrapper.dataset.columns || "").split(",").filter(Boolean);
    const checkable    = wrapper.dataset.checkable === "true";
    const actions      = (wrapper.dataset.actions  || "").split(",").filter(Boolean);
    const columnConfig = JSON.parse(wrapper.dataset.columnConfig || "{{}}");
    const rowHref      = wrapper.dataset.rowHref || "";

    if (!endpoint) continue;

    try {{
      const allData = await Burq.fetch(method, endpoint);
      const tbody   = wrapper.querySelector("tbody");
      if (!tbody || !Array.isArray(allData)) continue;

      const PAGE_SIZE  = 10;
      let currentPage  = 1;
      let filteredData = [...allData];

      const renderRow = (row) => {{
        const checkTd = checkable
          ? `<td class="table__checkbox-col"><input type="checkbox" class="table__checkbox" /></td>`
          : "";

        const cells = columns.map(col => {{
          const raw = row[col] ?? "";
          const val = typeof raw === "object" && raw !== null
            ? (raw?.value ?? JSON.stringify(raw))
            : String(raw);
          const cfg = columnConfig[col];

          if (!cfg) return `<td>${{val}}</td>`;

          switch (cfg.type) {{
            case "BadgeColumn": {{
              const variantMap = cfg.variant_map || {{}};
              const variant    = variantMap[val.toLowerCase()] || "default";
              const label      = val.charAt(0).toUpperCase() + val.slice(1);
              return `<td><span class="badge badge--${{variant}}">${{label}}</span></td>`;
            }}
            case "AvatarColumn": {{
              const name     = row[cfg.initials_key || col] || "";
              const initials = name.split(" ").map(w => w[0]).join("").slice(0,2).toUpperCase();
              const sub      = cfg.sub_key ? row[cfg.sub_key] || "" : "";
              const subHtml  = sub ? `<div class="table__cell-sub">${{sub}}</div>` : "";
              return `<td>
                <div class="table__cell-with-avatar">
                  <div class="table__avatar">${{initials}}</div>
                  <div>
                    <div class="table__cell-name">${{name}}</div>
                    ${{subHtml}}
                  </div>
                </div>
              </td>`;
            }}
            case "CurrencyColumn": {{
              const prefix   = cfg.prefix || "$";
              const decimals = cfg.decimals ?? 0;
              const num      = parseFloat(val) || 0;
              return `<td>${{prefix}}${{num.toLocaleString("en-US", {{minimumFractionDigits: decimals, maximumFractionDigits: decimals}})}}</td>`;
            }}
            case "DateColumn": {{
              const date      = new Date(val);
              const formatted = isNaN(date) ? val : date.toLocaleDateString("en-US", {{year:"numeric", month:"short", day:"numeric"}});
              return `<td>${{formatted}}</td>`;
            }}
            case "BoolColumn": {{
              const isTrue  = val === "true" || val === "1" || val === "True";
              const label   = isTrue ? (cfg.true_label   || "Yes") : (cfg.false_label   || "No");
              const variant = isTrue ? (cfg.true_variant || "success") : (cfg.false_variant || "danger");
              return `<td><span class="badge badge--${{variant}}">${{label}}</span></td>`;
            }}
            case "TextColumn": {{
              const cls = cfg.muted ? ' class="muted"' : "";
              return `<td${{cls}}>${{val}}</td>`;
            }}
            default:
              return `<td>${{val}}</td>`;
          }}
        }}).join("");

        const actionTd = actions.length
          ? `<td class="table__actions-col">
               <button class="table__action-btn" onclick="event.stopPropagation()">
                 <i data-lucide="ellipsis" class="table__action-icon"></i>
               </button>
             </td>`
          : "";

        if (rowHref) {{
          const href = rowHref.replace(/\\{{(\\w+)\\}}/g, (_, k) => row[k] ?? "");
          return `<tr style="cursor:pointer;" onclick="window.location.href='${{href}}'">${{checkTd}}${{cells}}${{actionTd}}</tr>`;
        }}

        return `<tr>${{checkTd}}${{cells}}${{actionTd}}</tr>`;
      }};

      const renderPage = () => {{
        const start    = (currentPage - 1) * PAGE_SIZE;
        const end      = start + PAGE_SIZE;
        const pageData = filteredData.slice(start, end);

        if (filteredData.length === 0) {{
          tbody.innerHTML = `
            <tr><td colspan="99">
              <div class="empty-state">
                <div class="empty-state__icon"><i data-lucide="inbox"></i></div>
                <div class="empty-state__title">No data yet</div>
                <p class="empty-state__message">Nothing to show here.</p>
              </div>
            </td></tr>`;
          lucide.createIcons();
          const info = wrapper.querySelector(".table-pagination__info");
          if (info) info.textContent = "0 results";
          const controls = wrapper.querySelector(".table-pagination__controls");
          if (controls) controls.innerHTML = "";
          return;
        }}

        tbody.innerHTML = pageData.map(renderRow).join("");
        lucide.createIcons();
        updatePagination();
      }};

      const updatePagination = () => {{
        const total      = filteredData.length;
        const totalPages = Math.ceil(total / PAGE_SIZE);
        const start      = Math.min((currentPage - 1) * PAGE_SIZE + 1, total);
        const end        = Math.min(currentPage * PAGE_SIZE, total);

        const info = wrapper.querySelector(".table-pagination__info");
        if (info) info.textContent = total > 0
          ? `Showing ${{start}}–${{end}} of ${{total}}`
          : "No results";

        const controls = wrapper.querySelector(".table-pagination__controls");
        if (!controls) return;

        controls.innerHTML = "";

        const prev = document.createElement("button");
        prev.className = "table-pagination__btn";
        prev.innerHTML = `<i data-lucide="chevron-left" style="width:14px;height:14px;"></i>`;
        prev.disabled  = currentPage === 1;
        prev.addEventListener("click", () => {{ currentPage--; renderPage(); }});
        controls.appendChild(prev);

        for (let i = 1; i <= totalPages; i++) {{
          if (totalPages > 7 && i > 2 && i < totalPages - 1 && Math.abs(i - currentPage) > 1) {{
            if (i === 3 || i === totalPages - 2) {{
              const dots = document.createElement("span");
              dots.className = "table-pagination__btn";
              dots.textContent = "…";
              dots.style.cursor = "default";
              controls.appendChild(dots);
            }}
            continue;
          }}
          const btn = document.createElement("button");
          btn.className = "table-pagination__btn" + (i === currentPage ? " table-pagination__btn--active" : "");
          btn.textContent = i;
          btn.addEventListener("click", () => {{ currentPage = i; renderPage(); }});
          controls.appendChild(btn);
        }}

        const next = document.createElement("button");
        next.className = "table-pagination__btn";
        next.innerHTML = `<i data-lucide="chevron-right" style="width:14px;height:14px;"></i>`;
        next.disabled  = currentPage === totalPages || totalPages === 0;
        next.addEventListener("click", () => {{ currentPage++; renderPage(); }});
        controls.appendChild(next);

        lucide.createIcons();
      }};

      // ── SEARCH ──
      const searchInput = wrapper.querySelector(".table-search__input");
      if (searchInput) {{
        searchInput.addEventListener("input", e => {{
          const query = e.target.value.toLowerCase().trim();
          filteredData = query
            ? allData.filter(row =>
                columns.some(col => {{
                  const val = String(row[col] ?? "").toLowerCase();
                  return val.includes(query);
                }})
              )
            : [...allData];
          currentPage = 1;
          renderPage();
        }});
      }}

      renderPage();

    }} catch (err) {{
      console.error(`Burq table error (${{endpoint}}):`, err);
      const tbody = wrapper.querySelector("tbody");
      if (tbody) tbody.innerHTML = `
        <tr><td colspan="99" style="text-align:center;padding:var(--space-6);color:var(--muted-foreground);">
          Failed to load data.
        </td></tr>`;
    }}
  }}
}}

// ── CHART HYDRATION ──
async function initCharts() {{
  if (typeof Chart === "undefined") return;

  const canvases = document.querySelectorAll("canvas[data-chart-type]");
  const style    = getComputedStyle(document.documentElement);

  const rawColors = style.getPropertyValue("--chart-colors").trim().replace(/^'|'$/g, "");
  let colors;
  try {{
    colors = JSON.parse(rawColors);
  }} catch(_) {{
    colors = ["#F08C1A","#60a5fa","#2ec97a","#e05252","#c97a2e","#a78bfa","#f472b6"];
  }}

  const fg     = style.getPropertyValue("--foreground").trim();
  const muted  = style.getPropertyValue("--muted-foreground").trim();
  const border = style.getPropertyValue("--border").trim();
  const surf   = style.getPropertyValue("--surface").trim();

  for (const canvas of canvases) {{
    const chartType     = canvas.dataset.chartType;
    const cfg           = JSON.parse(canvas.dataset.chartConfig || "{{}}");
    const fetchMethod   = canvas.dataset.fetchMethod   || "GET";
    const fetchEndpoint = canvas.dataset.fetchEndpoint || "";
    const inlineRaw     = canvas.dataset.inline        || "null";

    let rows = null;
    try {{
      if (fetchEndpoint) {{
        rows = await Burq.fetch(fetchMethod, fetchEndpoint);
      }} else {{
        rows = JSON.parse(inlineRaw);
      }}
    }} catch(e) {{
      console.error("Burq chart fetch error:", e);
      continue;
    }}

    if (!Array.isArray(rows) || rows.length === 0) continue;

    const yKeys = Array.isArray(cfg.y) ? cfg.y : [cfg.y];
    const xKey  = cfg.x || cfg.label;

    let chartConfig;

    if (chartType === "donut") {{
      const labels = rows.map(r => r[cfg.label]);
      const values = rows.map(r => r[cfg.value]);
      chartConfig = {{
        type: "doughnut",
        data: {{
          labels,
          datasets: [{{
            data:            values,
            backgroundColor: colors.slice(0, values.length),
            borderWidth:     2,
            borderColor:     surf,
          }}],
        }},
        options: {{
          responsive:          true,
          maintainAspectRatio: false,
          plugins: {{
            legend: {{
              position: "right",
              labels:   {{ color: fg, font: {{ size: 12 }} }},
            }},
          }},
        }},
      }};
    }} else {{
      const labels   = rows.map(r => r[xKey]);
      const datasets = yKeys.map((key, i) => {{
        const color  = colors[i % colors.length];
        const isArea = chartType === "area";
        const isBar  = chartType === "bar";
        return {{
          label:           key.replace(/_/g, " "),
          data:            rows.map(r => r[key]),
          borderColor:     color,
          backgroundColor: isArea
            ? color + "33"
            : isBar ? color : "transparent",
          tension:     cfg.smooth ? 0.4 : 0,
          fill:        isArea,
          pointRadius: isBar ? 0 : 3,
          borderWidth: 2,
        }};
      }});

      chartConfig = {{
        type: chartType === "bar" ? "bar" : "line",
        data: {{ labels, datasets }},
        options: {{
          responsive:          true,
          maintainAspectRatio: false,
          interaction:         {{ mode: "index", intersect: false }},
          plugins: {{
            legend: {{
              display: yKeys.length > 1,
              labels:  {{ color: fg, font: {{ size: 12 }} }},
            }},
          }},
          scales: {{
            x: {{
              stacked: cfg.stacked || false,
              grid:    {{ color: border }},
              ticks:   {{ color: muted, font: {{ size: 11 }} }},
            }},
            y: {{
              stacked: cfg.stacked || false,
              grid:    {{ color: border }},
              ticks:   {{ color: muted, font: {{ size: 11 }} }},
            }},
          }},
        }},
      }};
    }}

    new Chart(canvas, chartConfig);
  }}
}}

// ── SIDEBAR TOGGLE ──
function initSidebar() {{
  const layout = document.getElementById("layout");
  const toggle = document.getElementById("sidebarToggle");
  if (toggle && layout) {{
    toggle.addEventListener("click", () => {{
      layout.classList.toggle("layout--collapsed");
    }});
  }}
}}

// ── THEME TOGGLE ──
function initThemeToggle() {{
  const toggle = document.getElementById("themeToggle");
  const icon   = document.getElementById("themeIcon");
  const html   = document.documentElement;
  if (!toggle) return;

  const saved = localStorage.getItem("burq-theme");
  if (saved) {{
    html.setAttribute("data-theme", saved);
    if (icon) icon.setAttribute("data-lucide", saved === "dark" ? "sun" : "moon");
    lucide.createIcons();
  }}

  toggle.addEventListener("click", () => {{
    const current = html.getAttribute("data-theme");
    const next    = current === "dark" ? "light" : "dark";
    html.setAttribute("data-theme", next);
    localStorage.setItem("burq-theme", next);
    if (icon) {{
      icon.setAttribute("data-lucide", next === "dark" ? "sun" : "moon");
      lucide.createIcons();
    }}
  }});
}}

// ── ACTIVE NAV ──
function initActiveNav() {{
  const path = window.location.pathname;
  document.querySelectorAll(".nav-item[data-href]").forEach(a => {{
    const href = a.getAttribute("data-href");
    if (href === path || (href !== "/" && path.startsWith(href))) {{
      a.classList.add("nav-item--active");
    }}
  }});
}}

// ── URL PARAMS ──
function initUrlParams() {{
  const page = document.querySelector(".burq-page[data-url-pattern]");
  if (!page) return;
  const pattern = page.getAttribute("data-url-pattern");
  const path    = window.location.pathname;
  const keys    = [];
  const regexStr = pattern.replace(/\\{{(\\w+)\\}}/g, (_, k) => {{ keys.push(k); return "([^/]+)"; }});
  const match   = path.match(new RegExp("^" + regexStr + "$"));
  if (match) {{
    window.__burqParams = {{}};
    keys.forEach((k, i) => {{ window.__burqParams[k] = match[i+1]; }});
  }}
}}

// ── ACCORDIONS ──
function initAccordions() {{
  document.querySelectorAll(".accordion").forEach(accordion => {{
    const multiple = accordion.dataset.multiple === "true";
    accordion.querySelectorAll(".accordion__trigger").forEach(trigger => {{
      trigger.addEventListener("click", () => {{
        const item   = trigger.closest(".accordion__item");
        const isOpen = item.classList.contains("accordion__item--open");
        if (!multiple) {{
          accordion.querySelectorAll(".accordion__item--open")
            .forEach(i => i.classList.remove("accordion__item--open"));
        }}
        if (!isOpen) item.classList.add("accordion__item--open");
      }});
    }});
  }});
}}

// ── FILE UPLOADS ──
function initFileUploads() {{
  document.querySelectorAll(".file-upload").forEach(wrapper => {{
    const input   = wrapper.querySelector(".file-upload__input");
    const zone    = wrapper.querySelector(".file-upload__zone");
    const preview = wrapper.querySelector(".file-upload__preview");
    const nameEl  = wrapper.querySelector(".file-upload__filename");
    if (!input || !zone) return;

    function showFile(file) {{
      if (!file) return;
      zone.style.display    = "none";
      preview.style.display = "flex";
      nameEl.textContent    = file.name;
      lucide.createIcons();
    }}

    input.addEventListener("change", () => {{
      if (input.files[0]) showFile(input.files[0]);
    }});

    zone.addEventListener("dragover", e => {{
      e.preventDefault();
      wrapper.classList.add("file-upload--dragover");
    }});

    zone.addEventListener("dragleave", () => {{
      wrapper.classList.remove("file-upload--dragover");
    }});

    zone.addEventListener("drop", e => {{
      e.preventDefault();
      wrapper.classList.remove("file-upload--dragover");
      const file = e.dataTransfer.files[0];
      if (file) {{
        const dt = new DataTransfer();
        dt.items.add(file);
        input.files = dt.files;
        showFile(file);
      }}
    }});
  }});
}}

function burqClearFile(uid) {{
  const wrapper = document.getElementById(uid);
  if (!wrapper) return;
  const input   = wrapper.querySelector(".file-upload__input");
  const zone    = wrapper.querySelector(".file-upload__zone");
  const preview = wrapper.querySelector(".file-upload__preview");
  input.value           = "";
  zone.style.display    = "";
  preview.style.display = "none";
}}

// ── RICH TEXT EDITOR ──
function rteExec(cmd, uid) {{
  var editor = document.getElementById(uid);
  if (!editor) return;
  editor.focus();
  document.execCommand(cmd, false, null);
  rteSyncEditor(uid);
}}

function rteHeading(sel, uid) {{
  var editor = document.getElementById(uid);
  if (!editor) return;
  editor.focus();
  var val = sel.value;
  document.execCommand("formatBlock", false, val || "p");
  rteSyncEditor(uid);
}}

function rteBlockquote(uid) {{
  var editor = document.getElementById(uid);
  if (!editor) return;
  editor.focus();
  document.execCommand("formatBlock", false, "blockquote");
  rteSyncEditor(uid);
}}

function rteInlineCode(uid) {{
  var editor = document.getElementById(uid);
  if (!editor) return;
  editor.focus();
  var sel = window.getSelection();
  if (!sel.rangeCount) return;
  var range = sel.getRangeAt(0);
  var selected = range.toString();
  if (!selected) return;
  var code = document.createElement("code");
  code.textContent = selected;
  range.deleteContents();
  range.insertNode(code);
  rteSyncEditor(uid);
}}

function rteCodeBlock(uid) {{
  var editor = document.getElementById(uid);
  if (!editor) return;
  editor.focus();
  var sel = window.getSelection();
  var selected = sel.rangeCount ? sel.getRangeAt(0).toString() : "";
  var pre = document.createElement("pre");
  var code = document.createElement("code");
  code.textContent = selected || "// code here";
  pre.appendChild(code);
  if (sel.rangeCount) {{
    var range = sel.getRangeAt(0);
    range.deleteContents();
    range.insertNode(pre);
  }} else {{
    editor.appendChild(pre);
  }}
  rteSyncEditor(uid);
}}

function rteLink(uid) {{
  var url = prompt("URL:");
  if (url) rteExec("createLink", uid);
}}

function rteSyncEditor(uid) {{
  var editor  = document.getElementById(uid);
  var hidden  = document.getElementById(uid + "-hidden");
  var counter = document.getElementById(uid + "-count");
  if (!editor) return;
  var md = burqHtmlToMarkdown(editor.innerHTML);
  if (hidden)  hidden.value = md;
  if (counter) counter.textContent = editor.innerText.replace(/\\n/g, "").length + " chars";
}}

function burqHtmlToMarkdown(html) {{
  var div = document.createElement("div");
  div.innerHTML = html;
  function nodeToMd(node) {{
    if (node.nodeType === 3) return node.textContent;
    if (node.nodeType !== 1) return "";
    var tag   = node.tagName.toLowerCase();
    var inner = function() {{ return Array.from(node.childNodes).map(nodeToMd).join(""); }};
    if (tag === "br")  return "\\n";
    if (tag === "p" || tag === "div") return inner() + "\\n\\n";
    if (tag === "h1")  return "# "   + inner() + "\\n\\n";
    if (tag === "h2")  return "## "  + inner() + "\\n\\n";
    if (tag === "h3")  return "### " + inner() + "\\n\\n";
    if (tag === "strong" || tag === "b") return "**" + inner() + "**";
    if (tag === "em"     || tag === "i") return "_"  + inner() + "_";
    if (tag === "s"      || tag === "del") return "~~" + inner() + "~~";
    if (tag === "a") return "[" + inner() + "](" + (node.href || "") + ")";
    if (tag === "code" && node.parentElement && node.parentElement.tagName.toLowerCase() !== "pre")
      return "`" + inner() + "`";
    if (tag === "pre") {{
      var codeEl = node.querySelector("code");
      return "```\\n" + (codeEl ? codeEl.textContent : node.textContent) + "\\n```\\n\\n";
    }}
    if (tag === "blockquote") return inner().split("\\n").map(function(l) {{ return "> " + l; }}).join("\\n") + "\\n\\n";
    if (tag === "ul") {{
      return Array.from(node.querySelectorAll(":scope > li"))
        .map(function(li) {{ return "- " + li.innerText; }}).join("\\n") + "\\n\\n";
    }}
    if (tag === "ol") {{
      return Array.from(node.querySelectorAll(":scope > li"))
        .map(function(li, i) {{ return (i+1) + ". " + li.innerText; }}).join("\\n") + "\\n\\n";
    }}
    return inner();
  }}
  return Array.from(div.childNodes).map(nodeToMd).join("")
    .replace(/\\n{{3,}}/g, "\\n\\n").trim();
}}

// ── NAV GROUPS ──
function initNavGroups() {{
  document.querySelectorAll(".nav-group__trigger").forEach(trigger => {{
    trigger.addEventListener("click", () => {{
      trigger.closest(".nav-group").classList.toggle("nav-group--open");
    }});
  }});

  const path = window.location.pathname;
  document.querySelectorAll(".nav-group").forEach(group => {{
    const active = group.querySelector(`.nav-item[data-href="${{path}}"]`);
    if (active) group.classList.add("nav-group--open");
  }});
}}

// ── INIT ──
function burqInit() {{
  ToastManager.init();
  ModalManager.init();
  initSidebar();
  initThemeToggle();
  initTabs();
  initDropdowns();
  initCustomSelects();
  initAccordions();
  initUrlParams();
  initTables();
  initTableExport();
  initCharts();
  initActiveNav();
  initFileUploads();
  initNavGroups();
  lucide.createIcons();
}}

if (document.readyState === "loading") {{
  document.addEventListener("DOMContentLoaded", burqInit);
}} else {{
  burqInit();
}}
"""

    export_js = r"""
// ── TABLE EXPORT ──
function initTableExport() {
  document.querySelectorAll(".table-wrapper[data-fetch-endpoint]").forEach(wrapper => {
    const endpoint  = wrapper.dataset.fetchEndpoint || "export";
    const exportBtn = wrapper.querySelector(".btn--secondary");
    if (!exportBtn) return;
    exportBtn.addEventListener("click", () => {
      const table   = wrapper.querySelector("table");
      const headers = [...table.querySelectorAll("thead th")]
        .filter(th => !th.classList.contains("table__checkbox-col") && !th.classList.contains("table__actions-col"))
        .map(th => th.textContent.trim().replace(/\s+/g, " "));
      const rows = [...table.querySelectorAll("tbody tr")].map(tr =>
        [...tr.querySelectorAll("td")]
          .filter(td => !td.classList.contains("table__checkbox-col") && !td.classList.contains("table__actions-col"))
          .map(td => { const t = td.innerText.trim().replace(/\n/g, " ").replace(/,/g, ";"); return `"${t}"`; })
      );
      const csv  = [headers.join(","), ...rows.map(r => r.join(","))].join("\n");
      const blob = new Blob([csv], { type: "text/csv" });
      const url  = URL.createObjectURL(blob);
      const a    = document.createElement("a");
      a.href     = url;
      a.download = endpoint.replace(/\//g, "_").replace(/^_/, "") + ".csv";
      a.click();
      URL.revokeObjectURL(url);
    });
  });
}
"""

    return main_js + export_js