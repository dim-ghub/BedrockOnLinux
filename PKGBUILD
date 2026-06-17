# Maintainer: dim-ghub
# Contributor: Wyze3306 <https://github.com/Wyze3306>

pkgname=bedrock-on-linux-git
pkgver=1.0.13
pkgrel=1
pkgdesc="Minecraft Bedrock (Windows GDK edition) on Linux — native in-game Microsoft sign-in and multiplayer"
arch=('any')
url="https://github.com/dim-ghub/BedrockOnLinux"
license=('MIT')
depends=('python' 'tk')
makedepends=('git')
source=("git+https://github.com/dim-ghub/BedrockOnLinux.git")
sha256sums=('SKIP')

pkgver() {
  cd "BedrockOnLinux"
  printf "1.0.13.r%s.%s" "$(git rev-list --count HEAD)" "$(git rev-parse --short HEAD)"
}

package() {
  cd "BedrockOnLinux"
  install -Dm755 bedrock-on-linux "$pkgdir/usr/bin/bedrock-on-linux"
  install -Dm644 data/icon.png "$pkgdir/usr/share/icons/hicolor/256x256/apps/bedrock-on-linux.png"
  install -Dm644 data/bg.png "$pkgdir/usr/share/bedrock-on-linux/bg.png"
  install -Dm644 data/bedrock-on-linux.desktop "$pkgdir/usr/share/applications/bedrock-on-linux.desktop"
  install -Dm644 LICENSE "$pkgdir/usr/share/licenses/$pkgname/LICENSE"
}
