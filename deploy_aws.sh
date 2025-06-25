#!/bin/bash

# =============================================================================
# Script de Déploiement AWS - Facebook Publisher SaaS v3.1.0
# =============================================================================

set -e  # Exit on any error

echo "🚀 Déploiement Facebook Publisher SaaS v3.1.0 sur AWS"
echo "=================================================="

# Configuration
APP_NAME="facebook_publisher_saas"
APP_DIR="/opt/$APP_NAME"
SERVICE_NAME="facebook-publisher"
PYTHON_VERSION="python3.11"

# Couleurs pour les logs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Vérifier les privilèges sudo
check_sudo() {
    if [[ $EUID -ne 0 ]]; then
        log_error "Ce script doit être exécuté avec sudo"
        exit 1
    fi
}

# Installer les dépendances système
install_dependencies() {
    log_info "Installation des dépendances système..."
    
    apt-get update
    apt-get install -y \
        python3.11 \
        python3.11-pip \
        python3.11-venv \
        nginx \
        supervisor \
        git \
        curl \
        unzip
    
    log_success "Dépendances système installées"
}

# Créer l'utilisateur de l'application
create_app_user() {
    log_info "Création de l'utilisateur de l'application..."
    
    if ! id "$APP_NAME" &>/dev/null; then
        useradd --system --shell /bin/bash --home-dir $APP_DIR --create-home $APP_NAME
        log_success "Utilisateur $APP_NAME créé"
    else
        log_warning "Utilisateur $APP_NAME existe déjà"
    fi
}

# Déployer l'application
deploy_application() {
    log_info "Déploiement de l'application..."
    
    # Arrêter le service s'il existe
    if systemctl is-active --quiet $SERVICE_NAME; then
        systemctl stop $SERVICE_NAME
        log_info "Service $SERVICE_NAME arrêté"
    fi
    
    # Créer le répertoire de l'application
    mkdir -p $APP_DIR
    
    # Copier les fichiers (supposant que le code est dans le répertoire courant)
    if [ -d "./facebook_publisher_saas" ]; then
        cp -r ./facebook_publisher_saas/* $APP_DIR/
        log_success "Fichiers de l'application copiés"
    else
        log_error "Répertoire source ./facebook_publisher_saas non trouvé"
        exit 1
    fi
    
    # Changer les permissions
    chown -R $APP_NAME:$APP_NAME $APP_DIR
    chmod +x $APP_DIR/app.py
}

# Configurer l'environnement Python
setup_python_env() {
    log_info "Configuration de l'environnement Python..."
    
    # Créer l'environnement virtuel
    sudo -u $APP_NAME $PYTHON_VERSION -m venv $APP_DIR/venv
    
    # Installer les dépendances Python
    sudo -u $APP_NAME $APP_DIR/venv/bin/pip install --upgrade pip
    sudo -u $APP_NAME $APP_DIR/venv/bin/pip install \
        flask==3.1.1 \
        flask-cors==6.0.1 \
        requests==2.32.4 \
        python-dotenv==1.1.1 \
        gunicorn==21.2.0
    
    log_success "Environnement Python configuré"
}

# Configurer le service systemd
setup_systemd_service() {
    log_info "Configuration du service systemd..."
    
    cat > /etc/systemd/system/$SERVICE_NAME.service << EOF
[Unit]
Description=Facebook Publisher SaaS v3.1.0
After=network.target

[Service]
Type=exec
User=$APP_NAME
Group=$APP_NAME
WorkingDirectory=$APP_DIR
Environment=PATH=$APP_DIR/venv/bin
Environment=FLASK_APP=app.py
Environment=FLASK_ENV=production
ExecStart=$APP_DIR/venv/bin/gunicorn --bind 0.0.0.0:5001 --workers 4 --timeout 120 app:app
ExecReload=/bin/kill -s HUP \$MAINPID
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF
    
    systemctl daemon-reload
    systemctl enable $SERVICE_NAME
    
    log_success "Service systemd configuré"
}

# Configurer Nginx
setup_nginx() {
    log_info "Configuration de Nginx..."
    
    cat > /etc/nginx/sites-available/$APP_NAME << EOF
server {
    listen 80;
    server_name _;
    
    client_max_body_size 50M;
    
    location / {
        proxy_pass http://127.0.0.1:5001;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
    
    location /static {
        alias $APP_DIR/src/static;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
EOF
    
    # Activer le site
    ln -sf /etc/nginx/sites-available/$APP_NAME /etc/nginx/sites-enabled/
    rm -f /etc/nginx/sites-enabled/default
    
    # Tester la configuration
    nginx -t
    systemctl reload nginx
    
    log_success "Nginx configuré"
}

# Créer le fichier de configuration
create_config() {
    log_info "Création du fichier de configuration..."
    
    cat > $APP_DIR/.env << EOF
# Configuration Facebook Publisher SaaS v3.1.0
FACEBOOK_ACCESS_TOKEN=your_facebook_access_token_here
FACEBOOK_APP_ID=your_facebook_app_id_here
FACEBOOK_APP_SECRET=your_facebook_app_secret_here

# Configuration Flask
FLASK_ENV=production
FLASK_DEBUG=False

# Configuration de l'application
PORT=5001
HOST=0.0.0.0
EOF
    
    chown $APP_NAME:$APP_NAME $APP_DIR/.env
    chmod 600 $APP_DIR/.env
    
    log_success "Fichier de configuration créé"
}

# Créer les répertoires de données
create_data_dirs() {
    log_info "Création des répertoires de données..."
    
    mkdir -p $APP_DIR/data
    mkdir -p $APP_DIR/logs
    mkdir -p $APP_DIR/uploads
    
    # Créer les fichiers de données par défaut
    echo "[]" > $APP_DIR/data/audiences.json
    echo "[]" > $APP_DIR/data/scheduled_posts.json
    
    chown -R $APP_NAME:$APP_NAME $APP_DIR/data
    chown -R $APP_NAME:$APP_NAME $APP_DIR/logs
    chown -R $APP_NAME:$APP_NAME $APP_DIR/uploads
    
    log_success "Répertoires de données créés"
}

# Démarrer les services
start_services() {
    log_info "Démarrage des services..."
    
    systemctl start $SERVICE_NAME
    systemctl status $SERVICE_NAME --no-pager
    
    log_success "Service $SERVICE_NAME démarré"
}

# Vérifier le déploiement
verify_deployment() {
    log_info "Vérification du déploiement..."
    
    sleep 5
    
    # Vérifier que l'application répond
    if curl -f http://localhost:5001/ > /dev/null 2>&1; then
        log_success "Application accessible sur le port 5001"
    else
        log_error "Application non accessible sur le port 5001"
        return 1
    fi
    
    # Vérifier Nginx
    if curl -f http://localhost/ > /dev/null 2>&1; then
        log_success "Nginx fonctionne correctement"
    else
        log_error "Problème avec Nginx"
        return 1
    fi
    
    log_success "Déploiement vérifié avec succès"
}

# Afficher les informations finales
show_final_info() {
    echo ""
    echo "🎉 DÉPLOIEMENT TERMINÉ AVEC SUCCÈS !"
    echo "=================================="
    echo ""
    echo "📍 Application déployée dans : $APP_DIR"
    echo "🌐 URL d'accès : http://$(curl -s ifconfig.me)/"
    echo "🔧 Service systemd : $SERVICE_NAME"
    echo ""
    echo "📋 COMMANDES UTILES :"
    echo "  • Statut du service : sudo systemctl status $SERVICE_NAME"
    echo "  • Redémarrer : sudo systemctl restart $SERVICE_NAME"
    echo "  • Logs : sudo journalctl -u $SERVICE_NAME -f"
    echo "  • Configuration : sudo nano $APP_DIR/.env"
    echo ""
    echo "⚠️  N'OUBLIEZ PAS :"
    echo "  1. Configurer vos tokens Facebook dans $APP_DIR/.env"
    echo "  2. Redémarrer le service après configuration : sudo systemctl restart $SERVICE_NAME"
    echo ""
}

# Fonction principale
main() {
    log_info "Début du déploiement Facebook Publisher SaaS v3.1.0"
    
    check_sudo
    install_dependencies
    create_app_user
    deploy_application
    setup_python_env
    create_config
    create_data_dirs
    setup_systemd_service
    setup_nginx
    start_services
    verify_deployment
    show_final_info
    
    log_success "Déploiement terminé avec succès !"
}

# Exécuter le script principal
main "$@"

