# BedrockOnLinux v0.3.0

Minecraft Bedrock (Windows / GDK edition) on Linux, multiplayer included — a
real graphical app; everything is downloaded and configured automatically.

## Downloads

| Platform | File |
|---|---|
| Debian / Ubuntu / Mint | `bedrock-on-linux_0.3.0_all.deb` |
| Any distro (universal) | `BedrockOnLinux-0.3.0-x86_64.AppImage` |
| Portable / other | `bedrock-on-linux-0.3.0-portable.tar.gz` |

```bash
# .deb
sudo apt install ./bedrock-on-linux_0.3.0_all.deb
# AppImage
chmod +x BedrockOnLinux-0.3.0-x86_64.AppImage && ./BedrockOnLinux-0.3.0-x86_64.AppImage
```

## What's new in 0.3.0

- 🎨 Modern dark launcher UI (cards, logo, Play button).
- 🧱 Pick the **Minecraft version** (stable/beta, downloaded), **GDK-Proton**
  and **ProxyPass**; **in-app Microsoft login**.
- 🌐 Default server IP: `play.linesia.net`.
- 🛡️ **ProxyPass single instance**: dead instances are killed before relaunch
  (fixes `BindException: Address already in use`, which broke multiplayer and
  caused crashes).
- 🩺 **Automatic crash diagnostics**: on exit the probable cause is shown
  (port in use, GPU/Vulkan, ProxyPass version, missing patch, …) plus an
  **Open logs** button.
- 🐛 Fixed the `unexpected keyword argument 'game_dir'` bug.
- 📦 `.deb` + `AppImage` + portable tarball, icon, menu entry.

## Requirements

`python3`, `python3-tk`, `tar`, `bubblewrap`, `zstd` (the `.deb` pulls them
automatically; otherwise run `bedrock-on-linux doctor`).

## Known limitations

Realms and the *in-game* native Microsoft login are not supported (WineGDK
limitation) — server multiplayer goes through ProxyPass (LAN).
