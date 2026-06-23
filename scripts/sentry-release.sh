#!/usr/bin/env sh
set -eu

: "${SENTRY_AUTH_TOKEN:?Missing SENTRY_AUTH_TOKEN}"
: "${SENTRY_ORG:?Missing SENTRY_ORG}"
: "${SENTRY_PROJECT:?Missing SENTRY_PROJECT}"
: "${SENTRY_RELEASE:?Missing SENTRY_RELEASE}"

sentry-cli releases new "$SENTRY_RELEASE"
sentry-cli releases set-commits "$SENTRY_RELEASE" --auto
sentry-cli releases finalize "$SENTRY_RELEASE"
