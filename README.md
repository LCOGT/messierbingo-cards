# messierbingo-cards
Simple app to generate the bingo cards for Messier Bingo

This code uses `Jinja2` templates to generate PDFs of Bingo Cards for [Messier Bingo](https://messierbingo.lco.global). Each card is a random selection of the 110 objects from the [Messier Catalogue](https://en.wikipedia.org/wiki/Messier_object).

All of the images used on the cards and in the game were taken with [Las Cumbres Observatory](https://lco.global) telescopes.

## Usage
```bash
python makecards.py --cards 30
```
