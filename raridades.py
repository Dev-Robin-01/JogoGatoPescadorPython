import random


PEIXES_POR_RARIDADE = {
    "Comum": [
        "Fish(C1).png",
        "Fish(C2).png",
        "Fish(C3).png",
        "Fish(C4).png",
        "Fish(C5).png",
        "Fish(C6).png",
        "Fish(C7).png",
        "Fish(C8).png",
        "Fish(C9).png",
        "Fish(C10).png",
    ],
    "Raro": [
        "Fish(R1).png",
        "Fish(R2).png",
        "Fish(R3).png",
        "Fish(R4).png",
        "Fish(R5).png",
        "Fish(R6).png",
    ],
    "Épico": [
        "Fish(E1).png",
        "Fish(E2).png",
        "Fish(E3).png",
    ],
    "Lendário": [
        "Fish_King(L).png",
    ],
}


def raridades():
    raridade = random.choices(
        ["Comum", "Raro", "Épico", "Lendário"],
        weights=[60, 25, 10, 5],
        k=1,
    )[0]

    return raridade, random.choice(PEIXES_POR_RARIDADE[raridade])
