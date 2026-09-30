# Frontend notes — changes, hooks & variables

Reference for the HTML/CSS rebuild of the anonymous project/thought sharing site.
Everything here is additive: **no existing JS file was edited and no Python was touched.**

---

## 1. Theme system (light / dark)

| Item | Value |
| --- | --- |
| Toggle control | `#theme-toggle` (checkbox) + `.theme-toggle` (label button), rendered on **every** page by `layout.html` |
| Stored value | `localStorage["theme"]` → `"light"` or `"dark"` |
| Applied to | `<html data-theme="light">` (absent / `dark` = dark theme) |
| CSS driver | `static/base.css` → `html[data-theme="light"] { …tokens… }` |
| No-JS fallback | `html:has(#theme-toggle:checked) { …same tokens… }` |
| No flash | the theme is read in a `<head>` script **before** the page paints |
| Browser chrome | `<meta id="theme-color-meta">` is updated to `#f5f6f8` / `#0e0e11` |

**How it behaves:** click the button once → the choice is saved and *every* page
(now and later) opens in that theme. `localStorage` is per-browser, per-origin, so
it survives reloads and navigation.

> **Important:** CSS alone cannot remember a choice between page loads, so this is the
> one place where a small **inline** `<script>` was added — two of them, both inside
> `templates/layout.html`. They are self-contained, do not create a `.js` file, and do
> not touch `homepage.js` / `upload.js`.

To add the toggle's theme to a *new* page, just make sure it extends `layout.html`.

---

## 2. Files

| File | Status | Purpose |
| --- | --- | --- |
| `static/base.css` | rewritten | design tokens + both themes, reset, buttons, app shell/sidebar, search, panels, theme toggle, responsive |
| `static/feed.css` | new | `index.html` feed: layout, right rail, filter bar, posts, bottom-fixed composer |
| `static/homepage.css` | rewritten | `homepage.html` dashboard: header, CSS-only tabs, toolbar, file list, placeholders |
| `static/upload.css` | rewritten | `upload.html` two-column uploader |
| `static/login.css` | rewritten | `login.html` + `register.html` form card |
| `static/page.css` | rewritten | `about.html` + `Repo.html` content pages |
| `static/style.css` | **unused** | old landing-page styles — safe to delete |
| `static/index.css` | **unused** | old sidebar styles — safe to delete |
| `templates/layout.html` | rewritten | shell: head/meta/favicon, theme toggle + theme scripts, blocks |
| `templates/index.html` | rewritten | anonymous feed |
| `templates/homepage.html` | rewritten | management dashboard |
| `templates/upload.html` | rewritten | upload page |
| `templates/login.html` | rewritten | sign in |
| `templates/register.html` | rewritten | sign up |
| `templates/about.html` | rewritten | contact/about |
| `templates/Repo.html` | rewritten | repository placeholder |

### Design language
- Flat surfaces, **small radii** (`--radius-lg: 6px`, `--radius: 4px`, `--radius-sm: 4px`); only avatars are round.
- **Glass** is limited to the sidebar, top bar and composer bar (`backdrop-filter: blur`).
- **No** gradients, glows or background photo (`background1.jpg` is no longer referenced).
- All icons are **inline stroke SVGs using `currentColor`**, so they render light-on-dark
  and dark-on-light automatically. (Inactive nav items use `--text-2`, active uses `--text`.)

### CSS variables (design tokens, defined in `base.css`)
`--bg`, `--bg-soft`, `--surface`, `--surface-2`, `--surface-3`, `--border`, `--border-strong`,
`--text`, `--text-2`, `--text-3`, `--accent`, `--accent-strong`, `--accent-soft`,
`--accent-contrast`, `--green`, `--green-soft`, `--red`, `--glass`, `--glass-strong`,
`--shadow`, `--radius-lg`, `--radius`, `--radius-sm`, `--sidebar-w`, `--font`.
Every token is declared twice: dark in `:root`, light under `html[data-theme="light"]`.

---

## 3. Hooks per page

**Legend:** 🆕 = added by me (free to use in your JS) · 🔒 = pre-existing, **do not rename**
(used by your JS or Flask).

### 3.1 `templates/layout.html` (shared by every page)

| Hook | Kind | Notes |
| --- | --- | --- |
| `#theme-toggle` | 🆕 | checkbox that drives the theme |
| `#theme-color-meta` | 🆕 | `<meta>` whose `content` follows the theme |
| `.theme-toggle`, `.toggle-icon`, `.toggle-icon-sun`, `.toggle-icon-moon` | 🆕 | toggle button styling |
| `{% block style %}` / `{% block title %}` / `{% block body %}` | 🔒 | Jinja blocks all pages fill |

### 3.2 `templates/index.html` — the feed

| Hook | Kind | Notes |
| --- | --- | --- |
| `#login` | 🔒 | inline script attaches click → `/login` |
| `#logout` | 🔒 | inline script attaches click → `fetch('/logout')` |
| `{{ prompt }}` | 🔒 | session username (or empty when logged out) |
| `#search-input` | 🆕 | feed search box |
| `#feed` | 🆕 | post list container (sample cards live here) |
| `#filter-all`, `#filter-projects`, `#filter-thoughts` | 🆕 | feed filter buttons |
| `#composer`, `#composer-input`, `#post-button` | 🆕 | bottom-fixed post box |
| `#compose-button` | 🆕 | sidebar "Post" button (anchors to `#composer`) |
| `.app`, `.sidebar`, `.sidebar-brand`, `.sidebar-nav`, `.nav-item`, `.nav-icon`, `.nav-text`, `.compose-button`, `.sidebar-footer`, `.sidebar-user`, `.sidebar-avatar`, `.sidebar-username`, `.sidebar-sub` | 🆕 | shell + sidebar |
| `.feed-topbar`, `.feed-layout`, `.feed-column`, `.right-rail`, `.rail-card`, `.rail-title`, `.tag-list`, `.tag-link`, `.tag-count`, `.rail-text` | 🆕 | layout + right rail |
| `.filter-bar`, `.filter-btn` | 🆕 | filter tabs |
| `.composer-bar`, `.composer-bar-inner`, `.composer-avatar`, `.composer-hint` | 🆕 | fixed composer |
| `.post`, `.post-head`, `.post-avatar`, `.post-author`, `.post-meta`, `.post-menu`, `.post-type` (`.project` / `.thought`), `.post-title`, `.post-body`, `.post-tags`, `.post-tag`, `.post-actions`, `.post-action` (+ state `.liked`) | 🆕 | post cards; each card carries `data-post-id` |

### 3.3 `templates/homepage.html` — dashboard

| Hook | Kind | Notes |
| --- | --- | --- |
| `#file-list` | 🔒 | `homepage.js` reads it + `dataset.user` |
| `data-user="{{ session['user'] }}"` | 🔒 | read by `homepage.js` |
| `#file-empty` | 🔒 | empty state (now rendered only when `not file_existence`) |
| `{{ session['user'] }}`, `{% if file_existence %}` | 🔒 | Jinja |
| `.file-row`, `.file-icon`, `.file-name`, `.file-size`, `.file-modified` | 🔒 | class names `homepage.js` creates — **must stay** |
| `.file-list-header`, `.col-gutter`, `.col-name`, `.col-size`, `.col-modified` | 🆕 | list header (4-column grid) |
| `#search-input`, `#sort-select`, `#refresh-button` | 🆕 | file toolbar |
| `#tab-files`, `#tab-projects`, `#tab-posts` (radios) | 🆕 | CSS-only tab switcher |
| `#panel-files`, `#panel-projects`, `#panel-posts` | 🆕 | tab panels |
| `.tabs`, `.tab`, `.tab-radio`, `.tab-panel` | 🆕 | tab styling |
| `.dash-header`, `.breadcrumb`, `.dash-subtitle`, `.file-toolbar`, `.toolbar-spacer` | 🆕 | dashboard header/toolbar |
| `.placeholder-panel`, `.placeholder-icon` | 🆕 | Projects/Posts empty states |

Tabs are pure CSS: `#tab-files:checked ~ #panel-files { display:block }` etc. — no JS needed.

### 3.4 `templates/upload.html` — uploader

| Hook | Kind | Notes |
| --- | --- | --- |
| `#file-input`, `#folder-input` | 🔒 | read by `upload.js` |
| `name="file"` (both inputs) | 🔒 | Flask reads `request.files.getlist("file")` |
| `#preview-count`, `#preview-size`, `#preview-list`, `#preview-empty` | 🔒 | read by `upload.js` |
| `.preview-row`, `.preview-icon`, `.preview-name`, `.preview-size` | 🔒 | classes `upload.js` creates — **must stay** |
| `#clear-button` | 🆕 | "clear selection" button (no logic attached) |
| `.upload-topbar`, `.back-link`, `.topbar-title`, `.drop-zone`, `.drop-icon`, `.drop-text`, `.drop-title`, `.drop-subtitle`, `.preview-stats`, `.preview-header` | 🆕 | styling |

### 3.5 `templates/login.html` / `templates/register.html`

| Hook | Kind | Notes |
| --- | --- | --- |
| `name="username"`, `name="password"` | 🔒 | login POST |
| `name="fullname"`, `name="email"`, `name="password"`, `name="confirm_password"`, `name="gender"`, `name="terms"` | 🔒 | register POST |
| `#male`, `#female`, `#others` | 🔒 | targeted by radio `onclick` |
| `#terms`, `#alert-container`, `#prompt-text` | 🔒 | form + Flask flash area |
| `onclick="togglePassword('password')"`, `onclick="togglePassword('confirm_password')"`, `onclick="document.getElementById('male').click()"` (etc.) | 🔒 | inline handlers kept verbatim |
| `{{ prompt }}` | 🔒 | error message |
| `.glass-form`, `.form-avatar`, `.form-title`, `.form-subtitle`, `.input-group`, `.input-label`, `.input-wrapper`, `.input-icon`, `.glass-input`, `.toggle-password`, `.radio-group`, `.radio-option`, `.checkbox-group`, `.glass-button`, `.form-footer`, `.page-back` | 🆕 | styling |

### 3.6 `templates/about.html` / `templates/Repo.html`

| Hook | Kind | Notes |
| --- | --- | --- |
| `.page-back`, `.page-shell`, `.content-card`, `.eyebrow`, `.page-title`, `.page-lead` | 🆕 | shared page chrome |
| `.contact-list`, `.contact-item`, `.contact-icon`, `.contact-meta` | 🆕 | about page channels |
| `.repo-empty`, `.repo-empty-icon` | 🆕 | repo placeholder |

---

## 4. Known notes

1. **Two emoji remain, by design:** `.file-icon` (file rows) and `.preview-icon`
   (upload preview rows) are built by `homepage.js` / `upload.js`. Since those files
   must not change, their icons stay emoji. Swap them to inline SVG inside those two
   JS files if you want full line-icon consistency.
2. **Unused assets:** `static/background1.jpg`, `static/home.png`, `static/repo.png`,
   `static/style.css`, `static/index.css` are no longer referenced — safe to delete.
3. **Pre-existing data mismatches (untouched):**
   - `homepage.js` reads `item.name` / `item.size`, but `/api/files/<user>` returns
     `filename` / `filesize` → rows can show `undefined` until one side is aligned.
   - The register form sends `fullname` but no `username`/`phoneNumber`, while
     `register()` in `app.py` reads `username` / `email` / `phoneNumber`.
4. **Pre-existing JS ordering:** `homepage.js` assigns `permutation = []` after calling
   `init()`; it works only because that line runs synchronously before the fetch
   resolves. Fragile, but left untouched.
5. **`#compose-button`** currently just anchors to `#composer`. To focus the box, add:
   ```js
   document.getElementById('compose-button')
     .addEventListener('click', () => document.getElementById('composer-input').focus());
   ```
   Same idea for `#post-button`, `#refresh-button` and the filter buttons.
