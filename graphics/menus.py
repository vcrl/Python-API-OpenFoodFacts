"""
Module permettant la gestion des menus,
et la navigation dans le programme.
"""
import sys
from time import sleep
from graphics.display import Display
from api.category import Category
from database.db_exec import Database_Executions
from constants.constants import ERROR, MENU

class Menus:
    """
    Classe permettant l'affichage des menus
    et la navigation dans le programme.
    Méthodes:
    * show_main_menu:
        - Affiche le menu principal avec une
        boucle, et prend les inputs des
        utilisateurs.

    * option_1:
        - Affiche le menu 1 avec une
        boucle, et prend les inputs des
        utilisateurs
    
    * option_1_2:
        - Affiche le menu 1_2 avec une
        boucle, et prend les inputs des
        utilisateurs

    * option_1_2_1:
        - Affiche le menu 1_2 avec une
        boucle, et prend les inputs des
        utilisateurs
    """
    def __init__(self):
        self.db = Database_Executions()
        self.display = Display()
        self.category = Category()

    def show_main_menu(self, from_start=True):
        """
        Méthode permettant l'affichage du menu principal
        avec une boucle, et prend les inputs des
        utilisateurs.
        Selons les inputs, la boucle est cassée et le
        programme passe à la méthode option_1.
        Arguments:
        * from_start = True:
            - Permet d'afficher l'option 'réinitialiser'
            uniquement si le menu est affiché à l'ouverture
            du programme, pour des raisons de performances.
        """

        self.clear_console()
        menu_choice = ['0', '1', '2', '3']
        if not from_start:
            menu = MENU["!main_from_start"] # Menu principal
        else:
            menu = MENU["main_from_start"]
        while True:
            choice = ""
            while choice not in menu_choice:
                choice = input(menu)
                if choice not in menu_choice:
                    print(ERROR["invalid_choice"])
            
            if choice == '1':
                self.option_1()
            
            if choice == '2':
                self.option_2()

            if from_start:
                if choice == '3':
                    self.db.reset()
                    self.category.create_categories()
                    self.clear_console()
                    print("<La base de donnée a bien été réinitialisée.>")

            if choice == '0':
                print("<Merci d'avoir utilisé ce service. A bientôt !>")
                sleep(1)
                sys.exit()

    def option_1(self):
        """"
        Méthode permettant l'affichage du menu option_1
        avec une boucle, permettant à l'utilisateur
        de sélectionner une catégorie de produit.
        Selons les inputs, la boucle est cassée et le
        programme passe à la méthode option_1_2.
        """

        self.clear_console()
        menu_choice = ['0', '1', '2', '3', '4', '5']
        menu = MENU['option_1']
        while True:
            choice = ""
            while choice not in menu_choice:
                choice = input(menu)
                if choice not in menu_choice:
                    print(ERROR["invalid_choice"])
            if choice == '0':
                self.show_main_menu(from_start=False)
            for option in menu_choice:
                if choice == option:
                    self.option_1_2(option)
                    break

    def option_1_2(self, category):
        """
        Méthode permettant l'affichage du 1_2
        avec une boucle, permettant à l'utilisateur
        de choisir un produit dans la catégorie qu'il
        a sélectionné.
        Selons les inputs, la boucle est cassée et le
        programme passe à la méthode option_1_2_1.
        Arguments:
        * category:
            - Permet d'accéder à la variable category
            passée par la méthode option_1, permettant
            d'afficher les produits de la bonne catégorie.
        """

        self.clear_console()
        result = self.db.execute_query_with_return(
            f"""
            SELECT * FROM category_has_product 
            INNER JOIN product ON 
            category_has_product.product_id = product.product_id
            WHERE category_id={category}
            AND NOT product.nutriscore = 'a'
            AND NOT product.nutriscore = 'b'
            ORDER BY product.nutriscore;
            """
            )
        menu_choice = []
        while True:
            choice = ""
            while choice == "":
                for x in result:
                    self.display.display_products(
                        x[1], x[3], x[4], x[8]
                    )
                    menu_choice.append(str(x[1]))
                menu_choice.append('0')
                choice = input(MENU["option_1_2"])
                if choice not in menu_choice:
                    print(ERROR['invalid_choice'])
            if choice == "0":
                self.show_main_menu(from_start=False)
            
            if choice in menu_choice:
                self.option_1_2_1(choice, x[3], category)
    
    def option_1_2_1(self, product_id, product_name, category):
        """
        Méthode permettant l'affichage du 1_2_1
        avec une boucle, permettant à l'utilisateur
        de choisir un substitut du produit choisit
        dans la catégorie qu'il a sélectionné.
        Selons les inputs, la boucle est cassée et le
        programme passe à la méthode show_main_menu.
        Arguments:
        * product_id:
            - Permet d'accéder à la variable product_id
            passée par la méthode option_1 (choice), afin
            de savoir quel produit initial l'utilisateur a
            choisit.
        
        * product_name:
            - Permet d'accéder à la variable product_name
            passée par la méthode option_1 (x[1]), afin
            de savoir le nom produit initial l'utilisateur a
            choisit, pour que les substituts soient liés à
            ce produits.
        
        * category:
            - Permet d'accéder à la variable category
            passée par la méthode option_1 (category), afin
            de connaître la catégorie dans laquelle afficher
            les produits.
        """

        self.clear_console()
        product_name = product_name.split()
        result = self.db.execute_query_with_return(
            f"""
             SELECT * FROM category_has_product 
            INNER JOIN product ON 
            category_has_product.product_id = product.product_id 
            WHERE name LIKE '%{product_name[0]}%'
            AND category_id = '{category}'
            ORDER BY -product.nutriscore;
            """
            )
        menu_choice = []
        while True:
            choice = ""
            while choice == "":
                for x in result:
                    try:
                        self.display.display_products(
                            x[1], x[3], x[4], x[8]
                        )
                        menu_choice.append(str(x[1]))
                    except ValueError:
                        print(ERROR['no_products'])
                menu_choice.append('0')
                choice = input(MENU["option_1_2_1"])
                if choice not in menu_choice:
                    print(ERROR['invalid_choice'])

            if choice == "0":
                self.show_main_menu(from_start=False)
            
            if choice in menu_choice:
                self.db.execute_query(f"INSERT INTO substitute (product_id, substitute_id) VALUES ({product_id}, {choice});")
                print("<La sélection a bien été enregistrée.>")
                self.show_main_menu(from_start=False)

    def option_2(self):
        """
        Méthode permettant l'affichage du menu 2
        avec une boucle, permettant au programme
        d'afficher les substituts enregistrés.
        La méthode ne prend qu'un input, qui doit
        être '0' pour revenir au menu principal.
        """

        self.clear_console()
        menu_choice = ['0']
        menu = MENU["option_2_2"]
        while True:
            choice = ""
            while choice not in menu_choice:
                print(MENU["option_2_1"])
                result = self.db.execute_query_with_return("SELECT * FROM substitute;")
                if result:
                    for x in result:
                        old_product = self.db.execute_query_with_return(
                            f"""
                            SELECT * FROM product WHERE product_id={x[0]};
                            """
                        )
                        substitute = self.db.execute_query_with_return(
                            f"""
                            SELECT * FROM product WHERE product_id={x[1]};
                            """
                        )
                        self.display.display_subtitutes(
                            old_product[0][1], old_product[0][2], old_product[0][6],
                            substitute[0][1], substitute[0][2], substitute[0][6],
                            substitute[0][4], substitute[0][5]
                        )
                else:
                    print(ERROR['empty'])
                choice = input(menu)
                if choice not in menu_choice:
                    print(ERROR["invalid_choice"])
                
            if choice == "0":
                self.show_main_menu(from_start=False)
    
    def clear_console(self):
        """"
        Méthode permettant de nettoyer la
        console pour un affichage plus
        agréable.
        """

        for i in range(100):
            print('\n')