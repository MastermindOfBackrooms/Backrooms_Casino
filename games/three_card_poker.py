"""
Poker a 3 Carte - Variante del Level 777
"""
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
import random
import time

console = Console()

def create_deck():
    """Crea un mazzo di carte"""
    suits = ['♥️', '♦️', '♣️', '♠️']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    return [(rank, suit) for suit in suits for rank in ranks]

def get_card_value(card):
    """Ottiene il valore di una carta"""
    rank = card[0]
    if rank == 'A':
        return 14
    elif rank in ['K', 'Q', 'J']:
        return {'K': 13, 'Q': 12, 'J': 11}[rank]
    return int(rank)

def evaluate_hand(hand):
    """Valuta una mano di poker a 3 carte"""
    if len(hand) != 3:
        return (0, "Mano non valida")
    
    values = sorted([get_card_value(card) for card in hand], reverse=True)
    suits = [card[1] for card in hand]
    
    # Straight Flush
    if len(set(suits)) == 1 and values[0] - values[2] == 2:
        return (5, "Straight Flush")
    
    # Three of a Kind
    if values[0] == values[1] == values[2]:
        return (4, "Tris")
    
    # Straight
    if values[0] - values[2] == 2:
        return (3, "Scala")
    
    # Flush
    if len(set(suits)) == 1:
        return (2, "Colore")
    
    # Pair
    if values[0] == values[1] or values[1] == values[2]:
        return (1, "Coppia")
    
    return (0, "Carta Alta")

def display_hand(hand):
    """Visualizza una mano di carte"""
    cards = []
    for rank, suit in hand:
        color = 'red' if suit in ['♥️', '♦️'] else 'white'
        cards.append(f'[{color}]╔═════╗[/{color}]\n[{color}]║ {rank}{suit} ║[/{color}]\n[{color}]╚═════╝[/{color}]')
    return '\n'.join(cards)

def play(state, banker):
    console.print("\n[yellow]♠ POKER A 3 CARTE ♠[/yellow]")
    banker.game_taunt('poker')
    
    while True:
        console.print(f"\nLe tue fiches: {state.chips}")
        
        if state.chips <= 0:
            console.print("[red]Non hai abbastanza fiches per giocare![/red]")
            return
        
        # Fase di puntata
        ante_bet = int(Prompt.ask("Quanto vuoi puntare di Ante?", default="10"))
        while ante_bet > state.chips or ante_bet <= 0:
            console.print("[red]Puntata non valida![/red]")
            ante_bet = int(Prompt.ask("Quanto vuoi puntare di Ante?", default="10"))
        
        state.chips -= ante_bet
        
        # Distribuzione carte
        deck = create_deck()
        random.shuffle(deck)
        
        player_hand = [deck.pop() for _ in range(3)]
        dealer_hand = [deck.pop() for _ in range(3)]
        
        # Mostra le carte del giocatore
        console.print("\n[cyan]Le tue carte:[/cyan]")
        console.print(display_hand(player_hand))
        
        # Decisione del giocatore
        if Prompt.ask("\nVuoi continuare? (La puntata Play è uguale all'Ante)", choices=["s", "n"]) == "s":
            play_bet = ante_bet
            state.chips -= play_bet
            
            # Mostra le carte del dealer
            console.print("\n[red]Carte del Banchiere:[/red]")
            console.print(display_hand(dealer_hand))
            
            player_score = evaluate_hand(player_hand)
            dealer_score = evaluate_hand(dealer_hand)
            
            console.print(f"\n[cyan]La tua mano: {player_score[1]}[/cyan]")
            console.print(f"[red]Mano del Banchiere: {dealer_score[1]}[/red]")
            
            # Dealer deve avere almeno Q alta per qualificarsi
            dealer_qualifies = any(get_card_value(card) >= 12 for card in dealer_hand)
            
            if not dealer_qualifies:
                console.print("\n[yellow]Il Banchiere non si qualifica! Vinci l'Ante 1:1[/yellow]")
                state.chips += ante_bet * 2
                state.chips += play_bet  # Play bet push
            elif dealer_score > player_score:
                console.print("\n[red]Il Banchiere vince![/red]")
                banker.game_taunt('poker')
            elif dealer_score < player_score:
                console.print("\n[green]Hai vinto![/green]")
                state.chips += (ante_bet + play_bet) * 2
            else:
                console.print("\n[yellow]Pareggio! Recuperi le tue puntate[/yellow]")
                state.chips += ante_bet + play_bet
        else:
            console.print("\n[yellow]Hai abbandonato la mano[/yellow]")
        
        if not Prompt.ask("\nVuoi giocare un'altra mano?", choices=["s", "n"]) == "s":
            break
    
    state.save_game()
