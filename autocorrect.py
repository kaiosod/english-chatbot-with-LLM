from gramformer import Gramformer
from spellchecker import SpellChecker

# https://github.com/PrithivirajDamodaran/Gramformer

#Spelling verification
def spell_checker(input_text):
    text = input_text
    spell = SpellChecker(language="en")

    words = text.split()

    all_words = []

    for word in words:
        corrected_word = spell.correction(word)
        all_words.append(corrected_word)

    all_words = " ".join(all_words)

    return all_words

# Grammar verification
def grammar_checker(input_text):
    gf = Gramformer(models = 1, use_gpu=False)

    input_text2 = spell_checker(input_text)
    output = gf.correct(input_text2, max_candidates=1)

    if str(output)[2:-3] == input_text and input_text2 == input_text:
        return 1
    else:
        return str(output)[2:-3]

    