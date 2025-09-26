# Hackaton Teatro 4D

> Gestionale Rete 4D Teatro

## Utilizzo

installa il venv:

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```



## pagine create

- [x] home
- [ ] dettaglio prodotti
- [ ] cronologia scambi/prodotti
- [ ] inserimento prodotto
- [ ] aggiungi noleggio
- [ ] home
- [ ] dettaglio prodotti
- [ ] cronologia scambi/prodotti
- [ ] inserimento prodotto
- [ ] aggiungi noleggio

## to-do

- [x] aggiungere test mail (risolto con un log csv, meno figo ma funzionale il doppio)
- [x] login per entrare nel gestionale
- [x] Reimposta la password (scrauso)
- [x] sistemare qrcode
- [x] aggiungere link alla scatola nella descrizione oggetto
- [ ] sistemare front-end
- [ ] metterlo online
- [ ] stampare qr code
- [ ] popolare database con dati sensati
- [ ] check generale
- aggiungi la possibilità di modificare i tuoi oggetti/scatole/location, eliminarli

## feature del gestionale


- oggetti salvati e visualizzabili con tutte le loro caratteristiche (titolo, descrizione, proprietario, foto, scatola se presente e location(luogo fisico in cui si trova l'oggetto all'interno della sede) e categoria)
- scatole salvate e visualizzabili che contengono oggetti con descrizione
- location in cui sono depositate le scatole
- possibilità di muovere oggetti fra scatole
- possibilità di aggiungere,modificare o eliminare oggetti, scatole e location
- possibilità di scannerizzare tramite QR code gli oggetti o le scatole per avere un immediato resoconto delle caratteristiche
- possibilità di muovere oggetti fra sedi (prestandoli)
- cronologia dei prestiti (sede che possiede l'oggetto, sede in cui si trova l'oggetto, data di prestito)
- possibilità di filtrare le scatole per location e cercarle per nome
- possibilità di cercare gli oggetti per nome