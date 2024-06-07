import requetes

def affichage(titre, liste_programmes):
    ligne_tiret = "─" * len(titre)
    ligne_vide = " " * len(titre)
    print()
    print()
    print("┌" + ligne_tiret * 3 + "┐")
    print("│" + ligne_vide * 3 + "│")
    print("│" + ligne_vide + titre + ligne_vide + "│")
    print("│" + ligne_vide * 3 + "│")
    print("└" + ligne_tiret * 3 + "┘")
    print()
    print("Voici la liste des programmes que vous pouvez exécuter :\n")
    for i in range(len(liste_programmes)):
        print(str(i + 1).ljust(2), " --> ".ljust(6), liste_programmes[i])
    print()

def demander_nombre(message, borne_max):
    try:
        nombre = input(message)
        if nombre.isdecimal():
            nombre = int(nombre)
            if 1 <= nombre <= borne_max:
                return int(nombre)
            else:
                print("Entrez un nombre entre 1 et " + str(borne_max) + ".")
        else:
            print("Entrez un nombre entre 1 et " + str(borne_max) + ".")
    except:
        return None
    
def menu(titre, liste_programmes):
    affichage(titre, liste_programmes)
    choix_utilisateur = demander_nombre("Entrez votre choix [1-" + str(len(liste_programmes)) + "] : ", len(liste_programmes))
    if choix_utilisateur is not None:
        return choix_utilisateur
    else:
        return None

def lancement(data):
    liste_programmes = [
        "Donne les collaborateurs qui sont communs à deux acteurs",
        "Donne les collaborateurs proches d'un acteur",
        "Donne la centralité d'un acteur",
        "Donne l'acteur central d'Hollywood",
        "Donne la distance d'éloignement maximale entre deux acteurs",
        "Quitter"
    ]
    
    hollywood = requetes.json_vers_nx(data)
    fin = False
    while not fin:
        rep = menu("Hollywood", liste_programmes)
        reponse = str(rep)  # Conversion en chaîne de caractères pour la comparaison
        while reponse not in ["1", "2", "3", "4", "5", "6"]:
            reponse = input("Choix non reconnu. Choisissez une option : ")
        
        if reponse == "1":
            acteur1 = input("Choisissez votre premier acteur : ")
            acteur2 = input("Choisissez votre second acteur : ")
            collaboration = requetes.collaborateurs_communs(hollywood, acteur1, acteur2)
            if collaboration == set():
                print("Ces deux acteurs n'ont pas de collaborateurs communs")
            else:
                print(f"Les collaborateurs communs de ces deux acteurs sont {collaboration}")
        
        elif reponse == "2":
            acteur = input("Choisissez votre acteur : ")
            distance = input("Choisissez la distance maximale entre les collaborateurs : ")
            while not requetes.est_entier(distance):
                distance = input("Choix non reconnu. Choisissez la distance maximale entre les collaborateurs : ")
            nb_distance = int(distance)
            proche = requetes.collaborateurs_proches(hollywood, acteur, nb_distance)
            if proche is None:
                print("Cet acteur est inconnu")
            else:
                print(f"Les collaborateurs proches de cet acteur sont {proche}")
        
        elif reponse == "3":
            acteur = input("Choisissez votre acteur : ")
            centralité = requetes.centralite(hollywood, acteur)
            print(f"La personne la plus éloignée de votre acteur est éloignée de {centralité} personnes")

        elif reponse == "4":
            centre_hollywood = requetes.centre_hollywood(hollywood)
            print(f"L'acteur central d'Hollywood est {centre_hollywood}")
        
        elif reponse == "5":
            max_distance = requetes.eloignement_max(hollywood)
            print(f"Les deux acteurs les plus éloignés sont séparés de {max_distance} personnes")

        elif reponse == "6":
            fin = True
    
    return "Merci de votre consultation"

lancement("data_10000.txt")
