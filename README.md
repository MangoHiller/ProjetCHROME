# ProjetCHROME - Recognition of On-line Handwritten Mathematical Expressions

## Description du Projet
"ProjetCHROME" (Recognition of On-line Handwritten Mathematical Expression) s'inscrit dans le cadre des compétitions CROHME et est une réalisation dans l'UE 'Machine Learning For Computer Vision' du master ATAL. Ce projet traite des expressions mathématiques manuscrites, les convertissant de leur format manuscrit (InkML) en une représentation numérique. Il suit un pipeline de traitement, impliquant la segmentation, la sélection et la reconnaissance de symboles.

## Structure du Répertoire
- **models** : Contient les poids du modèle de réseau de neurones entraîné pour la reconnaissance des symboles.
- **scripts** : Contient les scripts principaux du pipeline de traitement.
  - **classification** : Sous-répertoire contenant `SymbolClassifier.py` et `train_SymbolClassifier.ipynb`.
- **input** : Dossier pour les expressions mathématiques au format InkML.
- **output** : Dossier pour les fichiers générés à chaque étape du pipeline.
  - **hyp_output** : Généré par `segmenter.py`.
  - **seg_output** : Généré par `segmentSelect.py`.
  - **symb_output** : Généré par `symbolReco.py`.

## Pipeline de Traitement
- `segmenter.py` : Génère à partir d'un fichier InkML des hypothèses de symboles dans un fichier LG.
- `segmentSelect.py` : Garde ou rejette chaque hypothèse de segment et génère un nouveau fichier LG.
- `symbolReco.py` : Reconnaît chaque hypothèse et sauvegarde toutes les reconnaissances acceptables dans un fichier LG.
- `selectBestSeg.py` : À partir d'un fichier LG avec plusieurs hypothèses, ne conserve qu'une solution globale cohérente (algorithme glouton sub-optimal).

## Technologies Utilisées
- Python
- PyTorch pour les modèles de réseaux de neurones
- OpenCV, scikit-image pour le traitement d'image

## Contributors

|                                                    |                  |
| -------------------------------------------------- | ---------------- |
| [@MangoHiller](https://github.com/MangoHiller)     | Hugo LEGUILLIER  |
| [@miranovic](https://github.com/miranovic)         | Imran NAAR       |
