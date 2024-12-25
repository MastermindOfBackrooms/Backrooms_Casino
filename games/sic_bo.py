from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
import random

console = Console()

# Lista degli achievement disponibili
ACHIEVEMENTS = {
    "seven_master": "Ottieni 7 vittorie consecutive con somma 7",
    "mystic_prophet": "Indovina 3 profezie del sette consecutive",
    "triple_seven": "Ottieni il Triple Seven's Curse 3 volte",
    "lucky_777": "Vinci con il Lucky 777 5 volte",
    "seventh_seal_master": "Completa il Seventh Seal 7 volte",
    "dice_philosopher": "Sblocca tutti gli achievement dei dadi"
}

def roll_dice(num_dice=3):
    """
    Genera il lancio dei dadi e restituisce una lista di risultati
    """
    return [random.randint(1, 6) for _ in range(num_dice)]

def check_achievement(state, achievement_type, progress=1):
    """
    Verifica e aggiorna gli achievement del giocatore
    """
    if not hasattr(state, 'achievements'):
        state.achievements = {}

    if achievement_type not in state.achievements:
        state.achievements[achievement_type] = 0

    state.achievements[achievement_type] += progress

    # Verifica se l'achievement è stato completato
    if achievement_type == "seven_master" and state.achievements[achievement_type] >= 7:
        console.print("[green]Achievement Sbloccato: Seven Master![/green]")
        state.chips += 777  # Bonus per l'achievement
        return True
    elif achievement_type == "mystic_prophet" and state.achievements[achievement_type] >= 3:
        console.print("[green]Achievement Sbloccato: Mystic Prophet![/green]")
        state.chips += 1777  # Bonus per l'achievement
        return True
    elif achievement_type == "triple_seven" and state.achievements[achievement_type] >= 3:
        console.print("[green]Achievement Sbloccato: Triple Seven Master![/green]")
        state.chips += 2777  # Bonus per l'achievement
        return True
    elif achievement_type == "lucky_777" and state.achievements[achievement_type] >= 5:
        console.print("[green]Achievement Sbloccato: Lucky 777 Master![/green]")
        state.chips += 7777  # Bonus per l'achievement
        return True
    elif achievement_type == "seventh_seal_master" and state.achievements[achievement_type] >= 7:
        console.print("[green]Achievement Sbloccato: Seventh Seal Master![/green]")
        state.chips += 17777  # Bonus per l'achievement
        return True

    # Verifica se tutti gli achievement sono stati sbloccati
    if all(state.achievements.get(ach, 0) >= required for ach, required in
           [("seven_master", 7), ("mystic_prophet", 3), ("triple_seven", 3),
            ("lucky_777", 5), ("seventh_seal_master", 7)]):
        console.print("[gold]Achievement Supremo Sbloccato: Dice Philosopher![/gold]")
        state.chips += 77777  # Bonus supremo
        return True

    return False

def check_win(state, bet_type, bet_number, dice, bet_amount):
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
        if total % 7 == 0:
            check_achievement(state, "seven_master")
            return True, bet_amount * 7
        return False, 0
    elif bet_type == "triple_seven":
        same_number = all(d == dice[0] for d in dice)
        if same_number and total % 7 == 0:
            check_achievement(state, "triple_seven")
            return True, bet_amount * 77
        return False, 0
    elif bet_type == "mystic_sequence":
        sorted_dice = sorted(dice)
        is_sequence = all(sorted_dice[i] + 1 == sorted_dice[i+1] for i in range(len(sorted_dice)-1))
        return is_sequence, bet_amount * 17
    elif bet_type == "seventh_seal":
        if total in [7, 17, 27]:
            check_achievement(state, "seventh_seal_master")
            return True, bet_amount * 27
        return False, 0
    elif bet_type == "lucky_777":
        product = dice[0] * dice[1] * dice[2]
        if product == 777:
            check_achievement(state, "lucky_777")
            return True, bet_amount * 777
        return False, 0
    elif bet_type == "sevens_prophecy":
        next_rolls = [random.randint(1,6) for _ in range(3)]
        next_total = sum(next_rolls)
        if next_total % 7 == 0:
            check_achievement(state, "mystic_prophet")
            return True, bet_amount * 7
        return False, 0

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
        dice_results = roll_dice()

        # Evento speciale: Somma 21 (7+7+7)
        if sum(dice_results) == 21:
            console.print("\n[red]🎲 TRIPLICE POTERE DEL SETTE! Le luci tremolano...[/red]")
            banker.game_taunt('sic_bo')
            banker.win_response('seven_related')
            bonus = bet_amount * 21
            state.chips += bonus
            console.print(f"[green]Bonus del potere: +{bonus} fiches![/green]")

        # Evento speciale: Sequenza con 7
        if sorted(dice_results) == [6, 7, 8]:
            console.print("\n[red]🌟 SEQUENZA DEL SETTIMO SIGILLO! Il tempo rallenta...[/red]")
            banker.game_taunt('sic_bo')
            banker.win_response('mystic_sequence')
            bonus = bet_amount * 77
            state.chips += bonus
            console.print(f"[green]Bonus mistico: +{bonus} fiches![/green]")

        # Evento speciale: Prodotto multiplo di 777
        product = dice_results[0] * dice_results[1] * dice_results[2]
        if product % 777 == 0:
            console.print("\n[red]💫 RISONANZA DEL 777! Le Backrooms sussurrano...[/red]")
            banker.game_taunt('sic_bo')
            banker.win_response('seven_related')
            bonus = int(bet_amount * 7.77)
            state.chips += bonus
            console.print(f"[green]Bonus della risonanza: +{bonus} fiches![/green]")

        # Evento speciale: Tutti i dadi uguali a 7 (se possibile nel gioco)
        if all(d == 7 for d in dice_results):
            console.print("\n[red]✨ MANIFESTAZIONE DEL 777! Il Level 777 risponde...[/red]")
            banker.game_taunt('sic_bo')
            banker.win_response('seven_related')
            bonus = bet_amount * 777
            state.chips += bonus
            console.print(f"[green]Bonus della manifestazione: +{bonus} fiches![/green]")

        console.print(f"\n[cyan]I dadi mostrano: {dice_results}[/cyan]")
        console.print(f"Somma totale: {sum(dice_results)}")

        won, winnings = check_win(state, bet_type, bet_number, dice_results, bet_amount)

        if won:
            state.chips += int(winnings)
            console.print(f"[green]Hai vinto {int(winnings)} fiches![/green]")
            if sum(dice_results) % 7 == 0:
                banker.win_response('seven_related')
            else:
                banker.win_response('normal')
        else:
            console.print("[red]Hai perso![/red]")
            banker.lose_response('normal')

        if state.chips <= 0:
            console.print("[red]Hai finito le fiches![/red]")
            banker.lose_response('bankruptcy')
            break

        if not Prompt.ask("\nVuoi continuare a giocare?", choices=["s", "n"]) == "s":
            break