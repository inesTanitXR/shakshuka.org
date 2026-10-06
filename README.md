# shakshuka.org — static rebuild

Replacement for the Wix site of Shakshuka.org, the Tunisian-American community of the DMV.
Same workflow as tanitxr.org and inessaid.com: one generator, output in `docs/`.

## Update the site

1. Edit the data and copy in `build.py` (`EVENTS`, `TEAM`, `TUNISIA`, `BLOG`, and the
   `build_*` page functions).
2. Rebuild:

   ```bash
   python3 build.py
   ```

3. Commit and push; GitHub Pages serves `main:/docs`.

## Add an event

Append a dict to `EVENTS` in `build.py`:

- `slug`, `title`, `date` (YYYY-MM-DD), `time`, `venue`, `address`, `kind`, `summary`, `body` (HTML)
- `img`: a file name in `docs/assets/img` without extension (drop the source in `src-images/wix/` as `ev-<name>.jpg`, then run the resize snippet in `SUGGESTIONS.md` or just add the sized jpg directly)
- paid: `tickets=[("Name", price), …]` and `reserve_url="https://…"` (Zeffy / Eventbrite checkout)
- free: `free=True` (the page gets an RSVP form that emails `CONTACT_EMAIL`)
- `draft=True` keeps it out of the calendar but builds the page for preview

Past events automatically move to the archive with a "This event has passed" badge.

## Layout

| Path | What it is |
|---|---|
| `build.py` | The whole site: data, CSS, pages |
| `docs/` | Generated site (deployed). Never edit by hand |
| `docs/assets/img/` | Sized images (jpg) |
| `src-images/wix/` | Originals kept from the old site (logo, headshots, event artwork) |
| `src-images/commons/` | Wikimedia Commons photos + `CREDITS.md` |
| `ref/` | Raw HTML snapshots of the old Wix pages |
| `SUGGESTIONS.md` | Findings, open questions, payment/reservation recommendation |

## Preview locally

```bash
python3 -m http.server 8766 --directory docs
```
