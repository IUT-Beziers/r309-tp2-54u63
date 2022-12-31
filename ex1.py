from tkinter import *
from PIL import Image,ImageTk
from time import *
from tkinter import ttk




root=Tk()#initialisation de la fenêtre
main_canva=Canvas(root,bg="white",width=1000,height=1000)
main_canva.pack()


########################################CREATION DE L'OBJET POINTEUR############################
class pointeur:
    """
    classe qui symbolise le pointeur de la souris
    ne sert qu'à stocker qu'un ensemble de données en lien avec celui-ci
    """
    def __init__(self):
        self.state:str="None"#état clické par l'utilisateur
        self.menu_enable:bool=False#si le menu est activé(menu click droit)
        self.icone:bool=False#si la fonction de chamngement d'icone est acessible à l'écran
        self.obj:list=[0,0]#l'objet cliqué
        self.rename:bool=False #si la fonction de renomage est disponible à l'écran
        self.control:bool=False#si la touche control est enfoncée
        self.delete:bool=False # si le mode suppression est actif
########################################CREATION DE L'OBJET EQUIPEMENT#########################
class equipement():
    # la classe équipement est la classe maitresse. Elle regroupe les méthode de tous
    #les objets. Elle représente tous les équipements possibles
    def __init__(self): 
        self.size:int=35
    def initialize(self,e,identifier):
        """
        initialise l'objet en l'important dans le canva
        à l'endroit ou l'utilisateur à cliqué et en ajoutant
        des extension à son constructeur
        """
        self.posx:int=e.x#position en x
        self.posy:int=e.y#et en y
        self.id:int=identifier#combien de routeur créé (0 sera R0, si un routeur créé identifier = 1)
        self.name:str=self.prefix+str(self.id)#nom
        self.rangeX:list=[e.x-self.size,e.x+self.size]#taille de la hitbox en x
        self.rangeY:list=[e.y-self.size,e.y+self.size]#taille de la hitbox en y
        self.object=main_canva.create_image(self.posx,self.posy,image=self.img)#pose de l'image sur le canva
        self.placeholder=main_canva.create_text(self.posx,self.posy+self.size,text=self.name)#pose du texte tenant le nom sur le canva
    def change_name(self,name):
        """
        input: constructeur,name
        output: None
        syn: Change le texte du placeholder avec le nom fournis en entrée
        """
        self.name:str=name
        main_canva.itemconfigure(self.placeholder,text=self.name)
    def destroy_itself(self):
        """
        destruction de l'objet en supprimant l'image et le nom
        """
        main_canva.delete(self.object)
        main_canva.delete(self.placeholder)
    def move_itself(self,mv:list):
        """
        input: constructeur,tableau de mouvement
        syn: mv est un tableau qui décrit en x et en y les déplacements du cursuer([1,0],[0,-1],....)
        déplacement des éléments en fonctions de ce tableau et mise à jour des valeurs.
        """
        main_canva.move(self.object,mv[0],mv[1])
        main_canva.move(self.placeholder,mv[0],mv[1])
        self.rangeX:list=[self.rangeX[0]+mv[0],self.rangeX[1]+mv[0]]
        self.rangeY:list=[self.rangeY[0]+mv[1],self.rangeY[1]+mv[1]]
        self.posx+=mv[0]
        self.posy+=mv[1]

################################################ENFANTS DE EQUIPEMENTS#######################################"""
class routeur(equipement):
    """
    classe représentant un routeur qui hérite de la classe des méthode de la super classe équipement
    """
    def __init__(self,images):
        """
        input: image représentant le routeur
        """
        super().__init__()
        self.prefix:str="R"
        self.img=images[0]#image de routeur
        self.port_max:int=4
        self.port_aviable:int=2

class switch(equipement):
    """ 
    classe représentant un switch qui hérite de la classe des méthode de la super classe équipement
    """
    def __init__(self,images):
        super().__init__()
        self.prefix:str="S"
        self.img=images[1]#image de switch
        self.port_max:int=4
        self.port_aviable:int=2

class client(equipement):
    """
    classe représentant un poste client qui hérite de la classe des méthode de la super classe équipement
    """
    def __init__(self,images):
        super().__init__()
        self.prefix:str="C"
        self.img=images[2]#image de PC
        self.port_max:int=2
        self.port_aviable:int=1

###################################################CLASSE MENU#####################################################
class menu_square:
    """
    classe définisant le menu affiché lorsque l'utilisateur fait click droit sur l'écran
    """
    def __init__(self): 
        self.size_x:int=100
        self.size_y:int=50
        self.text_1:str="renomer"
        self.text_2:str="icone"
        self.text_3:str="ports"
    def init_menu(self,e):
        """
        input: constructeur, objet évent
        output: None
        syn: pose sur le canva les éléments permettant l'affichage du menu
        """
        self.t1x:int=e.x+27
        self.t2x:int=e.x+18#les valeurs de x sont variable car le point de référence du texte est au centre et donc la taille de la hitbox 
                           #du mot varie en -x et +x en fontion de sa longueur
        self.t1y:int=e.y+7#police 7
        self.t2y:int=e.y+20
        self.t3y:int=e.y+33
        self.rect=main_canva.create_rectangle(e.x,e.y,e.x+self.size_x,e.y+self.size_y,outline="black",fill="white")#créé un rectangle blanc sur lequel repose les éléments
        self.t1=main_canva.create_text(self.t1x,self.t1y,text=self.text_1)#
        self.t2=main_canva.create_text(self.t2x,self.t2y,text=self.text_2)#puis poses sur le rectangle les différents texte avec les espaces donné
        self.t3=main_canva.create_text(self.t2x,self.t3y,text=self.text_3)#(réutilisation de t2x car t2 et t3 ont la même longueur de mots)
    def destroy_menu(self):
        """
        détruit le menu en supprimant les éléments du canva
        """
        main_canva.delete(self.rect)
        main_canva.delete(self.t1)
        main_canva.delete(self.t2)
        main_canva.delete(self.t3)
    def is_clicked(self,e):
        """
        input : l'élément e
        syn: lancement des fonction du menu en fontion des hitbox des mots
        """
        if e.x<self.t1x+(self.size_x-27) and e.x>self.t1x-27:
            if e.y<self.t1y+7 and e.y>self.t1y-7:
                global object_list
                rename()#lancement de la fonction de rename
                return 0
        if e.x<self.t2x+(self.size_x-18) and e.x>self.t2x-18:
            if e.y<self.t2y+7 and e.y>self.t2y-7:
                icone()#changment d'icone
                return 0
        if e.x<self.t2x+(self.size_x-18) and e.x>self.t2x-18:
            if e.y<self.t3y+7 and e.y>self.t3y-7:
                port()
###################################################CLASSE LIEN#####################################################
class link():
    """
    classe définissant les liens entre les équipements
    """
    def __init__(self,start,end):
        """
        input, start un objet de la classe équipement, end un objet de la classe équipement
        """
        self.start:list=[start.posx,start.posy]#positionnement du lien sur la racine de l'équipement sur lequel l'utilisateur à clické en premier
        self.end:list=[end.posx,end.posy]#positionnement du lien sur la racine de l'équipement sur lequel l'utilisateur à clické en dernier
        self.obj:list=[start,end]#référencement des deux objets du lien 
    def create_link(self):
        """
        syn: dessin du lien du le canva et retranchement dans les ports disponibles des équipements concernés
        """
        self.line=main_canva.create_line(self.start[0],self.start[1],self.end[0],self.end[1],fill="black",width=3)
        self.obj[0].port_aviable-=1
        self.obj[1].port_aviable-=1
        return self.line
    def destroy(self):
        """
        destruction de la ligne sur le canva, restitution des ports
        """
        self.obj[1].port_aviable+=1
        main_canva.delete(self.line)
    def move(self,obj,mv):
        """
        input: l'objet déplacé, le tableau de déplacement
        syn: déplace le lien en fontion de quel objet est déplacé
        """
        if obj==self.obj[0]:
            new_coord=[self.start[0]+mv[0],self.start[1]+mv[1],self.end[0],self.end[1]]#création d'un nouveau tableau avec les nouvelles coordonnées 
            main_canva.coords(self.line,new_coord[0],new_coord[1],new_coord[2],new_coord[3])#application de ces nouvelles coordonnées sur la ligne
            self.start[0]+=mv[0]#changement du tableau de définition en x et en y de la ligne
            self.start[1]+=mv[1]
            
        else:
            new_coord=[self.start[0],self.start[1],self.end[0]+mv[0],self.end[1]+mv[1]]
            main_canva.coords(self.line,new_coord[0],new_coord[1],new_coord[2],new_coord[3])
            self.end[0]+=mv[0]
            self.end[1]+=mv[1]
#########################################FONCTIONS####################################
def is_obj_click(e):
    """ 
    input : e
    output : l'objet cliqué par e
    syn: import la liste d'objet et vérifie si e est dans les hitbox de chaque élément
    sinon None est renvoyé
    """
    global object_list
    for i in range(len(object_list)):#la liste est référencée plus loin
        for j in range(len(object_list[i])):
            if e.x < object_list[i][j].rangeX[1] and e.x > object_list[i][j].rangeX[0]:#pour rappel rangeX est la hitbox en x de l'équipement
                if e.y<object_list[i][j].rangeY[1] and e.y > object_list[i][j].rangeY[0]:#et rangeY sa hitbox en Y
                    return object_list[i][j]  

def port():
    global object_list
    obj=object_list[selector.obj[0]][selector.obj[1]]

    def increment():
        num=int(value.get())+1
        value.set(str(num))
    def decrement():
        num=int(value.get())-1
        value.set(str(num))
    def validate():
        obj.port_aviable=int(value.get())
        for element in port_menu:
            main_canva.delete(element)
    validate=Button(root,text="valider",command=validate)
    def trace_value():
        if int(value.get())>obj.port_max or int(value.get())<0:
            validate["state"]="disabled"
        else:
            validate["state"]="normal"
    label=Label(root,text="port de "+obj.name+" :")
    value=StringVar()
    value.trace("w", lambda name, index, mode, value=value: trace_value())
    value.set(obj.port_aviable)
    num_holder=Label(root,textvariable=value)
    btn_plus=Button(root,text="+",command=increment)
    btn_moins=Button(root,text="-",command=decrement)
    cute_rectangle=main_canva.create_rectangle(200,200,800,800,outline="black",fill="white")
    cute_name=main_canva.create_window(500,400,window=label)
    cute_numholder=main_canva.create_window(500,425,window=num_holder)
    cute_plus=main_canva.create_window(475,450,window=btn_plus)
    cute_moins=main_canva.create_window(525,450,window=btn_moins)
    cute_validate=main_canva.create_window(500,500,window=validate)
    port_menu=[cute_name,cute_numholder,cute_plus,cute_moins,cute_validate,cute_rectangle]

def rename():
    """
    syn: import la liste d'objet, active l'état du selecteur rename, récupère l'objet cliqué
    puis créé un  recangle blanc sur lequel il dispose les éléments qu'il sotcke dans une tableau
    enfin il stocke le nom dans un stringvar et appelle la fonction get_name quand le boutton est clické.
    cette fonctionne appelle la méthode change_name de la classse équipement en lui passant en argument
    le nouveau nom puis détruit tous les éléments disposés sur le menu.
    """
    global object_list
    selector.rename=True
    obj=object_list[selector.obj[0]][selector.obj[1]]
    def get_name():
        selector.rename=False
        global menu_clicked
        obj.change_name(textbox.get())   
        for i in range(len(rename_menu)):
            main_canva.delete(rename_menu[i])
        menu_clicked.destroy_menu()
    cute_rectangle=main_canva.create_rectangle(200,200,800,800,outline="black",fill="white")
    textbox=Entry(root)
    label=Label(root,text="nom?")
    bouton=ttk.Button(root,text="valider",command=get_name)
    cute_labe=main_canva.create_window(500,400,window=label)
    cute_txtbox=main_canva.create_window(500,425,window=textbox)
    cute_button=main_canva.create_window(500,450,window=bouton)
    global rename_menu
    rename_menu=[cute_labe,cute_txtbox,cute_rectangle,cute_button]

def icone():
    """
    synopsis, importe l'objet clické ainsi que les images
    puis change l'image en fontion du préfixe utilisé à chaque click (C'est le nom qui change lors du rename pas le préfix).
    enfin il détruit le menu
    """ 
    global object_list
    obj=object_list[selector.obj[0]][selector.obj[1]]
    global images
    pref_list:list=["R","S","C"]
    index=pref_list.index(obj.prefix)
    pref_used:str=""
    if index==len(pref_list)-1:
        pref_used+=pref_list[0]
    else:
        pref_used+=pref_list[index+1]
    if pref_used=="R":
        main_canva.itemconfigure(obj.object,image=images[0])
    if pref_used=="C":
        main_canva.itemconfigure(obj.object,image=images[2])
    if pref_used=="S":
        main_canva.itemconfigure(obj.object,image=images[1])
    else:
        pass
    global menu_clicked
    menu_clicked.destroy_menu()
    obj.prefix=pref_used

def create_routeur(e,object_list,images):
    """
    input: la liste d'objet, l'objet évent, la liste d'image
    syn: créé un nouveau routeur et l'ajoute à la liste de référence des objets
    """
    selector.state="None" #réinitialisation de l'état du pointeur
    new_routeur=routeur(images)
    new_routeur.initialize(e,len(object_list[0]))
    object_list[0].append(new_routeur) 
    
def create_switch(e,object_list,images):
    """
    syn: exactement la même chose que la fonction "create_routeur" mais avec les switchs
    """
    selector.state="None" 
    new_switch=switch(images)
    new_switch.initialize(e,len(object_list[1]))
    object_list[1].append(new_switch)

def create_client(e,object_list,images):
    """
    syn: exactement la même chose que la fonction "create_routeur" mais avec les PC
    """
    selector.state="None" 
    new_client=client(images)
    new_client.initialize(e,len(object_list[2]))
    object_list[2].append(new_client)

def menu(e):
    """
    input:l'objet évent
    ouptut: les coordonnées du menu créé
    syn: instancie un tableau et change l'état du pointeur
    """
    global menu_clicked
    menu_clicked=menu_square()
    menu_clicked.init_menu(e)
    selector.menu_enable=True
    return [e.x,e.y,e.x+ 100,e.y+50]

def destroy_menu():
    """
    syn: détruit un menu, remet le pointeur sur son état initial
    """
    global menu_clicked 
    menu_clicked.destroy_menu()
    selector.menu_enable=False

def two_obj(numb_obj,e):
    """
    input: une liste d'objet,e
    output: un objet de la classe équipement déjà posé sur le canva ou 0
    syn renvoie l'objet clické par l'utilisateur, seulement si la liste contient moins de deux éléments
    
    """
    if len(numb_obj)<2:
        obj=is_obj_click(e)
        return obj
    else:
         return 0

def create_link(obj_list):
    """
    input: la liste des liens, la liste des objets entre lesquel les liens sont faits
    output: 0/1
    syn: vérifie le nombre de ports disponibles sur les deux machines et si c'est possible créé, instancie un lien entre les deux
    et l'ajoute à la liste des liens
    """
    global link_list
    if obj_list[0].port_aviable>0:
        if obj_list[1].port_aviable>0:
            current_link=link(obj_list[0],obj_list[1])
            current_link.create_link()
            link_list.append(current_link)
            return 0
    else:
        print("pas assez de port sur la machine!")
        return 1

def draw(e):
    """
    input : l'objet e
    output : la ligne dessinée
    syn: créé une ligne de 1px entre deux coordonées
    """
    line_drawed=None
    if main_canva.old_coords:
        p2_x,p2_y= main_canva.old_coords
        line_drawed=main_canva.create_line(p2_x,p2_y,e.x,e.y,width=3,fill="black")
    main_canva.old_coords=e.x,e.y
    return line_drawed

def straight_lines(e):
    """
    input: l'objet évent, un click counter
    output: la liogne créée
    syn: créé des lignes verticales ou horizontales entre deux points lorsque la touche control est enfoncée
    """
    global cc 
    if main_canva.old_coords:
        if cc%2==1:#si il y a bien eut deux clicks
            x,y=main_canva.old_coords
            difx:int=e.x-x#calcul de la différence en x
            dify:int=e.y-y#et en y entre les deux points
            if difx>=dify:
                line=main_canva.create_line(x,y,e.x,y,fill="black",width=3)
            if difx<dify:
                line=main_canva.create_line(x,y,x,e.y,fill="black",width=3)
            main_canva.old_coords=e.x,e.y
            cc+=1
            return line

        else:
            main_canva.create_line(e.x,e.y,e.x+1,e.y+1,width=3,fill="black")
            cc+=1
            main_canva.old_coords=e.x,e.y
    else:#sinon création d'un simple point
        main_canva.create_line(e.x,e.y,e.x+1,e.y+1,width=3,fill="black")
        cc+=1
        main_canva.old_coords=e.x,e.x

def get_link(obj):
    """
    input: un objet de la classe équipement, la liste des liens
    output: tous les liens de cet objet
    syn: vérifie la présence d'un objet aux extrémitées d'un lien et l'ajoute à un liste retournée à la fin de la fonction
    """
    global link_list
    link=[]
    for i in range(len(link_list)):
        if obj in link_list[i].obj:
           link.append(link_list[i])
    return link

def delete_obj(obj):
    """
    input : uun objet
    supprime un objet (sa représentation ainsi que son nom sur le canva)
    puis récupère la liste des lien auquel il est associé
    afin ces liens sont détruits et retirés de la liste des liens.
    l'objet est enfin retiré de la liste des objets
    """
    global link_list
    obj.destroy_itself()
    links=get_link(obj)
    for i in range(len(links)):
        links[i].destroy()
        link_list.remove(links[i])
    global object_list
    for i in range(3):
        if obj in object_list[i]:
             object_list[i].remove(obj)

def move_obj(obj,mv):
    """
    input: un objet
    modifie l\'état des liens et de l\'objet en fonction du déplacement de la souris
    """
    global link_list
    obj.move_itself(mv)
    links=get_link(obj)
    for link in links:
        link.move(obj,mv)


########################################VARIABLES####################################
selector=pointeur()#instantiation du sélecteur/pointeur/curseur
main_canva.old_coords=None
global link_list#liste des liens
link_list=[]
global object_list#liste des équipements dvisiée en 3 talbleau, un chacun des type
object_list=[[],[],[]]
exit_button=Button(root,text="X",command=root.destroy)#destruction de la fenêtre
main_canva.create_window(925,10,window=exit_button)#ajout du boutton dans le canva
global images#liste des images des différents équipements
images=[ImageTk.PhotoImage(Image.open("routeur.png")),
        ImageTk.PhotoImage(Image.open("switch.png")),
        ImageTk.PhotoImage(Image.open("PC.png"))]
global linked_obj#tableau stockant les deux objets à lier lors de la création d'un lien
linked_obj=[]
global draw_list#tableau de référencement des dessins
draw_list=[]
global drawing
drawing=[]#tableau stockant tout les points d'un dessin
global cc#compteur de click pour le traits horizontaux et verticaux
cc=0
global old_E_coord#anciennes coordonnées de e lors des déplacements
old_E_coord=[0,0]
global moved_obj#objet déplacés, initialisé a un objets différent pour éviter les erreurs lorsqu'il n'y a qu'un seul objet
moved_obj=pointeur
#########################################CALLBACKS###############################
def click(e):
    """
    input: objet évent
    syn: en fonction de la touche qui a été pressé et quand le b1 de la souris est pressé, appelle les différentes fonctions
    """
    global object_list
    if selector.rename==True:
        selector.state="None"
    if selector.state=="Routeur":
        create_routeur(e,object_list,images)
    elif selector.state=="Switch":
        create_switch(e,object_list,images)
    elif selector.state=="Client":
        create_client(e,object_list,images)
    elif selector.menu_enable==True and selector.state=="None":
        global menu_clicked
        menu_clicked.is_clicked(e)
    elif selector.state=="line":
        """
        appelle les fonction de création des liens et de vérification des clicks
        """
        global linked_obj
        re=two_obj(linked_obj,e)
        if re==0 and re not in linked_obj:
            create_link(linked_obj)
            linked_obj=[]
        elif re not in linked_obj:
            linked_obj.append(re)
        else:
            print("no link created")
    elif selector.state=="draw" and selector.control==True:
        """
        création des dessins
        """
        global draw_list
        re=straight_lines(e)
        if re!=None:
            draw_list.append(re)
        else:
            pass
    elif selector.state=="None" and selector.delete==True:
        """
        supression des objets
        """
        obj=is_obj_click(e)
        delete_obj(obj)
    else:
        pass

def pressed(e):
    """
    transforme l'état de la touche pressée en un état du sélecteur
    """
    if e.char=="r":
        selector.state="Routeur"
    elif e.char=="s":
        selector.state="Switch"
    elif e.char=="c":
        selector.state="Client"
    elif e.char=="e":
        selector.state="None"
        main_canva.old_coords=None
    elif e.char=="l":
        selector.state="line"
    elif e.char=="d":
        selector.state="draw"
    elif e.char=="m":
        selector.state="move"
    else:
        pass

def rmb(e):
    """
    gestion du click droit
    même fonction que "is_obj_clicked" mais adaptée au menu
    implémentation à retravailler, fonctionnel mais terriblement laid
    """
    global object_list
    test=0
    if selector.menu_enable is False:
        for i in range(len(object_list)):
            for j in range(len(object_list[i])):
                if e.x < object_list[i][j].rangeX[1] and e.x > object_list[i][j].rangeX[0]:
                    if e.y<object_list[i][j].rangeY[1] and e.y > object_list[i][j].rangeY[0]:
                        global menu_size
                        menu_size=menu(e)
                        selector.obj=[i,j]
                        return 0
    if selector.menu_enable is True:
         destroy_menu()#destruction du menu si deuxième clic droit et que menu activé

def escape(e):
    """
    réinitialisation de tout les paramètres si appui sur la touche echap
    """
    if selector.menu_enable==True:
        global menu_clicked
        menu_clicked.destroy_menu()
        selector.menu_enable==False
    if selector.rename==True:
        global rename_menu
        for i in range(len(rename_menu)):
            main_canva.delete(rename_menu[i])
    selector.state="None"
    main_canva.old_coords=None
    global drawing
    global draw_list
    draw_list.append(drawing)
    selector.delete=False
    print(selector.delete)

def motion(e):
    """
    gestion du click avec déplacement
    """
    if selector.state=="draw":
        """
        simple dessin
        """
        global drawing
        if selector.control==False:
            drawing.append(draw(e))
    elif selector.state=="move":
        """
        déplacement
        """
        global moved_obj
        obj=is_obj_click(e)
        global old_E_coord
        if old_E_coord==[0,0]or moved_obj!=obj:
            mvmnt=[0,0]
        else:
            mvmnt=[e.x-old_E_coord[0],e.y-old_E_coord[1]]
        old_E_coord=[e.x,e.y]
        move_obj(obj,mvmnt)
        moved_obj=obj

def control(e):
    """
    gestion de l'appuis de la touche ctrl
    """
    selector.control=True

def release(e):
    if selector.control==False:
        pass
    else:
        selector.control=False

def delete(e):
    """
    supression d'un item si click sur delete
    """
    selector.delete=True
    obj=is_obj_click(e)
    delete_obj(obj)

#############################################BINDINGS######################################"
root.bind("<KeyPress>",pressed)
root.bind("<Button-1>",click)
root.bind("<Button-2>",rmb)
root.bind("<Button-3>",rmb)
root.bind("<Escape>",escape)
root.bind("<B1-Motion>",motion)
root.bind("<KeyRelease>",release)
root.bind("<Control_L>",control)
root.bind("<Delete>",delete)
root.mainloop()
