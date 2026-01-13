#!/usr/bin/env bash
set -euo pipefail

NAMESPACE="${NAMESPACE:-stock-ui}"
RELEASE="${RELEASE:-stock-ui}"
CHART_PATH="${CHART_PATH:-helm/stock-ui}"

INGRESS_HOST="${INGRESS_HOST:-stock-ui.local}"

WEB_IMAGE_REPO="${WEB_IMAGE_REPO:-stock-ui}"
WEB_IMAGE_TAG="${WEB_IMAGE_TAG:-0.1.0}"

MASSIVE_API_KEY="${MASSIVE_API_KEY:-CHANGE_ME}"
MASSIVE_MOCK="${MASSIVE_MOCK:-true}"

echo "[helm] Namespace: ${NAMESPACE}"
kubectl get ns "${NAMESPACE}" >/dev/null 2>&1 || kubectl create ns "${NAMESPACE}"

echo "[helm] Dependency update (Postgres chart etc.)"
helm dependency update "${CHART_PATH}"

echo "[helm] Upgrade/install ${RELEASE}"
helm upgrade --install "${RELEASE}" "${CHART_PATH}" \
  -n "${NAMESPACE}" \
  --set image.repository="${WEB_IMAGE_REPO}" \
  --set image.tag="${WEB_IMAGE_TAG}" \
  --set ingress.host="${INGRESS_HOST}" \
  --set app.secret.MASSIVE_API_KEY="${MASSIVE_API_KEY}" \
  --set app.env.MASSIVE_MOCK="${MASSIVE_MOCK}"

echo "[helm] Rollout status"
kubectl -n "${NAMESPACE}" rollout status deploy/"${RELEASE}" --timeout=120s

echo "[helm] Done."
