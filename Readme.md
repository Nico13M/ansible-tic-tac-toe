# tic-tac-toe-ynov

## Description
Ce projet implémente un jeu simple de morpion (Tic-Tac-Toe) en Python. Le jeu permet à deux joueurs de jouer à tour de rôle sur une grille 3x3. Le premier joueur à aligner trois de ses symboles (horizontalement, verticalement ou en diagonale) gagne. Si la grille est pleine et qu’aucun joueur n’a aligné trois symboles, la partie se termine par un match nul.

## Fonctionnalités
- Jeu à deux joueurs
- Validation des saisies des joueurs
- Détection des conditions de victoire et de match nul
- Option de rejouer à la fin de chaque partie
- Suivi persistant du score pendant les parties rejouées

## Prérequis
- Python 3.6 ou version supérieure

---

# Déploiement Ansible

Cette partie automatise le déploiement complet de l’application conteneurisée sur une machine virtuelle Debian 13 fraîchement installée à l’aide d’Ansible.

## Architecture

```text
Machine de contrôle                VM cible (Debian 13)
─────────────────────    SSH →     ──────────────────────
ansible-tic-tac-toe/               - Docker (installé par Ansible)
├── inventory/                     - Conteneur tic-tac-toe (en cours d’exécution)
├── roles/
├── playbook.yml
└── requirements.yml
                         pull ←    Docker Hub (<dockerhub_username>/tic-tac-toe-ynov)
```

## Structure du projet Ansible

```text
ansible-tic-tac-toe/
├── inventory/
│   └── hosts.ini
├── roles/
│   └── deploy_app/
│       ├── defaults/
│       │   └── main.yml
│       ├── meta/
│       │   └── main.yml
│       └── tasks/
│           └── main.yml
├── playbook.yml
└── requirements.yml
```

## Prérequis

- Ansible installé sur la machine de contrôle (`brew install ansible` sur Mac, `pip install ansible` sinon)
- Accès SSH à une VM Debian 13 fraîche avec les droits `sudo`
- `PasswordAuthentication yes` activé dans `/etc/ssh/sshd_config` sur la VM

## Configuration de l’inventaire

Modifiez `inventory/hosts.ini` avec vos propres valeurs :

```ini
[debian_vm]
debian13 ansible_host=<VM_IP> ansible_user=<VM_USER> ansible_become=true ansible_port=<SSH_PORT>
```

Puis mettez à jour `roles/deploy_app/defaults/main.yml` :

```yaml
app_image: nico/tic-tac-toe-ynov
app_container_name: tic-tac-toe-app
app_env: production
```

## Déploiement

```bash
# Installer la collection Docker
ansible-galaxy collection install -r requirements.yml

# Exécuter le playbook
ansible-playbook -i inventory/hosts.ini playbook.yml --ask-pass --ask-become-pass
```

## Ce que fait le rôle

1. Met à jour le cache APT
2. Installe les prérequis Docker (`ca-certificates`, `curl`, `gnupg`)
3. Ajoute la clé GPG officielle de Docker et le dépôt APT
4. Installe Docker Engine (`docker-ce`, `docker-ce-cli`, `containerd.io`)
5. Démarre et active le service Docker au démarrage
6. Récupère l’image depuis Docker Hub
7. Lance le conteneur avec `restart_policy: unless-stopped`

## Justification du choix du conteneur

**Docker** a été choisi plutôt que Podman car :
- Il dispose d’un support natif via la collection Ansible `community.docker`
- Le `Dockerfile` et le `compose.yaml` existants sont déjà basés sur Docker
- Des modules idempotents (`docker_image`, `docker_container`) sont disponibles

## Remarques sur l’utilisation de `shell` / `command`

Une tâche `ansible.builtin.command` est utilisée pour récupérer l’architecture du système via `dpkg --print-architecture`. Aucun module Ansible spécialisé ne renvoie le format compatible Debian (`amd64`/`arm64`) requis par le dépôt APT de Docker — `ansible_architecture` renvoie `x86_64`, ce qui est incompatible. `changed_when: false` garantit l’idempotence.

## Idempotence

- `apt` avec `state: present` est naturellement idempotent
- `get_url` avec `force: false` évite le téléchargement si le fichier existe déjà
- `docker_image` avec `state: present` évite le téléchargement si l’image est déjà présente localement
- `docker_container` avec `state: started` ne recrée pas un conteneur déjà en cours d’exécution
- `restart_policy: unless-stopped` garantit que le conteneur survit aux redémarrages de la VM

## Accéder à l’application

Connectez-vous à la VM et attachez-vous au conteneur en cours d’exécution :

```bash
ssh -p <SSH_PORT> <VM_USER>@<VM_IP>
sudo docker exec -it tic-tac-toe-app python tic_tac_toe.py
```

## Sortie d’exécution du playbook

```text
PLAY [Deploy containerized application] *******************************************

TASK [Gathering Facts] ************************************************************
ok: [debian13]

TASK [deploy_app : Update apt cache] **********************************************
ok: [debian13]

TASK [deploy_app : Install Docker prerequisites] **********************************
changed: [debian13]

TASK [deploy_app : Create /etc/apt/keyrings directory] ****************************
ok: [debian13]

TASK [deploy_app : Download Docker GPG key] ***************************************
changed: [debian13]

TASK [deploy_app : Register system architecture] **********************************
ok: [debian13]

TASK [deploy_app : Add Docker APT repository] *************************************
changed: [debian13]

TASK [deploy_app : Install Docker Engine] *****************************************
changed: [debian13]

TASK [deploy_app : Ensure Docker service is started and enabled] ******************
ok: [debian13]

TASK [deploy_app : Pull application image] ****************************************
changed: [debian13]

TASK [deploy_app : Run application container] *************************************
changed: [debian13]

PLAY RECAP ************************************************************************
debian13 : ok=11   changed=6   unreachable=0   failed=0   skipped=0   rescued=0   ignored=0
```

---

## Hooks Pre-commit

Ce projet utilise le framework `pre-commit` afin de garantir la qualité du code. Les hooks suivants sont configurés :
- Suppression des espaces en fin de ligne
- Correction automatique de la fin de fichier
- Vérification des fichiers YAML
- Formatage du code Python avec `black`
- Analyse statique avec `flake8`

Pour installer les hooks :

```bash
pre-commit install
```

## Versionnage sémantique

Ce projet suit le versionnage sémantique (Semantic Versioning). Un tag sera créé pour chaque version publiée.

## Contribution

Tous les commits doivent respecter le format Conventional Commits. Veuillez créer des merge requests ou pull requests pour toute modification et vous assurer que les discussions sont correctement documentées.
