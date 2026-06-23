# Déploiement

## Staging

Le déploiement de staging s'exécute automatiquement sur `main`.

## Production

Le déploiement de production s'exécute sur tag Git, avec validation manuelle avant l'étape de déploiement.

## Variables attendues

- `KUBECONFIG_STAGING`
- `KUBECONFIG_PROD`
- `SONAR_HOST_URL`
- `SONAR_TOKEN`
- `SENTRY_DSN`
- `SENTRY_AUTH_TOKEN`
- `SENTRY_ORG`
- `SENTRY_PROJECT`
