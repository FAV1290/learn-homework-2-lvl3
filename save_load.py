import os


def save_score(savepath, score):
    with open(savepath, 'w', encoding='utf-8') as file_handler:
        file_handler.write(str(score))


def load_score(savepath):
    try:
        with open(savepath, 'r', encoding='utf-8') as file_handler:
            score = int(file_handler.read())
        os.remove(savepath)
    except (OSError, ValueError):
        score = 0
    return score
