from gramformer import Gramformer
import torch

# def set_seed(seed):
#   torch.manual_seed(seed)
#   if torch.cuda.is_available():
#     torch.cuda.manual_seed_all(seed)

# set_seed(1212)

def grammar_checker(input_text):
    gf = Gramformer(models = 1, use_gpu=False)
    # mytext = """I is testng grammar tool using python. It does not costt anythng."""
    output = gf.correct(input_text, max_candidates=1)
    # print(type(output))
    # print(type(input_text))

    # print()
    # print(input_text)

    if str(output)[2:-2] == input_text:
        return ""
    else:
        return output

    