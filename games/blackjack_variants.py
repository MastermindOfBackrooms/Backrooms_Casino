from rich.console import Console
from rich.prompt import Prompt
from rich.progress import Progress
import random
import time

console = Console()

def create_deck():
    suits = ['♥️', '♦️', '♣️', '♠️']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    return [(rank, suit) for suit in suits for rank in ranks]

def card_value(card):
    rank = card[0]
    if rank in ['K', 'Q', 'J']:
        return 10
    elif rank == 'A':
        return 11
    return int(rank)

def hand_value(hand):
    value = 0
    aces = 0
    
    for card in hand:
        if card[0] == 'A':
            aces += 1
        else:
            value += card_value(card)
    
    for _ in range(aces):
        if value + 11 <= 21:
            value += 11
        else:
            value += 1
    
    return value

def display_hand(hand, hide_first=False):
    cards = []
    for i, (rank, suit) in enumerate(hand):
        if i == 0 and hide_first:
            cards.append('[red]?? ?[/red]')
        else:
            cards.append(f'[white]{rank}{suit}[/white]')
    return ' '.join(cards)

def dramatic_card_deal(card, is_dealer=False):
    console.print("\n[cyan]Distribuzione carta...[/cyan]")
    with Progress() as progress:
        task = progress.add_task("[cyan]", total=100)
        while not progress.finished:
            progress.update(task, advance=2)
            time.sleep(0.01)

    prefix = "[red]Il Banchiere[/red]" if is_dealer else "[cyan]Tu[/cyan]"
    rank, suit = card
    console.print(f"{prefix} ricevi: [white]{rank}{suit}[/white]")
    time.sleep(0.5)

def play_spanish21(state, banker):
    deck = create_deck()
    # Rimuovi tutti i 10 dal mazzo (caratteristica dello Spanish 21)
    deck = [(r, s) for r, s in deck if r != '10']
    random.shuffle(deck)
    
    banker.game_taunt('blackjack')
    
    while True:
        console.print("\n[green]===== SPANISH 21 =====[/green]")
        console.print(f"[yellow]Le tue fiches: {state.chips}[/yellow]")
        
        bet = Prompt.ask("Inserisci la tua puntata", default="100")
        try:
            bet = int(bet)
            if bet > state.chips:
                console.print("[red]Non hai abbastanza fiches![/red]")
                continue
        except ValueError:
            console.print("[red]Puntata non valida![/red]")
            continue

        player_hand = []
        dealer_hand = []

        # Distribuzione iniziale
        for _ in range(2):
            card = deck.pop()
            dramatic_card_deal(card)
            player_hand.append(card)

            card = deck.pop()
            dramatic_card_deal(card, is_dealer=True)
            dealer_hand.append(card)

        while True:
            console.print("\n[purple]Mano del Banchiere:[/purple]", display_hand(dealer_hand, hide_first=True))
            console.print("[cyan]La tua mano:[/cyan]", display_hand(player_hand))

            player_value = hand_value(player_hand)
            if player_value == 21:
                console.print("[green]Spanish 21![/green]")
                banker.win_response('big_win')
                state.update_chips(int(bet * 1.5))
                break
            elif player_value > 21:
                console.print("[red]Sballato![/red]")
                banker.lose_response('big_loss')
                state.update_chips(-bet)
                break

            action = Prompt.ask("Cosa vuoi fare", choices=["carta", "stai", "raddoppia"])
            
            if action == "carta":
                card = deck.pop()
                dramatic_card_deal(card)
                player_hand.append(card)
            elif action == "raddoppia":
                if len(player_hand) == 2 and bet <= state.chips:
                    bet *= 2
                    card = deck.pop()
                    dramatic_card_deal(card)
                    player_hand.append(card)
                    break
                else:
                    console.print("[red]Non puoi raddoppiare![/red]")
                    continue
            else:
                break

        if player_value <= 21:
            console.print("\n[purple]Mano del Banchiere:[/purple]", display_hand(dealer_hand))
            while hand_value(dealer_hand) < 17:
                card = deck.pop()
                dramatic_card_deal(card, is_dealer=True)
                dealer_hand.append(card)

            dealer_value = hand_value(dealer_hand)
            if dealer_value > 21:
                console.print("[green]Il Banchiere ha sballato! Hai vinto![/green]")
                banker.win_response()
                state.update_chips(bet)
            elif dealer_value > player_value:
                console.print("[red]Il Banchiere vince![/red]")
                banker.lose_response()
                state.update_chips(-bet)
            elif dealer_value < player_value:
                console.print("[green]Hai vinto![/green]")
                banker.win_response()
                state.update_chips(bet)
            else:
                console.print("[yellow]Pareggio![/yellow]")

        if not Prompt.ask("\nVuoi giocare ancora?", choices=["s", "n"]) == "s":
            break

    state.save_game()

def play_double_exposure(state, banker):
    deck = create_deck()
    random.shuffle(deck)
    
    banker.game_taunt('blackjack')
    
    while True:
        console.print("\n[green]===== DOUBLE EXPOSURE BLACKJACK =====[/green]")
        console.print("[yellow]Particolare: Entrambe le carte del Banchiere sono visibili![/yellow]")
        console.print(f"[yellow]Le tue fiches: {state.chips}[/yellow]")
        
        bet = Prompt.ask("Inserisci la tua puntata", default="100")
        try:
            bet = int(bet)
            if bet > state.chips:
                console.print("[red]Non hai abbastanza fiches![/red]")
                continue
        except ValueError:
            console.print("[red]Puntata non valida![/red]")
            continue

        player_hand = []
        dealer_hand = []

        # Distribuzione iniziale
        for _ in range(2):
            card = deck.pop()
            dramatic_card_deal(card)
            player_hand.append(card)

            card = deck.pop()
            dramatic_card_deal(card, is_dealer=True)
            dealer_hand.append(card)

        while True:
            # Mostra entrambe le carte del dealer
            console.print("\n[purple]Mano del Banchiere:[/purple]", display_hand(dealer_hand))
            console.print("[cyan]La tua mano:[/cyan]", display_hand(player_hand))

            player_value = hand_value(player_hand)
            if player_value == 21:
                console.print("[green]Blackjack![/green]")
                banker.win_response('big_win')
                state.update_chips(bet)  # Paga solo 1:1 nel Double Exposure
                break
            elif player_value > 21:
                console.print("[red]Sballato![/red]")
                banker.lose_response('big_loss')
                state.update_chips(-bet)
                break

            action = Prompt.ask("Cosa vuoi fare", choices=["carta", "stai"])
            
            if action == "carta":
                card = deck.pop()
                dramatic_card_deal(card)
                player_hand.append(card)
            else:
                break

        if player_value <= 21:
            while hand_value(dealer_hand) < 17:
                card = deck.pop()
                dramatic_card_deal(card, is_dealer=True)
                dealer_hand.append(card)
                console.print("[purple]Mano del Banchiere:[/purple]", display_hand(dealer_hand))

            dealer_value = hand_value(dealer_hand)
            if dealer_value > 21:
                console.print("[green]Il Banchiere ha sballato! Hai vinto![/green]")
                banker.win_response()
                state.update_chips(bet)
            elif dealer_value > player_value:
                console.print("[red]Il Banchiere vince![/red]")
                banker.lose_response()
                state.update_chips(-bet)
            elif dealer_value < player_value:
                console.print("[green]Hai vinto![/green]")
                banker.win_response()
                state.update_chips(bet)
            else:
                console.print("[red]Il Banchiere vince i pareggi![/red]")
                banker.lose_response()
                state.update_chips(-bet)

        if not Prompt.ask("\nVuoi giocare ancora?", choices=["s", "n"]) == "s":
            break

    state.save_game()
