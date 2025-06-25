# Contributing to Facebook Publisher Bois Malin

Nous accueillons les contributions de la communauté ! Ce guide vous explique comment contribuer au projet.

## 🚀 Comment Contribuer

### 1. Fork et Clone

```bash
# Fork le repository sur GitHub
# Puis clonez votre fork
git clone https://github.com/VOTRE-USERNAME/FB-Publisher-Bois-Malin.git
cd FB-Publisher-Bois-Malin
```

### 2. Configuration de l'Environnement

```bash
# Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Installer les dépendances
pip install -r requirements.txt

# Installer les dépendances de développement
pip install pytest flake8 black
```

### 3. Créer une Branche

```bash
# Créer une branche pour votre fonctionnalité
git checkout -b feature/ma-nouvelle-fonctionnalite
```

### 4. Développement

- Respectez les standards **PEP 8**
- Ajoutez des **tests unitaires** pour les nouvelles fonctionnalités
- Mettez à jour la **documentation** si nécessaire
- Utilisez des **messages de commit** descriptifs

### 5. Tests

```bash
# Exécuter tous les tests
python -m pytest tests/ -v

# Vérifier le style de code
flake8 .

# Formater le code
black .
```

### 6. Commit et Push

```bash
git add .
git commit -m "feat: ajouter nouvelle fonctionnalité X"
git push origin feature/ma-nouvelle-fonctionnalite
```

### 7. Pull Request

1. Allez sur GitHub et créez une Pull Request
2. Décrivez clairement vos changements
3. Référencez les issues liées si applicable

## 📋 Guidelines

### Style de Code

- **Python** : Respectez PEP 8
- **Longueur de ligne** : 88 caractères (Black)
- **Imports** : Organisés selon PEP 8
- **Docstrings** : Format Google style

### Messages de Commit

Utilisez le format [Conventional Commits](https://www.conventionalcommits.org/) :

```
type(scope): description

feat: ajouter nouvelle fonctionnalité
fix: corriger bug dans l'API
docs: mettre à jour README
test: ajouter tests pour module X
refactor: restructurer le code Y
```

### Tests

- **Couverture** : Minimum 80%
- **Nommage** : `test_nom_de_la_fonction`
- **Structure** : Arrange, Act, Assert
- **Mocks** : Utilisez `responses` pour les API

### Documentation

- **README** : Mettre à jour si nécessaire
- **Docstrings** : Pour toutes les fonctions publiques
- **Commentaires** : Expliquer le "pourquoi", pas le "quoi"

## 🐛 Signaler des Bugs

1. Vérifiez que le bug n'est pas déjà signalé
2. Créez une issue avec le template bug
3. Incluez :
   - Description détaillée
   - Étapes pour reproduire
   - Environnement (OS, Python version)
   - Logs d'erreur

## 💡 Proposer des Fonctionnalités

1. Créez une issue avec le template feature
2. Décrivez :
   - Le problème à résoudre
   - La solution proposée
   - Les alternatives considérées

## 🔍 Code Review

Tous les PRs passent par une review :

- **Fonctionnalité** : Fonctionne comme attendu
- **Tests** : Couvrent les nouveaux cas
- **Code** : Lisible et maintenable
- **Documentation** : À jour

## 📞 Questions

- **Issues GitHub** : Pour les bugs et fonctionnalités
- **Discussions** : Pour les questions générales
- **Email** : contact@boismalin.com

Merci de contribuer au projet ! 🙏

