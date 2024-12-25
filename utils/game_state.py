import pickle
import os
from rich.console import Console
from rich.prompt import Prompt
import sys
import time

console = Console()

class GameState:
    def __init__(self):
        self.chips = 777  # Starting chips changed to 777
        self.has_loan = False
        self.loan = 0
        self.special_endings = {
            'banker_defeated': False,
            'membership_accepted': False,
            'membership_rejected': False,
            'secret_ending_1': False,  # Finale segreto 1
            'secret_ending_2': False,  # Finale segreto 2
            'final_challenge_completed': False,  # Sfida finale al banchiere
        }
        self.load_game()

    def update_chips(self, amount):
        # Se è una vincita e c'è un prestito attivo, dimezza la vincita
        if amount > 0 and self.has_loan:
            amount = amount // 2
            console.print("[red]Il prestito oscuro dimezza la tua vincita...[/red]")

        self.chips += amount

        # Gestione prestito
        if self.has_loan and self.chips >= self.loan:
            if Prompt.ask("\n[yellow]Vuoi restituire il prestito oscuro?[/yellow]", choices=["s", "n"]) == "s":
                self.chips -= self.loan
                self.has_loan = False
                self.loan = 0
                console.print("\n[green]Hai restituito il prestito oscuro![/green]")
                console.print("[yellow]Il Banchiere sorride... 'Sei libero... per ora.'[/yellow]")

        if self.chips <= 0:
            console.print("\n[red]Hai perso tutte le tue fiches...[/red]")
            console.print("[red]Gli occhi del Banchiere brillano di soddisfazione maligna...[/red]")
            console.print("[red]'La tua anima è mia ora...'[/red]")
            time.sleep(3)
            sys.exit()

        # Check per finali speciali e sfide
        if self.chips >= 1000000 and not self.special_endings['final_challenge_completed']:
            console.print("\n[red]Il Banchiere si alza lentamente dal suo trono...[/red]")
            time.sleep(2)
            console.print("\n[red]'Un milione di fiches... Dopo 777 anni, finalmente un degno avversario.'[/red]")
            time.sleep(2)
            console.print("\n[yellow]L'aria si fa pesante, le luci del casinò tremolano...[/yellow]")
            time.sleep(2)
            console.print("\n[red]'Ti sfido a una partita finale. 30 mani di poker. La tua libertà contro la mia eternità.'[/red]")
            return "final_challenge_available"
        elif self.chips == 777777 and not self.special_endings['secret_ending_1']:
            self.special_endings['secret_ending_1'] = True
            console.print("\n[yellow]Il Banchiere sussulta... qualcosa di antico si risveglia...[/yellow]")
            time.sleep(2)
            console.print("\n[red]'777777... Il numero perfetto...'[/red]")
            time.sleep(2)
            console.print("\n[yellow]Una luce dorata avvolge la stanza...[/yellow]")
            time.sleep(2)
            console.print("\n[green]✨ HAI SCOPERTO IL PRIMO FINALE SEGRETO! ✨[/green]")
            console.print("\n[yellow]Il Level 777 si piega alla tua volontà. Sei diventato parte di esso.[/yellow]")
            self.chips *= 7  # Bonus divino
            return "secret_ending_1"
        elif self.chips == 666666 and not self.special_endings['secret_ending_2']:
            self.special_endings['secret_ending_2'] = True
            console.print("\n[red]Le ombre del Level 777 tremano... hai scoperto qualcosa che non dovevi...[/red]")
            time.sleep(2)
            console.print("\n[red]'666666... Il numero del caos...'[/red]")
            time.sleep(2)
            console.print("\n[red]Le luci del casinò diventano cremisi, le ombre danzano sulle pareti...[/red]")
            time.sleep(2)
            console.print("\n[green]✨ HAI SCOPERTO IL SECONDO FINALE SEGRETO! ✨[/green]")
            console.print("\n[red]Il Level 777 si contorce nel caos. Hai ottenuto un potere oscuro.[/red]")
            self.chips = self.chips * 6 // 7  # Maledizione del caos
            return "secret_ending_2"
        elif self.chips >= 77777 and not self.special_endings['banker_defeated']:
            console.print("\n[yellow]Il Banchiere alza un sopracciglio...[/yellow]")
            console.print("[yellow]'Interessante... Forse vorresti tentare la sorte contro di me direttamente?'[/yellow]")
            return "challenge_available"
        return None

    def save_game(self):
        try:
            save_data = {
                'chips': self.chips,
                'has_loan': self.has_loan,
                'loan': self.loan,
                'special_endings': self.special_endings
            }
            with open('level777_save.dat', 'wb') as f:
                pickle.dump(save_data, f)
            console.print("[green]Partita salvata con successo![/green]")
        except Exception as e:
            console.print("[red]Errore nel salvataggio della partita[/red]")

    def load_game(self):
        try:
            if os.path.exists('level777_save.dat'):
                with open('level777_save.dat', 'rb') as f:
                    save_data = pickle.load(f)
                    self.chips = save_data.get('chips', 777)
                    self.has_loan = save_data.get('has_loan', False)
                    self.loan = save_data.get('loan', 0)
                    self.special_endings = save_data.get('special_endings', {
                        'banker_defeated': False,
                        'membership_accepted': False,
                        'membership_rejected': False,
                        'secret_ending_1': False,
                        'secret_ending_2': False,
                        'final_challenge_completed': False
                    })
        except Exception as e:
            console.print("[red]Errore nel caricamento del salvataggio[/red]")