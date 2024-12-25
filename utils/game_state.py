import pickle
import os
from rich.console import Console
from rich.prompt import Prompt
import sys
import time

console = Console()

class GameState:
    def __init__(self):
        self.chips = 777  # Starting chips
        self.has_loan = False
        self.loan = 0
        self.loan_repayment_rate = 0  # Tasso di restituzione del prestito
        self.original_loan = 0  # Ammontare originale del prestito
        self.loan_is_active = False  # Flag per prestito attivo
        self.played_chips = 0  # Fiches giocate con il prestito corrente
        self.loan_tier = 0  # Fascia di prestito corrente (1-6)
        self.loan_amounts = [1000, 5000, 10000, 50000, 100000, 500000]  # Sei fasce di prestito
        self.loan_maluses = [0.5, 0.6, 0.7, 0.8, 0.9, 0.95]  # Malus crescenti
        self.load_game()

    def update_chips(self, amount):
        if amount > 0:  # Se è una vincita
            if self.has_loan:
                # Metà della vincita va al banchiere come ripagamento del prestito
                banker_cut = int(amount * self.loan_maluses[self.loan_tier - 1])
                actual_amount = amount - banker_cut
                console.print(f"[red]Il Banchiere prende {banker_cut} fiches dalla tua vincita...[/red]")
                amount = actual_amount

        # Aggiorna il conteggio delle fiches giocate se c'è un prestito attivo
        if self.has_loan and not self.loan_is_active:
            self.played_chips += abs(amount)
            if self.played_chips >= self.original_loan:
                self.loan_is_active = True
                console.print("[yellow]Hai giocato l'intero ammontare del prestito.[/yellow]")

        self.chips += amount

        # Gestione prestito
        if self.has_loan and self.chips >= self.original_loan:
            if Prompt.ask("\n[yellow]Vuoi restituire il prestito oscuro?[/yellow]", choices=["s", "n"]) == "s":
                self.chips -= self.original_loan
                self.reset_loan()
                console.print("\n[green]Hai restituito il prestito oscuro![/green]")
                console.print("[yellow]Il Banchiere sorride... 'Sei libero... per ora.'[/yellow]")

        if self.chips <= 0:
            console.print("\n[red]Hai perso tutte le tue fiches...[/red]")
            console.print("[red]Gli occhi del Banchiere brillano di soddisfazione maligna...[/red]")
            console.print("[red]'La tua anima è mia ora...'[/red]")
            time.sleep(3)
            sys.exit()

    def reset_loan(self):
        """Resetta tutti i parametri del prestito"""
        self.has_loan = False
        self.loan = 0
        self.loan_repayment_rate = 0
        self.original_loan = 0
        self.loan_is_active = False
        self.played_chips = 0
        self.loan_tier = 0

    def save_game(self):
        try:
            save_data = {
                'chips': self.chips,
                'has_loan': self.has_loan,
                'loan': self.loan,
                'loan_repayment_rate': self.loan_repayment_rate,
                'original_loan': self.original_loan,
                'loan_is_active': self.loan_is_active,
                'played_chips': self.played_chips,
                'loan_tier': self.loan_tier
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
                    self.loan_repayment_rate = save_data.get('loan_repayment_rate', 0)
                    self.original_loan = save_data.get('original_loan', 0)
                    self.loan_is_active = save_data.get('loan_is_active', False)
                    self.played_chips = save_data.get('played_chips', 0)
                    self.loan_tier = save_data.get('loan_tier', 0)
        except Exception as e:
            console.print("[red]Errore nel caricamento del salvataggio[/red]")