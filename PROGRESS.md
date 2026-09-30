# Progress log — anonymous projects & thoughts site

**Project:** a site where people share projects and thoughts while staying anonymous
**Stack:** Flask (`app.py`, SQLite via SQLAlchemy) · Jinja2 templates · vanilla JS · hand-written CSS (no framework)
**Layout:** `templates/` = pages · `static/` = CSS + JS · `app.py` = routes
**Reference:** `FRONTEND_NOTES.md` = current hooks / variables per page

---

## How to use

- One entry per day, newest **at the top** (insert directly under the template).
- Copy the template block below, paste it above the previous entry, fill it in.
- Keep bullets to one line. Wrap file paths in backticks so they stay readable.
- Delete any section that doesn't apply — an entry with only *Done* and *Next* is fine.
- **Status legend:** ✅ done · 🚧 in progress · 🐞 blocked · 💤 paused

### Entry template (copy this)

```markdown
## YYYY-MM-DD — <one-line summary>

**Status:** ✅   **Time:** 1.5h   **Focus:** <area, e.g. dashboard>

### Done
-

### Changed files
- `path/to/file` — what changed and why

### New hooks / variables
- `#id` / `.class` — what it's for

### Decisions
- <what you chose + the reason>

### Blockers
- none

### Next
- [ ]
```

---

## 2026-09-30 — Frontend rebuilt: flat X/Reddit style, persistent light/dark

**Status:** ✅   **Time:** —   **Focus:** frontend (HTML + CSS)

### Done
- Replaced the old landing page with an anonymous **feed** (`index.html`) and a **management dashboard** (`homepage.html`).
- Sidebar restyled X-style with monochrome **line SVG icons**; corner radii cut to 4–6px; removed gradients, glows and the background photo.
- Feed widened to ~760px, added a Reddit-style right rail (trending tags + about), composer **pinned to the bottom**.
- Light/dark toggle now **persists across every page** (`localStorage` + `<html data-theme>`), applied before paint so there's no flash.
- Added a CSS-only **Select mode** that draws a circle at the start of every file row.
- Dashboard tabs (Files / Projects / Posts) implemented **without JS** via radio buttons.

### Changed files
- `static/base.css` — design tokens, both themes, sidebar shell, buttons, theme toggle
- `static/feed.css` — feed layout, right rail, bottom-fixed composer, post cards
- `static/homepage.css` — dashboard header, tabs, file list, select mode
- `static/upload.css`, `static/login.css`, `static/page.css` — restyled to the new tokens
- `templates/layout.html` — theme toggle + persistence scripts (only JS added)
- `templates/index.html`, `templates/homepage.html`, `templates/upload.html` — restructured
- `static/homepage.js` — swapped emoji icons for inline `ICONS` SVG constants *(your edit)*

### New hooks / variables
- `#theme-toggle`, `#theme-color-meta` — theme control + browser chrome colour
- `#search-input`, `#feed`, `#filter-all`, `#filter-projects`, `#filter-thoughts` — feed
- `#composer`, `#composer-input`, `#post-button`, `#compose-button` — composer
- `#select-toggle`, `.select-toggle`, `.select-toggle-input` — file select mode
- `#tab-files` / `#tab-projects` / `#tab-posts` + `#panel-*` — dashboard tabs
- `#sort-select`, `#refresh-button`, `#clear-button` — toolbar controls

### Decisions
- Kept the row selection circle as a CSS `::before` because `homepage.js` builds the rows, so no markup can live inside them.
- Chose a persisted `data-theme` attribute over the CSS-only `:has()` toggle, otherwise the choice is lost on every navigation.
- Used `:has()` for the theme anyway, as the no-JS fallback.

### Blockers
- none

### Next
- [ ] Add a real per-row `<input class="file-select">` in `homepage.js` and colour it on `:checked`
- [ ] Read the selection with a `Map` (checkbox → item) and enable a Delete / Move action
- [ ] Replace the last two emoji icons (`.file-icon`, `.preview-icon`) with SVG
- [ ] Show the current username in the feed sidebar when logged in

---

## Backlog / ideas

### Frontend
- [ ] `#select-all` checkbox in the file-list header
- [ ] Selected-count badge + bulk action bar (delete / move / download)
- [ ] Empty-state illustration for the feed when there are no posts
- [ ] Skeleton loaders while `/api/files` is fetching
- [ ] Keyboard shortcuts (`/` focuses `#search-input`, `n` focuses the composer)

### Backend
- [ ] `POST /api/posts` + a `Post` model (currently posts are static placeholders)
- [ ] Search endpoint for the feed
- [ ] Real authentication (passwords are stored in plain text today)
- [ ] Pagination for `/api/files` and the feed

### Bugs / debt
- [ ] Register form sends `fullname`, but `register()` reads `username` / `phoneNumber`
- [ ] `homepage.js` relies on `permutation = []` running before the fetch resolves
- [ ] `name.innerHTML = item.filename` is an XSS risk — use `textContent`
- [ ] Decide whether `static/style.css` and `static/index.css` can be deleted (now unused)

---

## Snapshot — 2026-09-30

| Area | State |
| --- | --- |
| Feed (`index.html`) | Layout ✅ · sample posts only 🚧 |
| Dashboard (`homepage.html`) | Files ✅ · Projects/Posts placeholders 🚧 |
| Upload (`upload.html`) | ✅ works, icons still partly emoji |
| Auth (`login` / `register`) | ✅ UI done · backend validation missing |
| Theming | ✅ light/dark, persists everywhere |
| Mobile | ✅ sidebar collapses to an icon rail |
