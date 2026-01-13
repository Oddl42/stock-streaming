#!/usr/bin/env bash
set -euo pipefail

# Defaults (anpassen)
WEB_IMAGE="${WEB_IMAGE:-stock-ui:0.1.0}"
WEB_DOCKERFILE="${WEB_DOCKERFILE:-docker/Dockerfile.web}"
WEB_CONTEXT="${WEB_CONTEXT:-.}"

# Optional Spark (falls vorhanden)
SPARK_ENABLED="${SPARK_ENABLED:-false}"
SPARK_IMAGE="${SPARK_IMAGE:-stock-ui-spark:0.1.0}"
SPARK_DOCKERFILE="${SPARK_DOCKERFILE:-docker/Dockerfile.spark}"
SPARK_CONTEXT="${SPARK_CONTEXT:-.}"

scripts/build-image.sh "${WEB_IMAGE}" "${WEB_DOCKERFILE}" "${WEB_CONTEXT}"
scripts/load-into-k3s.sh "${WEB_IMAGE}"

if [[ "${SPARK_ENABLED}" == "true" ]]; then
  scripts/build-image.sh "${SPARK_IMAGE}" "${SPARK_DOCKERFILE}" "${SPARK_CONTEXT}"
  scripts/load-into-k3s.sh "${SPARK_IMAGE}"
fi

echo "[build+load] Done."
