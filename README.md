<div align="center">

# 🟩 BedrockOnLinux

**Minecraft Bedrock (Windows / GDK edition) on Linux — multiplayer included.
A real app: install it, pick your version, play.**

`Ubuntu` · `Debian` · `Linux Mint / LMDE` · `Fedora` · `Arch` · `openSUSE`

![BedrockOnLinux](screenshot.png)

</div>

---

## ✨ What it does

Everything, for you, in one app:

- 📦 downloads **GDK-Proton** and applies the **2 binary patches** without
  which the game won't start (`combase.RoOriginateErrorW` + all of `ntdll`'s
  unimplemented-stub funnels);
- 🧩 downloads **umu-launcher** (Steam Linux Runtime → works on every distro),
  a bundled **Java 25**, and the **right ProxyPass build**;
- 🌐 runs **ProxyPass in the background** for multiplayer (WineGDK has no
  in-game Microsoft login — ProxyPass authenticates outside Wine);
- 🎮 sets up the Wine prefix, curl/SSL, GameInput, `options.txt`, then
  launches the game.

You pick the **Minecraft version** (stable or beta), **sign in to Microsoft**
(the code is shown in the app), set the **server IP**, click **Play**.

## ⬇️ Install

### Debian / Ubuntu / Mint — `.deb`

```bash
sudo apt install ./bedrock-on-linux_*_all.deb
```
Apt pulls the dependencies. **BedrockOnLinux then shows up in your menu /
search** with its icon.

### Any distro — `AppImage`

```bash
chmod +x BedrockOnLinux-*-x86_64.AppImage
./BedrockOnLinux-*-x86_64.AppImage
```

### Portable — tarball

```bash
tar xzf bedrock-on-linux-*-portable.tar.gz && cd bedrock-on-linux
./bedrock-on-linux gui          # or: ./bedrock-on-linux doctor
```

> Requirements (present almost everywhere): `python3`, `python3-tk`, `tar`,
> `bubblewrap`, `zstd`. `bedrock-on-linux doctor` tells you what's missing
> and the exact command to install it.

## ▶️ Play

1. Open **BedrockOnLinux**.
2. **① Version**: pick one (e.g. `1.26.21.1`) — downloaded for you.
3. **④ Microsoft account** → *Sign in*: open the shown link, enter the code,
   sign in with the account that **owns Minecraft**.
4. **③ Server**: default IP is `play.linesia.net` (editable).
5. **Install / Update**, then **▶ Play**.
6. In game: **Play ▸ Friends tab ▸ join the LAN game**
   *(the "Add server" button is greyed out under WineGDK — that's expected;
   we go through LAN, ProxyPass bridges to your server).*

## 🩺 If it crashes

The app **diagnoses automatically**: when the game exits, the likely cause
is printed in the log (port in use, GPU/Vulkan, ProxyPass version, missing
patch, …). Use **🗎 Open logs** to see everything
(`~/.local/share/bedrock-on-linux/logs/`). A common, already-handled cause:
stacked ProxyPass instances — the app now kills dead ones before relaunching.

## 🧑‍💻 Command line

```bash
bedrock-on-linux versions                 # available Minecraft versions
bedrock-on-linux setup --mc 1.26.21.1     # install that version + everything
bedrock-on-linux config --server play.linesia.net:19132
bedrock-on-linux play
bedrock-on-linux doctor
```

## ⚖️ Legal

BedrockOnLinux **ships no Minecraft files**: it is a **compatibility
launcher** (like Heroic / mcpelauncher). Game files come from a
**source you choose** (default: the community archive
[`bubbles-wow/mcbe-gdk-unpack-archive`](https://github.com/bubbles-wow/mcbe-gdk-unpack-archive))
or your own folder — you must own Minecraft. GDK-Proton, umu-launcher,
ProxyPass and Temurin are free software under their own licenses. Realms and
the *in-game* native Microsoft login are not supported (WineGDK limitation;
server multiplayer goes through ProxyPass).

## 🛠️ Build the packages

```bash
scripts/build-release.sh        # .deb + AppImage + portable tar.gz in dist/
```

## 📄 License

MIT — see [`LICENSE`](LICENSE).
