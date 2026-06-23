#!/usr/bin/env sh
set -eu

NAMESPACE=${1:?namespace required}
IMAGE_REF=${2:?image ref required}
APP_ENV=${3:?app environment required}
SENTRY_ENVIRONMENT=${4:?sentry environment required}
SENTRY_RELEASE=${5:?sentry release required}

kubectl create namespace "$NAMESPACE" --dry-run=client -o yaml | kubectl apply -f -
kubectl -n "$NAMESPACE" apply -f k8s/deployment.yaml -f k8s/service.yaml
kubectl -n "$NAMESPACE" set image deployment/tic-tac-toe-app tic-tac-toe-app="$IMAGE_REF"
kubectl -n "$NAMESPACE" set env deployment/tic-tac-toe-app APP_ENV="$APP_ENV" SENTRY_ENVIRONMENT="$SENTRY_ENVIRONMENT" SENTRY_RELEASE="$SENTRY_RELEASE"
kubectl -n "$NAMESPACE" rollout status deployment/tic-tac-toe-app --timeout=180s
