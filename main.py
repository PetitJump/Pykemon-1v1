from __future__ import annotations
from random import sample, randint
import os, json

class Pykemon:
    """
    Classe représentant un Pykemon.
    Contient ses attributs (nom, PV, type, attaques, faiblesse)
    et ses méthodes d'action (attaquer, soigner).
    """
    def __init__(self, nom: str, pv: int, type_: str, attaques: list, faiblesse: str):
        self.nom = nom
        self.pv = pv
        self.type = type_
        self.attaques = attaques  #Liste [("nom attaque", valeur), ("nom soin", valeur)]
        self.faiblesse = faiblesse

    def attaquer(self, adversaire: Pykemon) -> str:
        """
        Effectue l'attaque principale sur l'adversaire.
        Gère les dégâts de base, la faiblesse (+20) et le critique (+10).
        """
        degats = self.attaques[0][1]
        critique = False
        if self.type == adversaire.faiblesse:
            degats += 20 

        if randint(1, 100) <= 10:  #10% de chance de faire une attaque critique
            degats += 10
            critique = True

        adversaire.pv -= degats
        if adversaire.pv < 0: #Evite les bug de pokemon avec pv dégatif
            adversaire.pv = 0

        msg = f"{self.nom} attaque {adversaire.nom} ! Base {self.attaques[0][1]} dégâts"
        if self.type == adversaire.faiblesse:
            msg += " (+20 faiblesse)"
        if critique == True:
            msg += " (+10 critique)"
        msg += f"\n{adversaire.nom} perd {degats} PV"
        return msg

    def soigner(self) -> str:
        """Soigne le Pokemon"""
        self.pv += self.attaques[1][1]
        return f"{self.nom} se soigne de {self.attaques[1][1]} PV !"

    def est_ko(self) -> bool:
        """Retourne True si le Pykemon n'a plus de PV"""
        if self.pv <= 0:
            return True
        return False

    def stats(self) -> str:
        """Stats du Pokemon"""
        return f"{self.nom} | PV : {self.pv} | Type : {self.type} | Faiblesse : {self.faiblesse}"


class Joueur:
    def __init__(self, nom: str, pykemons: list[Pykemon], indice_depart: int):
        self.nom = nom
        self.pykemons = pykemons
        self.poke_en_cour = self.pykemons[indice_depart]

    def choix_action(self) -> int:
        """Affiche les actions possibles et retuorne le choix du joueur"""
        print("Veuillez choisir une action :")
        print(f"1 : {self.poke_en_cour.attaques[0][0]} (attaque, {self.poke_en_cour.attaques[0][1]} dégâts de base)")
        print(f"2 : {self.poke_en_cour.attaques[1][0]} (soin, {self.poke_en_cour.attaques[1][1]} PV)")
        print("3 : Changer de Pokémon")
        choix = 0
        while choix < 1 or choix > 3:
            choix = int(input("Votre choix : "))
        return choix

    def action(self, choix: int, adv: Joueur):
        """Effectue l'action choisie"""
        if choix == 1:  #Attaque
            print(self.poke_en_cour.attaquer(adv.poke_en_cour))

        elif choix == 2:  #Soin
            print(self.poke_en_cour.soigner())

        else:  #Changement de pokemon
            clear()
            print("Veuillez choisir un nouveau Pokémon :")
            self.choix_pokemon()

    def choix_pokemon(self):
        """Permet de choisir un nouveau Pokémon encore en vie"""
        vivants = []
        for p in self.pykemons: 
            if not p.est_ko(): #On garde seulement ceux qui sont encore en vie
                vivants.append(p)
        #Affichage des pokémons vivants
        i = 1
        for p in vivants:
            print(f"{i} : {p.stats()}")
            i += 1

        #Choix du joueur
        choix = 0
        while choix < 1 or choix > len(vivants):
            choix = int(input("Votre choix : "))
        self.poke_en_cour = vivants[choix - 1]
        clear()

    def stat(self, adv: Joueur):
        """Affiche les stats du joueur et de l'adversaire"""
        print("======================")
        print(f"{self.nom} - Pokémon actif : {self.poke_en_cour.stats()}")
        print("======================")
        print(f"Adversaire {adv.nom} - Pokémon actif : {adv.poke_en_cour.stats()}")
        print("======================")


class Jeu:
    def __init__(self):
        self.J1 = None
        self.J2 = None

    def generation_pokedex(self) -> list[Pykemon]:
        """Génère une équipe de 3 Pykemon"""
        pokedex = sample(total_pokemon, k=3)
        actuel = []
        for poke in pokedex:
            actuel.append(Pykemon(poke[0], poke[1], poke[2], poke[3], poke[4])) #Nom, pv, type, capacité, faiblesse
        return actuel

    def initialiser(self):
        """Initialise la partie"""
        print("Bienvenue dans PokeDave. Les faiblesses donnent +20 dégâts et il y a une chance de coup critique (+10).")
        pseudo1 = input("Choix pseudo 1 : ")
        clear()
        print("Bienvenue dans PokeDave. Les faiblesses donnent +20 dégâts et il y a une chance de coup critique (+10).")
        pseudo2 = input("Choix pseudo 2 : ")
        equipe1 = self.generation_pokedex()
        equipe2 = self.generation_pokedex()
        clear()

        #Choix joueur 1
        print(f"{pseudo1}, choisissez votre Pokémon de départ :")
        i = 1
        for p in equipe1:
            print(f"{i} : {p.stats()}")
            i += 1
        choix1 = int(input("Votre choix : ")) - 1
        clear()

        #Choix joueur 2
        print(f"{pseudo2}, choisissez votre Pokémon de départ :")
        i = 1
        for p in equipe2:
            print(f"{i} : {p.stats()}")
            i += 1
        choix2 = int(input("Votre choix : ")) - 1
        clear()

        self.J1 = Joueur(pseudo1, equipe1, choix1)
        self.J2 = Joueur(pseudo2, equipe2, choix2)
    
    def joueurs_ont_pykemon(self):
        """Retourne True si les deux joueurs ont encore au moins un Pykemon vivant"""
        vivant_J1 = 0
        for p in self.J1.pykemons:
            if not p.est_ko():
                vivant_J1 += 1

        vivant_J2 = 0
        for p in self.J2.pykemons:
            if not p.est_ko():
                vivant_J2 += 1

        if vivant_J1 > 0 and vivant_J2 > 0:
            return True
        else:
            return False


    def run(self) -> str:
        """Tour par tour jusqu'à la victoire d'un joueur"""
        while self.joueurs_ont_pykemon():

            ###### Tour J1 ######
            clear()
            self.J1.stat(self.J2)
            choix = self.J1.choix_action()
            self.J1.action(choix, self.J2)
            clear()
            if self.J2.poke_en_cour.est_ko():
                print(f"{self.J2.poke_en_cour.nom} est K.O !")
                vivant = False
                for p in self.J2.pykemons:
                    if p.est_ko() == False:  
                        vivant = True
                if vivant == True:
                    print(f"{self.J2.nom}, choisisez un autre Pokémon :")
                    self.J2.choix_pokemon()
                else:
                    break

            ###### Tour J2 ######
            self.J2.stat(self.J1)
            choix = self.J2.choix_action()
            self.J2.action(choix, self.J1)
            clear()
            if self.J1.poke_en_cour.est_ko():
                print(f"{self.J1.poke_en_cour.nom} est K.O !")
                vivant = False
                for p in self.J1.pykemons:
                    if p.est_ko() == False:  
                        vivant = True
                if vivant == True:
                    print(f"{self.J1.nom}, choisisez un autre Pokémon :")
                    self.J2.choix_pokemon()
                else:
                    break

        vivants_J1 = 0
        for p in self.J1.pykemons:
            if p.est_ko() == False:
                vivants_J1 += 1

        vivants_J2 = 0
        for p in self.J2.pykemons:
            if p.est_ko() == False:
                vivants_J2 += 1

        if vivants_J1 == 0:
            return f"Bravo {self.J2.nom}, vous avez gagné !"
        elif vivants_J2 == 0:
            return f"Bravo {self.J1.nom}, vous avez gagné !"
        else:
            return f"Bug :( \nInfo : pokeJ1 : {self.J1.pykemons} ; pokeJ2 : {self.J2.pykemons}"

def clear():
    """Efface le terminal (Windows ou Linux/Mac)"""
    os.system('cls' if os.name == 'nt' else 'clear')


#Prend tout les pokemon existant depuis data.json
with open('data.json', 'r', encoding='utf-8') as f:
    total_pokemon = json.load(f)

clear()

Partie_en_cour = Jeu()
Partie_en_cour.initialiser()
print(Partie_en_cour.run())
