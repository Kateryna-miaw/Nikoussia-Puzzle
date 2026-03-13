# Nikoussia Puzzle

Un puzzle de 256 pièces construit avec Streamlit. L'image est découpée en grille 16×16, les pièces sont mélangées et tournées aléatoirement, et il faut tout remettre en place par glisser-déposer. L'image du puzzle, c'est Nikoussia, ma vraie peluche.

C'est un jeu complet avec système de combo, indices, aimantation magnétique, bande-son, et un profiler de debug intégré.

---

## De quoi il s'agit

Le joueur commence avec 256 pièces en vrac dans un tiroir en bas de l'écran. Chaque pièce est orientée au hasard (0°, 90°, 180° ou 270°). Il faut les glisser sur le plateau, les tourner dans le bon sens, et les déposer au bon endroit. Quand une pièce bien orientée s'approche de sa position correcte, un effet d'aimantation l'attire doucement vers sa place.

Les pièces ne sont pas de simples carrés. Elles ont des bords dentelés générés procéduralement (tabs et blanks), comme un vrai puzzle. Chaque bord est dessiné avec des courbes de Bézier, et les pièces voisines s'emboîtent visuellement.

Le système de combo récompense les placements consécutifs : chaque pièce bien placée donne un indice, et à partir de trois d'affilée, c'est deux indices. Rater un placement casse le combo. Les indices permettent de placer automatiquement une pièce aléatoire.

L'aperçu de l'image complète est limité à 3 secondes par consultation, pour garder un minimum de défi mémoire.

---

## Fonctionnement technique

Tout tourne dans un seul fichier HTML injecté dans Streamlit via `st.components.v1.html`. Le rendu est entièrement fait sur un `<canvas>` 2D, redessiné à chaque frame via `requestAnimationFrame`.

**Génération des pièces.** Les bords sont créés au lancement : pour chaque frontière entre deux cellules de la grille, un tab (convexe ou concave) est assigné aléatoirement. Le dessin de chaque pièce utilise ces informations pour tracer le contour avec des courbes de Bézier cubiques. Le résultat donne des pièces qui s'emboîtent visuellement, avec un rendu qui imite le carton découpé (ombre portée, biseautage, reflet spéculaire).

**Aimantation.** Quand une pièce correctement orientée passe dans un rayon de 1.8× la taille d'une cellule autour de sa cible, elle est progressivement attirée avec une force proportionnelle à la distance. En dessous de 0.4× la taille de cellule, elle se verrouille. L'effet est accompagné d'un halo animé avec des particules qui orbitent autour de la zone cible.

**Audio.** Les assets audio (musique de fond, clics, survols, son d'indice) sont encodés en base64 et injectés directement dans le HTML. Chaque effet sonore est cloné à la volée pour permettre des déclenchements simultanés sans couper le précédent.

---

## Le profiler

Le jeu embarque un panneau de debug complet, accessible avec la touche F2 ou le bouton PROFILER dans la barre du haut. Il est découpé en quatre colonnes.

**Render.** La première colonne affiche le FPS en temps réel, le budget frame en millisecondes (temps écoulé entre deux frames), le nombre de draw calls par frame (pièces placées + pièces flottantes), et la résolution du canvas en pixels. En dessous, une sparkline trace l'historique FPS sur les 60 dernières mesures. Les valeurs sont colorées selon leur état : vert au-dessus de 55 FPS, jaune au-dessus de 30, rouge en dessous. Le budget frame suit la même logique (vert sous 20ms, jaune sous 33ms, rouge au-delà).

**Algorithme snap.** La deuxième colonne expose les métriques internes du système de placement. À chaque drop, elle affiche le nombre de tests effectués (complexité O(n) sur les pièces non placées), si l'aimant est actif et à quelle intensité (en pourcentage), la distance en pixels entre la pièce lâchée et sa cible, le seuil de snap en pixels (40% de la largeur d'une cellule), et la streak de ratés consécutifs. Un log horodaté en bas de la colonne enregistre chaque événement : placement réussi avec distance et combo, raté avec distance et seuil, erreur de rotation, utilisation d'indice.

**Heatmap.** La troisième colonne affiche une grille 16×16 où chaque cellule est colorée selon son ordre de placement. Les cellules non encore remplies sont sombres, les premières placées tirent vers le violet, et les dernières vers le rose/doré. Ça permet de visualiser d'un coup d'œil la stratégie du joueur : est-ce qu'il commence par les bords, par un coin, par le centre, ou au hasard. La heatmap se met à jour en temps réel à chaque nouveau placement.

**Session.** La quatrième colonne résume la partie en cours : durée totale, pièces par minute, précision (ratio placements réussis sur tentatives totales), nombre d'indices utilisés, et nombre total de drops. Le bouton d'export en bas génère un fichier JSON complet de la session.

---

## Les pièces en détail

Chaque pièce est dessinée en plusieurs passes sur le canvas :

1. Une ombre floue décalée, plus prononcée quand la pièce est en cours de déplacement.
2. Le clip de l'image source, découpé selon le contour dentelé de la pièce.
3. Un dégradé de biseautage (clair en haut à gauche, sombre en bas à droite) pour simuler l'épaisseur du carton.
4. Un reflet spéculaire radial en haut à gauche.
5. Un contour fin, rose vif si la pièce est sélectionnée, translucide sinon.

La rotation est gérée par transformation du contexte canvas (`translate` + `rotate`) autour du centre de la pièce, ce qui permet de garder les bords dentelés cohérents quelle que soit l'orientation.

---

## Contrôles

Clic gauche pour sélectionner et glisser une pièce. Clic droit ou touche R pour tourner. Le bouton Aperçu montre l'image complète pendant 3 secondes. Le bouton Indice place une pièce au hasard. Le bouton Finir pour moi complète le puzzle automatiquement, pièce par pièce.

---

## Score

Le score final est calculé comme suit :

```
score = pièces_placées × meilleur_combo - (temps_en_secondes / 10)
```

Un bon score demande à la fois de la vitesse et de la régularité (maintenir un combo élevé sans rater de placement).

---

## Export de session

Le profiler permet d'exporter un fichier JSON contenant toute la session. Le fichier est structuré en quatre blocs :

`meta` contient le nom du jeu, la version, et la date d'export. `config` décrit les paramètres de la grille : taille, nombre total de pièces, seuil de snap en pixels, et rayon d'aimantation. `session` regroupe les métriques de la partie : durée en secondes, pièces placées, drops totaux, ratés, indices utilisés, précision en pourcentage, meilleur combo, score final, pièces par minute, FPS moyen et FPS minimum sur la durée de la partie. `heatmap` contient une matrice 16×16 avec l'ordre de placement de chaque cellule (0 si pas encore placée, 1 pour la première, 2 pour la deuxième, etc.).

Ce fichier peut servir à analyser les stratégies de résolution, comparer des sessions entre elles, ou alimenter des visualisations externes.

---

## Licence

Tous droits réservés.
