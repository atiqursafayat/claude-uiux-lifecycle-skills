#!/usr/bin/env python3
"""uxl: token-saving helpers for the ux-lifecycle skill (Python 3.9+, standard library only).

Run from the project root. Every command prints compact text meant to be read by an agent.

  toc      <specialist|file>                 headings with line ranges and token estimates
  section  <specialist|file> <heading>...    print only the matching section(s)
  scan     [root]                            project facts: stack, UI files, roles, statuses, i18n, notifications
  lint     [paths...]                        static accessibility/UX checks on templates and components
  contrast <fg> <bg> [<fg> <bg> ...]         WCAG contrast ratios (hex colours)
  new      <template> --name <slug>          create a docs/ux artifact from a template
  shots    <url> [--widths 375,768,1280]     viewport screenshots (needs Python playwright)
"""
import argparse
import datetime
import json
import os
import re
import subprocess
import sys

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SPECIALISTS = os.path.join(SKILL_DIR, "specialists")
TEMPLATES = os.path.join(SKILL_DIR, "templates")

SKIP_DIRS = {".git", "node_modules", "venv", ".venv", "env", "__pycache__", "dist", "build", ".next",
             ".nuxt", "vendor", "staticfiles", "coverage", ".tox", ".mypy_cache", ".pytest_cache",
             "migrations", ".ux-shots", ".claude"}
UI_EXT = (".html", ".htm", ".jinja", ".jinja2", ".j2", ".njk", ".hbs", ".erb", ".blade.php", ".twig",
          ".vue", ".svelte", ".astro", ".jsx", ".tsx", ".php", ".liquid", ".cshtml", ".razor")
CODE_EXT = (".py", ".ts", ".tsx", ".js", ".jsx", ".mjs", ".php", ".rb", ".go", ".java", ".kt", ".cs",
            ".dart", ".swift", ".ex", ".exs", ".prisma", ".graphql")


def tok(text):
    return max(1, len(text) // 4)


def out(lines, limit=None, label="more"):
    lines = list(lines)
    shown = lines if limit is None else lines[:limit]
    for line in shown:
        print(line)
    if limit is not None and len(lines) > limit:
        print(f"  … +{len(lines) - limit} {label}")


# ---------------------------------------------------------------- specialists: toc / section

def resolve_doc(name):
    if os.path.isfile(name):
        return name
    for cand in (os.path.join(SPECIALISTS, name, "SKILL.md"), os.path.join(SPECIALISTS, name),
                 os.path.join(SPECIALISTS, name + ".md"), os.path.join(SKILL_DIR, name)):
        if os.path.isfile(cand):
            return cand
    folder = os.path.join(SPECIALISTS, name)
    if os.path.isdir(folder):
        mds = sorted(f for f in os.listdir(folder) if f.endswith(".md"))
        if len(mds) == 1:
            return os.path.join(folder, mds[0])
    names = sorted(d for d in os.listdir(SPECIALISTS) if os.path.isdir(os.path.join(SPECIALISTS, d)))
    sys.exit(f"uxl: no specialist or file '{name}'. Specialists: {', '.join(names)}")


def headings(lines):
    """Return [(index, level, title)] for markdown headings outside code fences."""
    found, fence = [], False
    for i, line in enumerate(lines):
        if line.lstrip().startswith(("```", "~~~")):
            fence = not fence
            continue
        m = None if fence else re.match(r"^(#{1,6})\s+(.*?)\s*#*\s*$", line)
        if m:
            found.append((i, len(m.group(1)), m.group(2)))
    return found


def section_end(lines, heads, k):
    _, level, _ = heads[k]
    for j in range(k + 1, len(heads)):
        if heads[j][1] <= level:
            return heads[j][0]
    return len(lines)


def cmd_toc(a):
    path = resolve_doc(a.doc)
    lines = read(path, 10_000_000).splitlines()
    heads = [h for h in headings(lines) if h[1] <= a.depth]
    rel = os.path.relpath(path, SKILL_DIR) if path.startswith(SKILL_DIR) else path
    print(f"{rel}: {len(lines)} lines, ~{tok(chr(10).join(lines))} tokens")
    first = heads[0][0] if heads else len(lines)
    if first > 0:
        print(f"  (preamble) L1-{first} ~{tok(chr(10).join(lines[:first]))}")
    all_heads = headings(lines)
    for i, level, title in heads:
        k = next(n for n, h in enumerate(all_heads) if h[0] == i)
        end = section_end(lines, all_heads, k)
        print(f"{'  ' * (level - 1)}{title}  L{i + 1}-{end} ~{tok(chr(10).join(lines[i:end]))}")


def cmd_section(a):
    path = resolve_doc(a.doc)
    lines = read(path, 10_000_000).splitlines()
    heads = headings(lines)
    printed = 0
    for query in a.heading:
        if query.lower() in ("preamble", "intro"):
            end = heads[0][0] if heads else len(lines)
            text = lines[:end]
            if text and text[0].strip() == "---":  # skip YAML front matter
                close = next((n for n in range(1, len(text)) if text[n].strip() == "---"), 0)
                text = text[close + 1:]
            print("\n".join(text).strip() + "\n")
            printed += 1
            continue
        matches = [k for k, h in enumerate(heads) if query.lower() in h[2].lower()]
        if not matches:
            print(f"uxl: no heading matching '{query}' in {os.path.basename(os.path.dirname(path))}; run toc.")
            continue
        for k in matches[: a.max_matches]:
            start, end = heads[k][0], section_end(lines, heads, k)
            body = lines[start:end]
            if a.outline:
                body = [l for l in body if re.match(r"^#{1,6}\s", l) or l.startswith(("- **", "| "))][:60]
            print("\n".join(body).rstrip() + "\n")
            printed += 1
    if not printed:
        sys.exit(1)


# ---------------------------------------------------------------- scan

def project_files(root):
    try:
        res = subprocess.run(["git", "-C", root, "ls-files", "-co", "--exclude-standard"],
                             capture_output=True, text=True, timeout=30)
        if res.returncode == 0 and res.stdout.strip():
            files = [f for f in res.stdout.splitlines()
                     if not any(p in SKIP_DIRS for p in f.split("/")[:-1])]
            return [os.path.join(root, f) for f in files if os.path.isfile(os.path.join(root, f))]
    except (OSError, subprocess.SubprocessError):
        pass
    files = []
    for d, dirs, names in os.walk(root):
        dirs[:] = [x for x in dirs if x not in SKIP_DIRS and not x.startswith(".")]
        files += [os.path.join(d, n) for n in names]
    return files


def read(path, limit=400_000):
    try:
        with open(path, encoding="utf-8", errors="ignore") as fh:
            return fh.read(limit)
    except OSError:
        return ""


def rel(path, root):
    return os.path.relpath(path, root)


DEP_HINTS = {
    "django": "Django", "flask": "Flask", "fastapi": "FastAPI", "react": "React", "next": "Next.js",
    "vue": "Vue", "nuxt": "Nuxt", "svelte": "Svelte", "@sveltejs/kit": "SvelteKit", "@angular/core": "Angular",
    "astro": "Astro", "tailwindcss": "Tailwind", "@radix-ui/react-slot": "shadcn/Radix", "laravel/framework": "Laravel",
    "rails": "Rails", "alpinejs": "Alpine.js", "htmx.org": "htmx", "bootstrap": "Bootstrap", "@mui/material": "MUI",
    "chart.js": "Chart.js", "playwright": "Playwright", "@playwright/test": "Playwright", "cypress": "Cypress",
    "i18next": "i18next", "react-intl": "react-intl", "next-intl": "next-intl", "vue-i18n": "vue-i18n",
    "django-allauth": "allauth", "crispy-tailwind": "crispy-tailwind", "django-crispy-forms": "crispy-forms",
}


def detect_stack(root, files, texts):
    found = []
    manifests = {"requirements.txt", "pyproject.toml", "Pipfile", "package.json", "composer.json", "Gemfile",
                 "go.mod", "pubspec.yaml", "Cargo.toml"}
    for f in files:
        if os.path.basename(f) in manifests and f.count(os.sep) - root.count(os.sep) <= 2:
            body = read(f).lower()
            for key, label in DEP_HINTS.items():
                if re.search(r'(^|["\s/=<>~^])' + re.escape(key) + r'(["\s=<>~^\[:]|$)', body, re.M):
                    found.append(label)
            if os.path.basename(f) == "pubspec.yaml":
                found.append("Flutter")
    cdn = {"cdn.tailwindcss.com": "Tailwind (Play CDN)", "unpkg.com/htmx": "htmx", "alpinejs": "Alpine.js",
           "bootstrap.min.css": "Bootstrap", "chart.js": "Chart.js"}
    for text in texts:
        for key, label in cdn.items():
            if key in text:
                found.append(label)
    seen, ordered = set(), []
    for x in found:
        if x not in seen:
            seen.add(x)
            ordered.append(x)
    return ordered


CHOICE_START = re.compile(
    r"^\s*(?:class\s+(\w*(?:Status|State|Stage|Phase|Role)\w*)\s*\((?:models\.)?(?:Text|Integer)?Choices\)"
    r"|([A-Z0-9_]*(?:STATUS|STATE|STAGE|PHASE|ROLE)[A-Z0-9_]*)\s*[:=]\s*[\[\(]"
    r"|(?:export\s+)?enum\s+(\w*(?:Status|State|Stage|Phase|Role)\w*)"
    r"|(?:export\s+)?type\s+(\w*(?:Status|State|Stage|Role)\w*)\s*=)")
TUPLE_VAL = re.compile(r"""\(\s*(?:['"]([^'"]+)['"]|([A-Z][A-Z0-9_]+))\s*,""")
CONST_VAL = re.compile(r"^\s*([A-Z][A-Z0-9_]+)\s*[=,:]")
QUOTED_VAL = re.compile(r"""['"]([\w\-]+)['"]""")


def find_statuses(root, files):
    rows = []
    for f in files:
        if not f.endswith(CODE_EXT) or "test" in os.path.basename(f).lower():
            continue
        lines = read(f).splitlines()
        i = 0
        while i < len(lines):
            m = CHOICE_START.match(lines[i])
            if not m:
                i += 1
                continue
            name = next(g for g in m.groups() if g)
            block, j, depth = [], 0, 0
            for j, line in enumerate(lines[i:i + 40]):
                if j > 0 and re.match(r"^\s*(class|def|export|const|let|function)\b", line):
                    break
                block.append(line if j else line.split("=", 1)[-1])
                depth += sum(line.count(c) for c in "[({") - sum(line.count(c) for c in "])}")
                if j > 0 and depth <= 0:
                    break
            text = "\n".join(block)
            values = [a or b for a, b in TUPLE_VAL.findall(text)]
            if not values:
                values = CONST_VAL.findall(text) or QUOTED_VAL.findall(text)
            values = list(dict.fromkeys(v for v in values if v.lower() not in ("none", "null", "true", "false")))
            if len(values) >= 2:
                rows.append(f"{rel(f, root)}:{i + 1} {name}: {', '.join(values[:12])}{' …' if len(values) > 12 else ''}")
            i += max(1, j)
    return rows


def grep(root, files, pattern, exts=CODE_EXT, flags=re.I):
    rx = re.compile(pattern, flags)
    hits = []
    for f in files:
        if not f.endswith(exts):
            continue
        for n, line in enumerate(read(f).splitlines(), 1):
            if rx.search(line):
                hits.append((rel(f, root), n, line.strip()))
    return hits


def cmd_scan(a):
    root = os.path.abspath(a.root)
    files = project_files(root)
    ui = [f for f in files if f.lower().endswith(UI_EXT)]
    ui_texts = [read(f, 60_000) for f in ui[:400]]
    print(f"# uxl scan: {os.path.basename(root)} ({len(files)} files)")
    print("stack:", ", ".join(detect_stack(root, files, ui_texts)) or "unknown")

    dirs = {}
    for f in ui:
        d = os.path.dirname(rel(f, root)) or "."
        top = "/".join(d.split(os.sep)[:2])
        dirs[top] = dirs.get(top, 0) + 1
    print(f"ui files: {len(ui)}; top dirs: " + ", ".join(f"{d} ({n})" for d, n in sorted(dirs.items(), key=lambda x: -x[1])[:10]))
    comps = sorted({os.path.dirname(rel(f, root)) for f in ui if re.search(r"components?|partials?|includes?|widgets?", f)})
    if comps:
        print("component dirs:", ", ".join(comps[:6]))

    cfg = [rel(f, root) for f in files if re.search(r"tailwind\.config|theme\.(js|ts|json)$|tokens?\.(json|css|ts)$|variables\.s?css$", f)]
    inline = sum(1 for t in ui_texts if "tailwind.config" in t)
    print("design tokens:", ", ".join(cfg[:5]) or "-", f"; inline tailwind.config in {inline} templates" if inline else "")

    print("\n## roles")
    roles = grep(root, files, r"\bis_(?:[a-z_]*(?:er|or|ent|ant|ist|ee|admin|staff|superuser|member|owner))\s*=\s*models\.BooleanField|^\s*[A-Z_]*ROLES?[A-Z_]*\s*=|\broles?\s*:\s*\[['\"]"
                 r"|Group\.objects\.(get_or_)?create\(name=|enum\s+\w*Role|role\s*:\s*['\"][a-z]+['\"]\s*\|", exts=CODE_EXT, flags=0)
    out((f"{p}:{n} {l[:110]}" for p, n, l in roles), a.limit)

    print("\n## statuses / lifecycles")
    out(find_statuses(root, files), a.limit * 2)

    print("\n## routes")
    route_files = {}
    for p, n, l in grep(root, files, r"^\s*(re_)?path\(|Route::(get|post|resource)|^\s*(get|post|resources?)\s+['\":]|@(app|router)\.(get|post|route)\("):
        route_files[p] = route_files.get(p, 0) + 1
    pages = [rel(f, root) for f in files if re.search(r"(^|/)(app|pages)/.*(page|index)\.(tsx|jsx|vue|svelte|astro)$", rel(f, root))]
    print(f"{sum(route_files.values())} route definitions in {len(route_files)} files" + (f"; {len(pages)} file-based pages" if pages else ""))
    out((f"{p} ({c})" for p, c in sorted(route_files.items(), key=lambda x: -x[1])), 8, "route files")

    print("\n## notifications (email/SMS/push)")
    notes = grep(root, files, r"send_?mail|send_?email|sendMail|send_sms|sendSms|\.notify\(|Notification\.create|create_in_app|push_notification|mail\(|Mail::to")
    commented = [h for h in notes if h[2].startswith(("#", "//", "*", "/*", "<!--"))]
    print(f"{len(notes)} call sites; {len(commented)} commented out")
    if commented:
        out((f"{p}:{n} (commented)" for p, n, _ in commented), a.limit)

    print("\n## i18n / locale")
    loc_dirs = sorted({rel(os.path.dirname(f), root).split("/LC_MESSAGES")[0] for f in files if re.search(r"(^|/)(locale|locales|lang|i18n|translations)/", rel(f, root))})
    tags = sum(1 for t in ui_texts if re.search(r"{%\s*(trans|blocktrans|translate)|\bt\(['\"]|\$t\(|useTranslation|__\(|@lang\(|i18n\.", t))
    settings = grep(root, files, r"^\s*(LANGUAGE_CODE|LANGUAGES|USE_I18N|defaultLocale|locales)\s*[=:]")
    print(f"locale dirs: {', '.join(loc_dirs[:5]) or '-'}; ui files with translation calls: {tags}/{len(ui_texts)}")
    out((f"{p}:{n} {l[:90]}" for p, n, l in settings), 5)

    print("\n## analytics / monitoring")
    an = {"gtag(": "Google Analytics", "googletagmanager": "GTM", "plausible": "Plausible", "posthog": "PostHog",
          "mixpanel": "Mixpanel", "analytics.js": "Segment", "hotjar": "Hotjar", "clarity.ms": "Clarity",
          "matomo": "Matomo", "umami": "Umami", "sentry": "Sentry"}
    hits = sorted({label for key, label in an.items() if any(key in t for t in ui_texts)}
                  | {label for key, label in an.items() if any(key in os.path.basename(f).lower() for f in files)})
    print(", ".join(hits) or "none found")

    tests = [rel(f, root) for f in files if re.search(r"playwright\.config|cypress\.config|(^|/)e2e/|conftest\.py$|pytest\.ini$|jest\.config|vitest\.config", rel(f, root))]
    print("\n## tests:", ", ".join(tests[:6]) or "none found")


# ---------------------------------------------------------------- lint

TAG = lambda name: re.compile(r"<" + name + r"\b(?:[^>\"']|\"[^\"]*\"|'[^']*')*>", re.I | re.S)
RULES = {
    "img-alt": ("serious", "img without alt (use alt=\"\" if decorative)"),
    "input-label": ("serious", "form field without a label, aria-label or aria-labelledby"),
    "button-name": ("serious", "button or link with no text and no aria-label"),
    "click-div": ("serious", "click handler on non-interactive element (use <button> or add role+tabindex+keys)"),
    "html-lang": ("serious", "<html> without lang"),
    "zoom-blocked": ("serious", "viewport blocks zoom (user-scalable=no / maximum-scale=1)"),
    "tabindex-positive": ("moderate", "positive tabindex breaks focus order"),
    "focus-removed": ("moderate", "outline removed without a visible focus style"),
    "link-href": ("moderate", "<a> without a real href (use <button> for actions)"),
    "vague-link": ("moderate", "vague link text (click here / read more / here)"),
    "native-dialog": ("minor", "alert()/confirm()/prompt(): use an accessible in-page dialog"),
    "blank-noopener": ("minor", "target=_blank without rel=noopener"),
    "autofocus": ("minor", "autofocus can disorient screen-reader and mobile users"),
}


def attr(tag, name):
    m = re.search(r"\b" + name + r"\s*=\s*(\"[^\"]*\"|'[^']*'|[^\s>]+)", tag, re.I)
    return None if not m else m.group(1).strip("\"'")


def has_attr(tag, *names):
    return any(re.search(r"(?:^|[\s:@])" + re.escape(n) + r"(\s*=|[\s>/])", tag, re.I) for n in names)


def lint_text(text):
    findings = []
    add = lambda rule, pos: findings.append((rule, text.count("\n", 0, pos) + 1))
    label_for = set(re.findall(r"\bfor\s*=\s*[\"']([^\"']+)", text)) | set(re.findall(r"\bhtmlFor\s*=\s*[\"{']([^\"'}]+)", text))

    for m in TAG("img").finditer(text):
        if not has_attr(m.group(0), "alt", ":alt", "v-bind:alt"):
            add("img-alt", m.start())
    for m in TAG("(?:input|select|textarea)").finditer(text):
        t = m.group(0)
        typ = (attr(t, "type") or "").lower()
        if typ in ("hidden", "submit", "button", "image", "reset"):
            continue
        if has_attr(t, "aria-label", "aria-labelledby", "title", ":aria-label"):
            continue
        fid = attr(t, "id")
        before = text[max(0, m.start() - 300):m.start()]
        wrapped = before.rfind("<label") > before.rfind("</label>")
        if not wrapped and (not fid or fid not in label_for):
            add("input-label", m.start())
    for m in re.finditer(r"<(button|a)\b((?:[^>\"']|\"[^\"]*\"|'[^']*')*)>(.*?)</\1\s*>", text, re.I | re.S):
        tag, inner = m.group(0)[: m.group(0).find(">") + 1], m.group(3)
        visible = re.sub(r"<[^>]+>|{#.*?#}", " ", inner, flags=re.S)
        visible = re.sub(r"{%.*?%}", " ", visible, flags=re.S).strip()
        has_img_alt = re.search(r"<img[^>]+alt\s*=\s*[\"'][^\"']+", inner, re.I)
        has_sr = re.search(r"sr-only|visually-hidden|aria-label", inner, re.I)
        if not visible and not has_img_alt and not has_sr and not has_attr(tag, "aria-label", "aria-labelledby", "title", ":aria-label"):
            add("button-name", m.start())
        if m.group(1).lower() == "a":
            href = attr(tag, "href")
            if (href is None and not has_attr(tag, ":href", "v-bind:href", "routerlink", "to")) or href in ("#", "") or (href or "").startswith("javascript:"):
                add("link-href", m.start())
            if re.fullmatch(r"(?i)\s*(click here|here|read more|more|learn more|link)\s*", visible or "x"):
                add("vague-link", m.start())
            if attr(tag, "target") == "_blank" and "noopener" not in (attr(tag, "rel") or "") and "noreferrer" not in (attr(tag, "rel") or ""):
                add("blank-noopener", m.start())
    for m in TAG("(?:div|span|li|td|tr|p|img|section|article)").finditer(text):
        t = m.group(0)
        if re.search(r"\s(onclick|@click|v-on:click|onClick|x-on:click|hx-(get|post))\s*=", t) and not has_attr(t, "role"):
            add("click-div", m.start())
    for m in TAG("html").finditer(text):
        if not has_attr(m.group(0), "lang"):
            add("html-lang", m.start())
    for m in re.finditer(r"user-scalable\s*=\s*(no|0)|maximum-scale\s*=\s*1(\.0)?\b", text, re.I):
        add("zoom-blocked", m.start())
    for m in re.finditer(r"tabindex\s*=\s*[\"']?([1-9]\d*)", text, re.I):
        add("tabindex-positive", m.start())
    for m in re.finditer(r"class(?:Name)?\s*=\s*[\"']([^\"']*\boutline-none\b[^\"']*)[\"']", text):
        if not re.search(r"focus(-visible)?:(ring|outline|border|shadow|bg|underline)", m.group(1)):
            add("focus-removed", m.start())
    for m in re.finditer(r"outline\s*:\s*(none|0)\b", text, re.I):
        add("focus-removed", m.start())
    for m in re.finditer(r"(?<![\w.])(alert|confirm|prompt)\s*\(", text):
        add("native-dialog", m.start())
    for m in re.finditer(r"\sautofocus\b", text, re.I):
        add("autofocus", m.start())
    return findings


def cmd_lint(a):
    root = os.getcwd()
    targets = []
    for p in a.paths or ["."]:
        if os.path.isdir(p):
            targets += [f for f in project_files(os.path.abspath(p)) if f.lower().endswith(UI_EXT)]
        elif os.path.isfile(p):
            targets.append(os.path.abspath(p))
    by_rule = {}
    for f in targets:
        for rule, line in lint_text(read(f)):
            by_rule.setdefault(rule, []).append(f"{rel(f, root)}:{line}")
    order = {"critical": 0, "serious": 1, "moderate": 2, "minor": 3}
    total = sum(len(v) for v in by_rule.values())
    if a.json:
        print(json.dumps({r: {"severity": RULES[r][0], "count": len(v), "locations": v} for r, v in by_rule.items()}))
        return
    print(f"# uxl lint: {len(targets)} files, {total} findings (static heuristics; verify, then fix)")
    for rule in sorted(by_rule, key=lambda r: (order[RULES[r][0]], -len(by_rule[r]))):
        sev, msg = RULES[rule]
        locs = by_rule[rule]
        print(f"\n[{sev}] {rule} ×{len(locs)}: {msg}")
        out(("  " + l for l in locs), None if a.all else a.per_rule, "locations (use --all)")
    if not total:
        print("no findings")


# ---------------------------------------------------------------- contrast

def hex_rgb(value):
    v = value.strip().lstrip("#")
    if len(v) == 3:
        v = "".join(c * 2 for c in v)
    if not re.fullmatch(r"[0-9a-fA-F]{6}", v):
        sys.exit(f"uxl: '{value}' is not a hex colour")
    return [int(v[i:i + 2], 16) / 255 for i in (0, 2, 4)]


def luminance(rgb):
    lin = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in rgb]
    return 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]


def cmd_contrast(a):
    if len(a.colours) % 2:
        sys.exit("uxl: pass colours in fg bg pairs")
    for fg, bg in zip(a.colours[::2], a.colours[1::2]):
        l1, l2 = sorted((luminance(hex_rgb(fg)), luminance(hex_rgb(bg))), reverse=True)
        r = (l1 + 0.05) / (l2 + 0.05)
        ok = lambda x: "pass" if r >= x else "FAIL"
        print(f"{fg} on {bg}: {r:.2f}:1  text AA {ok(4.5)} | large/UI AA {ok(3)} | text AAA {ok(7)}")


# ---------------------------------------------------------------- new

DEST = {
    "PRODUCT": "docs/ux/PRODUCT.md",
    "feature-brief": "docs/ux/features/{name}/brief.md",
    "flow-spec": "docs/ux/features/{name}/flow.md",
    "release-checklist": "docs/ux/features/{name}/release.md",
    "usability-test-plan": "docs/ux/features/{name}/usability-test.md",
    "journey-map": "docs/ux/journeys/{name}.md",
    "lifecycle": "docs/ux/journeys/{name}-lifecycle.md",
    "interview-guide": "docs/ux/research/{name}-interview-guide.md",
}


def cmd_new(a):
    key = a.template.replace(".md", "")
    if key not in DEST:
        sys.exit(f"uxl: templates: {', '.join(DEST)}")
    if "{name}" in DEST[key] and not a.name:
        sys.exit("uxl: --name <slug> is required for this template")
    dest = a.dest or DEST[key].format(name=a.name)
    if os.path.exists(dest) and not a.force:
        sys.exit(f"uxl: {dest} exists (read it instead, or pass --force)")
    os.makedirs(os.path.dirname(dest) or ".", exist_ok=True)
    text = read(os.path.join(TEMPLATES, key + ".md"))
    title = (a.name or "").replace("-", " ").strip()
    for ph in ("<name>", "<feature>", "<object, e.g. Application>", "<flow or prototype>", "<topic>", "<Product name>"):
        if title:
            text = text.replace(ph, title)
    text = text.replace("<date>", datetime.date.today().isoformat())
    with open(dest, "w", encoding="utf-8") as fh:
        fh.write(text)
    print(f"created {dest} (~{tok(text)} tokens); fill the blanks, delete rows that don't apply")


# ---------------------------------------------------------------- shots

def cmd_shots(a):
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        sys.exit("uxl: needs Python playwright: pip install playwright && python -m playwright install chromium "
                 "(or set PLAYWRIGHT_BROWSERS_PATH / --executable to an existing Chromium)")
    os.makedirs(a.out, exist_ok=True)
    heights = {375: 812, 390: 844, 768: 1024, 1024: 768, 1280: 800, 1440: 900}
    slug = re.sub(r"[^a-z0-9]+", "-", a.url.lower().split("://")[-1]).strip("-")[:60] or "page"
    with sync_playwright() as p:
        kw = {"executable_path": a.executable} if a.executable else {}
        if not a.executable and os.path.exists("/opt/pw-browsers/chromium"):
            kw["executable_path"] = "/opt/pw-browsers/chromium"
        browser = p.chromium.launch(**kw)
        for w in [int(x) for x in a.widths.split(",")]:
            ctx = browser.new_context(viewport={"width": w, "height": heights.get(w, 900)},
                                      storage_state=a.storage_state if a.storage_state else None,
                                      device_scale_factor=1)
            page = ctx.new_page()
            errors = []
            page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
            page.on("requestfailed", lambda r: errors.append(f"request failed: {r.url}"))
            page.goto(a.url, wait_until="networkidle", timeout=a.timeout * 1000)
            if a.wait_for:
                page.wait_for_selector(a.wait_for, timeout=a.timeout * 1000)
            overflow = page.evaluate("document.documentElement.scrollWidth > window.innerWidth + 1")
            path = os.path.join(a.out, f"{slug}-{w}.jpg")
            page.screenshot(path=path, full_page=a.full, type="jpeg", quality=a.quality)
            notes = []
            if overflow:
                notes.append("HORIZONTAL SCROLL")
            if errors:
                notes.append(f"{len(errors)} console/network errors: " + "; ".join(e[:80] for e in errors[:3]))
            print(f"{path} ({os.path.getsize(path) // 1024} KB){'  ' + ' | '.join(notes) if notes else ''}")
            ctx.close()
        browser.close()


# ---------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser(prog="uxl", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("toc", help="headings with line ranges and token estimates")
    s.add_argument("doc")
    s.add_argument("--depth", type=int, default=3)
    s.set_defaults(fn=cmd_toc)

    s = sub.add_parser("section", help="print matching section(s); 'preamble' for the intro")
    s.add_argument("doc")
    s.add_argument("heading", nargs="+")
    s.add_argument("--outline", action="store_true", help="only sub-headings and bold bullets")
    s.add_argument("--max-matches", type=int, default=2)
    s.set_defaults(fn=cmd_section)

    s = sub.add_parser("scan", help="compact project facts for docs/ux/PRODUCT.md")
    s.add_argument("root", nargs="?", default=".")
    s.add_argument("--limit", type=int, default=12)
    s.set_defaults(fn=cmd_scan)

    s = sub.add_parser("lint", help="static accessibility/UX checks on UI files")
    s.add_argument("paths", nargs="*")
    s.add_argument("--per-rule", type=int, default=5)
    s.add_argument("--all", action="store_true")
    s.add_argument("--json", action="store_true")
    s.set_defaults(fn=cmd_lint)

    s = sub.add_parser("contrast", help="WCAG contrast for fg/bg hex pairs")
    s.add_argument("colours", nargs="+")
    s.set_defaults(fn=cmd_contrast)

    s = sub.add_parser("new", help="create a docs/ux artifact from a template")
    s.add_argument("template")
    s.add_argument("--name")
    s.add_argument("--dest")
    s.add_argument("--force", action="store_true")
    s.set_defaults(fn=cmd_new)

    s = sub.add_parser("shots", help="viewport screenshots at several widths")
    s.add_argument("url")
    s.add_argument("--widths", default="375,1280")
    s.add_argument("--out", default=".ux-shots")
    s.add_argument("--full", action="store_true", help="full page (costs more image tokens)")
    s.add_argument("--quality", type=int, default=60)
    s.add_argument("--wait-for")
    s.add_argument("--storage-state", help="Playwright storage state JSON for logged-in pages")
    s.add_argument("--executable")
    s.add_argument("--timeout", type=int, default=30)
    s.set_defaults(fn=cmd_shots)

    a = ap.parse_args()
    try:
        a.fn(a)
    except BrokenPipeError:  # output piped into head etc.
        sys.stderr.close()


if __name__ == "__main__":
    main()
