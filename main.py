from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich import print
import os
import time
from utils.banker import Banker
from utils.game_state import GameState
from utils.ascii_art import TITLE_ART, CASINO_ART
from games import blackjack, poker, roulette, caribbean_stud, blackjack_variants, baccarat, sic_bo, craps
from games import poker_variants

console = Console()

class Level777:
    def __init__(self):
        self.banker = Banker()
        self.state = GameState()
        self.base_games = {
            '1': ('Blackjack Tradizionale', blackjack.play),
            '2': ('Poker Texas Hold\'em', poker.play),
            '3': ('Roulette', roulette.play),
            '4': ('Spanish 21', blackjack_variants.play_spanish21),
            '5': ('Double Exposure Blackjack', blackjack_variants.play_double_exposure),
            '6': ('Baccarat - Punto Banco', baccarat.play_punto_banco),
            '7': ('Sic Bo', sic_bo.play),
            '8': ('Craps', craps.play),
            '9': ('Seven Card Stud - 777 Edition', poker_variants.play_seven_card_stud),
            '10': ('Seven Devils Poker', poker_variants.play_seven_devils),
        }

        self.special_games = {
            'B': ('Sfida il Banchiere', caribbean_stud.challenge_banker, 77777),
            'F': ('Sfida Finale', caribbean_stud.final_challenge, 1000000)
        }

    def clear_screen(self):
        os.system('clear' if os.name == 'posix' else 'cls')

    def show_intro(self):
        self.clear_screen()
        print(Panel.fit(TITLE_ART, title="[red]LIVELLO 777[/red]", border_style="red"))
        console.print("\n[yellow]Benvenuto al Livello 777 - Il Casinò Infinito[/yellow]")
        console.print("[dim]Dove il tempo perde significato e le fiches non finiscono mai...[/dim]")
        console.print("\n[dim]Creato da Jashin L.[/dim]")
        console.print("[dim]© 2024 Level 777 - Tutti i diritti riservati[/dim]")
        time.sleep(2)
        self.banker.welcome_message()

    def show_menu(self):
        console.print("\n[green]Le tue fiches:[/green]", self.state.chips)
        console.print("\n[purple]Giochi Disponibili:[/purple]")

        # Mostra i giochi base
        for key, (game_name, _) in self.base_games.items():
            console.print(f"[cyan]{key}.[/cyan] {game_name}")

        # Mostra i giochi speciali solo se sono sbloccati
        for key, (game_name, _, required_chips) in self.special_games.items():
            if self.state.chips >= required_chips:
                console.print(f"[cyan]{key}.[/cyan] {game_name}")

        console.print("[cyan]P.[/cyan] Chiedi un Prestito")
        console.print("[cyan]S.[/cyan] Salva Partita")
        console.print("[cyan]E.[/cyan] Esci")

    def request_loan(self):
        console.print("\n[red]═══════ PRESTITO OSCURO ═══════[/red]")
        console.print("[yellow]Il Banchiere ti guarda con un sorriso malizioso...[/yellow]")
        time.sleep(1)
        console.print("\n[red]'Ti offro un prestito... ma ogni vincita sarà dimezzata finché non lo restituirai.'[/red]")
        time.sleep(1)

        amounts = ["1000", "5000", "10000"]
        loan_amount = Prompt.ask("\n[yellow]Quanto desideri prendere in prestito?[/yellow]", choices=amounts)
        loan_amount = int(loan_amount)

        if Prompt.ask("\n[red]Accetti le condizioni del prestito oscuro?[/red]", choices=["s", "n"]) == "s":
            self.state.chips += loan_amount
            self.state.loan = loan_amount
            self.state.has_loan = True
            console.print(f"\n[green]Hai ricevuto {loan_amount} fiches[/green]")
            console.print("[red]Il Banchiere ride sommessamente...[/red]")
        else:
            console.print("\n[yellow]Hai rifiutato il prestito oscuro...[/yellow]")

    def explain_game_rules(self, game_key):
        """Mostra le regole del gioco selezionato in modo criptico"""
        rules = {
            '1': "Il numero perfetto è 21... Ma attenzione, superarlo significa perdersi nel vuoto...",
            '2': "Due carte nascoste, cinque destini condivisi... La verità si rivela in tre atti...",
            '3': "La ruota del destino gira eternamente... Rosso o nero, pari o dispari, il fato decide...",
            '4': "Come il Blackjack, ma i 10 sono svaniti nel nulla... Il potere del 21 rimane...",
            '5': "Vedi il mio destino, ma il pareggio... ah, il pareggio è sempre mio...",
            '6': "Punto o Banco, due facce della stessa moneta... La semplicità nasconde l'abisso...",
            '7': "Tre dadi danzano nel vuoto... Le loro facce raccontano storie infinite...",
            '8': "I dadi rotolano, il 7 chiama... Pass o Don't Pass, scegli il tuo destino...",
            '9': "Sette carte, sette destini... Il potere del 7 scorre nelle vene del gioco...",
            '10': "Sette demoni attendono la sfida... Ogni vittoria è un passo verso la dannazione...",
            'B': "La sfida suprema... Solo i più ricchi osano sfidarmi direttamente...",
            'F': "La sfida finale... solo i più audaci possono affrontare il mio potere!"
        }
        if game_key in rules:
            if Prompt.ask("\n[yellow]Vuoi che il Banchiere ti sussurri le regole del gioco?[/yellow]", choices=["s", "n"]) == "s":
                console.print(f"\n[red]Il Banchiere sussurra le regole:[/red]")
                console.print(f"[italic]{rules[game_key]}[/italic]")
                time.sleep(3)

    def run(self):
        try:
            self.show_intro()

            while True:
                try:
                    self.show_menu()
                    available_choices = list(self.base_games.keys()) + ['P', 'S', 'E']

                    # Aggiungi le opzioni speciali solo se sbloccate
                    for key, (_, _, required_chips) in self.special_games.items():
                        if self.state.chips >= required_chips:
                            available_choices.append(key)

                    choice = Prompt.ask("\n[yellow]Scegli il tuo gioco[/yellow]", choices=available_choices)

                    if choice == 'P':
                        self.request_loan()
                        continue

                    if choice == 'S':
                        self.state.save_game()
                        console.print("\n[green]Partita salvata con successo![/green]")
                        time.sleep(1)
                        continue

                    if choice == 'E':
                        console.print("\n[red]Il Banchiere ti saluta mentre la realtà inizia a svanire...[/red]")
                        time.sleep(2)
                        break

                    # Gestione giochi base
                    if choice in self.base_games:
                        game_name, game_func = self.base_games[choice]
                        self.explain_game_rules(choice)
                        console.print(f"\n[green]Iniziando {game_name}...[/green]")
                        time.sleep(1)
                        self.clear_screen()
                        game_func(self.state, self.banker)

                    # Gestione giochi speciali
                    elif choice in self.special_games:
                        game_name, game_func, required_chips = self.special_games[choice]
                        if self.state.chips >= required_chips:
                            self.explain_game_rules(choice)
                            console.print(f"\n[green]Iniziando {game_name}...[/green]")
                            time.sleep(1)
                            self.clear_screen()
                            game_func(self.state, self.banker)

                    self.clear_screen()

                except (KeyboardInterrupt, EOFError):
                    console.print("\n[red]Il gioco è stato interrotto...[/red]")
                    time.sleep(1)
                    if Prompt.ask("\n[yellow]Vuoi salvare la partita?[/yellow]", choices=["s", "n"]) == "s":
                        self.state.save_game()
                        console.print("\n[green]Partita salvata con successo![/green]")
                    break
                except Exception as e:
                    console.print(f"\n[red]Errore imprevisto: {str(e)}[/red]")
                    time.sleep(2)
                    continue

        except Exception as e:
            console.print(f"\n[red]Errore fatale: {str(e)}[/red]")
            return

if __name__ == "__main__":
    game = Level777()
    game.run()