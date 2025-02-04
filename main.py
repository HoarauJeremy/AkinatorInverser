# Importation de la fonction chat depuis la librairie ollama
from colorama import Fore, Style
import ollama

# Liste pour stocker l'historique des messages
messages_history = []

agents = open('agents.txt', 'r', newline="")
liste_agents = agents.read()

def initialize_context(role_description: str) -> None:
    """
    Initialise le contexte du chatbot avec un rôle spécifique
    Args:
        role_description: Description du rôle que doit jouer le modèle
    """
    # On efface l'historique existant
    messages_history.clear()

    # On ajoute le message de contexte qui définit le rôle
    context_message = {
        'role': 'system',
        'content': f"Tu es un joueur qui agit en tant que {role_description}. " f"Réponds toujours en respectant ce rôle. " f" Voici une liste des agents pour que tes informations soient à jour {liste_agents}. N'oublie pas, c'est à moi de deviner quel agent tu as choisi."
    }
    messages_history.append(context_message)


def send_message_with_history(model_name: str, message: str) -> str:
    """
    Envoie un message en tenant compte de l'historique et du contexte
    Args:
        model_name: Nom du modèle à utiliser
        message: Message à envoyer
    Returns:
        La réponse du modèle
    """
    # Ajout du nouveau message à l'historique
    messages_history.append({
        'role': 'user',
        'content': message
    })

    # Envoi de tout l'historique au modèle
    response = ollama.chat(model=model_name, messages=messages_history)

    # Ajout de la réponse à l'historique
    messages_history.append(response.message)

    return response.message.content


def error_message():
    print("\nMmm... Il semblerait qu'une erreur soit survenue\n")


def recherche_agents():
    print(Fore.GREEN + 'Vous pouvez écrire "quitter" pour sortir du jeu.' + Style.RESET_ALL)

    while True:
        try:
           message = input("Posez votre question : ")
        except ValueError:
            error_message()
        else:
            match message:
                case "quitter":
                    break
                case _:
                    reponse = send_message_with_history('llama3.2', message)
                    print(Fore.LIGHTYELLOW_EX + reponse + Style.RESET_ALL)


# Exemple d'utilisation
if __name__ == "__main__":

    # Initialisation du contexte
    initialize_context(f"joueur d'akinator qui veut faire deviner un agent de Valorant.")

    while True:
        print(' 1 - Démarrer le jeu')
        print(' 2 - Quitter')

        try:
            option = int(input("Sélectionner une option : "))
        except ValueError:
            error_message()
        else:
            match option:
                case 1:
                    recherche_agents()
                case 2:
                    break
                case _:
                    error_message()

