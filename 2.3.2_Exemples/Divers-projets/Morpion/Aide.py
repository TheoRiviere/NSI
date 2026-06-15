
def afficher_grille(grille):
    print("-----------------")
    for i in range(3):
        print(" | "+str(grille[i]), end='')
    print(" |")
    print("-----------------")
    for i in range(3):
        print(" | "+str(grille[i+3]), end='')
    print(" |")
    print("-----------------")


jeu =[0,1,0,0,2,0]
afficher_grille(jeu)



