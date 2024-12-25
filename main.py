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
from games import poker_variants, red_room, three_card_poker

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
            '7': ('Lightning Baccarat', baccarat.play_lightning_baccarat),
            '8': ('Sic Bo', sic_bo.play),
            '9': ('Craps', craps.play),
            '10': ('Seven Card Stud - 777 Edition', poker_variants.play_seven_card_stud),
            '11': ('Seven Devils Poker', poker_variants.play_seven_devils),
            '12': ('Red Room - Bet Behind Challenge', red_room.play_red_room),
            '13': ('Poker a 3 Carte', three_card_poker.play),
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

        console.print("[cyan]P.[/cyan] Chiedi un Prestito")
        console.print("[cyan]S.[/cyan] Salva Partita")
        console.print("[cyan]E.[/cyan] Esci")

    def request_loan(self):
        console.print("\n[red]═══════ PRESTITO OSCURO ═══════[/red]")
        console.print("[yellow]Il Banchiere ti guarda con un sorriso malizioso...[/yellow]")
        time.sleep(1)

        # Verifica se c'è già un prestito attivo
        if self.state.has_loan and not self.state.loan_is_active:
            console.print("\n[red]Il Banchiere sorride malignamente...[/red]")
            time.sleep(1)
            self.banker.loan_response('already_has_loan')
            return

        # Definizione delle fasce di prestito con condizioni sempre più opprimenti
        loan_tiers = [
            (1000, "Prestito del Principiante - Level 0: The Lobby", 0.5),  # 50% delle vincite al banchiere
            (5000, "Prestito dell'Esploratore - Level 1: The Warehouse", 0.6),  # 60% delle vincite al banchiere
            (10000, "Prestito dell'Audace - Level 2: Pipe Dreams", 0.7),  # 70% delle vincite al banchiere
            (50000, "Prestito del Temerario - Level 3: Electrical Station", 0.8),  # 80% delle vincite al banchiere
            (100000, "Prestito del Dannato - Level 4: Abandoned Office", 0.9),  # 90% delle vincite al banchiere
            (500000, "Prestito dell'Anima - Level 5: The Hotel", 0.95)  # 95% delle vincite al banchiere
        ]

        console.print("\n[red]'Scegli il tuo veleno... ogni prestito è un nuovo livello di dannazione.'[/red]")
        time.sleep(1)

        # Debug: Mostra che stiamo entrando nella sezione prestiti
        console.print("\n[dim]DEBUG: Mostrando le fasce di prestito delle Backrooms...[/dim]")

        # Mostra le opzioni di prestito con descrizioni dettagliate
        for i, (amount, name, rate) in enumerate(loan_tiers, 1):
            console.print(f"\n[cyan]{i}.[/cyan] {name}")
            console.print(f"   Ammontare: {amount} fiches")
            console.print(f"   Condizioni: {int(rate * 100)}% delle vincite al Banchiere")
            if i == 1:
                console.print("   [dim]L'infinito corridoio giallo ti attende...[/dim]")
            elif i == 2:
                console.print("   [dim]Tra scaffali infiniti e luci tremolanti...[/dim]")
            elif i == 3:
                console.print("   [dim]Dove i tubi sussurrano segreti dimenticati...[/dim]")
            elif i == 4:
                console.print("   [dim]L'elettricità statica della follia...[/dim]")
            elif i == 5:
                console.print("   [dim]Cubicoli vuoti che echeggiano di disperazione...[/dim]")
            else:
                console.print("   [dim]Camere infinite, ospiti eterni...[/dim]")

        # Debug: Mostra che stiamo aspettando la scelta dell'utente
        console.print("\n[dim]DEBUG: In attesa della scelta della fascia di prestito...[/dim]")

        # Richiedi la scelta
        choice = Prompt.ask("\n[yellow]Quale prestito desideri?[/yellow]", 
                               choices=[str(i) for i in range(1, len(loan_tiers) + 1)])

        chosen_tier = loan_tiers[int(choice) - 1]
        loan_amount, loan_name, repayment_rate = chosen_tier

        # Debug: Mostra la fascia di prestito selezionata
        console.print(f"\n[dim]DEBUG: Selezionata fascia di prestito {choice} - {loan_name}[/dim]")

        # Descrizione dettagliata del prestito scelto
        console.print(f"\n[red]═══ {loan_name} ═══[/red]")
        console.print(f"[yellow]Ammontare: {loan_amount} fiches[/yellow]")
        console.print(f"[yellow]Condizioni: {int(repayment_rate * 100)}% delle tue vincite andrà al Banchiere[/yellow]")

        if Prompt.ask("\n[red]Accetti le condizioni del prestito oscuro?[/red]", choices=["s", "n"]) == "s":
            self.state.chips += loan_amount
            self.state.loan = loan_amount
            self.state.loan_repayment_rate = repayment_rate
            self.state.has_loan = True
            self.state.original_loan = loan_amount
            self.state.loan_is_active = False  # Il prestito non è ancora stato giocato
            self.state.loan_tier = int(choice)  # Salva la fascia del prestito
            console.print(f"\n[green]Hai ricevuto {loan_amount} fiches[/green]")
            self.banker.loan_response(f'tier{choice}')  # Risposta specifica per la fascia di prestito
        else:
            console.print("\n[yellow]Hai rifiutato il prestito oscuro...[/yellow]")
            self.banker.loan_response('rejected')

    def explain_game_rules(self, game_key):
        rules = {
            '1': "Il numero perfetto è 21... Ma attenzione, superarlo significa perdersi nel vuoto...",
            '2': "Due carte nascoste, cinque destini condivisi... La verità si rivela in tre atti...",
            '3': "La ruota del destino gira eternamente... Rosso o nero, pari o dispari, il fato decide...",
            '4': "Come il Blackjack, ma i 10 sono svaniti nel nulla... Il potere del 21 rimane...",
            '5': "Vedi il mio destino, ma il pareggio... ah, il pareggio è sempre mio...",
            '6': "Punto o Banco, due facce della stessa moneta... La semplicità nasconde l'abisso...",
            '7': "Fulmini colpiscono il tavolo, moltiplicando le tue vincite... ma attenzione al rischio!",
            '8': "Tre dadi danzano nel vuoto... Le loro facce raccontano storie infinite...",
            '9': "I dadi rotolano, il 7 chiama... Pass o Don't Pass, scegli il tuo destino...",
            '10': "Sette carte, sette destini... Il potere del 7 scorre nelle vene del gioco...",
            '11': "Sette demoni attendono la sfida... Ogni vittoria è un passo verso la dannazione...",
            '12': "Benvenuto nella Red Room... Qui il rischio è altissimo, ma le ricompense altrettanto...",
            '13': "Tre carte, un destino... indovina la mano migliore per vincere!"
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