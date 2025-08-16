# Dashboard 3D – Bilan énergétique d’un bâtiment

Application Streamlit avec menu latéral (Vue d’ensemble, Chauffage, Électricité, Photovoltaïque), KPIs et visualisation 3D (Plotly).

## Lancer en local

```bash
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt
.venv\Scripts\python -m streamlit run streamlit_app.py
```

Ouvrir `http://localhost:8501` (ou le port affiché) dans votre navigateur.

## Déploiement – Streamlit Community Cloud
1. Créez un dépôt GitHub public (ex: `dashboard-3d-bilan-energetique-batiment`).
2. Poussez ce code dans le dépôt.
3. Sur Streamlit Cloud, choisissez "New app", connectez votre compte GitHub, sélectionnez le dépôt, branche principale, et fichier principal `streamlit_app.py`.
4. Laissez l’installation utiliser `requirements.txt`.

## Structure
- `streamlit_app.py`: application principale
- `requirements.txt`: dépendances Python

## Crédits
Données et contexte fournis par la politique énergétique municipale (KPIs synthétisés dans l’app).
