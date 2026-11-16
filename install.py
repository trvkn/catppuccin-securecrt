#!/usr/bin/env python3
"""Install Catppuccin color schemes + ANSI palettes into SecureCRT's Global.ini.

Usage:  python install.py [path/to/Global.ini]
Close SecureCRT first: it rewrites Global.ini on exit.
Idempotent: re-running updates existing Catppuccin entries instead of duplicating.
"""
import os, re, shutil, sys, time

THEMES = {
    "Catppuccin Latte": {
        "palette": " Catppuccin Latte,5C5F7700,D20F3900,40A02B00,DF8E1D00,1E66F500,EA76CB00,17929900,ACB0BE00,6C6F8500,DE293E00,49AF3D00,EEA02D00,456EFF00,FE85D800,2D9FA800,BCC0CC00",
        "scheme": " Catppuccin Latte,010101,4C4F6900,4C4F6900,4C4F6900,4C4F6900,4C4F6900,4C4F6900,4C4F6900,4C4F6900,EFF1F500,EFF1F500,EFF1F500,EFF1F500,EFF1F500,EFF1F500,EFF1F500,EFF1F500,Catppuccin Latte"
    },
    "Catppuccin Frappe": {
        "palette": " Catppuccin Frappe,51576D00,E7828400,A6D18900,E5C89000,8CAAEE00,F4B8E400,81C8BE00,A5ADCE00,62688000,E6717200,8EC77200,D9BA7300,7B9EF000,F2A4DB00,5ABFB500,B5BFE200",
        "scheme": " Catppuccin Frappe,010101,C6D0F500,C6D0F500,C6D0F500,C6D0F500,C6D0F500,C6D0F500,C6D0F500,C6D0F500,30344600,30344600,30344600,30344600,30344600,30344600,30344600,30344600,Catppuccin Frappe"
    },
    "Catppuccin Macchiato": {
        "palette": " Catppuccin Macchiato,494D6400,ED879600,A6DA9500,EED49F00,8AADF400,F5BDE600,8BD5CA00,A5ADCB00,5B607800,EC748600,8CCF7F00,E1C68200,78A1F600,F2A9DD00,63CBC000,B8C0E000",
        "scheme": " Catppuccin Macchiato,010101,CAD3F500,CAD3F500,CAD3F500,CAD3F500,CAD3F500,CAD3F500,CAD3F500,CAD3F500,24273A00,24273A00,24273A00,24273A00,24273A00,24273A00,24273A00,24273A00,Catppuccin Macchiato"
    },
    "Catppuccin Mocha": {
        "palette": " Catppuccin Mocha,45475A00,F38BA800,A6E3A100,F9E2AF00,89B4FA00,F5C2E700,94E2D500,A6ADC800,585B7000,F3779900,89D88B00,EBD39100,74A8FC00,F2AEDE00,6BD7CA00,BAC2DE00",
        "scheme": " Catppuccin Mocha,010101,CDD6F400,CDD6F400,CDD6F400,CDD6F400,CDD6F400,CDD6F400,CDD6F400,CDD6F400,1E1E2E00,1E1E2E00,1E1E2E00,1E1E2E00,1E1E2E00,1E1E2E00,1E1E2E00,1E1E2E00,Catppuccin Mocha"
    }
}

def default_path():
    cands = []
    if os.environ.get("APPDATA"):
        cands.append(os.path.join(os.environ["APPDATA"], "VanDyke", "Config", "Global.ini"))
    home = os.path.expanduser("~")
    cands += [os.path.join(home, "Library", "Application Support", "VanDyke", "SecureCRT", "Config", "Global.ini"),
              os.path.join(home, ".vandyke", "SecureCRT", "Config", "Global.ini")]
    for c in cands:
        if os.path.isfile(c):
            return c
    sys.exit("Global.ini not found, pass its path as an argument "
             "(Options > Global Options > General > Configuration Paths).")

def upsert(lines, key, entries):
    """entries: {name: full line}. Returns (added, updated)."""
    pat = re.compile(r'^Z:"%s"=([0-9a-fA-F]{8})\s*$' % re.escape(key))
    for i, l in enumerate(lines):
        m = pat.match(l)
        if m:
            break
    else:
        sys.exit('Section Z:"%s" not found in Global.ini' % key)
    end = i + 1
    while end < len(lines) and lines[end].startswith(" "):
        end += 1
    body = lines[i + 1:end]
    declared = int(m.group(1), 16)
    if declared != len(body):
        sys.exit('Z:"%s" declares %d entries but %d found, refusing to edit' % (key, declared, len(body)))
    added = updated = 0
    for name, line in entries.items():
        for j, b in enumerate(body):
            if b.startswith(" " + name + ","):
                if b != line:
                    body[j] = line
                    updated += 1
                break
        else:
            body.append(line)
            added += 1
    count = "%08x" % len(body)
    if m.group(1) != m.group(1).lower():
        count = count.upper()
    lines[i:end] = ['Z:"%s"=%s' % (key, count)] + body
    return added, updated

def main():
    path = sys.argv[1] if len(sys.argv) > 1 else default_path()
    raw = open(path, "rb").read()
    if raw[:2] in (b"\xff\xfe", b"\xfe\xff"):
        enc = "utf-16"
    else:
        enc = "latin-1"  # byte-transparent: keeps UTF-8/BOM/ANSI content intact
    text = raw.decode(enc)
    nl = "\r\n" if "\r\n" in text else "\n"
    lines = text.split(nl)
    r1 = upsert(lines, "ANSI Color Palettes", {n: t["palette"] for n, t in THEMES.items()})
    r2 = upsert(lines, "Color Schemes", {n: t["scheme"] for n, t in THEMES.items()})
    if not any(r1 + r2):
        print("Already up to date:", path)
        return
    backup = path + ".bak-" + time.strftime("%Y%m%d-%H%M%S")
    shutil.copy2(path, backup)
    new = nl.join(lines)
    data = new.encode("utf-16-le" if raw[:2] == b"\xff\xfe" else "utf-16-be") if enc == "utf-16" else new.encode(enc)
    if enc == "utf-16":
        data = raw[:2] + data
    open(path, "wb").write(data)
    print("Patched:", path)
    print("Backup: ", backup)
    print("ANSI palettes: +%d added, %d updated; color schemes: +%d added, %d updated" % (r1 + r2))

if __name__ == "__main__":
    main()
