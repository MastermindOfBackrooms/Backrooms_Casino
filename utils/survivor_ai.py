from dataclasses import dataclass
from typing import List, Tuple
import random

@dataclass
class SurvivorPersonality:
    name: str
    risk_tolerance: float  # 0.0 = molto conservativo, 1.0 = molto aggressivo
    counting_ability: float  # 0.0 = non conta le carte, 1.0 = conta perfettamente
    pattern_recognition: float  # 0.0 = ignora i pattern, 1.0 = riconosce tutti i pattern
    tilt_probability: float  # 0.0 = sempre calmo, 1.0 = si tilta facilmente
    story: str

class SurvivorAI:
    def __init__(self, personality: SurvivorPersonality):
        self.personality = personality
        self.card_count = 0
        self.hands_played = 0
        self.consecutive_losses = 0
        self.is_tilted = False
        self.hand_history = []
        self.winning_streak = 0
        self.total_wins = 0
        self.total_losses = 0

    def count_cards(self, card: Tuple[str, str]):
        """Sistema avanzato di conteggio carte basato sulla personalità"""
        if random.random() > self.personality.counting_ability:
            return

        rank = card[0]
        if rank in ['10', 'J', 'Q', 'K', 'A']:
            self.card_count -= 1
        elif rank in ['2', '3', '4', '5', '6']:
            self.card_count += 1

        # Pattern recognition evoluto
        if len(self.hand_history) >= 3:
            last_three = self.hand_history[-3:]
            if all(c[0] in ['10', 'J', 'Q', 'K', 'A'] for c in last_three):
                self.card_count -= 1 * self.personality.pattern_recognition
            elif all(c[0] in ['2', '3', '4', '5', '6'] for c in last_three):
                self.card_count += 1 * self.personality.pattern_recognition

        self.hand_history.append(card)

    def should_bet_behind(self, player_hand: List[Tuple[str, str]], dealer_upcard: Tuple[str, str]) -> bool:
        """Logica migliorata per decidere se qualcuno dovrebbe fare bet behind"""
        if self.is_tilted:
            return False

        # Analisi avanzata basata sulla personalità
        count_factor = self.card_count * self.personality.counting_ability
        hand_value = self.calculate_hand_value(player_hand)
        win_rate = self.total_wins / max(1, (self.total_wins + self.total_losses))

        # Valutazione strategica
        if hand_value >= 18:
            return True

        if count_factor > 2 and self.personality.counting_ability > 0.7:
            return True

        # Analisi del dealer upcard
        dealer_value = self.get_card_value(dealer_upcard)
        if dealer_value in [6, 5, 4] and hand_value >= 12:
            return True

        # Considerazione del momentum
        if self.winning_streak >= 3 and win_rate > 0.6:
            return True

        return False

    def decide_action(self, hand: List[Tuple[str, str]], dealer_upcard: Tuple[str, str], can_split: bool, can_double: bool) -> str:
        """Logica di decisione avanzata basata sulla personalità e stato mentale"""
        if self.is_tilted:
            # Comportamento più erratico durante il tilt
            risk_factor = random.random() + self.personality.risk_tolerance
            if risk_factor > 1.5:
                return 'hit'
            return random.choice(['hit', 'stand'])

        hand_value = self.calculate_hand_value(hand)
        dealer_value = self.get_card_value(dealer_upcard)

        # Basic strategy evoluta
        if hand_value < 12:
            return 'hit'
        elif hand_value == 12:
            if 4 <= dealer_value <= 6 and random.random() < self.personality.risk_tolerance:
                return 'stand'
            return 'hit'
        elif 13 <= hand_value <= 16:
            # Sistema di decisione avanzato
            if self.card_count > 2 and self.personality.counting_ability > 0.7:
                return 'stand'
            if self.winning_streak >= 2 and self.personality.risk_tolerance < 0.4:
                return 'stand'
            if 2 <= dealer_value <= 6:
                return 'stand'
            if random.random() < self.personality.risk_tolerance:
                return 'hit'
            return 'stand'
        else:
            # Gestione mani forti con personalità
            if hand_value == 17 and dealer_value >= 7 and self.personality.risk_tolerance > 0.8:
                return 'hit'
            if hand_value >= 19 and self.is_tilted and random.random() < self.personality.risk_tolerance:
                return 'hit'  # Decisione molto rischiosa durante il tilt
            return 'stand'

    def update_tilt_status(self, won_last_hand: bool):
        """Sistema evoluto di gestione del tilt e momentum"""
        if won_last_hand:
            self.consecutive_losses = 0
            self.winning_streak += 1
            self.total_wins += 1

            # Recupero dal tilt
            if self.is_tilted and random.random() < (0.3 + self.personality.risk_tolerance):
                self.is_tilted = False

            # Gestione momentum positivo
            if self.winning_streak >= 3:
                self.card_count *= 1.2  # Aumenta la fiducia nel conteggio
        else:
            self.consecutive_losses += 1
            self.winning_streak = 0
            self.total_losses += 1

            # Gestione tilt avanzata
            tilt_chance = self.personality.tilt_probability * (1 + self.consecutive_losses * 0.2)
            if self.consecutive_losses >= 3 and random.random() < tilt_chance:
                self.is_tilted = True
                self.hands_played = 0
                self.card_count *= 0.8  # Riduce l'affidabilità del conteggio durante il tilt

    @staticmethod
    def calculate_hand_value(hand: List[Tuple[str, str]]) -> int:
        """Calcola il valore di una mano considerando gli assi"""
        value = 0
        aces = 0

        for card in hand:
            rank = card[0]
            if rank in ['K', 'Q', 'J']:
                value += 10
            elif rank == 'A':
                aces += 1
            else:
                value += int(rank)

        for _ in range(aces):
            if value + 11 <= 21:
                value += 11
            else:
                value += 1

        return value

    @staticmethod
    def get_card_value(card: Tuple[str, str]) -> int:
        """Ottiene il valore numerico di una carta"""
        rank = card[0]
        if rank in ['K', 'Q', 'J']:
            return 10
        elif rank == 'A':
            return 11
        return int(rank)

# Definizione dei sopravvissuti con personalità uniche e storie elaborate
SURVIVORS = [
    SurvivorPersonality(
        name="Il Veterano",
        risk_tolerance=0.3,
        counting_ability=0.9,
        pattern_recognition=0.8,
        tilt_probability=0.2,
        story="Un ex-dealer di Las Vegas che ha attraversato innumerevoli livelli delle Backrooms. Sussurra di aver visto il 'pattern' ripetersi all'infinito, e di come il Level 777 sia solo uno dei tanti riflessi di una realtà più vasta. I suoi occhi tradiscono il peso di segreti che non osa rivelare completamente."
    ),
    SurvivorPersonality(
        name="L'Impulsivo",
        risk_tolerance=0.9,
        counting_ability=0.2,
        pattern_recognition=0.4,
        tilt_probability=0.8,
        story="Arrivato qui dopo aver seguito un'insegna al neon in un corridoio infinito. Parla ossessivamente di un 'gioco più grande' e di come le Backrooms stesse siano una gigantesca partita d'azzardo. La sua apparente follia nasconde lampi di lucidità inquietante quando menziona 'gli altri livelli'."
    ),
    SurvivorPersonality(
        name="Il Matematico",
        risk_tolerance=0.5,
        counting_ability=0.7,
        pattern_recognition=0.9,
        tilt_probability=0.3,
        story="Ex professore di topologia che sostiene di aver scoperto una formula matematica nelle Backrooms. I suoi appunti sono pieni di equazioni che collegano il numero 777 a schemi geometrici impossibili. Sembra capire più di quanto ammetta sulla vera natura del Level 777."
    ),
    SurvivorPersonality(
        name="Il Fortunato",
        risk_tolerance=0.7,
        counting_ability=0.1,
        pattern_recognition=0.3,
        tilt_probability=0.5,
        story="Nessuno sa come sopravviva così a lungo nelle Backrooms. Alcuni mormorano che abbia fatto un patto con qualcosa nei livelli più profondi. La sua 'fortuna' sembra quasi soprannaturale, e a volte il Banchiere stesso lo guarda con un misto di curiosità e preoccupazione."
    ),
    SurvivorPersonality(
        name="L'Osservatore",
        risk_tolerance=0.4,
        counting_ability=0.6,
        pattern_recognition=1.0,
        tilt_probability=0.1,
        story="Un enigmatico giocatore che non parla mai. I suoi occhi sembrano vedere oltre le pareti del Level 777, come se percepisse la vera struttura delle Backrooms. Alcuni sopravvissuti giurano di averlo visto in più livelli contemporaneamente."
    )
]

def get_survivor_comment(survivor, action, hand_value=None):
    """Genera commenti personalizzati per ogni sopravvissuto con riferimenti alle Backrooms"""
    if survivor.personality.name == "Il Veterano":
        if action == "hit":
            return random.choice([
                "[cyan]'Ho visto questa situazione migliaia di volte... in ogni livello.'[/cyan]",
                "[cyan]'Le carte seguono lo stesso pattern delle pareti...'[/cyan]",
                "[cyan]'Dopo 777 livelli, certe cose le senti nelle ossa.'[/cyan]",
                "[cyan]'Il mazzo ha un ritmo particolare... come il ronzio delle luci fluorescenti.'[/cyan]",
                "[cyan]'Questo mi ricorda il livello 456... ma meglio non parlarne.'[/cyan]"
            ])
        elif action == "stand":
            return random.choice([
                "[cyan]'Il conteggio non mente... proprio come le Backrooms.'[/cyan]",
                "[cyan]'So quando fermarmi... l'ho imparato nel modo più duro.'[/cyan]",
                "[cyan]'Ho visto troppi perdersi per l'avidità... in ogni senso.'[/cyan]",
                "[cyan]'Le probabilità sono come i corridoi... devi sapere quando svoltare.'[/cyan]",
                "[cyan]'Certi pattern non dovresti seguirli troppo a lungo...'[/cyan]"
            ])
    elif survivor.personality.name == "L'Impulsivo":
        if action == "hit":
            return random.choice([
                "[cyan]'L'istinto mi ha portato qui... e mi porterà fuori!'[/cyan]",
                "[cyan]'Le luci... le carte... tutto è collegato!'[/cyan]",
                "[cyan]'Ho seguito un'insegna al neon fino qui... doveva significare qualcosa!'[/cyan]",
                "[cyan]'Il rischio è ovunque nelle Backrooms... tanto vale abbracciarlo!'[/cyan]",
                "[cyan]'Sento che la prossima carta... cambierà tutto!'[/cyan]"
            ])
        elif action == "stand":
            return random.choice([
                "[cyan]'A volte devi fermarti... come quando senti quel suono...'[/cyan]",
                "[cyan]'Il mio sesto senso... l'unica cosa che mi tiene vivo qui.'[/cyan]",
                "[cyan]'Ho imparato a fidarmi delle sensazioni... dopo quello che ho visto.'[/cyan]",
                "[cyan]'Qualcosa mi dice di fermarmi... come quella volta al livello 666...'[/cyan]",
                "[cyan]'Le pareti... stanno sussurrando di nuovo...'[/cyan]"
            ])
    elif survivor.personality.name == "Il Matematico":
        if action == "hit":
            return random.choice([
                "[cyan]'La sequenza si ripete... proprio come la struttura delle Backrooms.'[/cyan]",
                "[cyan]'Le probabilità qui seguono pattern non euclidei...'[/cyan]",
                "[cyan]'Ho calcolato le variabili considerando la curvatura dello spazio...'[/cyan]",
                "[cyan]'Questi numeri... riflettono la geometria impossibile del luogo.'[/cyan]",
                "[cyan]'La formula è quasi completa... manca solo una variabile.'[/cyan]"
            ])
        elif action == "stand":
            return random.choice([
                "[cyan]'Le variabili convergono... come i corridoi infiniti.'[/cyan]",
                "[cyan]'L'equazione è in equilibrio... per ora.'[/cyan]",
                "[cyan]'I numeri non mentono... ma le Backrooms sì.'[/cyan]",
                "[cyan]'Ho mappato questo pattern... si ripete all'infinito.'[/cyan]",
                "[cyan]'La topologia di questo luogo... meglio non parlarne.'[/cyan]"
            ])
    elif survivor.personality.name == "Il Fortunato":
        if action == "hit":
            return random.choice([
                "[cyan]'Le carte... mi chiamano come i corridoi infiniti.'[/cyan]",
                "[cyan]'La fortuna è una cosa strana nelle Backrooms...'[/cyan]",
                "[cyan]'Il Level 777 mi sorride... come [i]loro[/i].'[/cyan]",
                "[cyan]'Sento che la prossima carta... è predestinata.'[/cyan]",
                "[cyan]'Il destino qui ha un sapore particolare...'[/cyan]"
            ])
        elif action == "stand":
            return random.choice([
                "[cyan]'Certi doni... hanno un prezzo nelle Backrooms.'[/cyan]",
                "[cyan]'La fortuna va rispettata... come gli accordi presi.'[/cyan]",
                "[cyan]'Questi presentimenti... mi hanno salvato troppe volte.'[/cyan]",
                "[cyan]'Meglio fermarsi... prima che [i]loro[/i] si accorgano.'[/cyan]",
                "[cyan]'Il mio... protettore... mi suggerisce cautela.'[/cyan]"
            ])
    elif survivor.personality.name == "L'Osservatore":
        if action == "hit":
            return random.choice([
                "[cyan]*i suoi occhi sembrano guardare attraverso le carte, verso un altro livello*[/cyan]",
                "[cyan]*un impercettibile cenno, come se rispondesse a qualcosa che solo lui può vedere*[/cyan]",
                "[cyan]*le sue pupille seguono pattern invisibili nell'aria*[/cyan]",
                "[cyan]*per un momento, la sua forma sembra... sfuocare*[/cyan]",
                "[cyan]*un sussurro in una lingua che ricorda il ronzio delle luci*[/cyan]"
            ])
        elif action == "stand":
            return random.choice([
                "[cyan]*il suo sguardo attraversa le pareti del Level 777*[/cyan]",
                "[cyan]*un gesto che sembra ripetersi all'infinito in corridoi invisibili*[/cyan]",
                "[cyan]*i suoi occhi riflettono geometrie impossibili*[/cyan]",
                "[cyan]*il tempo sembra distorcersi intorno alla sua figura immobile*[/cyan]",
                "[cyan]*un silenzio che nasconde verità indicibili sulle Backrooms*[/cyan]"
            ])
    return ""