# Dashboard 3D – Bilan énergétique d’un bâtiment

Application Streamlit présentant le bilan et l’avancement des politiques énergétiques d’un parc immobilier municipal à horizon 2050. L’interface combine un menu latéral, des KPIs, des graphiques et une visualisation 3D simplifiée du bâtiment (Plotly) pour raconter l’évolution de la consommation, du mix énergétique et de la production photovoltaïque.

Démo en ligne: https://3d-dashboard-energy-balance-building.streamlit.app/

## Fonctionnalités
- **Menu latéral**: navigation entre les pages Vue d’ensemble, Chauffage, Électricité, Photovoltaïque
- **KPIs clés**: variations annuelles, parc d’installations, objectifs atteints/restants
- **3D Plotly**: volume de bâtiment et position symbolique des panneaux photovoltaïques
- **Graphiques**: barres et courbes pour tendances de consommation et économies
- **Indicateurs d’objectifs**: jauges pour le suivi des cibles 2025 (x2) et 2030 (x5) sur le photovoltaïque

## Pages
- **Vue d’ensemble**: synthèse des KPIs (chauffage −8% en 2023, électricité −4.8% en 2023, ~1 GWh/an PV, 42 chaufferies au mazout restantes)
- **Chauffage**: baisse de la demande, régulation dynamique (37 immeubles équipés en 2023, ~146’000 kWh économisés mi-oct → fin déc), assainissement des vitrages (128 bâtiments, ~20% d’économie), sortie du mazout et raccordements au CAD
- **Électricité**: tendance −4.8% en 2023 malgré l’augmentation du parc, effets des rénovations et optimisations
- **Photovoltaïque**: 46 centrales en service, ~1 GWh/an produit, autoconsommation sur 14 sites, surplus injecté (SIG), trajectoires x2 d’ici 2025 et x5 d’ici 2030

## Données et hypothèses
Les valeurs affichées illustrent les ordres de grandeur et objectifs mentionnés (année 2023 et cibles 2025/2030). L’application est prête à être connectée à des données réelles (CSV/Excel/base de données) pour alimenter automatiquement les KPIs et courbes.

Intégration typique (exemple CSV):
1. Ajouter un fichier `data/kpis_energie.csv` avec colonnes: `annee, conso_chauffage_delta, conso_elec_delta, pv_centrales, pv_prod_gwh, mazout_chaufferies, part_gaz_pct`
2. Charger le fichier dans `streamlit_app.py` (via `pandas.read_csv`) et mapper les colonnes aux KPIs

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

## Pile technologique
- **Python**: Streamlit, pandas, numpy
- **Visualisation**: Plotly (graphes et Mesh3d)
- **Déploiement**: Streamlit Community Cloud

## Structure
- `streamlit_app.py`: application principale
- `requirements.txt`: dépendances Python

## Feuille de route (suggestions)
- Import automatique de données (CSV/Excel/API) et historisation multi-années
- Cartographie et multiples bâtiments avec sélecteur
- Modèle 3D plus riche (surfaces, teintes par intensité énergétique)
- Exports PDF des tableaux de bord

## Crédits
Données et contexte fournis par la politique énergétique municipale (KPIs synthétisés dans l’app).
