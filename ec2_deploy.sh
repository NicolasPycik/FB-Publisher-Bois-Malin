#!/bin/bash

# FB-Publisher-Bois-Malin EC2 Deployment Script
# For deployment on existing AWS EC2 instances
# Author: Manus AI
# Version: 1.0

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Configuration
APP_USER="fbpublisher"
APP_DIR="/opt/fb-publisher"
REPO_URL="https://github.com/NicolasPycik/FB-Publisher-Bois-Malin.git"

log() { echo -e "${BLUE}[$(date +'%H:%M:%S')]${NC} $1"; }
error() { echo -e "${RED}[ERROR]${NC} $1" >&2; }
success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }

# Check if running as root
if [[ $EUID -eq 0 ]]; then
    error "Don't run as root. Run as ubuntu user with sudo privileges."
    exit 1
fi

echo "=================================================="
echo "FB-Publisher-Bois-Malin EC2 Deployment"
echo "=================================================="
echo ""

# Step 1: Update system
log "Step 1: Updating system packages..."
sudo apt update && sudo apt upgrade -y
success "System updated"

# Step 2: Install dependencies
log "Step 2: Installing system dependencies..."
sudo apt install -y \
    software-properties-common \
    build-essential \
    python3-pip \
    git \
    curl \
    wget \
    xvfb \
    x11vnc \
    bc

# Install Python 3.11
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt update
sudo apt install -y python3.11 python3.11-venv python3.11-dev python3.11-tk
success "Dependencies installed"

# Step 3: Create application user
log "Step 3: Setting up application user and directories..."
if ! id "$APP_USER" &>/dev/null; then
    sudo useradd -m -s /bin/bash "$APP_USER"
fi

sudo mkdir -p "$APP_DIR"/{app,data,logs,backups}
sudo mkdir -p "$APP_DIR/data"/{pages,campaigns,schedules}
sudo chown -R "$APP_USER:$APP_USER" "$APP_DIR"
success "User and directories created"

# Step 4: Setup virtual display
log "Step 4: Setting up virtual display..."
sudo tee /etc/systemd/system/xvfb.service > /dev/null << 'EOF'
[Unit]
Description=X Virtual Frame Buffer Service
After=network.target

[Service]
ExecStart=/usr/bin/Xvfb :1 -screen 0 1024x768x24
Restart=on-failure
User=nobody
Group=nogroup

[Install]
WantedBy=multi-user.target
EOF

sudo tee /etc/systemd/system/x11vnc.service > /dev/null << 'EOF'
[Unit]
Description=x11vnc service
After=xvfb.service
Requires=xvfb.service

[Service]
ExecStart=/usr/bin/x11vnc -display :1 -nopw -listen localhost -xkb -forever
Restart=on-failure
User=nobody
Group=nogroup

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable xvfb.service x11vnc.service
sudo systemctl start xvfb.service x11vnc.service
success "Virtual display configured"

# Step 5: Clone repository
log "Step 5: Downloading application..."
sudo -u "$APP_USER" git clone "$REPO_URL" "$APP_DIR/app"
sudo find "$APP_DIR/app" -type f -exec chmod 644 {} \;
sudo find "$APP_DIR/app" -type d -exec chmod 755 {} \;
sudo chmod +x "$APP_DIR/app/main.py"
success "Application downloaded"

# Step 6: Setup Python environment
log "Step 6: Setting up Python environment..."
sudo -u "$APP_USER" python3.11 -m venv "$APP_DIR/venv"
sudo -u "$APP_USER" bash -c "
    source '$APP_DIR/venv/bin/activate'
    pip install --upgrade pip
    pip install -r '$APP_DIR/app/requirements.txt'
"
success "Python environment ready"

# Step 7: Create configuration
log "Step 7: Creating configuration files..."
sudo -u "$APP_USER" tee "$APP_DIR/app/.env" > /dev/null << 'EOF'
# Facebook API Configuration - EDIT THESE VALUES
APP_ID=your_facebook_app_id_here
APP_SECRET=your_facebook_app_secret_here
USER_ACCESS_TOKEN=your_long_term_access_token_here

# Application Settings
DEBUG=False
LOG_LEVEL=INFO
DATA_DIR=/opt/fb-publisher/data
LOG_DIR=/opt/fb-publisher/logs
DISPLAY=:1
GUI_ENABLED=True
SCHEDULER_ENABLED=True
EOF

sudo chmod 600 "$APP_DIR/app/.env"

# Create initial data files
sudo -u "$APP_USER" tee "$APP_DIR/data/pages/pages.json" > /dev/null << 'EOF'
{"pages": [], "last_updated": null, "version": "2.1"}
EOF

sudo -u "$APP_USER" tee "$APP_DIR/data/campaigns/campaigns.json" > /dev/null << 'EOF'
{"campaigns": [], "ad_accounts": [], "last_sync": null}
EOF

sudo -u "$APP_USER" tee "$APP_DIR/data/schedules/scheduled_posts.json" > /dev/null << 'EOF'
{"scheduled_posts": [], "next_execution": null}
EOF

success "Configuration created"

# Step 8: Create systemd service
log "Step 8: Creating system service..."
sudo tee /etc/systemd/system/fb-publisher.service > /dev/null << EOF
[Unit]
Description=Facebook Publisher Bois Malin Application
After=network.target xvfb.service
Requires=xvfb.service

[Service]
Type=simple
User=$APP_USER
Group=$APP_USER
WorkingDirectory=$APP_DIR/app
Environment=DISPLAY=:1
ExecStart=$APP_DIR/venv/bin/python main.py
Restart=on-failure
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable fb-publisher.service
success "Service created"

# Step 9: Create management scripts
log "Step 9: Creating management scripts..."

# Monitoring script
sudo -u "$APP_USER" tee "$APP_DIR/monitor.sh" > /dev/null << 'EOF'
#!/bin/bash
echo "FB-Publisher Status Check"
echo "========================"
echo "Service Status: $(systemctl is-active fb-publisher.service)"
echo "Process: $(pgrep -f 'python.*main.py' && echo 'RUNNING' || echo 'NOT RUNNING')"
echo "Display: $(DISPLAY=:1 xdpyinfo >/dev/null 2>&1 && echo 'OK' || echo 'ERROR')"
echo "Disk Usage: $(df /opt/fb-publisher | awk 'NR==2 {print $5}')"
echo ""
echo "Recent logs:"
sudo journalctl -u fb-publisher.service --no-pager -n 5
EOF

# Backup script
sudo -u "$APP_USER" tee "$APP_DIR/backup.sh" > /dev/null << 'EOF'
#!/bin/bash
BACKUP_DIR="/opt/fb-publisher/backups"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="fb-publisher-backup-${DATE}.tar.gz"

mkdir -p ${BACKUP_DIR}
tar -czf ${BACKUP_DIR}/${BACKUP_FILE} \
    --exclude='*.log' \
    --exclude='__pycache__' \
    /opt/fb-publisher/app \
    /opt/fb-publisher/data

find ${BACKUP_DIR} -name "fb-publisher-backup-*.tar.gz" -mtime +7 -delete
echo "Backup created: ${BACKUP_FILE}"
EOF

sudo chmod +x "$APP_DIR/monitor.sh" "$APP_DIR/backup.sh"
success "Management scripts created"

# Step 10: Configure firewall
log "Step 10: Configuring basic firewall..."
if command -v ufw >/dev/null; then
    sudo ufw allow ssh
    sudo ufw allow 5900/tcp
    echo "y" | sudo ufw enable
    success "Firewall configured"
else
    warning "UFW not available, configure security groups manually"
fi

# Final tests
log "Running deployment tests..."
if sudo -u "$APP_USER" bash -c "source '$APP_DIR/venv/bin/activate' && python3.11 --version"; then
    success "Python environment OK"
else
    error "Python environment test failed"
fi

if sudo systemctl is-active --quiet xvfb.service; then
    success "Virtual display OK"
else
    error "Virtual display test failed"
fi

echo ""
echo "=================================================="
echo "🎉 DEPLOYMENT COMPLETED SUCCESSFULLY! 🎉"
echo "=================================================="
echo ""
echo "NEXT STEPS:"
echo ""
echo "1. Configure Facebook API credentials:"
echo "   sudo nano $APP_DIR/app/.env"
echo ""
echo "2. Edit these values:"
echo "   APP_ID=your_facebook_app_id"
echo "   APP_SECRET=your_facebook_app_secret"
echo "   USER_ACCESS_TOKEN=your_access_token"
echo ""
echo "3. Start the application:"
echo "   sudo systemctl start fb-publisher.service"
echo ""
echo "4. Check status:"
echo "   sudo systemctl status fb-publisher.service"
echo "   $APP_DIR/monitor.sh"
echo ""
echo "5. Access GUI via VNC (optional):"
echo "   ssh -L 5901:localhost:5900 ubuntu@$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4)"
echo "   Then connect VNC client to localhost:5901"
echo ""
echo "6. View logs:"
echo "   sudo journalctl -u fb-publisher.service -f"
echo ""
echo "USEFUL COMMANDS:"
echo "- Monitor: $APP_DIR/monitor.sh"
echo "- Backup: $APP_DIR/backup.sh"
echo "- Restart: sudo systemctl restart fb-publisher.service"
echo ""
echo "For troubleshooting, check the deployment guide."
echo "=================================================="

