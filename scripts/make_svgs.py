"""Generates the Neon Pixel Team profile graphics into assets/.

No dependencies, no fonts to embed, no live data: run it, commit assets/.
    python scripts/make_svgs.py
Each graphic has a dark and a light version, picked by the README's <picture> tags.
"""
import random
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parent.parent / "assets"
SANS = "'Helvetica Neue', Arial, sans-serif"
MONO = "Consolas, 'Courier New', monospace"
CYAN, PINK = "#00E5FF", "#FF2E97"

THEMES = {
    "dark": dict(bg="#0b0b0b", surface="#141414", border="#2a2a2a", fg="#f2f2f2",
                 muted="#9a9a9a", cyan=CYAN, pink=PINK, dim="#333333"),
    "light": dict(bg="#ffffff", surface="#f4f4f4", border="#dcdcdc", fg="#0b0b0b",
                  muted="#5c5c5c", cyan="#00A3BD", pink="#D6197A", dim="#d0d0d0"),
}


def svg(w, h, body, label):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
            f'role="img" aria-label="{escape(label)}">\n{body}\n</svg>\n')


def text_w(s, size, mono=False):
    return len(s) * size * (0.6 if mono else 0.56)


def pill(x, y, label, t, size=12.5, height=30, filled=False, mono=False, anchor="start"):
    w = text_w(label, size, mono) + 28
    px = x - w / 2 if anchor == "middle" else x
    bg = t["fg"] if filled else t["surface"]
    fg = t["bg"] if filled else t["muted"]
    fam = MONO if mono else SANS
    s = (f'<rect x="{px:.1f}" y="{y}" width="{w:.1f}" height="{height}" rx="{height / 2}" '
         f'fill="{bg}" stroke="{t["border"]}"/>'
         f'<text x="{px + w / 2:.1f}" y="{y + height / 2 + size * 0.35:.1f}" text-anchor="middle" '
         f'font-family="{fam}" font-size="{size}" fill="{fg}">{escape(label)}</text>')
    return s, w


def logo(x, y, scale, t):
    """The team mark: a thick bracket with a dot, drawn in the foreground colour."""
    return (f'<g transform="translate({x} {y}) scale({scale})">'
            f'<path d="M150 62 Q150 34 122 34 H70 Q42 34 42 62 V178 Q42 206 70 206 H118" '
            f'fill="none" stroke="{t["fg"]}" stroke-width="26" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<circle cx="196" cy="46" r="16" fill="{t["fg"]}"/></g>')


def pixel_field(x0, y0, cols, rows, cell, t, cx, cy, seed):
    """Dot grid that fades out away from the mark; a few cells glow."""
    rnd = random.Random(seed)
    out = []
    for r in range(rows):
        for c in range(cols):
            px, py = x0 + c * cell, y0 + r * cell
            d = ((px - cx) ** 2 + (py - cy) ** 2) ** 0.5
            if d < 90 or rnd.random() < 0.25 + max(0, 0.6 - d / 260):
                continue
            col = t["cyan"] if rnd.random() < 0.06 else (t["pink"] if rnd.random() < 0.04 else t["dim"])
            op = max(0.15, min(1, 1.1 - d / 260))
            out.append(f'<rect x="{px}" y="{py}" width="{cell - 3}" height="{cell - 3}" fill="{col}" opacity="{op:.2f}"/>')
    return "".join(out)


def hero(t):
    W, H = 880, 300
    left = [
        f'<rect x="48" y="52" width="224" height="30" rx="15" fill="{t["surface"]}" stroke="{t["border"]}"/>',
        f'<circle cx="64" cy="67" r="3.5" fill="{t["pink"]}"/>',
        f'<text x="76" y="71.5" font-family="{MONO}" font-size="12.5" fill="{t["muted"]}">neonpixelteam · open source</text>',
        f'<text x="48" y="130" font-family="{SANS}" font-size="42" font-weight="700" fill="{t["fg"]}">Open-source apps</text>',
        f'<text x="48" y="182" font-family="{SANS}" font-size="42" font-weight="700" fill="{t["fg"]}">for people who build.</text>',
        f'<text x="48" y="222" font-family="{SANS}" font-size="15" fill="{t["muted"]}">Desktop apps, downloaders and learning material,</text>',
        f'<text x="48" y="244" font-family="{SANS}" font-size="15" fill="{t["muted"]}">made in the open and kept simple.</text>',
        f'<rect x="48" y="262" width="330" height="26" rx="13" fill="{t["surface"]}" stroke="{t["border"]}"/>',
        f'<text x="62" y="279" font-family="{MONO}" font-size="12" fill="{t["muted"]}">'
        f'<tspan fill="{t["cyan"]}">$</tspan> gh repo list neonpixelteam --source</text>',
    ]
    field = pixel_field(520, 16, 14, 16, 18, t, cx=690, cy=150, seed=7)
    body = (f'<rect width="{W}" height="{H}" rx="18" fill="{t["bg"]}" stroke="{t["border"]}"/>'
            f'{field}{logo(560, 50, 1.15, t)}{"".join(left)}')
    return svg(W, H, body, "Neon Pixel Team: open-source apps for people who build.")


def button(label, t, primary):
    W, H = 230, 44
    bg, fg = (t["fg"], t["bg"]) if primary else (t["surface"], t["fg"])
    body = (f'<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="22" fill="{bg}" stroke="{t["border"]}"/>'
            f'<text x="{W / 2 - 8}" y="{H / 2 + 5}" text-anchor="middle" font-family="{SANS}" font-size="15" '
            f'font-weight="600" fill="{fg}">{escape(label)}</text>'
            f'<path d="M{W / 2 + text_w(label, 15) / 2 - 2:.1f} {H / 2 - 4}l8 4-8 4" fill="none" stroke="{fg}" '
            f'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>')
    return svg(W, H, body, label)


def card(name, desc_lines, chips, t, link_label):
    W, H = 440, 190
    chip_parts, x = [], 28
    for c in chips:
        s, w = pill(x, 136, c, t, size=11.5, height=24, mono=True)
        chip_parts.append(s)
        x += w + 8
    desc = "".join(f'<text x="28" y="{78 + i * 22}" font-family="{SANS}" font-size="14.5" fill="{t["muted"]}">{escape(l)}</text>'
                   for i, l in enumerate(desc_lines))
    body = (f'<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="16" fill="{t["surface"]}" stroke="{t["border"]}"/>'
            f'<rect x="28" y="22" width="26" height="4" rx="2" fill="{t["cyan"]}"/>'
            f'<text x="28" y="54" font-family="{SANS}" font-size="20" font-weight="700" fill="{t["fg"]}">{escape(name)}</text>'
            f'<text x="{W - 28}" y="54" text-anchor="end" font-family="{MONO}" font-size="11.5" fill="{t["pink"]}">{escape(link_label)}</text>'
            f'{desc}{"".join(chip_parts)}')
    return svg(W, H, body, f"{name}: {' '.join(desc_lines)}")


def toolbox(t, rows):
    W, H = 880, 40 + len(rows) * 46
    body = [f'<rect width="{W}" height="{H}" rx="18" fill="{t["bg"]}"/>']
    for r, row in enumerate(rows):
        widths = [text_w(s, 12.5, True) + 28 for s in row]
        total = sum(widths) + 8 * (len(row) - 1)
        x = (W - total) / 2
        y = 20 + r * 46
        for s in row:
            p, w = pill(x, y, s, t, size=12.5, height=30, mono=True)
            body.append(p)
            x += w + 8
    return svg(W, H, "".join(body), "Toolbox: " + ", ".join(s for r in rows for s in r))


def footer(t):
    W, H = 880, 170
    rnd = random.Random(3)
    dots = []
    for i in range(60):
        x, y = rnd.uniform(0, W), rnd.uniform(0, H)
        d = min(x, W - x) / W
        if rnd.random() < 0.5 + d:
            continue
        col = t["cyan"] if rnd.random() < 0.08 else (t["pink"] if rnd.random() < 0.05 else t["dim"])
        dots.append(f'<rect x="{x:.0f}" y="{y:.0f}" width="6" height="6" fill="{col}" opacity="{0.25 + d:.2f}"/>')
    body = (f'<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="18" fill="{t["bg"]}" stroke="{t["border"]}"/>'
            f'{"".join(dots)}'
            f'<text x="{W / 2}" y="{H / 2 + 6}" text-anchor="middle" font-family="{SANS}" font-size="30" '
            f'font-weight="700" fill="{t["fg"]}">Thanks for stopping by.</text>')
    return svg(W, H, body, "Thanks for stopping by.")


PROJECTS = [
    ("NEO·DL", ["A minimal download manager with resumable,", "multi-connection downloads and EN / FA / AR UI."],
     ["Python", "PyQt6", "Windows"], "open source"),
    ("NEX Chat", ["An Android chat app, a fork of an existing", "project, extended by the team."],
     ["Java", "Android"], "open source"),
]
TOOLBOX = [
    ["Python", "PyQt6", "PHP", "Node.js", "Java", "Android"],
    ["React", "Next.js", "Tailwind CSS", "C++", "Pygame", "Shell"],
    ["Git", "GitHub Actions", "Windows", "Linux", "REST APIs"],
]


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for mode, t in THEMES.items():
        files = {
            f"hero-{mode}.svg": hero(t),
            f"btn-projects-{mode}.svg": button("Browse projects", t, True),
            f"btn-web-{mode}.svg": button("Visit website", t, False),
            f"toolbox-{mode}.svg": toolbox(t, TOOLBOX),
            f"footer-{mode}.svg": footer(t),
        }
        for i, (name, desc, chips, link) in enumerate(PROJECTS, 1):
            slug = name.lower().replace("·", "").replace(" ", "-")
            files[f"card-{slug}-{mode}.svg"] = card(name, desc, chips, t, link)
        for fname, content in files.items():
            (OUT / fname).write_text(content, encoding="utf-8")
    print("wrote", len(list(OUT.glob("*.svg"))), "svg files to", OUT)


if __name__ == "__main__":
    main()
