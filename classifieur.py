import math



class Instance(object):
    
    def __init__(self,categorie,coords):
        """ Constructeur d'Instances.

        Arguments:
            categorie (str): La catégorie de l'instance
            coords (tuple): Un tuple de floats
                représentant la position de l'instance?
        """
        self.cat = categorie
        self.coords = coords

    def __str__(self):
        """ Méthode qui décrit l'instance elle-même.

        Variables:
            description (str): représente la description de notre instance
        """
        descriptionFruit = "Je susi un fruit de catégorie : " + self.cat + "  Et ma position dans l'espace est : "+ str(self.coords)
        return descriptionFruit
    
    def distance(self,other):
        """ Méthode qui calcule la distance entre deux instances

            Argument:
                other (instance) : représente notre instance que ce soit une orange ou un citron
            Vairables:
                resulatat (float) : représente la somme sur chaque dimension du carré de la coordonée de x moins la coordonnée de y pour cette dimension
                                    on retrun la racine carrée de la variable resultat -> elle représente la distance finale entre les deux instances
                distance (float) : représente la distance réelle entre les deux instances
        """
        resultat = 0
        distance = 0
        if(other.coords != 0):
            for i in range (0, len(self.coords),1):
               resultat = resultat + (self.coords[i] - other.coords[i])**2
            distance = math.sqrt(resultat)
            return distance
        
    def knn(self,k,listeInstances):
        """ Méthode qui calcule et renvoie une liste de taille k qui contient les instances plus proches de notre instance
            Arguments :
                k (int): représente le nombre d'instance plus proche de notre instance
                listeInstances (list) : représente la liste des instances.

            Variables:
                liste (list): c est une liste de liste. Exemple :
                      liste = [ ["la distance entre self et l' une des instances de la listeInstances ", " l instance elle-même "] , ...]
                      cette liste sera trié en fonction des distances. Ps : on a pas besoin de la méthode first_elem puisque python peut trier sur le premier élément
                returnListe (list) : c est une liste qui contiendra les k instances plus proche de notre instance (self).
                j (int) : c est un compteur
        """
        liste = []
        returnListe=[]
        j=1
        if k <= len(listeInstances):
            for instance in listeInstances:
                dist = self.distance(instance)
                liste.append([dist,instance])
            liste.sort()
            for i in range(0,k,1):
                returnListe.append(liste[i][1])
            return returnListe
                        
def most_common(listInstances):
    
    """ Méthode la catégorie la plus fréquente parmi une liste d'instances
        Arguments :
               listInstances (list) : représente la liste des instances.
      Variables :
          compteur_orange (int) : représente le nombre des oranges
                compteur_citron (int) : représente le nombre des citrons
                catOrange (str): représente la catégorie orange
                catCitron (str): représente la catégorie citron
        """
    compteur_orange = 0
    compteur_citron = 0
    catOrange = "orange"
    catCitron = "citron"
    for instance in listInstances:
        if instance.cat == "orange":
            compteur_orange+=1
        else: compteur_citron+=1
    if compteur_orange > compteur_citron:
        return catOrange
    else:
        return catCitron
    
def classify_instance(k,instance,all_instance):
        """ Méthode qui renvoie la catégorie la plus fréquente parmi les k plus proches voisins de instance.

            Arguments:
                k (int) : représente les k plus proches voisins de instance.
                instance (Instance) : représente l'instance conceranée
                all_instance (list) : représente la liste des instances
        """
        return most_common(instance.knn(k,all_instance))
    
def read_instances(filename):
        """ Méthode qui lit un fichier et renvoie une liste d'instances
            Arguments:
                filename (str) : représente le nom du fichier à lire
            Variables:
                ListeInstance (list) : représente la liste d instances lues à partir du fichier filename
                f : l'objet qui permet de lire le fichier
        """
        listeInstance = []
        f = open(filename,'r')
        lignes  = f.readlines()
        f.close()
        for ligne in lignes:
            cat = ligne.split("\t")[0]
            coords = (int(ligne.split("\t")[1]),int(ligne.split("\t")[2]))
            instance = Instance(cat,coords)
            listeInstance.append(instance)
        return listeInstance
    
def predict(listeInstancesConnues,listeInstancesInconnues,k):
        """ Méthode qui permet de prédir et de catégoriser une instance
            Arguements:
                listIntancesConnues (list) : représente la liste des instances connues
                listeInstanceInconnues (list) : représente la liste eds instances inconnues
                k (int) : représente les k plus proches voisin d'une instance
        """
        for instanceInconnue in listeInstancesInconnues:
            instanceInconnue.cat = classify_instance(k,instanceInconnue,listeInstancesConnues)
    
def eval_classif(ref_instances, pred_instances):
    """ Fonction qui donne le pourcentage de deux liste qui sont catégorisées de manière identique
        Arguments:
            ref_instances (list) : représente une liste d'instances connues
            pred_instances (list) : représente une liste d'instances inconnues

        Variables:
            ordonnee (boolean) : c'est la variable qui nous renseigne si nos deux liste sont ordonnées ou non.
            idem (int) : variable qui nous renseigne sur le nombre d'instances catégorisées de manière identique
            pourcentage : représente le pourcentage d'instance qui sont catégorisées de manière identique
    """
    ordonnee = True
    idem = 0
    pourcentage = 0
    listesNonOrdonnees = "Malheureusement, les deux listes ne sont pas ordonnées comme décrit dans l énoncé!!"
    listDeTailleDifferente = "Malheureusement, les deux listes ne sont pas de la même taille!!"
    taille = len(ref_instances)
    if taille == len(pred_instances):
        for i in range (0, taille, 1):
            if ref_instances[1].coords == ref_instances[i].coords:
                ordonnee = False
            break               
        if ordonnee == True:
            for i in range (0, taille ,1):
                if ref_instances[i].cat == pred_instances[i].cat:
                    idem+=1
            pourcentage = idem * 100 / taille
            return pourcentage
        else: return listesNonOrdonnees
    else: return listDeTailleDifferente
        
def test(filename):
    """ focntion suplémentaire, pour automatiser les tests de la question 9
        Arguments:
            filename (str): représente le fichier à lire
        Variables:
            listInstancesLues (list) : représente la liste des instances lues à partir du fichier.
            ListInstancesConnues (list): représente la liste des 10 instances connues
            listInstanceInconnues (list): représente la liste des intances inconnues
    """
    listInstancesLues = read_instances(filename)
    listInstancesConnues = []
    listInstancesInconnues = []
    for i in range (0, len(listInstancesLues),1):
        if i < 10:
            listInstancesConnues.append(listInstancesLues[i])
        else:
            listInstancesInconnues.append(listInstancesLues[i])
    predict(listInstancesConnues,listInstancesInconnues,3)
    listInstancesConnues.extend(listInstancesInconnues)
    listInstancesLues2 = read_instances(filename)
    print(eval_classif(listInstancesLues2,listInstancesConnues))
