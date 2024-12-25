from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
import random
import time

console = Console()

# Achievement del Craps
CRAPS_ACHIEVEMENTS = {
    "seventh_heaven": "Completa Seven's Heaven 7 volte",
    "devils_dancer": "Vinci la Seven Devils' Dance con 7 vittorie consecutive",
    "prophecy_master": "Indovina 7 Seven's Prophecy consecutive",
    "banker_doom": "Sconfiggi il Banker's Doom 3 volte",
    "craps_legend": "Sblocca tutti gli achievement dei dadi nel Craps"
}

def roll_dice(num_dice=2):
    """
    Genera il lancio dei dadi e restituisce una lista di risultati
    """
    dice_results = [random.randint(1, 6) for _ in range(num_dice)]
    if hasattr(roll_dice, 'consecutive_sevens'):
        if sum(dice_results) == 7:
            roll_dice.consecutive_sevens += 1
        else:
            roll_dice.consecutive_sevens = 0
    else:
        roll_dice.consecutive_sevens = 1 if sum(dice_results) == 7 else 0

    return dice_results

def check_craps_achievement(state, achievement_type, progress=1):
    """
    Verifica e aggiorna gli achievement del giocatore nel Craps
    """
    if not hasattr(state, 'craps_achievements'):
        state.craps_achievements = {}

    if achievement_type not in state.craps_achievements:
        state.craps_achievements[achievement_type] = 0

    state.craps_achievements[achievement_type] += progress

    # Verifica se l'achievement è stato completato
    if achievement_type == "seventh_heaven" and state.craps_achievements[achievement_type] >= 7:
        console.print("[green]Achievement Sbloccato: Seventh Heaven Master![/green]")
        state.chips += 7777
        return True
    elif achievement_type == "devils_dancer" and state.craps_achievements[achievement_type] >= 7:
        console.print("[green]Achievement Sbloccato: Master of the Devils' Dance![/green]")
        state.chips += 17777
        return True
    elif achievement_type == "prophecy_master" and state.craps_achievements[achievement_type] >= 7:
        console.print("[green]Achievement Sbloccato: Prophet of the Sevens![/green]")
        state.chips += 27777
        return True
    elif achievement_type == "banker_doom" and state.craps_achievements[achievement_type] >= 3:
        console.print("[green]Achievement Sbloccato: Doom Bringer![/green]")
        state.chips += 77777
        return True

    # Verifica se tutti gli achievement sono stati sbloccati
    if all(state.craps_achievements.get(ach, 0) >= required for ach, required in
           [("seventh_heaven", 7), ("devils_dancer", 7), ("prophecy_master", 7),
            ("banker_doom", 3)]):
        console.print("[gold]Achievement Supremo Sbloccato: Craps Legend![/gold]")
        state.chips += 777777  # Bonus leggendario
        return True

    return False

def check_come_out_roll(total):
    if total in [7, 11]:
        return "win"
    elif total in [2, 3, 12]:
        return "lose"
    return "point"

def show_betting_options(point=None, chips=0):
    table = Table(title="Opzioni di Scommessa")
    table.add_column("Tipo", style="cyan")
    table.add_column("Descrizione", style="green")
    table.add_column("Pagamento", style="yellow")

    if point is None:
        table.add_row("1", "Pass Line", "1:1")
        table.add_row("2", "Don't Pass", "1:1")
        table.add_row("3", "Lucky 7 (Somma 7)", "7:1")
    else:
        table.add_row("1", f"Point è {point}", "1:1")
        table.add_row("2", "Field (2,3,4,9,10,11,12)", "1:1, 2:1 per 2/12")
        table.add_row("3", "Any Craps (2,3,12)", "7:1")

    console.print(table)

def animate_roll(banker, special_roll=False):
    if special_roll:
        console.print("\n[red]I dadi brillano di un'aura mistica...[/red]")
        time.sleep(1.5)
        banker.special_message("777_ritual")
    else:
        console.print("\n[cyan]I dadi danzano nell'aria...[/cyan]")
        time.sleep(1)
    banker.game_taunt('craps')
    time.sleep(1)

def check_special_777_events(dice_results, bet_amount, state, banker):
    """Verifica e gestisce eventi speciali legati al 777"""
    total = sum(dice_results)

    # Evento: Triple Seven's Path (3 lanci consecutivi che sommano 7)
    if total == 7:
        if not hasattr(state, 'seven_streak'):
            state.seven_streak = 1
        else:
            state.seven_streak += 1

        if state.seven_streak == 3:
            console.print("\n[red]✧･ﾟ TRIPLE SEVEN'S PATH COMPLETATO! ･ﾟ✧[/red]")
            bonus = bet_amount * 777
            state.chips += bonus
            check_craps_achievement(state, "seventh_heaven")
            banker.special_message("777_ritual")
            state.seven_streak = 0  # Reset dopo il bonus
            return True
    else:
        if hasattr(state, 'seven_streak'):
            state.seven_streak = 0

    # Evento: Seven's Resonance (due dadi uguali che sommano con l'altro a 7)
    if dice_results[0] == dice_results[1] and total == 7:
        console.print("\n[red]✧･ﾟ SEVEN'S RESONANCE! ･ﾟ✧[/red]")
        bonus = bet_amount * 77
        state.chips += bonus
        banker.special_message("777_ritual")
        return True

    # Evento: Mystic Seven (somma dei dadi è un multiplo di 7)
    if total % 7 == 0:
        console.print("\n[red]✧･ﾟ MYSTIC SEVEN! ･ﾟ✧[/red]")
        multiplier = (total // 7) * 7  # Il moltiplicatore aumenta con i multipli di 7
        bonus = bet_amount * multiplier
        state.chips += bonus
        banker.special_message("777_ritual")
        return True

    # Evento: Seven's Prophecy (previsione del prossimo lancio)
    if not hasattr(state, 'prophecy_active'):
        state.prophecy_active = False
        state.prophecy_target = None

    if not state.prophecy_active and random.random() < 0.07:  # 7% di probabilità
        state.prophecy_active = True
        state.prophecy_target = 7
        console.print("\n[yellow]Il Banchiere sussurra: 'Il prossimo lancio porterà il numero sacro...'[/yellow]")
    elif state.prophecy_active:
        if total == state.prophecy_target:
            console.print("\n[red]✧･ﾟ LA PROFEZIA SI AVVERA! ･ﾟ✧[/red]")
            bonus = bet_amount * 77
            state.chips += bonus
            check_craps_achievement(state, "prophecy_master")
            banker.special_message("777_ritual")
        state.prophecy_active = False
        state.prophecy_target = None

    return False

def play(state, banker):
    while True:
        console.print("\n[yellow]♠ CRAPS - Il Gioco dei Dadi ♠[/yellow]")
        console.print(f"\nLe tue fiches: {state.chips}")

        if state.chips <= 0:
            console.print("[red]Non hai abbastanza fiches per giocare![/red]")
            return

        point = None
        show_betting_options(point, state.chips)

        bet_type = Prompt.ask("Scegli il tipo di scommessa", choices=["1", "2", "3", "E"])
        if bet_type == "E":
            break

        bet_amount = int(Prompt.ask("Quanto vuoi scommettere?", default="10"))
        while bet_amount > state.chips or bet_amount <= 0:
            console.print("[red]Scommessa non valida![/red]")
            bet_amount = int(Prompt.ask("Quanto vuoi scommettere?", default="10"))

        state.chips -= bet_amount

        # Prima fase: Come Out roll
        console.print("\n[cyan]Come Out Roll[/cyan]")
        dice = roll_dice()
        animate_roll(banker, special_roll=roll_dice.consecutive_sevens >= 2)
        total = sum(dice)
        console.print(f"Dadi: {dice} (Totale: {total})")

        # Verifica eventi speciali 777
        special_event = check_special_777_events(dice, bet_amount, state, banker)
        if special_event:
            time.sleep(2)  # Pausa per l'effetto drammatico

        result = check_come_out_roll(total)

        if result == "win" and bet_type == "1" or result == "lose" and bet_type == "2":
            winnings = bet_amount * 2
            state.chips += winnings
            console.print(f"[green]Hai vinto {winnings} fiches![/green]")
            won = True
        elif result == "lose" and bet_type == "1" or result == "win" and bet_type == "2":
            console.print("[red]Hai perso![/red]")
        else:
            point = total
            console.print(f"\n[yellow]Point è {point}[/yellow]")

            while True:
                show_betting_options(point, state.chips)
                bet_choice = Prompt.ask("Vuoi fare una scommessa aggiuntiva?", choices=["1", "2", "3", "N"])

                if bet_choice == "N":
                    break

                side_bet = int(Prompt.ask("Quanto vuoi scommettere?", default="5"))
                while side_bet > state.chips or side_bet <= 0:
                    console.print("[red]Scommessa non valida![/red]")
                    side_bet = int(Prompt.ask("Quanto vuoi scommettere?", default="5"))

                state.chips -= side_bet
                dice = roll_dice()
                total = sum(dice)
                console.print(f"\nDadi: {dice} (Totale: {total})")

                # Verifica eventi speciali 777 per le scommesse aggiuntive
                special_event = check_special_777_events(dice, side_bet, state, banker)
                if special_event:
                    time.sleep(2)  # Pausa per l'effetto drammatico

                if bet_choice == "2" and total in [2, 3, 4, 9, 10, 11, 12]:
                    multiplier = 2 if total in [2, 12] else 1
                    winnings = side_bet * (multiplier + 1)
                    state.chips += winnings
                    console.print(f"[green]Hai vinto {winnings} fiches sulla scommessa Field![/green]")
                    won = True
                elif bet_choice == "3" and total in [2, 3, 12]:
                    winnings = side_bet * 8
                    state.chips += winnings
                    console.print(f"[green]Hai vinto {winnings} fiches su Any Craps![/green]")
                    won = True
                else:
                    console.print("[red]Hai perso la scommessa aggiuntiva![/red]")

                if total == point:
                    if bet_type == "1":
                        winnings = bet_amount * 2
                        state.chips += winnings
                        console.print(f"[green]Hai vinto {winnings} fiches sulla scommessa principale![/green]")
                        won = True
                    break
                elif total == 7:
                    if bet_type == "2":
                        winnings = bet_amount * 2
                        state.chips += winnings
                        console.print(f"[green]Hai vinto {winnings} fiches sulla scommessa principale![/green]")
                        won = True
                    break

        if state.chips <= 0:
            console.print("[red]Hai finito le fiches![/red]")
            break

        if not Prompt.ask("\nVuoi continuare a giocare?", choices=["s", "n"]) == "s":
            break