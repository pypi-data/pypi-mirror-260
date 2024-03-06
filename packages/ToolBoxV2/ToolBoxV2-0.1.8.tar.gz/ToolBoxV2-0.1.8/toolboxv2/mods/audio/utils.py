
def split_text_x_symbol(text: str, symbol: str='\n\n', split_n: int=2):
    # Initialisiere eine Liste, um die gesplitteten Textteile zu speichern
    split_texts = []
    # Initialisiere eine temporäre Variable, um den aktuellen Textabschnitt zu speichern
    current_text = ''
    # Initialisiere einen Zähler für die Punkte
    dot_count = 0

    text = text.strip()

    def get_parts(s: str, part_len: int) -> list:
        parts = []
        for i in range(len(s) - part_len + 1):
            yield s[i:i + part_len]

    # Durchlaufe jeden Charakter im Text
    for char in get_parts(text, len(symbol)):
        # Füge den aktuellen Charakter zum aktuellen Textabschnitt hinzu
        current_text += char
        # Überprüfe, ob der Charakter ein Punkt ist
        if char in symbol:
            # Erhöhe den Punktezähler
            dot_count += 1
            # Überprüfe, ob drei Punkte erreicht wurden
            if dot_count == split_n:
                # Füge den aktuellen Textabschnitt zur Liste hinzu
                split_texts.append(current_text)
                # Setze den aktuellen Textabschnitt und den Punktezähler zurück
                current_text = ''
                dot_count = 0

    # Überprüfe, ob nach dem letzten Punkt noch Text übrig ist
    if current_text:
        # Füge den verbleibenden Text zur Liste hinzu
        split_texts.append(current_text)

    return split_texts
