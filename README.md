# Catppuccin for SecureCRT

[Catppuccin](https://github.com/catppuccin/catppuccin) color schemes and 16-color ANSI palettes for [SecureCRT](https://www.vandyke.com/products/securecrt/), in all four flavors: Latte, Frappé, Macchiato and Mocha.

This is an unofficial community port. It is not affiliated with or endorsed by the Catppuccin organization.

Colors come from the official Catppuccin palette (v1.8.0), including its ANSI mapping for normal and bright colors.

> [!NOTE]
> The installer has been tested against a synthetic `Global.ini` only, not against a live SecureCRT install. It makes a backup before writing. If something looks off on your version, please open an issue.

## Requirements

- SecureCRT 7 or later (schemes are stored as `Z:` lists in `Global.ini`)
- Python 3 for the installer (optional, you can also install by hand)

## Install

Close SecureCRT completely first. It rewrites `Global.ini` on exit and will discard your changes otherwise.

### Option 1: installer

```sh
python install.py
```

The script looks for `Global.ini` in the default locations:

| OS | Path |
|---|---|
| Windows | `%APPDATA%\VanDyke\Config\Global.ini` |
| macOS | `~/Library/Application Support/VanDyke/SecureCRT/Config/Global.ini` |
| Linux | `~/.vandyke/SecureCRT/Config/Global.ini` |

If your config lives elsewhere (see Options > Global Options > General > Configuration Paths), pass the path:

```sh
python install.py "D:\path\to\Config\Global.ini"
```

What it does:

- saves a backup next to the file as `Global.ini.bak-YYYYMMDD-HHMMSS`
- adds four entries to `Z:"ANSI Color Palettes"` and four to `Z:"Color Schemes"`, updating both counters
- keeps the file's encoding and line endings
- is safe to re-run: existing Catppuccin entries are updated, not duplicated

### Option 2: by hand

1. Back up `Global.ini` and open it in a text editor.
2. Find `Z:"ANSI Color Palettes"=000000XX`. Append the four palette lines from [`global-ini-lines.txt`](global-ini-lines.txt) after the last entry of that list, and add 4 to the count. The count is hexadecimal.
3. Do the same for `Z:"Color Schemes"=000000XX` with the four scheme lines.

Keep the single leading space on every line you paste.

### Option 3: GUI

Create the scheme and the ANSI palette in Options > Global Options > Terminal > Appearance, using the decimal RGB values from [`PALETTE.md`](PALETTE.md).

## Apply

1. Open Session Options > Terminal > Appearance and pick a `Catppuccin ...` color scheme. To use it everywhere, edit the Default Session.
2. In Terminal > Emulation, set the terminal to Xterm and make sure ANSI Color is checked.
3. Optional: set the cursor color to Rosewater. It is not part of a color scheme, so it has to be set per session. The values are in [`PALETTE.md`](PALETTE.md).

## Uninstall

Restore the backup, or remove the `Catppuccin ...` lines from both lists and lower each count by the number of lines removed.

## Files

| File | Purpose |
|---|---|
| `install.py` | Patches `Global.ini` |
| `global-ini-lines.txt` | Raw lines for manual install |
| `PALETTE.md` | Hex and decimal RGB for every slot |

## Credits

- [Catppuccin](https://github.com/catppuccin/catppuccin) for the palette. Color values are taken from [catppuccin/palette](https://github.com/catppuccin/palette), MIT License, Copyright (c) 2021 Catppuccin
- [Dracula for SecureCRT](https://github.com/dracula/securecrt) for documenting the `Global.ini` format

## License

[MIT](LICENSE). The Catppuccin palette is also MIT licensed; its copyright notice is kept in [NOTICE](NOTICE).
