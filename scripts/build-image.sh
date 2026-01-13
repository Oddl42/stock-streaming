#!/usr/bin/env bash
set -euo pipefail

IMAGE="${1:?Usage: build-image.sh <image:tag> <dockerfile> [context] }"
DOCKERFILE="${2:?Usage: build-image.sh <image:tag> <dockerfile> [context] }"
CONTEXT="${3:-.}"

echo "[build] Building ${IMAGE} using ${DOCKERFILE} (context: ${CONTEXT})"
docker build -t "${IMAGE}" -f "${DOCKERFILE}" "${CONTEXT}"
echo "[build] Done: ${IMAGE}"
