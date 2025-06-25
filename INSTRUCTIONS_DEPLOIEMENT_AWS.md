# 🚀 Instructions de Déploiement AWS - Facebook Publisher SaaS v3.1.0

## 📋 **DÉPLOIEMENT SUR VOTRE SERVEUR AWS**

### 🎯 **Méthode Recommandée : Script Automatisé**

#### **Étape 1 : Transférer les fichiers sur votre serveur AWS**

```bash
# Sur votre machine locale, transférer le package vers AWS
scp -i your-key.pem Facebook_Publisher_SaaS_v3.1.0_FINAL.zip ubuntu@ec2-35-180-252-182.eu-west-3.compute.amazonaws.com:~/
scp -i your-key.pem deploy_aws.sh ubuntu@ec2-35-180-252-182.eu-west-3.compute.amazonaws.com:~/
```

#### **Étape 2 : Se connecter au serveur AWS**

```bash
ssh -i your-key.pem ubuntu@ec2-35-180-252-182.eu-west-3.compute.amazonaws.com
```

#### **Étape 3 : Extraire et déployer**

```bash
# Extraire le package
unzip Facebook_Publisher_SaaS_v3.1.0_FINAL.zip

# Exécuter le script de déploiement automatisé
sudo ./deploy_aws.sh
```

### 🔧 **Le Script Automatisé Fait Tout :**

- ✅ **Installe Python 3.11** et toutes les dépendances
- ✅ **Configure Nginx** comme reverse proxy
- ✅ **Crée le service systemd** pour auto-démarrage
- ✅ **Configure l'environnement virtuel** Python
- ✅ **Déploie l'application** dans `/opt/facebook_publisher_saas`
- ✅ **Configure les permissions** et sécurité
- ✅ **Démarre automatiquement** l'application

### 🌐 **Après Déploiement**

L'application sera accessible sur :
- **http://votre-ip-aws/** (via Nginx)
- **http://votre-ip-aws:5001/** (accès direct)

### ⚙️ **Configuration Facebook**

Éditer le fichier de configuration :
```bash
sudo nano /opt/facebook_publisher_saas/.env
```

Ajouter vos tokens Facebook :
```env
FACEBOOK_ACCESS_TOKEN=votre_token_ici
FACEBOOK_APP_ID=votre_app_id_ici
FACEBOOK_APP_SECRET=votre_app_secret_ici
```

Redémarrer l'application :
```bash
sudo systemctl restart facebook-publisher
```

### 📊 **Commandes de Gestion**

```bash
# Statut du service
sudo systemctl status facebook-publisher

# Redémarrer l'application
sudo systemctl restart facebook-publisher

# Voir les logs en temps réel
sudo journalctl -u facebook-publisher -f

# Arrêter l'application
sudo systemctl stop facebook-publisher

# Démarrer l'application
sudo systemctl start facebook-publisher
```

### 🔍 **Vérification du Déploiement**

```bash
# Vérifier que l'application fonctionne
curl http://localhost:5001/

# Vérifier Nginx
curl http://localhost/

# Vérifier les processus
ps aux | grep facebook
```

### 🛠️ **Dépannage**

#### **Si l'application ne démarre pas :**
```bash
# Vérifier les logs
sudo journalctl -u facebook-publisher -n 50

# Vérifier la configuration
sudo nginx -t

# Redémarrer Nginx
sudo systemctl restart nginx
```

#### **Si problème de permissions :**
```bash
sudo chown -R facebook_publisher_saas:facebook_publisher_saas /opt/facebook_publisher_saas
```

### 🔒 **Sécurité**

Le script configure automatiquement :
- ✅ **Utilisateur système dédié** (non-root)
- ✅ **Permissions restrictives** sur les fichiers
- ✅ **Nginx comme proxy** (sécurité supplémentaire)
- ✅ **Isolation des processus** via systemd

### 📈 **Performance**

Configuration optimisée pour production :
- ✅ **Gunicorn** avec 4 workers
- ✅ **Nginx** pour servir les fichiers statiques
- ✅ **Auto-restart** en cas de crash
- ✅ **Timeout** configurés pour les requêtes longues

---

## 🎉 **RÉSULTAT FINAL**

Après exécution du script, vous aurez :
- ✅ **Application v3.1.0** déployée et fonctionnelle
- ✅ **Service automatique** qui redémarre au boot
- ✅ **Nginx configuré** pour l'accès web
- ✅ **Logs centralisés** via systemd
- ✅ **Configuration sécurisée** pour la production

**Votre Facebook Publisher SaaS v3.1.0 sera opérationnel sur votre serveur AWS !** 🚀

