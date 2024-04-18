import pyfiglet
from colorama import init, Fore, Style
from InquirerPy import inquirer
from rich.emoji import Emoji
from rich.console import Console
from rich.table import Table
import data_conn


def app():
    if not data_app["user"].get("id", None):
        id = data_conn.search_user(data_app["user"]["name"],
                                   data_app["user"]["passwd"])
        data_app["user"]["id"] = id

    # Texte de bienvenue
    print(Fore.LIGHTGREEN_EX + Style.BRIGHT)
    print(pyfiglet.figlet_format("BIENVENUE", font="starwars", width=200))
    print(Style.RESET_ALL)

    app_menu = ["Lister mes tâches", "Nouvelle tâche", "Statistiques",
                "Modifier une tâche", "Quitter"]

    while data_app["run"]:
        act = inquirer.select(message=f"{data_app['user']['name']} >",
                              amark="",
                              qmark="", choices=app_menu).execute()

        # Liste des tâches
        if act == app_menu[0]:
            table = Table(title="Liste Des Tâches")

            table.add_column("ID", justify="center")
            table.add_column("Titre")
            table.add_column("Description")
            table.add_column("Terminee", justify="center")

            for task in data_conn.list_tasks(data_app["user"]["id"]):
                row = list(task[:-1])
                row[0] = str(row[0])
                row[-1], col = ("OUI", "green") if row[-1] == 1 else ("NON", "red")
                # print(row)
                table.add_row(*row, style=col)

            console = Console()
            console.print(table)

        # Nouvelle tâche
        elif act == app_menu[1]:
            ...

        # Stats
        elif act == app_menu[2]:
            ...

        # Modifier un tâche
        elif act == app_menu[3]:
            ...

        # Quitter
        else:
            data_app["run"] = False


def main():
    # Initialiser colorama pour activer la coloration
    init()

    print(Emoji.replace("\n:no_entry: \U0001F46E Declinez votre identite"))

    # Define menu items
    auth_menu = ['Se connecter', 'Creer un compte', 'Quitter']

    # Create the menu
    answ = inquirer.select(message="Que voulez vous faire ?",
                           amark=">>",
                           choices=auth_menu).execute()

    # Connection
    if answ == auth_menu[0]:
        name = inquirer.text(message="Nom d'utilisateur:", amark="").execute()
        passwd = inquirer.text(message="Mot de passe:", amark="",
                               transformer=lambda txt: '*' * len(txt),
                               is_password=True).execute()
        user = data_conn.search_user(name, passwd)
        if user:
            data_app["user"] = {"name": user[1],
                                "admin": user[4], "id": user[0]}
            app()
        else:
            print(Fore.LIGHTRED_EX + "<!> " + Style.RESET_ALL, end="")
            print("Ce compte n'existe pas, revérifiez les valeurs entreés")

    # Creation de compte
    elif answ == auth_menu[1]:
        name = inquirer.text(message="Nom d'utilisateur:", qmark="",
                             amark="").execute()

        email = inquirer.text(message="Email:", qmark="", amark="").execute()

        passwd = inquirer.text(message="Mot de passe:", qmark="", amark="",
                               transformer=lambda txt: '*' * len(txt)).execute()

        admin = inquirer.select(message="Type de compte:", qmark="", amark="",
                                choices=["simple", "administrateur"]).execute()

        admin = 0 if admin == "simple" else 1
        # print(name, email, passwd, admin)

        # Verifier si le compte existe deja
        user = data_conn.search_user(name, passwd)
        if user:
            print(Fore.LIGHTRED_EX + "<!> " + Style.RESET_ALL, end="")
            print("Ce compte existe déja, connectez vous")
        else:
            data_conn.insert_user(name, email, passwd, admin)
            data_app["user"] = {"name": name, "passwd": passwd, "admin": admin}
            app()

    # Quitter
    else:
        data_app["run"] = False


data_app = {"run": True}
if __name__ == "__main__":
    # data_conn.create_database()
    while data_app["run"]:
        main()
