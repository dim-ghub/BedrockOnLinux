# BedrockOnLinux v0.3.0

Minecraft Bedrock (édition Windows / GDK) sur Linux, multijoueur compris —
une vraie appli graphique, tout est téléchargé et configuré automatiquement.

## Téléchargements

| Plateforme | Fichier |
|---|---|
| Debian / Ubuntu / Mint | `bedrock-on-linux_0.3.0_all.deb` |
| Toutes distros (universel) | `BedrockOnLinux-0.3.0-x86_64.AppImage` |
| Portable / autres | `bedrock-on-linux-0.3.0-portable.tar.gz` |

```bash
# .deb
sudo apt install ./bedrock-on-linux_0.3.0_all.deb
# AppImage
chmod +x BedrockOnLinux-0.3.0-x86_64.AppImage && ./BedrockOnLinux-0.3.0-x86_64.AppImage
```

## Nouveautés v0.3.0

- 🎨 Interface launcher moderne (thème sombre, cartes, logo, bouton JOUER).
- 🧱 Choix de la **version Minecraft** (stable/bêta, téléchargée), de
  **GDK‑Proton** et de **ProxyPass** ; **login Microsoft dans l'appli**.
- 🌐 IP serveur par défaut : `play.linesia.net`.
- 🛡️ **ProxyPass en instance unique** : les instances mortes sont tuées
  avant relance (corrige le `BindException: Address already in use` qui
  cassait le multi et provoquait des crashes).
- 🩺 **Diagnostic automatique de crash** : à la fermeture du jeu, la cause
  probable s'affiche (port occupé, GPU/Vulkan, version ProxyPass, patch
  manquant, …) + bouton **Ouvrir les logs**.
- 🐛 Correction du bug `unexpected keyword argument 'game_dir'`.
- 📦 Paquets `.deb` + `AppImage` + tarball portable, icône, entrée menu.

## Prérequis

`python3`, `python3-tk`, `tar`, `bubblewrap`, `zstd` (le `.deb` les tire
seul ; sinon `bedrock-on-linux doctor`).

## Limites connues

Realms et le login Microsoft *natif dans le jeu* ne sont pas supportés
(limite WineGDK) — le multijoueur serveurs passe par ProxyPass (LAN).

🤖 Generated with [Claude Code](https://claude.com/claude-code)
