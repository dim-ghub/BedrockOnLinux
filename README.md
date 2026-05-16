# BedrockOnLinux

**Installer et jouer à Minecraft Bedrock (édition Windows / GDK) sur n'importe
quel Linux — multijoueur compris — avec une vraie appli.** Tu l'installes, elle
apparaît dans le menu/la recherche, tu choisis ta version, tu te connectes à
Microsoft, tu mets l'IP du serveur, tu joues. Pas 40 trucs à installer.

> Ubuntu · Debian · Linux Mint/LMDE · Fedora · Arch · openSUSE …

## Installer

### .deb (Debian / Ubuntu / Mint) — recommandé

```bash
scripts/build-deb.sh                       # produit dist/bedrock-on-linux_*.deb
sudo apt install ./dist/bedrock-on-linux_*_all.deb
```

Apt installe automatiquement les dépendances (python3‑tk, bubblewrap, zstd…).
**BedrockOnLinux apparaît alors dans le menu et la barre de recherche** (icône
incluse).

### AppImage (toutes distros, sans root)

```bash
scripts/build-appimage.sh                  # produit dist/BedrockOnLinux-x86_64.AppImage
```

### Sans installer

```bash
./bedrock-on-linux gui          # interface
./bedrock-on-linux doctor       # vérifie les prérequis
```

## L'interface launcher

Avant de lancer le jeu, l'appli te laisse tout régler :

| Réglage | Détail |
|--------|--------|
| **Version Minecraft** | liste déroulante (stables **et** bêtas) — téléchargée pour toi ; ou « choisir un dossier » si tu as déjà tes fichiers |
| **GDK‑Proton** | version au choix (défaut : la dernière) — **patchée automatiquement** pour que le jeu démarre |
| **ProxyPass** | auto‑sélectionné selon ta version de Minecraft (ou manuel) |
| **Serveur** | adresse + port du serveur où te connecter (config ProxyPass) |
| **Compte Microsoft** | bouton *Se connecter* → le code `microsoft.com/link` s'affiche dans l'appli (boutons *Ouvrir le lien* / *Copier le code*), état « Connecté ✓ » |

Puis **Installer / Mettre à jour** (téléchargements, une fois) et **▶ JOUER**.
ProxyPass tourne en arrière‑plan ; **en jeu : Jouer ▸ onglet Amis ▸ rejoindre
la partie LAN** (sous WineGDK le bouton « Ajouter un serveur » est grisé, c'est
normal, on passe par le LAN).

## En ligne de commande

```bash
bedrock-on-linux versions                    # liste les versions dispo
bedrock-on-linux setup --mc 1.26.21.1        # télécharge cette version + tout
bedrock-on-linux config --server play.galaxite.net:19132
bedrock-on-linux play
```

## Ce que l'appli télécharge et fait, seule

GDK‑Proton (+ **2 patchs binaires** indispensables : `combase.RoOriginateErrorW`
et tous les *stub funnels* de `ntdll`), umu‑launcher (Steam Linux Runtime →
marche partout), Java 25 embarqué, la bonne build de ProxyPass, libcurl/SSL,
prefix Wine, GameInput, `options.txt`. Détails : [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md).

## Légal

BedrockOnLinux **ne distribue aucun fichier Minecraft**. C'est un **lanceur de
compatibilité** (comme Heroic / mcpelauncher). Les fichiers de jeu proviennent
d'une **source choisie par l'utilisateur** (par défaut l'archive communautaire
[`bubbles-wow/mcbe-gdk-unpack-archive`](https://github.com/bubbles-wow/mcbe-gdk-unpack-archive))
ou de ton propre dossier. Tu dois posséder Minecraft. GDK‑Proton,
umu‑launcher, ProxyPass et Temurin sont libres, récupérés depuis leurs sources
officielles, sous leurs licences respectives. Realms / connexion Microsoft
*native dans le jeu* : non supportés (limite WineGDK) — le multi serveurs passe
par ProxyPass.

## Licence

MIT — voir [`LICENSE`](LICENSE).
