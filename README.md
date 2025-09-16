## Présentation du programme ##
Le jeu gère :
- Les attaques avec dégâts de base
- Les faiblesses (+20 dégâts)
- Les coups critiques (+10 dégâts, 10% de chance)
- Les soins
- Le changement de Pokémon
- La détection de victoire et de défaite

Tout le projet est codé en Programmation Orientée Objet, avec 3 classes principales :
- Pykemon : représente un Pokémon
- Joueur : représente un joueur et son équipe
- Jeu : gère le déroulement du combat


## Règles ##
Chaque joueur choisit un pseudo.
Une équipe de 3 Pykemons aléatoires est générée depuis data.json.
Les deux joueurs choisissent leur Pokémon de départ.
À chaque tour, un joueur choisit une action :
- Attaquer : inflige des dégâts (faiblesses et critiques possibles).
- Se soigner : regagne des PV.
- Changer de Pokémon : choisit un autre encore en vie.
Quand un Pokémon tombe à 0 PV, il est K.O.
Le jeu se termine quand un joueur n’a plus de Pokémon en vie.

## Modifications possibles ##
- Modification de data.json masi garder la structure [Nom du pokemon, pv, type, ("nom attaque", valeur), ("nom soin", valeur), faiblesse]