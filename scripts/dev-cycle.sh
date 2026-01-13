#!/usr/bin/env bash
set -euo pipefail

# 1) build+load images into k3s containerd
scripts/build-and-load.sh

# 2) deploy via helm
scripts/deploy-helm.sh

# Optional: wenn du oft den gleichen Tag nutzt und K8s cached,
# kannst du Rollout erzwingen (eigentlich besser: Tag hochzählen).
# kubectl -n stock-ui rollout restart deploy/stock-ui

echo "[dev-cycle] Open: http://stock-ui.local"
echo "[dev-cycle] If needed: echo '127.0.0.1 stock-ui.local' | sudo tee -a /etc/hosts"
