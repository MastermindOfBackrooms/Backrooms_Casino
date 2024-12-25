from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
import random

console = Console()

def roll_dice(num_dice=3):
    return [random.randint(1, 6) for _ in range(num_dice)]

def check_win(bet_type, bet_number, dice, bet_amount):
    total = sum(dice)

    if bet_type == "small":
        return (total >= 4 and total <= 10, bet_amount * 1.5) if total != 3 else (False, 0)
    elif bet_type == "big":
        return (total >= 11 and total <= 17, bet_amount * 1.5) if total != 18 else (False, 0)
    elif bet_type == "specific":
        count = dice.count(bet_number)
        if count == 1:
            return True, bet_amount * 1
        elif count == 2:
            return True, bet_amount * 2
        elif count == 3:
            return True, bet_amount * 3
        return False, 0
    elif bet_type == "total":
        return total == bet_number, bet_amount * (get_total_payout(bet_number))
    elif bet_type == "lucky_seven":
        # Vinci se la somma è un multiplo di 7
        return total % 7 == 0, bet_amount * 7
    elif bet_type == "triple_seven":
        # Vinci se tutti i dadi mostrano lo stesso numero che sommato fa 7
        same_number = all(d == dice[0] for d in dice)
        return same_number and total % 7 == 0, bet_amount * 77
    elif bet_type == "mystic_sequence":
        # Nuova variante: sequenza mistica (1-2-3, 2-3-4, ecc.)
        sorted_dice = sorted(dice)
        is_sequence = all(sorted_dice[i] + 1 == sorted_dice[i+1] for i in range(len(sorted_dice)-1))
        return is_sequence, bet_amount * 17
    elif bet_type == "seventh_seal":
        # Nuova variante: il settimo sigillo (somma = 7 o 17 o 27)
        return total in [7, 17, 27], bet_amount * 27
    elif bet_type == "lucky_777":
        # Nuova variante: i dadi moltiplicati fanno 777
        product = dice[0] * dice[1] * dice[2]
        return product == 777, bet_amount * 777
    elif bet_type == "sevens_prophecy":
        # Nuova variante: i prossimi tre tiri sommano a un multiplo di 7
        next_rolls = [random.randint(1,6) for _ in range(3)]
        next_total = sum(next_rolls)
        return next_total % 7 == 0, bet_amount * 7
    elif bet_type == "mystical_triad":
        # Nuova variante: combinazioni speciali di tre numeri legati al 7
        sorted_dice = sorted(dice)
        special_patterns = [[1,3,3],[2,2,3],[1,2,4],[7,7,7]]
        return sorted_dice in special_patterns, bet_amount * 77

    return False, 0

def get_total_payout(total):
    payouts = {
        4: 60, 17: 60,
        5: 30, 16: 30,
        6: 17, 15: 17,
        7: 12, 14: 12,
        8: 8, 13: 8,
        9: 6, 12: 6,
        10: 6, 11: 6,
    }
    # Bonus speciale per il numero 7
    if total == 7:
        return payouts[7] * 7
    return payouts.get(total, 1)

def show_betting_options():
    table = Table(title="Opzioni di Scommessa")
    table.add_column("Tipo", style="cyan")
    table.add_column("Descrizione", style="green")
    table.add_column("Pagamento", style="yellow")

    table.add_row("1", "Piccolo (4-10)", "1.5x")
    table.add_row("2", "Grande (11-17)", "1.5x")
    table.add_row("3", "Numero Specifico (1-6)", "1x-3x")
    table.add_row("4", "Somma Totale (4-17)", "Varia")
    table.add_row("5", "Lucky Seven (Multipli di 7)", "7x")
    table.add_row("6", "Triple Seven (Tutti uguali = 7)", "77x")
    table.add_row("7", "Sequenza Mistica (123,234,etc)", "17x")
    table.add_row("8", "Settimo Sigillo (7,17,27)", "27x")
    table.add_row("9", "Lucky 777 (Prodotto = 777)", "777x")
    table.add_row("10", "Seven's Prophecy (Prossimi 3 tiri multiplo di 7)", "7x")
    table.add_row("11", "Triade Mistica (Combinazioni speciali del 7)", "77x")

    console.print(table)

def play(state, banker):
    while True:
        console.print("\n[yellow]♠ SIC BO - Il Gioco dei Tre Dadi ♠[/yellow]")
        console.print("\n[red]Level 777 Special Edition[/red]")
        console.print(f"\nLe tue fiches: {state.chips}")

        if state.chips <= 0:
            console.print("[red]Non hai abbastanza fiches per giocare![/red]")
            return

        show_betting_options()

        choice = Prompt.ask("Scegli il tipo di scommessa", choices=["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "E"])

        if choice == "E":
            break

        bet_amount = int(Prompt.ask("Quanto vuoi scommettere?", default="10"))
        while bet_amount > state.chips or bet_amount <= 0:
            console.print("[red]Scommessa non valida![/red]")
            bet_amount = int(Prompt.ask("Quanto vuoi scommettere?", default="10"))

        bet_type = ""
        bet_number = 0

        if choice == "1":
            bet_type = "small"
        elif choice == "2":
            bet_type = "big"
        elif choice == "3":
            bet_number = int(Prompt.ask("Scegli un numero (1-6)", choices=[str(i) for i in range(1, 7)]))
            bet_type = "specific"
        elif choice == "4":
            bet_number = int(Prompt.ask("Scegli la somma totale (4-17)", choices=[str(i) for i in range(4, 18)]))
            bet_type = "total"
        elif choice == "5":
            bet_type = "lucky_seven"
        elif choice == "6":
            bet_type = "triple_seven"
        elif choice == "7":
            bet_type = "mystic_sequence"
        elif choice == "8":
            bet_type = "seventh_seal"
        elif choice == "9":
            bet_type = "lucky_777"
        elif choice == "10":
            bet_type = "sevens_prophecy"
        elif choice == "11":
            bet_type = "mystical_triad"

        state.chips -= bet_amount
        dice = roll_dice()

        console.print(f"\n[cyan]I dadi mostrano: {dice}[/cyan]")
        console.print(f"Somma totale: {sum(dice)}")

        won, winnings = check_win(bet_type, bet_number, dice, bet_amount)

        if won:
            state.chips += int(winnings)
            console.print(f"[green]Hai vinto {int(winnings)} fiches![/green]")
            if sum(dice) % 7 == 0:
                banker.special_message("777")
                console.print("[yellow]Il Banchiere sorride... il 7 porta fortuna in questo livello![/yellow]")

            # Bonus speciale per sequenze mistiche, sigilli e nuove varianti
            if bet_type in ["mystic_sequence", "seventh_seal", "lucky_777", "sevens_prophecy", "mystical_triad"] and won:
                banker.special_message("777")
                console.print("[yellow]Il Banchiere sussurra... 'I segreti del Level 777 si svelano...'[/yellow]")
        else:
            console.print("[red]Hai perso![/red]")

        if state.chips <= 0:
            console.print("[red]Hai finito le fiches![/red]")
            break

        if not Prompt.ask("\nVuoi continuare a giocare?", choices=["s", "n"]) == "s":
            break