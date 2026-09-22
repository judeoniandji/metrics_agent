# System Metrics Agent

Application Python modulaire pour collecter et monitorer les métriques système (CPU, mémoire, charge système).

## Architecture

- **API** : FastAPI avec uvicorn exposant les endpoints /health, /metrics, /metrics/latest
- **Agent** : Collecteur autonome qui envoie les métriques à l'API via HTTP
- **Communication** : Réseau interne Docker (pas localhost)

## Prérequis

- Docker 29.7+ et Docker Compose
- Compte Docker Hub (pour le déploiement)
- Git

## Lancer en développement

```bash
docker compose build
docker compose up
```

L'API démarre sur http://localhost:8000 avec hot-reload.

## Lancer en production

### Depuis les images Docker Hub

```bash
docker compose -f docker-compose.prod.yaml pull
docker compose -f docker-compose.prod.yaml up
```

### Depuis un build local

```bash
docker compose build
docker compose up
```

## Pipeline CI/CD

Le workflow GitHub Actions (.github/workflows/ci-cd.yml) :
1. Build l'image Docker
2. Exécute pytest
3. Si les tests passent, push vers Docker Hub avec les tags :
   - latest (dernière version)
   - <commit-sha> (version spécifique)

### Secrets requis

Ajoute ces secrets dans GitHub Settings > Secrets:
- DOCKERHUB_USERNAME : ton username Docker Hub
- DOCKERHUB_TOKEN : ton access token Docker Hub

## Images Docker Hub

Disponibles sur : https://hub.docker.com/r/jude1955/system-metrics

Tags :
- latest : dernière version stable
- <sha> : version spécifique au commit

## Tests

```bash
docker run --rm system-metrics:latest pytest tests/
```

Les tests incluent :
- test_api.py : tests des endpoints FastAPI (/health, /metrics, /metrics/latest)
- test_collector.py : tests du collecteur de métriques système

## Déploiement Cloud

API en production sur Render : https://metrics-agent-awlo.onrender.com

Endpoint de test :
```bash
curl https://metrics-agent-awlo.onrender.com/health
```

Réponse :
```json
{"status":"ok"}
```

Note : L'instance Render gratuite s'endort après 15 minutes d'inactivité. Le premier appel peut prendre quelques secondes.

## Choix techniques

- Base image : python:3.12-slim (moderne, légère)
- Build multi-stage : sépare build et runtime, réduit la taille finale
- Non-root user : sécurité renforcée (utilisateur appuser)
- procps : pour la commande uptime sur Linux
- Réseau Docker : communication interne entre services (pas localhost)
- httpx : pour les tests du client HTTP

## Déploiement vérifié

OK - API démarre correctement
OK - Agent collecte les métriques
OK - Communication entre services fonctionnelle
OK - Images publiées sur Docker Hub
OK - Déploiement depuis images Docker Hub réussi
OK - Déploiement cloud sur Render fonctionnel
OK - Pipeline CI/CD automatisé et fonctionnel