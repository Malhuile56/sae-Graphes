#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import random
import matplotlib.pyplot as plt
import time
import networkx as nx



# 6.1
def enlever_elem(nom): # 0(N)
    """Fonction supprimant les éléments indésirables dans les noms des acteurs.
    
    Paramètres:
        nom: nom de l'acteur
    """
    elem = "[']"
    for x in range(len(elem)):
        nom = nom.replace(elem[x], "")
    parts = nom.split("|")
    nom = parts[-1]
    return nom

def json_vers_nx(fichier): # O(N^4)
    """Fonction renvoyant le graphe à partir d'un fichier texte.

    Paramètres:
        fichier : un fichier .txt
    """
    # Création du graphe
    G = nx.Graph()
    # Lecture du fichier texte
    with open(fichier, 'r', encoding="utf-8") as fic:
        # Parcourir le fichier ligne par ligne
        for ligne in fic:  
            # Initialisation automatique du dictionnaire à partir des données du fichier pour chaque film
            dico = json.loads(ligne)
            
            # Parcours du dictionnaire des acteurs 
            for i in range(len(dico["cast"])):
                # Remettre les noms des acteurs au propre
                dico["cast"][i] = enlever_elem(dico["cast"][i])
                # S'il n'est pas déjà dans le graphe, l'ajouter
                if dico["cast"][i] not in G:
                    G.add_node(dico["cast"][i], label='A')

            # Pour chaque acteur, former un lien entre eux dans le graphe pour signifier qu'ils ont travaillé ensemble 
            for acteur1 in dico["cast"]:
                for acteur2 in dico["cast"]:
                    if (acteur1, acteur2) not in G and acteur1 != acteur2:
                        G.add_edge(acteur1, acteur2)
    # Dessiner et afficher le graphe
    nx.draw(G, with_labels=True)
    plt.show()
    return G 

c = json_vers_nx("data_100.txt")
d = json_vers_nx("data_1000.txt")
e = json_vers_nx("data_10000.txt")

# 6.2
def collaborateurs_communs(acteur1, acteur2, G): # 0(N)
    """Fonction renvoyant l'ensemble des acteurs ayant collaboré avec ces deux acteurs placés en paramètre.

    Paramètres:
        acteur1 : un acteur
        acteur2 : un acteur
        G : un graphe NetworkX
    """
    # Initialisation de l'ensemble des collaborateurs
    collab = set()

    # Pour chaque acteur du graphe, s'il n'est pas égal aux deux acteurs et qu'il a déjà travaillé avec ces deux acteurs, on l'ajoute à l'ensemble
    for acteur in G.nodes:
        if acteur != acteur1 and acteur != acteur2:
            if (acteur1, acteur) in G.edges and (acteur2, acteur) in G.edges:
                collab.add(acteur)
    return collab
print(len(collaborateurs_communs("Al Pacino","Robert De Niro", "data_100.txt")))

# 6.3
def collaborateurs_proches(G, u, k): # O(N)
    """Fonction renvoyant l'ensemble des acteurs à distance au plus k de l'acteur u dans le graphe G. La fonction renvoie None si u est absent du graphe.
    
    Paramètres:
        G: le graphe
        u: le sommet de départ
        k: la distance depuis u
    """
    if u not in G.nodes:
        print(u, "est un illustre inconnu")
        return None
    proches = set()
    proches.add(u)
    for i in range(k):
        proches_directs = set()
        for c in proches:
            for voisin in G.adj[c]:
                if voisin not in proches:
                    proches_directs.add(voisin)
        proches = proches.union(proches_directs)
    return proches

print(collaborateurs_proches(c, "Al Pacino", 2))

def est_proche(G, acteur1, acteur2, k): # 0(N)
    """Fonction qui permet de savoir si acteur2 se situe à k distance de acteur1.

    Paramètres:
        G (graph): Un graphe NetworkX
        acteur1 (string): un acteur
        acteur2 (string): un acteur
        k (int): la distance

    Returns:
        boolean: True si acteur2 se situe à k distance de acteur1, False sinon et None s'il n'y a pas d'acteurs à distance k de acteur1
    """    
    acteurs = collaborateurs_proches(G, acteur1, k)
    if acteurs is not None:
        return acteur2 in acteurs
    return None

print(est_proche(c, "Al Pacino", "John Randolph", 1))

def distance_naive(G, acteur1, acteur2): # O(N^3)
    """Permet de calculer la distance entre deux acteurs.

    Paramètres:
        G (graph): Un graphe NetworkX
        acteur1 (String): un acteur
        acteur2 (String): un acteur

    Returns:
        int: la distance entre deux acteurs et None si l'acteur2 n'est pas dans le graphe
    """    
    dist = 0
    while not est_proche(G, acteur1, acteur2, dist) and dist < len(G.nodes):
        dist += 1
    return dist
print(distance_naive(c, "Holly Hunter", "John Randolph"))

def distance(G, acteur1, acteur2): # O(N^2)
    """Permet de calculer la distance entre deux acteurs.

    Paramètres:
        G (graph): Un graphe NetworkX
        acteur1 (String): un acteur
        acteur2 (String): un acteur

    Returns:
        int: la distance entre deux acteurs et None si l'acteur2 n'est pas dans le graphe
    """
    dist = 0
    if acteur1 == acteur2:
        return 0
    if acteur1 not in G.nodes or acteur2 not in G.nodes:
        return None
    while not est_proche(G, acteur1, acteur2, dist) and dist < len(G.nodes):
        dist += 1
    return dist
print(distance(c, 'Holly Hunter', 'John Randolph'))

# 6.4
def centralite(G, acteur): # O(N^2)
    """Retourne la distance entre un acteur et l'acteur le plus éloigné de lui.

    Paramètres:
        G : un graphe NetworkX
        acteur : un acteur 

    Returns:
        int : la distance maximale entre acteur et un autre acteur
    """    
    if acteur not in G:
        return None
    liste_acteurs = [(acteur, 0)]  # Début de la liste d'acteurs
    visite = {acteur}  # Acteurs déjà visités
    dist_max = 0

    while liste_acteurs:  # Tant que tous les acteurs dans la liste ne sont pas passés
        acteur_actuel, distance = liste_acteurs.pop(0)  # Supprime celui qui va être traité pour les faire l'un après l'autre
        for voisin in G.adj[acteur_actuel]:  # On ajoute les voisins dans la liste à visiter
            if voisin not in visite:
                visite.add(voisin)
                liste_acteurs.append((voisin, distance + 1))
                dist_max = distance + 1
    return dist_max
print(centralite(c,"Al Pacino"))

def centre_hollywood(G): # O(N^2)
    """Fonction renvoyant l'acteur avec la centralité la plus élevée.

    Paramètres:
        G : un graphe NetworkX
    
    Returns:
        acteur : l'acteur avec le plus de centralité
        valmax : la distance la plus élevée
    """
    valmax = 0
    actmax = ""

    # Boucle for cherchant la valeur max de centralité et renvoyant l'acteur avec la plus haute valeur de centralité
    for acteur in G.nodes:
        centr = centralite(G, acteur)
        if centr > valmax:
            valmax = centr
            actmax = acteur
    return actmax, valmax

print(centre_hollywood(c))

# 6.5
def eloignement_max(G): # O(N)
    """Fonction renvoyant le couple d'acteurs le plus éloigné.

    Paramètres:
        G : un graphe NetworkX
    """
    dist_max = 0
    act_max = ("", "")
    deja_vu = set()

    for acteur in G.nodes:
        if acteur not in deja_vu:
            acteur_plus_loin, distance = le_plus_eloigne(acteur, G)  # Appel de fonction pour trouver l'acteur le plus éloigné de l'acteur 
            if distance > dist_max:  # Si l'acteur est plus éloigné que le précédent, on remplace les valeurs
                dist_max = distance
                act_max = (acteur, acteur_plus_loin)
            deja_vu.add(acteur)
            deja_vu.add(acteur_plus_loin)
    
    return act_max

def le_plus_eloigne(acteur, G): # O(N^2)
    """Fait une recherche en largeur pour explorer tous les voisins.

    Paramètres:
        acteur : un acteur dont on veut trouver l'acteur le plus éloigné
        G : un graphe NetworkX

    Returns:
        tuple : l'acteur le plus éloigné et sa distance avec l'acteur passé en paramètre
    """        
    deja_vu = {acteur}  # Voisins déjà traités
    liste_acteurs = [(acteur, 0)]  # Initialisation de la liste
    plus_loin = acteur 
    dist_max = 0
        
    while liste_acteurs:
        act, distance = liste_acteurs.pop(0)  # Supprime celui qui va être traité pour les faire l'un après l'autre
        if distance > dist_max:
            plus_loin = act
            dist_max = distance
            
        for voisin in G.adj[act]:   
            if voisin not in deja_vu:
                deja_vu.add(voisin)  # Ajout des voisins qu'on vient de découvrir
                liste_acteurs.append((voisin, distance + 1))  # Mise dans la file pour les parcourir plus tard
        
    return plus_loin, dist_max  # Retourne l'acteur le plus loin et sa distance avec l'acteur passé en paramètre
print(le_plus_eloigne(c))