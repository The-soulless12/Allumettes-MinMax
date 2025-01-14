import random

n = 25

def affichage_allumettes(nb_total, nb_prises):
    limite = 25
    # Les allumettes prises (▮)
    # Les allumettes restantes (▯)
    prises = '▮ ' * nb_prises
    restantes = '▯ ' * (nb_total - nb_prises)
    allumettes = prises + restantes
    
    print("Allumettes :")
    for i in range(0, len(allumettes), limite):
        print(allumettes[i:i + limite])

    print(f"\n🚨 Prises : {nb_prises} | Restantes : {nb_total - nb_prises}\n")

def fonction_cout(nb_total, joueur):
    if nb_total == 0:
        if joueur == 1:
            return 5 # Le joueur 1 a gagné
        elif joueur == 2:
            return -5 # Le joueur 2 a gagné
    return 0 

def minmax(restant, profondeur, joueur, alpha, beta):
    score_actuel = fonction_cout(restant, joueur)
    
    # Si le jeu est terminé on retourne le score
    if restant == 0:
        return score_actuel 

    # Si c'est au tour du joueur 01 (maximiser le score)
    if joueur == 1:
        meilleur_score = -float('inf')
        for prise in range(1, 4):  # Le joueur peut prendre 1, 2 ou 3 allumettes
            if restant >= prise:
                score = minmax(restant - prise, profondeur + 1, 2, alpha, beta)
                meilleur_score = max(meilleur_score, score)
                alpha = max(alpha, meilleur_score)
                if beta <= alpha:
                    break  # Élagage bêta
        return meilleur_score
    
    # Si c'est au tour du joueur 02 (minimiser le score)
    else: 
        meilleur_score = float('inf')
        for prise in range(1, 4):  # Le joueur peut prendre 1, 2 ou 3 allumettes
            if restant >= prise:
                score = minmax(restant - prise, profondeur + 1, 1, alpha, beta)
                meilleur_score = min(meilleur_score, score)
                beta = min(beta, meilleur_score)
                if beta <= alpha:
                    break  # Élagage alpha
        return meilleur_score
    
def meilleur_coup(prises, joueur):
    meilleur_score = -float('inf') if joueur == 1 else float('inf')
    meilleur_prise = 1

    for prise in range(1, 4):
        if n - prises >= prise:
            score = minmax(n - prises - prise, 0, 2 if joueur == 1 else 1, -float('inf'), float('inf'))
            if (joueur == 1 and score > meilleur_score) or (joueur == 2 and score < meilleur_score):
                meilleur_score = score
                meilleur_prise = prise

    return meilleur_prise

def tour_jeu(prises, joueur, conseils, hard, est_humain):
    if est_humain:
        print(f"C'est à votre tour, joueur {joueur} !")
        if conseils == "Y":
            conseil = meilleur_coup(prises, joueur)
            print(f"💡 Conseil : Nous vous suggérons de prendre {conseil} allumette{'s' if conseil > 1 else ''}.")
        while True:
            try:
                prise = int(input("Combien d'allumettes voulez-vous prendre ? (1, 2 ou 3) : "))
                if 1 <= prise <= 3 and prise <= (n - prises):
                    break
                else:
                    print("Choix invalide. Veuillez choisir entre 1 et 3 allumettes, dans la limite disponible.")
            except ValueError:
                print("Veuillez entrer un nombre valide.")
    else:
        print(f"C'est au tour du joueur {joueur} :")
        if hard == "Y":
            prise = meilleur_coup(prises, joueur)
        elif hard == "N":
            while True:
                prise = random.randint(1, 3)
                if 1 <= prise <= 3 and prise <= (n - prises):
                    break
        print(f"L'ordinateur prend {prise} allumette{'s' if prise > 1 else ''}.")

    prises += prise
    affichage_allumettes(n, prises)
    
    if prises == n:
        print(f"{'Vous avez' if est_humain == True else 'Le PC a'} perdu !")
        return True, prises

    return False, prises

def humain_contre_pc(conseils, hard):
    prises = 0
    while True:
        print("----------------------------")
        # Tour de joueur 01 (humain)
        fin, prises = tour_jeu(prises, 1, conseils, hard, est_humain=True)
        if fin:
            break
        print("----------------------------")
        # Tour de joueur 02 (PC)
        fin, prises = tour_jeu(prises, 2, conseils, hard, est_humain=False)
        if fin:
            break

def pc_contre_humain(conseils, hard):
    prises = 0
    while True:
        print("----------------------------")
        # Tour de joueur 01 (PC)
        fin, prises = tour_jeu(prises, 1, conseils, hard, est_humain=False)
        if fin:
            break
        print("----------------------------")
        # Tour de joueur 02 (humain)
        fin, prises = tour_jeu(prises, 2, conseils, hard, est_humain=True)
        if fin:
            break

def menu():
        print("\nMenu principal :")
        print("1. Jouer en tant que player 01 contre pc")
        print("2. Jouer en tant que player 02 contre pc")
        print("3. Quitter")
        choix = input("Choisissez une option (1/2/3) : ")
        return choix

def activer_conseils():
        while True:
            choix_conseils = input("💡 Voulez-vous activer les conseils ? (Y/N) : ").strip().upper()
            if choix_conseils in {"Y", "N"}:
                return choix_conseils
            else:
                print("Entrée invalide. Veuillez répondre par 'Y' ou 'N'.")

def activer_hard():
        while True:
            choix_conseils = input("⚙️  Voulez-vous activer le mode hard ? (Y/N) : ").strip().upper()
            if choix_conseils in {"Y", "N"}:
                return choix_conseils
            else:
                print("Entrée invalide. Veuillez répondre par 'Y' ou 'N'.")

def main():
    while True:
        choix = menu()
        if choix == "1":
            conseils = activer_conseils()
            hard = activer_hard()
            humain_contre_pc(conseils, hard)
        elif choix == "2":
            conseils = activer_conseils()
            hard = activer_hard()
            pc_contre_humain(conseils, hard)
        elif choix == "3":
            print("Merci d'avoir joué. À bientôt !")
            break
        else:
            print("Choix invalide. Veuillez réessayer.")

if __name__ == "__main__":
    main()


