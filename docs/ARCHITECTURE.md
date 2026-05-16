# Architecture & technical notes

This documents *why* each piece exists, so contributors can maintain it when
GDK-Proton / Minecraft / ProxyPass move.

## The launch chain

```
bedrock-on-linux  →  umu-run (Steam Linux Runtime / pressure-vessel)
                   →  GDK-Proton (Wine fork, binary-patched)
                   →  Minecraft.Windows.exe (user-supplied, GDK build)
ProxyPass (Java 25, background)  ←─ LAN ─→  Minecraft   ──auth──→  real server
```

umu-launcher is used (instead of Heroic) so there is **no launcher GUI
dependency** and the Steam Linux Runtime gives a consistent environment on
every distro.

## The two binary patches (the heart of it)

Minecraft Bedrock **GDK** 1.26+ does not start under stock GDK-Proton. Two
distinct stubs abort the process. Both are patched in
`files/lib/wine/x86_64-windows/` of the GDK-Proton tree; originals are kept as
`*.bol-orig`, and patching is idempotent (safe across re-runs / Proton updates).

### 1. `combase.dll` — `RoOriginateErrorW`

* Symptom: game window never appears; process exits immediately.
* Cause: Minecraft calls `GetCurrentPackageFullName` (no package identity in
  the prefix) → takes a WinRT error path → calls `combase.RoOriginateErrorW`,
  which GDK-Proton exports as `__wine_stub_RoOriginateErrorW` → the Wine
  unimplemented-stub handler aborts.
* Fix: locate the export via the PE export table (robust to version changes —
  see `pe_export_offset`) and overwrite the 24-byte stub with
  `31 C0 C3` (`xor eax,eax; ret`) → returns `FALSE` harmlessly.
* Must stay a Wine **builtin** (combase is a pure-PE builtin, no unixlib);
  loading it `native`, or under another name, breaks all of combase.

### 2. `ntdll.dll` — `stub_entry_point`

* Symptom: game reaches the **main menu**, then crashes after ~10 min with an
  unhandled C++ exception (`0xe06d7363`).
* Cause: `gameinputredistservice` (from `GameInputRedist.msi`) calls
  `ntdll.NtQueryWnfStateData`. Wine has no such export → the importer is routed
  to Wine's shared `stub_entry_point`, which raises `EXCEPTION_WINE_STUB` and
  kills the service → later `device_notify` RPC fails
  (`RPC_S_SERVER_UNAVAILABLE`) → Minecraft throws a fatal C++ exception.
* Fix: `stub_entry_point` is not an export, so it is found by a byte signature
  (prologue `55 53 48 81 EC C8 00 00 00 48 8D AC 24 C0 00 00 00`, validated by
  the nearby `mov rcx,rbx; call RtlRaiseException`). Its entry is replaced with
  `B8 02 00 00 C0  C3` → `mov eax,0xC0000002 (STATUS_NOT_IMPLEMENTED); ret`.
  Every unimplemented Wine stub now returns an error instead of aborting; in
  practice only `NtQueryWnfStateData` is hit, and callers handle the failure.

If GDK-Proton changes layout, `patch_bytes` refuses (clear error) rather than
corrupting the DLL.

## Online / SSL

Bedrock GDK ships a stub `XCurl.dll`. It is replaced with a real
`libcurl-4.dll` (from MSYS2 mingw-w64) and a CA bundle is placed at
`<prefix>/etc/ssl/certs/ca-bundle.crt`. Without this, all HTTPS (auth, packs,
PlayFab) fails.

## Multiplayer — why ProxyPass + LAN

WineGDK has **no in-game Microsoft sign-in** (`XUser`/XSAPI not implemented).
Consequently Minecraft greys out *Servers ▸ Add server* (Microsoft gates
third-party servers behind sign-in). LAN multiplayer is **not** gated.

ProxyPass (`online-mode: true`) authenticates the user's Microsoft account
*outside* Wine and relays to the real destination server. Bound to
`0.0.0.0:19132`, Bedrock discovers it via the RakNet LAN broadcast and lists it
under **Play ▸ Friends**. The user joins it there; ProxyPass forwards to
`destination` with a legitimate Xbox Live identity.

`options.txt` gets `do_not_show_multiplayer_online_safety_warning:1`
(otherwise the warning can wedge the connect screen). Edited only while the
game is not running (Bedrock rewrites it on exit).

## Version matching

ProxyPass protocol is compiled-in. The Minecraft version is read from
`appxmanifest.xml` (`Identity Version="1.26.2101.0"` → game `1.26.21`). The
launcher picks ProxyPass release `pre/<ver>-*` (exact, else the highest
`<= ver`, else latest `master-*`). A mismatch shows "outdated client/server"
in game and a `NullPointerException` in ProxyPass on disconnect.

## Display

Wine-Wayland proved fragile (white screen / hang on X11 sessions). The launcher
defaults to X11, passing `DISPLAY`/`XAUTHORITY` through, and does **not** enable
the Wine Wayland driver.

## Data layout

```
~/.local/share/bedrock-on-linux/
├── settings.json     game_dir, server, chosen tags, flags
├── proton/GDK-Proton*/        (patched)
├── umu/umu-run
├── jre/                       (Temurin 25)
├── proxypass/{ProxyPass.jar,config.yml,data/,logs/}
├── prefix/                    (Wine prefix; options.txt; ca-bundle)
├── content  ->  <user game dir>
├── cache/                     (downloads)
└── logs/{minecraft.log,proxypass.log}
```

## v0.2 — versions, game source, packaging

* **Minecraft version source**: GitHub releases of a user-configurable archive
  repo (`GAME_ARCHIVE_REPO`, default `bubbles-wow/mcbe-gdk-unpack-archive`).
  Each release tag = a game version; the `*.zip` asset is the full GDK folder.
  `list_mc_versions()` enumerates them (stable/beta), `download_game()` fetches
  + unzips into `games/<tag>/`. A user folder can be used instead — no game
  files are shipped.
* **Version pickers**: GDK-Proton (`ensure_proton(tag)`), ProxyPass
  (`ensure_proxypass(tag)` or auto via `pick_proxypass`), Minecraft — all
  surfaced in the GUI, all stored in `settings.json`.
* **Microsoft login** is surfaced from ProxyPass stdout: the device-code URL +
  code are parsed and shown in the launcher (open-link / copy-code), with a
  "signed in" state derived from `proxypass/data/` + auth log lines.
* **Packaging**: `scripts/build-deb.sh` produces a real `.deb`
  (`/usr/lib/bedrock-on-linux/`, `/usr/bin` symlink, `.desktop`, hicolor icon;
  `Depends` pulls python3-tk/bubblewrap/zstd/…). `scripts/build-appimage.sh`
  for a portable single file. Icon generated by `scripts/make_icon.py` (pure
  zlib, no Pillow). The launcher resolves its bundled icon via
  `Path(__file__).resolve().parent/"data/icon.png"`, so the `/usr/bin` symlink
  must point into `/usr/lib/bedrock-on-linux/`.

## v0.3 — robustness & crash diagnostics

* **ProxyPass single instance**: `_pkill("ProxyPass.jar")` before every start
  (and on stop). Stacked instances → `BindException: Address already in use`
  on 0.0.0.0:19132 → dead relay → the joined LAN game points at nothing →
  disconnect/crash. This was a real, common crash source.
* **`diagnose()`**: after the game exits, the Proton/ProxyPass logs are
  scanned against `_DIAG_RULES` (combase/ntdll patch missing, display,
  GPU/Vulkan device-lost, OOM, ProxyPass bind, protocol mismatch, MS auth)
  and a human cause is surfaced. `launch()` now sets `PROTON_LOG=1` +
  `PROTON_LOG_DIR=logs/` and renames `steam-0.log` → `proton.log` so a crash
  is always analyzable. GUI has an "Ouvrir les logs" button.
* **Stale game cleanup**: `_pkill("Minecraft.Windows.exe")` before launch.
* **Release packaging**: `scripts/build-release.sh` → `.deb` + AppImage
  (`--appimage-extract-and-run`, no FUSE needed) + portable tarball;
  `RELEASE.md` is the release body. Tag scheme `vX.Y.Z`.

## Known limits / TODO

* Realms & native in-game Microsoft login: unsupported (WineGDK limit).
* GameInput partially stubbed (mouse/keyboard fine; some controllers may not).
* A token-injection `XUser` shim could enable in-game login — large RE effort,
  see project issues.
* AppImage packaging in `scripts/build-appimage.sh` is a scaffold.
