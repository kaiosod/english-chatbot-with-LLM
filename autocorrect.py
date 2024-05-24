from gramformer import Gramformer


# https://github.com/PrithivirajDamodaran/Gramformer

def grammar_checker(input_text):
    gf = Gramformer(models = 1, use_gpu=False)
    output = gf.correct(input_text, max_candidates=1)

    if str(output)[2:-3] == input_text:
        return 1
    else:
        return str(output)[2:-3]

    