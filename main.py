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
                                   data_app["user"]["passwd"])[0]
        data_app["user"]["id"] = id

    # Texte de bienvenue
    print(Fore.LIGHTGREEN_EX + Style.BRIGHT)
    print(pyfiglet.figlet_format("BIENVENUE", font="starwars", width=200))
    print(Style.RESET_ALL)

    app_menu = ["Lister mes tâches", "Nouvelle tâche", "Statistiques",
                "Marquer comme termine", "Supprimer une tâche", "Quitter"]

    while data_app["run"]:
        act = inquirer.select(message=f"\n{data_app['user']['name']} >",
                              amark="",
                              qmark="", choices=app_menu).execute()

        # Liste des tâches
        if act == app_menu[0]:
            table = Table(title="Liste Des Tâches", show_lines=True)

            table.add_column("ID", justify="center")
            table.add_column("Titre")
            table.add_column("Description")
            table.add_column("Terminee", justify="center")

            for task in data_conn.list_tasks(data_app["user"]["id"]):
                row = list(task[:-1])
                row[0] = str(row[0])
                # row[-1], col = ("OUI", "green") if row[-1] == 1 else ("NON", "red")
                # table.add_row(*row, style=col)
                row[-1] = "[green]OUI[/]" if row[-1] == 1 else "[red]NON[/]"
                table.add_row(*row)
                # print(row)

            console = Console()
            print()
            console.print(table)

        # Nouvelle tâche
        elif act == app_menu[1]:
            titre = inquirer.text(message="Titre:", amark="").execute()
            desc = inquirer.text(message="Description:", amark="").execute()
            done = int(inquirer.confirm(message="Marquer comme termine ?").execute())
            data_conn.insert_tasks(titre, desc, done, data_app["user"]["id"])
            print(Fore.GREEN + "<!> Operation effectuee avec succes\n" + Style.RESET_ALL)

        # Stats
        elif act == app_menu[2]:
            if data_app["user"]["admin"]:
                table = Table(title="Statistiques Generales", show_lines=True)

                table.add_column("Nom", justify="center")
                table.add_column("Termine")
                table.add_column("Total")
                table.add_column("Taux d'execution", justify="center")
                for name, id in data_conn.get_users():
                    total, done = data_conn.get_stats(id)
                    rate = round(done/total, 2) * 100 if total else 0.0
                    if rate > 50:
                        rate = "[green]" + str(rate) + "%[/]"
                    else:
                        rate = "[red]" + str(rate) + "%[/]"
                    table.add_row(name, str(done), str(total), rate)
                console = Console()
                print()
                console.print(table)
            else:
                total, done = data_conn.get_stats(data_app["user"]["id"])
                print("Total ->", Fore.BLUE, total, Style.RESET_ALL)
                print("Fini ->", Fore.BLUE, done, Style.RESET_ALL)
                rate = round(done/total, 2) * 100 if total else 0.0
                color = Fore.GREEN if rate > 50 else Fore.RED
                print("Taux d'execution ->", color,
                      str(rate) + "%", Style.RESET_ALL)

        # Marquer comme termine
        elif act == app_menu[3]:
            id = inquirer.number(message="ID de la tâche:", amark="").execute()
            if not data_conn.set_task_done(id, data_app["user"]["id"]):
                print(Fore.RED + "<!> Erreur! Reverifiez l'ID entre" + Style.RESET_ALL)
            else:
                print(Fore.GREEN + "<!> Operation effectuee avec succes" + Style.RESET_ALL)

        # Supprimer une tâche
        elif act == app_menu[4]:
            id = inquirer.number(message="ID de la tâche:", amark="").execute()
            if not data_conn.delete_task(id, data_app["user"]["id"]):
                print(Fore.RED + "<!> Erreur! Reverifiez l'ID entre" + Style.RESET_ALL)
            else:
                print(Fore.GREEN + "<!> Operation effectuee avec succes" + Style.RESET_ALL)

        # Quitter
        else:
            data_app["run"] = False


def main():
    # Initialiser colorama pour activer la coloration
    init()

    print(Emoji.replace("\n:no_entry: 👮 Declinez votre identite"))

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
            print("Ce compte n'existe pas, reverifiez les valeurs entreés")

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
    data_conn.create_database()
    while data_app["run"]:
        main()
