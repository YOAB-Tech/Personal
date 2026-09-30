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

## 2026-09-30 (session 2) — Select mode wired, cells are links, full project audit

**Status:** 🐞 blocked on backend   **Focus:** dashboard + code review

### Done
- Added a **Select** button to the file toolbar (CSS-only switch, `#select-toggle`).
- Added the **real per-row checkbox** `<input class="file-select">` as the first child of every row; `:checked` fills it with the accent colour + a white tick and tints the row.
- Guarded the drawn `::before` circle with `:not(:has(.file-select))`, so it only applies to rows that have no real checkbox — no double circles, and it removes itself once JS adds one.
- Converted the file-list **cells to links**: `.file-icon`, `.file-name`, `.file-size`, `.file-modified`, `.col-name`, `.col-size`, `.col-modified` are now `<a href="#">`; `.sidebar-avatar` links to the profile.
- Left the spans that already sit inside an `<a>` (`.brand-text`, `.nav-icon`, `.nav-text`, compose label) as spans — nested anchors are invalid HTML.
- Added the `LINK CELLS` CSS so the anchors look identical to the old spans.
- Documented it all in `FRONTEND_NOTES.md` (§3.3, corrected §4, new §5 Change log).
- Ran a **read-only audit** of `app.py`, `homepage.js`, `upload.js`, the templates and the SQLite DB.

### Changed files
- `templates/homepage.html` — select checkbox added, spans → `<a href>`
- `static/homepage.css` — new `SELECT MODE` and `LINK CELLS` blocks
- `FRONTEND_NOTES.md` — hooks table, corrected stale notes, new change log

### New hooks / variables
- `#select-toggle`, `.select-toggle`, `.select-toggle-input` — CSS-only select switch (must stay a sibling **before** `#file-list`)
- `.file-select` — the real per-row checkbox; **first child** of a `.file-row`
- `rowdata: Map` (in `homepage.js`) — checkbox element → file object

### Audit — problems found (nothing fixed yet)

**🔴 Blockers**

1. **Registration returns HTTP 500.** `register.html` sends `name="fullname"`, but `app.py:74` reads `request.form.get("username")` → `None`; the `username` column is `nullable=False` → `IntegrityError: NOT NULL constraint failed: User.username` at `app.py:87`. The form also never sends `phoneNumber` (`app.py:77`) — the DB confirms it: both users have `phonenumber = NULL`.
2. **`homepage.js` throws on load.** Lines 5–6 grab `#delete` and `#addtoproject`, and **neither id exists** in `homepage.html` → both are `null`, so `deletebutton.addEventListener(...)` at line 76 throws `TypeError: Cannot read properties of null`. The delete feature can never run.
3. **The selection always comes back empty.** `homepage.js:64` queries `'.file-list:checked'` — that's the container `<div class="file-list">`, not the checkboxes. It must be `'.file-select:checked'`, so `picked` is always `[]`.
4. **`/api/filedelete` is unreachable.** The route uses `<string:filepath>`, but Flask's `string` converter rejects `/`. The API returns `filepath = "Repo/admin/Daily"` (`app.py:158`) and the JS builds `/api/filedelete/admin/Repo/admin/Daily` → **404**.
5. **`/api/filedelete` is dangerous.** No auth check at all, and the raw URL segment goes straight into `Path(...)` with no validation — with a `<path:>` converter that becomes arbitrary file deletion. It also: crashes on folders (`rglob` returns directories and `unlink()` on one raises), compares a `str` to a `Path` (`app.py:175`, never matches), calls `.filepath` on a JSON **dict** (`AttributeError`), and `return 1` is not a valid Flask response.

**🟠 Security / authorization**

6. **IDOR on `/homepage/<username>`** (`app.py:91-98`) — only checks that *someone* is logged in, not that it's the right user, so `admin` can open `YOAB`'s dashboard. A non-existent user also 500s (`user.file` on `None`).
7. **`/upload/<username>` has no login check** (`app.py:108`) — anyone can upload into anyone's folder.
8. **Path traversal on upload** (`app.py:118-122`) — the `..` / leading-`/` guard misses absolute Windows paths: `Path('C:\evil.txt').as_posix()` → `'C:/evil.txt'` passes, and `personalfolder / 'C:\evil.txt'` discards the base and writes outside `Repo/`.
9. **Plain-text passwords** (`app.py:20, 62, 85`) — no hashing.
10. **No upload size limit** — `MAX_CONTENT_LENGTH` is unset (disk-fill DoS).

**🟡 Correctness**

11. **Duplicate rows in the DB on every upload** (`app.py:128-140`) — `fileinfo` is a *full* folder re-scan and it gets `extend()`ed, so the JSON column accumulates duplicates forever. Should be `user.file = fileinfo`.
12. **Wrong "modified" dates** (`app.py:133, 160`) — `datetime.now()` at scan time, so every upload resets every file to "just now". Use `item.stat().st_mtime`.
13. **`id = count + 1`** (`app.py:84`) — primary key derived from a row count → collides after any delete. Let the column auto-increment.
14. **`or` in the query is a silent no-op** (`app.py:78`) — verified against the installed SQLAlchemy 2.0.54: `User.username == username or User.email == email` evaluates to just `u.username = :username_1`, so the email-duplicate check is dropped. Use `db.or_(...)`.
15. **`Settings` / `Files` models are dead and unusable** — both tables exist but are empty and no route touches them. `Settings` has no `user_id` FK (can't be per-user; the theme really lives in `localStorage`), and `Files.author_id` is the PK, so a user could only ever have one row.
16. **`upload.js` double-counts** (lines 22-24, 51-52) — `size` / `number` are never reset, so re-picking files adds to the previous totals.
17. **`upload.js` duplicates preview rows** (lines 47-72) — rows are never cleared on re-pick; and `files[0]` (line 28) throws if the folder dialog is cancelled.
18. **Implicit globals / dead code** — `itemsize` (`homepage.js:48`), `totalsize` (`upload.js:26, 53`), `permutation` (`homepage.js:60`) have no declaration; `mergesort` is never called; `fileempty` and `folder` (`upload.js:11`) are unused.
19. **Stored XSS** (`homepage.js:45`) — `name.innerHTML = item.filename` writes a user-controlled filename as HTML. Use `textContent`.
20. **No fetch error handling** (`homepage.js:16-19`) — a failed request leaves an empty list with only a console error.

**⚪ Housekeeping** — unused `static/style.css` + `static/index.css`; unused `background1.jpg` / `home.png` / `repo.png`; unused imports in `app.py:1-7`; `debug=True` + hardcoded `SECRET_KEY`; dead `path = request.form.get("Path")` in `/repo`; and inert UI controls (`#search-input`, `#filter-*`, `#post-button`, `#sort-select`, `#refresh-button`, `#clear-button`).

### Decisions
- Fixed the double-circle risk structurally rather than by hand: the `::before` circle is now conditional on the row having no checkbox, so it removes itself automatically when `homepage.js` adds one.
- Left the spans inside `<a>` alone instead of producing invalid nested anchors.

### Blockers
- Registration is broken, so no new account can be created and the logged-in flows can't be tested end-to-end.

### Next
- [ ] Fix the register field mismatch (`fullname` vs `username`, missing `phoneNumber`) — highest priority
- [ ] Add `#delete` / `#addtoproject` to `homepage.html`, or null-guard them in `homepage.js`
- [ ] Fix `.file-list:checked` → `.file-select:checked` (`homepage.js:64`)
- [ ] Rework `/api/filedelete`: `<path:filepath>`, auth check, path validation, `shutil.rmtree`, `jsonify`
- [ ] Hash passwords and set `MAX_CONTENT_LENGTH`
- [ ] Replace `extend` with assignment in `/upload`

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

### Bugs / debt — from the 2026-09-30 audit (full detail in that entry)
- [ ] 🔴 Register 500s — form sends `fullname`, backend reads `username`; no `phoneNumber` field
- [ ] 🔴 `homepage.js` throws on load — `#delete` / `#addtoproject` don't exist in the HTML
- [ ] 🔴 `homepage.js:64` — `.file-list:checked` → `.file-select:checked`
- [ ] 🔴 `/api/filedelete` — route unreachable (`<string:>` can't take `/`) + no auth + unsanitised path
- [ ] 🟠 IDOR on `/homepage/<username>` and no login check on `/upload/<username>`
- [ ] 🟠 Path traversal in `/upload` via absolute Windows paths
- [ ] 🟠 Hash passwords (`generate_password_hash`); set `MAX_CONTENT_LENGTH`
- [ ] 🟡 `/upload` — `extend()` → assignment (duplicate rows pile up in the DB)
- [ ] 🟡 `datetime.now()` → `item.stat().st_mtime` for real modified dates
- [ ] 🟡 `id = count + 1` → let the primary key auto-increment
- [ ] 🟡 `or` → `db.or_(...)` in the register lookup (email check is silently dropped)
- [ ] 🟡 `upload.js` — reset `size`/`number`, clear rows on re-pick, guard `files[0]`
- [ ] 🟡 `name.innerHTML` → `textContent` (stored XSS via filename)
- [ ] ⚪ Delete unused `style.css`, `index.css`, `background1.jpg`, `home.png`, `repo.png`
- [ ] ⚪ Remove unused imports + `debug=True` + hardcoded `SECRET_KEY`

---

## Snapshot — 2026-09-30

| Area | State |
| --- | --- |
| Feed (`index.html`) | Layout ✅ · sample posts only 🚧 |
| Dashboard (`homepage.html`) | Files ✅ · Projects/Posts placeholders 🚧 |
| Upload (`upload.html`) | ✅ works, icons still partly emoji |
| Auth (`login` / `register`) | 🐞 login ✅ · **register 500s** (field mismatch) · plain-text passwords |
| File select mode | ✅ checkbox + colour + row tint · 🐞 read-back broken (`.file-list:checked`) |
| Delete files | 🐞 not wired — missing `#delete`, route 404s |
| Theming | ✅ light/dark, persists everywhere |
| Mobile | ✅ sidebar collapses to an icon rail |
| Security | 🐞 no auth on `/api/filedelete`, IDOR on `/homepage`, path traversal in `/upload` |
