from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
from rich.panel import Panel
from rich.layout import Layout
import random
import time
from utils.survivor_ai import SurvivorAI, SURVIVORS

console = Console()

def create_deck():
    """Crea un mazzo di carte standard"""
    suits = ['♥️', '♦️', '♣️', '♠️']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    return [(rank, suit) for suit in suits for rank in ranks]

def display_hand(hand, hide_first=False):
    """Visualizza una mano di carte"""
    cards = []
    for i, (rank, suit) in enumerate(hand):
        # Modifica: nascondi la seconda carta invece della prima se hide_first è True
        if hide_first and i == 1:
            cards.append('[red]╔═════╗[/red]\n[red]║ ?? ║[/red]\n[red]╚═════╝[/red]')
        else:
            color = 'red' if suit in ['♥️', '♦️'] else 'white'
            cards.append(f'[{color}]╔═════╗[/{color}]\n[{color}]║ {rank}{suit} ║[/{color}]\n[{color}]╚═════╝[/{color}]')
    return '\n'.join(cards)

def dramatic_card_deal(card, player_name="", is_dealer=False, hide_card=False):
    """Distribuisce una carta con effetto drammatico"""
    console.print("\n[cyan]Distribuzione carta in corso...[/cyan]")
    time.sleep(1)
    prefix = "[red]Il Banchiere[/red]" if is_dealer else f"[cyan]{player_name}[/cyan]"

    if hide_card:
        console.print(f"\n{prefix} riceve una carta coperta.")
        time.sleep(0.5)
        console.print("[red]╔═════╗[/red]")
        time.sleep(0.3)
        console.print("[red]║ ?? ║[/red]")
        time.sleep(0.3)
        console.print("[red]╚═════╝[/red]")
        return

    # Se è il banchiere e non è una carta nascosta, mostra solo il valore della carta
    rank, suit = card
    color = 'red' if suit in ['♥️', '♦️'] else 'white'
    console.print(f"\n{prefix} riceve:")
    time.sleep(0.5)
    console.print(f"[{color}]╔═════╗[/{color}]")
    time.sleep(0.3)
    console.print(f"[{color}]║ {rank}{suit} ║[/{color}]")
    time.sleep(0.3)
    console.print(f"[{color}]╚═════╝[/{color}]")

def show_betting_table(survivors, active_bets=None):
    """Mostra una tabella con le opzioni di scommessa e le scommesse attive"""
    table = Table(
        title="[red]═══ TAVOLO DELLE SCOMMESSE DELLA RED ROOM ═══[/red]",
        show_lines=True,
        border_style="red",
        padding=(0, 1)
    )
    table.add_column("ID", justify="center", style="cyan", width=4)
    table.add_column("Nome", style="cyan", width=20)
    table.add_column("Personalità", style="yellow", width=40)
    table.add_column("Scommessa", justify="right", style="green", width=15)
    table.add_column("Status", style="magenta", width=15)

    active_bets = active_bets or {}  # Inizializza a dizionario vuoto se None
    total_bets = sum(active_bets.values())
    active_count = len(active_bets)
    table.caption = f"[yellow]Scommesse attive: {active_count}/5 | Totale puntato: {total_bets} fiches[/yellow]"

    for i, survivor in enumerate(survivors, 1):
        bet_amount = active_bets.get(i-1, "---")
        bet_style = "red" if bet_amount == "---" else "green"

        # Status della scommessa con simbolo
        status = "[green]✓ Scommessa Attiva[/green]" if bet_amount != "---" else "[yellow]↑ Disponibile[/yellow]"

        table.add_row(
            str(i),
            f"[bold cyan]{survivor.personality.name}[/bold cyan]",
            survivor.personality.story[:37] + "...",
            f"[{bet_style}]{'🎰 ' + str(bet_amount) if bet_amount != '---' else '---'}[/{bet_style}]",
            status
        )

    console.print("\n[yellow]Comandi Scommesse:[/yellow]")
    console.print("[cyan]B[/cyan] - Piazza una nuova scommessa")
    console.print("[cyan]R[/cyan] - Rimuovi una scommessa esistente")
    console.print("[cyan]S[/cyan] - [green]Inizia la partita[/green]")
    console.print("[cyan]I[/cyan] - Mostra questo menu")
    console.print(Panel(table, border_style="red", padding=(1, 2)))

def show_game_status(survivors, hands, dealer_hand=None, active_bets=None):
    """Mostra lo stato attuale del gioco con punteggi migliorati"""
    layout = Layout()
    active_bets = active_bets or {}

    if dealer_hand and len(dealer_hand) > 0:
        layout.split_column(
            Layout(name="dealer", size=15),
            Layout(name="players", size=35)
        )

        # Mostra il valore della prima carta del banchiere solo all'inizio
        dealer_value = SurvivorAI.get_card_value(dealer_hand[0])
        if len(dealer_hand) == 1:
            value_display = f" (Prima carta: {dealer_value})"
        elif len(dealer_hand) == 2:
            value_display = ""  # Seconda carta nascosta
        else:
            # Mostra il valore totale solo quando tutte le carte sono visibili
            total_value = SurvivorAI.calculate_hand_value(dealer_hand)
            value_display = f" (Totale: {total_value})"

        dealer_panel = Panel(
            display_hand(dealer_hand, hide_first=len(dealer_hand) == 2),
            title=f"[bold red]═══ IL BANCHIERE{value_display} ═══[/bold red]",
            border_style="red",
            padding=(1, 2)
        )
        layout["dealer"].update(dealer_panel)
    else:
        layout.split_column(
            Layout(name="players", size=50)
        )

    # Tabella dei giocatori con punteggi colorati
    players_table = Table(
        title="[bold red]═══ SOPRAVVISSUTI IN GIOCO ═══[/bold red]",
        show_lines=True,
        border_style="red",
        padding=(0, 1)
    )
    players_table.add_column("Nome", style="cyan", width=20)
    players_table.add_column("Mano", justify="center")
    players_table.add_column("Valore", justify="center", style="yellow", width=8)
    players_table.add_column("Scommessa", justify="right", style="green", width=12)

    for i, (survivor, hand) in enumerate(zip(survivors, hands)):
        hand_value = SurvivorAI.calculate_hand_value(hand) if hand else 0
        bet_amount = active_bets.get(i, "---")
        hand_display = display_hand(hand) if hand else "[dim]In attesa[/dim]"

        # Colorazione dei punteggi basata sul valore
        if hand_value == 0:
            value_style = "dim"
            value_display = "---"
        elif hand_value == 21:
            value_style = "yellow bold"
            value_display = "21 ⭐"
        elif hand_value > 21:
            value_style = "red bold"
            value_display = f"BUST ({hand_value})"
        else:
            value_style = "green"
            value_display = str(hand_value)

        # Formattazione punteggi e scommesse
        value_display = f"[{value_style}]{value_display}[/{value_style}]"
        bet_style = "green" if bet_amount != "---" else "dim"
        bet_display = f"[{bet_style}]{'🎰 ' + str(bet_amount) if bet_amount != '---' else '---'}[/{bet_style}]"

        players_table.add_row(
            f"[bold cyan]{survivor.personality.name}[/bold cyan]",
            hand_display,
            value_display,
            bet_display
        )

    layout["players"].update(Panel(players_table, border_style="red", padding=(1, 2)))
    console.print(layout)

def get_survivor_comment(survivor, action, hand_value=None):
    """Genera commenti personalizzati per ogni sopravvissuto"""
    if survivor.personality.name == "Il Veterano":
        if action == "hit":
            return "[cyan]'Ho visto questa situazione migliaia di volte...'[/cyan]"
        elif action == "stand":
            return "[cyan]'Il conteggio suggerisce di fermarsi qui.'[/cyan]"
    elif survivor.personality.name == "L'Impulsivo":
        if action == "hit":
            return "[cyan]'Il mio istinto mi dice di rischiare!'[/cyan]"
        elif action == "stand":
            return "[cyan]'Questa volta mi fermo... forse.'[/cyan]"
    elif survivor.personality.name == "Il Matematico":
        if action == "hit":
            return "[cyan]'La probabilità di successo è del 67.3%.'[/cyan]"
        elif action == "stand":
            return "[cyan]'Le variabili suggeriscono di mantenere questa mano.'[/cyan]"
    elif survivor.personality.name == "Il Fortunato":
        if action == "hit":
            return "[cyan]'Le carte... mi chiamano.'[/cyan]"
        elif action == "stand":
            return "[cyan]'Il destino mi sussurra di fermarmi.'[/cyan]"
    elif survivor.personality.name == "L'Osservatore":
        if action == "hit":
            return "[cyan]'...'[/cyan]"
        elif action == "stand":
            return "[cyan]*osserva intensamente le carte*[/cyan]"
    return ""

def play_red_room(state, banker):
    """Funzione principale della Red Room"""
    console.print(Panel.fit(
        "[red]╔═══════════════════════════════════════╗[/red]\n" +
        "[red]║          LA RED ROOM                  ║[/red]\n" +
        "[red]║  Dove i sopravvissuti sfidano        ║[/red]\n" +
        "[red]║  il destino e tu scommetti           ║[/red]\n" +
        "[red]║  sulle loro anime...                 ║[/red]\n" +
        "[red]╚═══════════════════════════════════════╝[/red]",
        border_style="red"
    ))

    time.sleep(2)
    banker.game_taunt('red_room')

    survivors = [SurvivorAI(personality) for personality in SURVIVORS]
    deck = create_deck() * 6  # 6 mazzi
    random.shuffle(deck)

    while True:
        if len(deck) < 52:
            deck = create_deck() * 6
            random.shuffle(deck)
            console.print("\n[red]Il Banchiere rimescola i mazzi...[/red]")
            banker.game_taunt('red_room')
            for survivor in survivors:
                survivor.card_count = 0

        # Inizializzazione della mano
        survivor_hands = [[] for _ in survivors]
        dealer_hand = []
        active_bets = {}  # Dizionario per tenere traccia delle scommesse attive

        console.print("\n[red]═══ Nuova mano nella Red Room ═══[/red]")
        show_game_status(survivors, survivor_hands)  # Non mostriamo il dealer all'inizio

        # Fase di scommesse
        while True:
            fiches_rimaste = state.chips
            total_bets = sum(active_bets.values()) if active_bets else 0
            console.print(f"\n[yellow]Le tue fiches: {fiches_rimaste} | Totale scommesso: {total_bets}[/yellow]")
            show_betting_table(survivors, active_bets)

            action = Prompt.ask(
                "\n[yellow]Cosa vuoi fare?[/yellow]",
                choices=["S", "B", "R", "I"],
                show_choices=False
            )

            if action == "S":  # Start
                if not active_bets:
                    console.print("\n[yellow]Non hai ancora piazzato scommesse. Vuoi davvero iniziare?[/yellow]")
                    if Prompt.ask("\n[yellow]Confermi di voler iniziare senza scommesse?[/yellow]", choices=["s", "n"]) == "s":
                        break
                else:
                    console.print(f"\n[green]Iniziamo con {len(active_bets)} scommesse attive per un totale di {total_bets} fiches![/green]")
                    time.sleep(2)
                    break
            elif action == "B":  # Bet
                if len(active_bets) >= 5:
                    console.print("[red]Hai raggiunto il limite massimo di 5 scommesse simultanee![/red]")
                    continue

                console.print("\n[cyan]═══ PIAZZAMENTO SCOMMESSA ═══[/cyan]")
                survivor_id = int(Prompt.ask("\n[yellow]Su quale sopravvissuto vuoi scommettere?[/yellow] (1-5)")) - 1

                if survivor_id < 0 or survivor_id >= len(survivors):
                    console.print("[red]Numero sopravvissuto non valido![/red]")
                    continue

                if survivor_id in active_bets:
                    console.print("[red]Hai già una scommessa attiva su questo sopravvissuto![/red]")
                    continue

                bet_amount = int(Prompt.ask("Quanto vuoi scommettere?", default="100"))
                if bet_amount > state.chips:
                    console.print(f"[red]Non hai abbastanza fiches! (Disponibili: {state.chips})[/red]")
                    continue
                if bet_amount <= 0:
                    console.print("[red]La scommessa deve essere positiva![/red]")
                    continue

                state.chips -= bet_amount
                active_bets[survivor_id] = bet_amount
                console.print(f"\n[green]✓ Scommessa di {bet_amount} fiches piazzata su {survivors[survivor_id].personality.name}[/green]")
                console.print(f"[yellow]Scommesse attive: {len(active_bets)}/5 | Totale: {sum(active_bets.values())} fiches[/yellow]")
                banker.bet_behind_response('follow')

            elif action == "R":  # Remove bet
                if not active_bets:
                    console.print("[red]Non hai ancora piazzato scommesse![/red]")
                    continue

                console.print("\n[cyan]═══ RIMOZIONE SCOMMESSA ═══[/cyan]")
                survivor_id = int(Prompt.ask("\n[yellow]Da quale sopravvissuto vuoi rimuovere la scommessa?[/yellow] (1-5)")) - 1

                if survivor_id < 0 or survivor_id >= len(survivors):
                    console.print("[red]Numero sopravvissuto non valido![/red]")
                    continue

                if survivor_id not in active_bets:
                    console.print("[red]Non hai scommesse attive su questo sopravvissuto![/red]")
                    continue

                removed_amount = active_bets[survivor_id]
                state.chips += removed_amount
                del active_bets[survivor_id]
                console.print(f"\n[yellow]✓ Rimossa scommessa di {removed_amount} fiches da {survivors[survivor_id].personality.name}[/yellow]")
                remaining_bets = sum(active_bets.values())
                console.print(f"[yellow]Scommesse attive: {len(active_bets)}/5 | Totale rimanente: {remaining_bets} fiches[/yellow]")

            else:  # Info
                console.print("\n[cyan]═══ GUIDA SCOMMESSE ═══[/cyan]")
                console.print("[yellow]• Puoi scommettere su più sopravvissuti (max 5)[/yellow]")
                console.print("[yellow]• Una sola scommessa per sopravvissuto[/yellow]")
                console.print("[yellow]• Usa i comandi B/R per gestire le scommesse[/yellow]")
                console.print("[yellow]• Premi S quando sei pronto per iniziare[/yellow]")
                continue

        # Distribuzione iniziale
        console.print("\n[red]Il Banchiere inizia a distribuire le carte con movimenti ipnotici...[/red]")
        time.sleep(3)
        banker.game_taunt('red_room')

        for _ in range(2):
            for i, survivor in enumerate(survivors):
                card = deck.pop()
                dramatic_card_deal(card, SURVIVORS[i].name)
                survivor_hands[i].append(card)
                survivor.count_cards(card)
                time.sleep(0.8)

            card = deck.pop()
            # Nascondi la seconda carta del dealer
            dramatic_card_deal(card, is_dealer=True, hide_card=True)
            dealer_hand.append(card)
            for survivor in survivors:
                survivor.count_cards(card)
            time.sleep(1)

        show_game_status(survivors, survivor_hands, dealer_hand, active_bets)

        # Turno dei sopravvissuti
        dealer_value = SurvivorAI.get_card_value(dealer_hand[1])

        for i, current_survivor in enumerate(survivors):
            console.print(f"\n[cyan]═══ Turno di {SURVIVORS[i].name} ═══[/cyan]")
            time.sleep(2)

            if i in active_bets:
                banker.bet_behind_response('follow')

            while True:
                hand_value = current_survivor.calculate_hand_value(survivor_hands[i])
                if hand_value > 21:
                    console.print("[red]Sballato![/red]")
                    if current_survivor.is_tilted:
                        console.print(f"[red]{SURVIVORS[i].name} mostra segni di tilt evidenti...[/red]")
                    if i in active_bets:
                        banker.bet_behind_response('loss')
                    time.sleep(2)
                    break

                action = current_survivor.decide_action(
                    survivor_hands[i],
                    dealer_hand[1],
                    can_split=False,
                    can_double=False
                )

                comment = get_survivor_comment(current_survivor, action, hand_value)
                console.print(comment)
                time.sleep(2)

                if action == 'stand':
                    console.print(f"[cyan]{SURVIVORS[i].name}[/cyan] decide di stare.")
                    time.sleep(1.5)
                    break
                elif action == 'hit':
                    console.print(f"[cyan]{SURVIVORS[i].name}[/cyan] chiede carta.")
                    time.sleep(1.5)
                    card = deck.pop()
                    dramatic_card_deal(card, SURVIVORS[i].name)
                    survivor_hands[i].append(card)
                    current_survivor.count_cards(card)
                    show_game_status(survivors, survivor_hands, dealer_hand, active_bets)

        # Turno del dealer
        console.print("\n[red]Il Banchiere rivela la sua mano nascosta...[/red]")
        time.sleep(3)
        banker.game_taunt('red_room')
        show_game_status(survivors, survivor_hands, dealer_hand, active_bets)

        dealer_value = SurvivorAI.calculate_hand_value(dealer_hand)
        while dealer_value < 17:
            console.print("\n[red]Il Banchiere deve pescare...[/red]")
            time.sleep(2)
            card = deck.pop()
            dramatic_card_deal(card, is_dealer=True)
            dealer_hand.append(card)
            dealer_value = SurvivorAI.calculate_hand_value(dealer_hand)
            for survivor in survivors:
                survivor.count_cards(card)
            show_game_status(survivors, survivor_hands, dealer_hand, active_bets)
            banker.game_taunt('red_room')

        # Determinazione vincitori con più suspense
        console.print("\n[red]═══ Momento del verdetto ═══[/red]")
        time.sleep(3)
        banker.game_taunt('red_room')

        total_winnings = 0
        winning_bets = []
        losing_bets = []

        for i, (current_survivor, hand) in enumerate(zip(survivors, survivor_hands)):
            if i not in active_bets:
                continue

            hand_value = current_survivor.calculate_hand_value(hand)
            bet_amount = active_bets[i]

            console.print(f"\n[cyan]Valutazione della mano di {current_survivor.personality.name}[/cyan]")
            time.sleep(1)

            if hand_value <= 21 and (dealer_value > 21 or hand_value > dealer_value):
                winnings = bet_amount * 2
                total_winnings += winnings - bet_amount  # Sottrai la puntata originale
                winning_bets.append((current_survivor.personality.name, winnings))
                console.print(f"[green]{current_survivor.personality.name} ha vinto con {hand_value}![/green]")
                banker.bet_behind_response('win')
            else:
                losing_bets.append((current_survivor.personality.name, bet_amount))
                console.print(f"[red]{current_survivor.personality.name} ha perso con {hand_value}.[/red]")
                banker.bet_behind_response('loss')

            time.sleep(1)
            current_survivor.update_tilt_status(hand_value <= 21 and (dealer_value > 21 or hand_value > dealer_value))
            if current_survivor.is_tilted:
                console.print(f"[red]{current_survivor.personality.name} mostra segni evidenti di tilt![/red]")
                time.sleep(1)

        # Riepilogo finale
        if winning_bets:
            console.print("\n[green]═══ Scommesse Vincenti ═══[/green]")
            for name, amount in winning_bets:
                console.print(f"[green]{name}: +{amount} fiches[/green]")

        if losing_bets:
            console.print("\n[red]═══ Scommesse Perdenti ═══[/red]")
            for name, amount in losing_bets:
                console.print(f"[red]{name}: -{amount} fiches[/red]")

        # Aggiorna le fiches del giocatore
        if total_winnings > 0:
            state.chips += total_winnings
            console.print(f"\n[green]Vincita totale: {total_winnings} fiches![/green]")
        elif total_winnings < 0:
            console.print(f"\n[red]Perdita totale: {abs(total_winnings)} fiches.[/red]")
        else:
            console.print("\n[yellow]Pareggio![/yellow]")

        if not Prompt.ask("\n[yellow]Vuoi giocare un'altra mano?[/yellow]", choices=["s", "n"]) == "s":
            break

    state.save_game()