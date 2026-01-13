#!/usr/bin/env bash
set -euo pipefail

IMAGE="${1:?Usage: load-into-k3s.sh <image:tag>}"

if ! command -v k3s >/dev/null 2>&1; then
  echo "ERROR: k3s not found. Is k3s installed?" >&2
  exit 1
fi

echo "[load] Saving ${IMAGE} and importing into k3s containerd..."
docker save "${IMAGE}" | sudo k3s ctr images import -

echo "[load] Verifying image exists in k3s containerd..."
sudo k3s ctr images ls | grep -F "${IMAGE}" >/dev/null

echo "[load] OK: ${IMAGE} is available to k3s"
