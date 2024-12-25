from rich.console import Console
import random
import time

console = Console()

class Banker:
    def __init__(self):
        self.greetings = [
            "Benvenuto nel mio eterno stabilimento...",
            "Ah, un nuovo giocatore... Che... fortuna.",
            "La casa vince sempre, ma prego... tenta la sorte.",
            "Il tempo qui non ha significato... solo le fiches contano.",
            "Finalmente... carne fresca.",
            "777... un numero così perfetto, non trovi?",
            "Le tue fiches brillano... come anime intrappolate.",
            "Ogni gioco è un passo verso... l'eternità."
        ]

        self.loan_responses = {
            'offer': [
                "Un prestito... interessante proposta.",
                "Le mie condizioni sono... ragionevoli.",
                "Il prezzo è alto... ma ne vale la pena?",
                "La disperazione ha un... sapore delizioso.",
                "Un prestito può essere... un cappio al collo."
            ],
            'tier1': [  # Level 0 - The Lobby
                "Solo un assaggio... del potere oscuro.",
                "Un piccolo passo... nel labirinto del debito.",
                "Le Backrooms sono generose... all'inizio.",
                "Un prestito modesto... per un'anima modesta.",
                "Il primo livello... è sempre il più dolce.",
                "Come il ronzio delle luci fluorescenti... costante ma sopportabile.",
                "Il principiante non sa... quanto in profondità può cadere.",
                "La moquette sotto i tuoi piedi... ancora familiare.",
                "Le pareti gialle... ti sembrano ancora normali.",
                "Il primo prestito... come il primo passo nel vuoto."
            ],
            'tier2': [  # Level 1 - The Warehouse
                "Gli scaffali infiniti... nascondono il tuo debito.",
                "Tra casse e container... si cela il tuo destino.",
                "Il freddo metallo... riflette la tua disperazione.",
                "Un prestito più grande... un abisso più profondo.",
                "Le luci del magazzino... tremano al tuo passaggio.",
                "I corridoi si allungano... come i tuoi debiti.",
                "Le etichette sbiadite... raccontano di altri come te.",
                "Il secondo livello... dove molti si perdono.",
                "L'eco dei tuoi passi... risuona nell'infinito.",
                "Un magazzino di anime... in attesa di redenzione."
            ],
            'tier3': [  # Level 2 - Pipe Dreams
                "I tubi sussurrano... di debiti più profondi.",
                "Il vapore nasconde... la verità del contratto.",
                "Un prestito che scorre... come acqua nera.",
                "Le tubature cantano... il tuo nome.",
                "Il calore aumenta... con il peso del debito.",
                "Labirinti di metallo... riflettono la tua follia.",
                "Il terzo livello... dove la realtà si piega.",
                "Le valvole controllano... il flusso della tua anima.",
                "Un prestito tossico... come il vapore che respiri.",
                "Le Pipe Dreams... diventano incubi reali."
            ],
            'tier4': [  # Level 3 - Electrical Station
                "L'elettricità oscura... alimenta questo prestito.",
                "Scintille di debito... bruciano la tua anima.",
                "Un prestito potente... come corrente ad alto voltaggio.",
                "I generatori ronzano... al ritmo del tuo cuore.",
                "L'energia del debito... scorre nelle tue vene.",
                "Il quarto livello... dove la corrente è letale.",
                "Pannelli elettrici... controllano il tuo destino.",
                "Un prestito che elettrifica... la tua disperazione.",
                "L'ozono del debito... brucia i tuoi sogni.",
                "La stazione elettrica... alimenta la tua dannazione."
            ],
            'tier5': [  # Level 4 - Abandoned Office
                "Un prestito sepolto... tra file dimenticati.",
                "I cubicoli vuoti... testimoniano il tuo fallimento.",
                "Computer fantasma... calcolano il tuo debito.",
                "Le deadline del prestito... sono infinite.",
                "Un contratto stampato... in inchiostro dell'anima.",
                "Il quinto livello... dove le anime si perdono.",
                "Meeting room dell'oblio... dove si sigilla il patto.",
                "Un prestito che cresce... come pile di documenti.",
                "La burocrazia dell'inferno... ha il tuo nome.",
                "L'ufficio ricorda... ogni anima che ha firmato."
            ],
            'tier6': [  # Level 5 - The Hotel
                "Una suite nel void... il prezzo è la tua anima.",
                "Il prestito finale... nella hall dell'eternità.",
                "Un contratto sigillato... con sangue oscuro.",
                "L'hotel accoglie... un nuovo ospite eterno.",
                "Il sesto livello... dove il tempo muore.",
                "Chiavi dorate... per porte di disperazione.",
                "Un prestito di lusso... per una dannazione eterna.",
                "L'ascensore scende... verso l'abisso finale.",
                "La reception dell'inferno... ha la tua prenotazione.",
                "The Hotel... la tua ultima destinazione."
            ],
            'repaid': [
                "Il debito è saldato... ma il marchio rimane.",
                "Libero dal prestito... non da me.",
                "Hai mantenuto la parola... impressionante.",
                "Il contratto è concluso... per ora.",
                "La libertà ha un sapore... dolce, vero?"
            ],
            'already_has_loan': [
                "Le Backrooms non dimenticano i debiti...",
                "Un prestito alla volta... come i livelli del labirinto.",
                "La tua avidità... ti renderà come gli altri vagabondi.",
                "Prima consuma questo veleno... poi ne parleremo.",
                "La pazienza è una virtù... nelle Backrooms."
            ]
        }

        self.membership_responses = {
            'offer': [
                "Hai dimostrato il tuo valore... vuoi unirti a noi?",
                "La tessera del Level 777... ti chiama.",
                "Potresti diventare... parte di qualcosa di più grande.",
                "Il casinò ti vuole... come membro permanente.",
                "La scelta è tua... ma scegli saggiamente."
            ],
            'accepted': [
                "Benvenuto... nella famiglia.",
                "Il Level 777 ha un nuovo... guardiano.",
                "La tua anima ora appartiene... al casinò.",
                "Uno di noi... per l'eternità.",
                "Il cerchio si chiude... inizia il tuo regno.",
                "Eccellente... ora mi appartieni un po' di più.",
                "Le fiches sono tue... per ora.",
                "Il contratto è sigillato... con la tua essenza.",
                "Saggio... o folle? Lo scopriremo presto.",
                "Il tempo del debito... è iniziato."
            ],
            'rejected': [
                "La libertà... ha un prezzo alto.",
                "Rifiuti il potere... interessante.",
                "Forse più saggio... di quanto credessi.",
                "La tua scelta... ti condanna alla libertà.",
                "Il casinò ricorderà... questo momento.",
                "Forse più saggio... di quanto pensassi.",
                "La prudenza ti salva... per ora.",
                "Un'occasione sprecata... o forse no?",
                "La paura ti rende... cauto.",
                "Tornerai... quando la disperazione crescerà."
            ]
        }

        self.secret_ending_responses = {
            'first_secret': [
                "777777... il numero della perfezione assoluta.",
                "Hai scoperto... ciò che era nascosto.",
                "Il Level 777 trema... al tuo potere.",
                "L'impossibile... diventa realtà.",
                "Il velo si squarcia... rivelandoti la verità."
            ],
            'second_secret': [
                "666666... il numero del caos primordiale.",
                "Hai visto... ciò che non dovevi vedere.",
                "Le ombre sussurrano... il tuo nome.",
                "Il Level 777 si piega... alla tua volontà oscura.",
                "Il confine tra realtà e incubo... svanisce."
            ]
        }

        self.game_specific_taunts = {
            'craps': [
                "I dadi raccontano storie... di destini spezzati.",
                "Sette... un numero potente in questo regno.",
                "I dadi danzano... come spiriti inquieti.",
                "Ogni lancio è un sussurro... del fato.",
                "Il Seventh Sign attende... il prescelto.",
                "La profezia del sette... si sta avverando?",
                "I numeri mistici... risuonano nell'aria.",
                "Le ombre danzano... al ritmo dei dadi.",
                "Il destino si svela... ad ogni lancio.",
                "Sento il potere del 7... crescere."
            ],
            'sic_bo': [
                "Tre dadi... tre destini intrecciati.",
                "Il caos dei dadi... riflette la tua anima.",
                "I numeri si combinano... come una danza macabra.",
                "Antichi segreti... nei simboli dei dadi.",
                "La sequenza mistica... chiama il tuo nome.",
                "Il settimo sigillo... attende di essere spezzato.",
                "Tre è il numero del caos... sette della perfezione.",
                "I dadi sussurrano... antiche verità.",
                "Le combinazioni... nascondono segreti.",
                "Il Level 777... benedice i coraggiosi."
            ],
            'poker': [
                "I tuoi tell sono... affascinanti.",
                "Le tue fiches tremano... come la tua anima.",
                "Bluffare con me è... pericoloso.",
                "Vedo la paura nei tuoi occhi... deliziosa.",
                "Le tue carte nascondono... segreti oscuri."
            ],
            'blackjack': [
                "Il 21 è un numero interessante... come la vita e la morte.",
                "Le carte non mentono mai... ma io sì.",
                "Ogni carta è un passo verso... il tuo destino.",
                "Vuoi un'altra carta? O hai... paura?",
                "Il mazzo sussurra... ascolta attentamente."
            ],
            'roulette': [
                "La ruota gira eternamente... come il tuo destino.",
                "Rosso o nero... vita o morte... scegli.",
                "I numeri sussurrano... li senti?",
                "La pallina danza... come un'anima perduta.",
                "Ogni giro è un nuovo... tormento."
            ],
            'baccarat': [
                "Punto o Banco... due facce dello stesso destino.",
                "Le carte scorrono... come il tempo in questo luogo.",
                "Un gioco elegante... per anime raffinate.",
                "La semplicità nasconde... profonda oscurità."
            ],
            'red_room': [
                "Benvenuti nella Red Room... dove le anime danzano con il destino.",
                "I sopravvissuti... così fragili, così determinati.",
                "Ogni carta rivela... un pezzo della loro anima.",
                "Il sangue sulle pareti... racconta storie di sfide passate.",
                "Scommetti sulla sopravvivenza... o sulla disperazione?",
                "La Red Room ha fame... di nuove vittime.",
                "Osserva come combattono... per la loro libertà.",
                "Le loro strategie... sono affascinanti quanto inutili.",
                "Chi sopravviverà... a questa danza macabra?",
                "Il destino dei sopravvissuti... è nelle carte.",
                "Sento l'odore... della loro paura.",
                "La disperazione... ha un sapore particolare qui.",
                "Le loro anime... brillano di determinazione.",
                "Ogni sopravvissuto... ha i suoi demoni.",
                "Il tempo scorre diversamente... nella Red Room.",
                "Le carte sussurrano... storie di perdizione.",
                "La speranza... è un'illusione preziosa.",
                "I loro occhi... rivelano verità nascoste.",
                "Il tavolo è apparecchiato... per il festino.",
                "La Red Room accoglie... tutti i disperati.",
                "Le loro strategie... sono come ragnatele nella tempesta.",
                "Ogni mano... potrebbe essere l'ultima.",
                "Il silenzio... nasconde urla di disperazione.",
                "Le ombre danzano... al ritmo delle carte.",
                "I sopravvissuti... così determinati a sfidare il destino.",
                "Questa stanza ha visto... infinite anime perdersi.",
                "Il gioco continua... all'infinito.",
                "Le loro menti... si spezzano una carta alla volta.",
                "La pazzia... è solo l'inizio.",
                "Ogni vittoria... li avvicina alla dannazione.",
                "I loro sogni... alimentano questa stanza.",
                "Le carte... sono solo lo strumento del loro tormento.",
                "La disperazione... ha un suono particolare qui.",
                "Osserva come lottano... contro l'inevitabile.",
                "Il destino... è scritto nel mazzo.",
                "Le loro anime... sono già parte della Red Room.",
                "Ogni decisione... li condanna ulteriormente.",
                "Il tempo non esiste... in questa stanza.",
                "Le loro speranze... sono come cenere al vento.",
                "La Red Room ricorda... ogni anima perduta.",
                "I loro occhi... specchi di disperazione infinita.",
                "Ogni scelta... un passo verso la follia.",
                "Le loro menti vacillano... come castelli di carte.",
                "Vedo la paura crescere... ad ogni carta.",
                "Il loro coraggio... è solo un'illusione.",
                "Le strategie che usano... riflettono la loro pazzia.",
                "Ogni mano rivela... un nuovo livello di disperazione.",
                "I sopravvissuti più forti... cadono più duramente.",
                "Le loro anime... brillano di una luce morente.",
                "Il tavolo verde... divora le loro speranze.",
                "L'aria è densa... di destini intrecciati.",
                "Il silenzio urla... verità nascoste.",
                "Le ombre danzano... al ritmo delle carte.",
                "Il tempo si contorce... in questo luogo maledetto.",
                "Sento il battito... di cinque cuori terrorizzati.",
                "La Red Room si nutre... della loro angoscia.",
                "Le pareti sussurrano... storie di perdizione.",
                "L'atmosfera è elettrica... carica di destino.",
                "Il tavolo verde... un altare di sacrificio.",
                "L'oscurità cresce... ad ogni mano giocata.",
                "Osserva come calcolano... ogni mossa disperata.",
                "Le loro strategie... sono ragnatele nella tempesta.",
                "Ogni decisione... li avvicina all'abisso.",
                "La matematica del caos... governa le loro scelte.",
                "Vedo pattern... che loro non possono comprendere.",
                "Le probabilità... sono catene che li legano.",
                "Il conteggio delle carte... una danza futile.",
                "Le loro tecniche... sono sabbia nel vento.",
                "Ogni split... è un taglio nella loro anima.",
                "Il double down... un salto nel vuoto.",
                "La ruota gira... sempre uguale, sempre diversa.",
                "Ogni mano... un nuovo ciclo di tormento.",
                "Il tempo qui... è un serpente che si morde la coda.",
                "La storia si ripete... in infinite variazioni.",
                "Nuovo giro... nuove anime da reclamare.",
                "Il carosello della disperazione... gira ancora.",
                "Un nuovo capitolo... della stessa storia infinita.",
                "La danza macabra... non ha fine.",
                "Le loro anime danzano... come marionette spezzate.",
                "Ogni carta è un passo... verso l'oblio.",
                "I sopravvissuti... così fragili, così determinati.",
                "Vedo la paura crescere... nei loro occhi stanchi.",
                "Le loro menti vacillano... al ritmo delle carte.",
                "Il tavolo verde... divora le loro speranze.",
                "Sento l'eco... delle loro preghiere disperate.",
                "La Red Room si nutre... della loro angoscia.",
                "Osserva come tremano... davanti al destino.",
                "Le loro strategie... sono ragnatele nella tempesta.",
                "Il tempo qui scorre... come sangue nero.",
                "I loro sogni... alimentano questa stanza.",
                "Ascolta il silenzio... grida di disperazione.",
                "Le ombre danzano... al ritmo del loro terrore.",
                "Ogni decisione... li avvicina all'abisso.",
                "La matematica del caos... governa le loro scelte.",
                "I pattern emergono... nella loro follia.",
                "Le probabilità... sono catene che li legano.",
                "Il conteggio delle carte... una danza futile.",
                "Le loro tecniche... sono sabbia nel vento.",
                "Ogni split... è un taglio nella loro anima.",
                "Il double down... un salto nel vuoto.",
                "La ruota gira... sempre uguale, sempre diversa.",
                "Il ciclo continua... inesorabile.",
                "Un nuovo giro... nuove anime da reclamare.",
                "Il carosello della disperazione... gira ancora.",
                "La danza macabra... non ha fine.",
                "I sopravvissuti più forti... cadono più duramente.",
                "Le loro anime... brillano di una luce morente.",
                "Il silenzio urla... verità nascoste.",
                "L'aria è densa... di destini intrecciati.",
                "Il tempo si contorce... in questo luogo maledetto.",
                "La Red Room ricorda... ogni anima perduta.",
                "Sento il battito... di cinque cuori terrorizzati.",
                "Le pareti sussurrano... storie di perdizione.",
                "L'atmosfera è elettrica... carica di destino.",
                "L'oscurità cresce... ad ogni mano giocata.",
                "Vedo pattern... che loro non possono comprendere.",
                "Ogni vittoria... li avvicina alla dannazione.",
                "Le loro menti si sgretolano... come castelli di carte.",
                "Le pareti hanno orecchie... e memoria.",
                "Ogni livello conduce qui... alla fine.",
                "Il Level 777... un rifugio per anime perdute.",
                "I corridoi infiniti... portano tutti al mio tavolo.",
                "La geometria di questo luogo... è perfetta.",
                "Le luci fluorescenti... cantano per noi.",
                "Vedo i segni del loro vagare... nei loro occhi.",
                "Alcuni conoscono troppo... altri troppo poco.",
                "Il nostro Veterano... ha visto più di quanto dovrebbe.",
                "La Matematica... si avvicina alla verità.",
                "L'Osservatore... forse non è nemmeno qui.",
                "Il Fortunato... ha fatto patti pericolosi.",
                "L'Impulsivo... la sua follia è quasi saggezza.",
                "Ogni sopravvissuto porta... i segni del viaggio.",
                "Le Backrooms hanno molti livelli... questo è speciale.",
                "Il Level 777... un nodo nella trama della realtà.",
                "I pattern si ripetono... all'infinito.",
                "Alcuni livelli sono più reali... di altri.",
                "Le pareti cambiano... ma il gioco resta.",
                "Il ronzio delle luci... nasconde segreti.",
                "Ogni carta... è un pezzo del labirinto.",
                "I corridoi ricordano... ogni passo falso.",
                "La moquette racconta... storie infinite.",
                "Il tempo qui... è solo un'illusione.",
                "Alcuni trovano questo posto... altri vengono trovati.",
                "Le Backrooms scelgono... i propri ospiti.",
                "Ogni porta chiusa... nasconde un nuovo livello.",
                "I numeri hanno significati... oltre la matematica.",
                "Il casinò è ovunque... e in nessun luogo.",
                "Le regole qui... sono diverse."
            ]
        }

        self.win_responses = {
            'seven_related': [
                "Il potere del 7 scorre... attraverso di te.",
                "Tre 7... un segno del destino.",
                "Il numero sacro ti ha benedetto... oggi.",
                "777... la chiave di questo regno.",
                "I sette sigilli si incrinano... interessante.",
                "Le stelle si allineano... nel segno del 7.",
                "Il Level 777 riconosce... il tuo potere.",
                "Questa vittoria ha un sapore... particolare.",
                "Il numero perfetto ti sorride...",
                "Sento i numeri cantare... per te."
            ],
            'devils_defeated': [
                "I demoni si inchinano... davanti a te.",
                "Sette prove superate... impossibile.",
                "Le ombre si ritirano... per ora.",
                "Mai visto nulla di simile... in 777 anni.",
                "Il Level 777 ha un nuovo... campione.",
                "La tua anima brucia... di potere oscuro.",
                "I demoni ricorderanno... questo giorno.",
                "Le carte tremano... al tuo tocco.",
                "Questa vittoria echeggerà... nell'eternità.",
                "Forse... sei più di un semplice giocatore."
            ],
            'normal': [
                "Che... inaspettato. Congratulazioni.",
                "Goditi la vittoria. Finché dura.",
                "Forse sei più interessante di quanto pensassi...",
                "Una vittoria... ma a quale prezzo?",
                "Il Level 777 ti sorride... per ora."
            ],
            'big_win': [
                "Impressionante... molto impressionante.",
                "Le tue abilità sono... notevoli.",
                "Questa vittoria ti è costata... più di quanto pensi.",
                "Il 777 risuona con la tua fortuna...",
                "Una vittoria degna... del mio regno."
            ],
            'streak': [
                "La fortuna ti sorride... per ora.",
                "Il pendolo oscilla... presto cambierà direzione.",
                "La tua fortuna sta attirando... attenzione indesiderata.",
                "Vedo il 777 nei tuoi occhi...",
                "Le tue vittorie alimentano... qualcosa di più grande."
            ],
            'mystic_sequence': [
                "La sequenza si completa... perfetta.",
                "I numeri danzano... in armonia.",
                "Il ritmo del caos... si rivela.",
                "La danza dei dadi... è completa.",
                "Una combinazione... predestinata."
            ],
            'seventh_seal': [
                "Il sigillo si spezza... finalmente.",
                "Il potere del 7... scorre attraverso te.",
                "I segreti del Level 777... si svelano.",
                "Le barriere... cadono.",
                "L'impossibile... diventa realtà."
            ]
        }

        self.lose_responses = {
            'devils_defeat': [
                "I demoni reclamano... il loro premio.",
                "Sette prove... sette fallimenti.",
                "Le ombre ti consumano... delizioso.",
                "Un'altra anima per la collezione...",
                "I Seven Devils rimangono... imbattuti.",
                "Il buio ti avvolge... per sempre.",
                "La tua audacia... ti è costata cara.",
                "I demoni si nutrono... della tua sconfitta.",
                "Nessuno sfugge... ai Seven Devils.",
                "Il Level 777 reclama... la sua preda."
            ],
            'normal': [
                "Come previsto. La casa vince sempre.",
                "La tua fortuna è finita. Come sempre qui.",
                "Un'altra anima reclamata dal casinò...",
                "Le tue fiches mi appartengono... come la tua anima.",
                "Il Level 777 reclama... il suo tributo."
            ],
            'big_loss': [
                "Le tue fiches... ora sono mie.",
                "La disperazione... ti dona.",
                "Sento l'odore della tua paura...",
                "Il prezzo della sfida... è alto.",
                "La tua sconfitta alimenta... questo luogo."
            ],
            'bankruptcy': [
                "Game over... letteralmente.",
                "La tua anima ora mi appartiene...",
                "Un'altra collezione alla mia... raccolta.",
                "777 anime... e la tua fa 778.",
                "Il Level 777 ha... un nuovo residente."
            ]
        }

        self.challenge_taunts = {
            'start': [
                "Osi sfidarmi... nel mio dominio?",
                "777 anime hanno tentato... tutte hanno fallito.",
                "La posta in gioco è... la tua essenza.",
                "Questa sfida sarà... memorabile.",
                "Il Level 777 osserva... con interesse."
            ],
            'during': [
                "Senti il peso... della tua scelta?",
                "Le carte danzano... tra vita e morte.",
                "Ogni mossa potrebbe essere... l'ultima.",
                "Il tempo si contorce... in questo momento.",
                "777 battiti... nel silenzio della sfida."
            ],
            'victory': [
                "Impossibile... dopo 777 vittorie...",
                "Il Level 777 ha un nuovo... campione.",
                "La tua vittoria risuonerà... eternamente.",
                "Hai vinto... ma sei ancora qui.",
                "Forse... non sei un semplice giocatore."
            ],
            'defeat': [
                "Come tutti gli altri... prima di te.",
                "La tua anima arricchirà... la mia collezione.",
                "777 vittorie... e counting.",
                "Il Level 777 reclamava... il tuo destino.",
                "Un'altra storia... per la mia eternità."
            ]
        }

        self.special_message_new = {
            "777": [
                "Il Level 777 è un punto focale... un nodo nella rete delle Backrooms.",
                "Qui, le regole sono diverse... la realtà stessa è in discussione.",
                "Ho visto innumerevoli anime passare da qui... alcuni hanno lasciato tracce indelebili.",
                "Questo luogo è collegato ad altri livelli... ma solo pochi conoscono i percorsi.",
                "I sopravvissuti parlano di strane entità... e di geometrie impossibili.",
                "La moquette... emette strani sussurri...",
                "Le luci fluorescenti... vibrano con un'energia inquietante.",
                "Il tempo qui non scorre linearmente... alcuni si perdono per sempre.",
                "Il Level 777 è più di un semplice casinò... è un portale.",
                "Se sei abbastanza fortunato o sfortunato... potresti trovare la via d'uscita."
            ]
        }

        self.bet_behind_responses = {
            'follow': [
                "Scommetti sull'anima giusta... o ti perderai con loro.",
                "La loro fortuna... potrebbe essere la tua rovina.",
                "Seguire il destino altrui... che scelta interessante.",
                "Le loro decisioni... ora sono anche le tue.",
                "Il loro fato... è intrecciato al tuo.",
                "Affidi la tua fortuna... a un altro disperato.",
                "La disperazione... si moltiplica nel bet behind.",
                "Le loro scelte... determineranno il tuo destino.",
                "Un legame pericoloso... si è formato.",
                "La loro strada... ora è anche la tua.",
                "Affidi il tuo destino... a un altro dannato.",
                "La loro fortuna... sarà la tua condanna.",
                "Due anime... un unico destino.",
                "Il loro fallimento... ti trascinerà con sé.",
                "La scelta è fatta... non puoi più tornare indietro.",
                "Le loro decisioni... ora sono le tue catene.",
                "Un legame pericoloso... si è formato.",
                "La disperazione... si moltiplica nel bet behind.",
                "Le loro scelte... saranno il tuo tormento.",
                "Un patto con il destino... attraverso un altro disperato.",
                "Il loro cammino... diventa il tuo sentiero oscuro.",
                "La fiducia... è una lama a doppio taglio.",
                "Le loro carte... ora sono le tue spine.",
                "Un destino condiviso... una dannazione moltiplicata.",
                "La loro strategia... ora è la tua prigione.",
                "Un'alleanza... forgiata nella disperazione.",
                "Il loro coraggio... sarà la tua rovina.",
                "Le loro decisioni... eco del tuo destino.",
                "Un legame mistico... nato dalla necessità.",
                "La loro sorte... ora è la tua maledizione.",
                "Segui il loro destino... verso l'inevitabile."
            ],
            'win': [
                "La fortuna sorride... ai temerari.",
                "La loro vittoria... ti ha trascinato con sé.",
                "Il destino premia... chi sa scegliere.",
                "La loro abilità... ti ha portato fortuna.",
                "Le anime vincenti... attraggono altre anime.",
                "Il destino sorride... ai temerari.",
                "La loro vittoria... ti ha trascinato con sé.",
                "Il destino premia... chi sa scegliere.",
                "La loro abilità... ti ha portato fortuna.",
                "Le anime vincenti... attraggono altre anime.",
                "Il destino sorride... ai temerari.",
                "Una scelta fortunata... per ora.",
                "Le loro vittorie... ti trascinano in alto.",
                "Il successo condiviso... ha un sapore particolare.",
                "Le catene del destino... si allentano.",
                "La fortuna degli stolti... vi benedice entrambi.",
                "Due anime... un momento di gloria.",
                "Il vostro legame... porta frutti amari.",
                "Una vittoria condivisa... raddoppia il prezzo.",
                "Le vostre strade... si intrecciano nel trionfo."
            ],
            'loss': [
                "La loro sconfitta... ora è anche la tua.",
                "Il prezzo della fiducia... è alto.",
                "Le loro debolezze... ti hanno condannato.",
                "La disperazione... si propaga come un virus.",
                "Il loro fallimento... era prevedibile.",
                "La loro sconfitta... ora è anche la tua.",
                "Il prezzo della fiducia... è alto.",
                "Le loro debolezze... ti hanno condannato.",
                "La disperazione... si propaga come un virus.",
                "Il loro fallimento... era prevedibile.",
                "Cadete insieme... nel vuoto.",
                "La sconfitta condivisa... ha un sapore più amaro.",
                "Il prezzo del legame... si paga doppio.",
                "Le vostre anime... precipitano all'unisono.",
                "La caduta comune... era prevedibile.",
                "Due destini... una singola rovina.",
                "Il fallimento risuona... in entrambe le anime.",
                "La fiducia mal riposta... vi condanna entrambi.",
                "Le catene del destino... vi trascinano giù.",
                "Una scelta sbagliata... due anime perdute."
            ]
        }

        self.stories = {
            1: [  # Level 0 - The Lobby
                "Le pareti gialle sussurrano... storie di anime perdute.",
                "Il ronzio delle luci fluorescenti... la prima melodia dell'infinito.",
                "Seicento milioni di metri quadrati... di moquette umida.",
                "Corridoi infiniti... che portano ovunque e in nessun luogo.",
                "L'aria è densa... di disperazione e neon.",
                "Le pareti vibrano... al ritmo del nulla.",
                "Il silenzio è rotto... solo dal ronzio eterno.",
                "Questo è solo l'inizio... del tuo viaggio nell'abisso.",
                "La moquette ricorda... ogni passo dei perduti.",
                "Le luci fluorescenti... non smettono mai di ronzare."
            ],
            2: [  # Level 1 - The Warehouse
                "Scaffali infiniti... si perdono nell'oscurità.",
                "Casse impilate... contenenti sogni dimenticati.",
                "Il freddo metallo... risuona di echi lontani.",
                "Carrelli elevatori fantasma... si muovono da soli.",
                "Le luci oscillano... creando ombre danzanti.",
                "L'odore di cartone... e speranze abbandonate.",
                "Il silenzio è interrotto... da cigolii metallici.",
                "Tra gli scaffali... si nascondono segreti.",
                "Le etichette sbiadite... raccontano storie perdute.",
                "Un magazzino infinito... di anime dimenticate."
            ],
            3: [  # Level 2 - Pipe Dreams
                "I tubi serpeggianti... cantano melodie impossibili.",
                "Vapore tossico... danza nell'aria stagnante.",
                "Il metallo sussurra... segreti dimenticati.",
                "Labirinti di condotti... che portano alla follia.",
                "L'acqua gocciola... con un ritmo ipnotico.",
                "Scale a chiocciola... che sfidano la gravità.",
                "Valvole arrugginite... controllano destini perduti.",
                "Il calore soffocante... distorce la realtà.",
                "Tunnel claustrofobici... si contorcono nell'infinito.",
                "Le tubature pulsano... come vene metalliche."
            ],
            4: [  # Level 4 - Abandoned Office
                "Cubicoli vuoti... sussurrano di vite interrotte.",
                "Computer accesi... che nessuno usa più.",
                "File e documenti... di un'azienda inesistente.",
                "Le sedie girevoli... ruotano da sole.",
                "Fotocopiatrici fantasma... stampano fogli vuoti.",
                "Meeting room vuote... dove si tengono ancora riunioni.",
                "Le scrivanie pulite... aspettano proprietari scomparsi.",
                "Email non lette... da caselle postali abbandonate.",
                "Il silenzio dell'ufficio... nasconde sussurri inquietanti.",
                "Le deadline sono passate... ma il tempo qui è fermo."
            ],
            5: [  # Level 4 - Abandoned Office
                "Un prestito sepolto... tra file dimenticati.",
                "I cubicoli vuoti... testimoniano il tuo fallimento.",
                "Computer fantasma... calcolano il tuo debito.",
                "Le deadline del prestito... sono infinite.",
                "Un contratto stampato... ininchiostro dell'anima.",
                "Il quinto livello... dove le anime si perdono.",
                "Meeting room dell'oblio... dove si sigilla il patto.",
                "Un prestito che cresce... come pile di documenti.",
                "La burocrazia dell'inferno... ha il tuo nome.",
                "L'ufficio ricorda... ogni anima che ha firmato."
            ],
            6: [  # Level 5 - The Hotel
                "Corridoi infiniti... di porte numerate.",
                "Il tappeto rosso... nasconde macchie oscure.",
                "Le chiavi tintinnano... nelle serrature vuote.",
                "Stanze che cambiano... quando non guardi.",
                "Il servizio in camera... arriva sempre vuoto.",
                "L'ascensore si muove... tra piani impossibili.",
                "Le lampade dondolano... senza vento.",
                "La reception è sempre... presidiata dalle ombre.",
                "Le suite di lusso... nascondono orrori indicibili.",
                "Il check-out... non è mai un'opzione."
            ]
        }

        self.descriptions = {
            1: "Il prezzo è leggero... per ora. Solo il 50% delle tue vincite mi apparterrà.",
            2: "Il costo cresce... il 60% delle tue vittorie alimenterà il vuoto.",
            3: "Il tributo si fa pesante... il 70% delle tue fortune sarà mio.",
            4: "L'80% delle tue vincite... un piccolo prezzo per la dannazione.",
            5: "Il 90% di ogni tua vittoria... nutrirà le Backrooms.",
            6: "Quasi tutto ciò che vinci... il 95% sarà assorbito dall'oscurità."
        }


    def welcome_message(self):
        message = random.choice(self.greetings)
        console.print(f"\n[red]Il Banchiere:[/red] [italic]{message}[/italic]")
        time.sleep(2)

    def game_taunt(self, game_type):
        messages = self.game_specific_taunts.get(game_type, self.game_specific_taunts['poker'])
        message = random.choice(messages)
        console.print(f"\n[red]Il Banchiere:[/red] [italic]{message}[/italic]")
        time.sleep(1)

    def win_response(self, type='normal'):
        responses = self.win_responses.get(type, self.win_responses['normal'])
        message = random.choice(responses)
        console.print(f"\n[red]Il Banchiere:[/red] [italic]{message}[/italic]")
        time.sleep(1)

    def lose_response(self, type='normal'):
        responses = self.lose_responses.get(type, self.lose_responses['normal'])
        message = random.choice(responses)
        console.print(f"\n[red]Il Banchiere:[/red] [italic]{message}[/italic]")
        time.sleep(1)

    def challenge_taunt(self, phase='start'):
        taunts = self.challenge_taunts.get(phase, self.challenge_taunts['start'])
        message = random.choice(taunts)
        console.print(f"\n[red]Il Banchiere:[/red] [italic]{message}[/italic]")
        time.sleep(1.5)

    def special_message(self, trigger):
        messages = self.special_message_new.get(trigger, [])
        if messages:
            message = random.choice(messages)
            console.print(f"\n[red]Il Banchiere:[/red] [italic]{message}[/italic]")
            time.sleep(1)

    def request_loan_story(self, tier):
        """Racconta una storia delle Backrooms basata sulla fascia di prestito"""
        return random.choice(self.stories.get(tier, self.stories[1]))

    def request_loan_malus_description(self, tier):
        """Descrivi il malus del prestito in modo tematico"""
        return self.descriptions.get(tier, self.descriptions[1])

    def loan_response(self, response_type):
        """Gestisce le risposte per i prestiti con integrazione delle Backrooms"""
        if response_type.startswith('tier'):
            tier = int(response_type[-1])
            story = self.request_loan_story(tier)
            malus = self.request_loan_malus_description(tier)
            console.print(f"\n[red]Il Banchiere sussurra:[/red] {story}")
            time.sleep(1)
            console.print(f"[red]Il Banchiere sorride:[/red] {malus}")
        elif response_type in self.loan_responses:
            response = random.choice(self.loan_responses[response_type])
            console.print(f"\n[red]Il Banchiere:[/red] {response}")
        time.sleep(1)

    def membership_response(self, type='offer'):
        responses = self.membership_responses.get(type, self.membership_responses['offer'])
        message = random.choice(responses)
        console.print(f"\n[red]Il Banchiere:[/red] [italic]{message}[/italic]")
        time.sleep(1.5)

    def secret_ending_response(self, type='first_secret'):
        responses = self.secret_ending_responses.get(type, self.secret_ending_responses['first_secret'])
        message = random.choice(responses)
        console.print(f"\n[red]Il Banchiere:[/red] [italic]{message}[/italic]")
        time.sleep(2)

    def bet_behind_response(self, type='follow'):
        responses = self.bet_behind_responses.get(type, self.bet_behind_responses['follow'])
        message = random.choice(responses)
        console.print(f"\n[red]Il Banchiere:[/red] [italic]{message}[/italic]")
        time.sleep(1.5)