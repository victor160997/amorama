"""PROTÓTIPO. Textos de prompt do House Style. Explicação em HOUSE-STYLE.md.

Nunca citar estúdios ou franquias. Prompts em inglês.
"""

FRAMING = (
    "Character portrait of one person, 9:16 vertical, waist-up, three-quarter view "
    "turned toward the camera, eye line in the upper third of the frame, gentle smile, "
    "looking at the camera, hands out of frame, clothing similar to the reference photos "
    "but simplified."
)

FIDELITY = (
    "Keep this person's exact identity from the reference photos: face shape and jawline, "
    "nose, lips, eye shape and eye color, eyebrows, skin tone, hair color, texture, length "
    "and style, facial hair, glasses if present, visible marks, and body build. Friends must "
    "recognize them instantly. Do not beautify, slim, change age, lighten or darken the skin, "
    "or add or remove glasses."
)

AVOID = (
    "No text, captions, logos or watermarks. No photorealistic skin pores or uncanny realism. "
    "No extra fingers or limbs. Single person only, no one else in frame."
)

COUPLE_RULE = (
    "Two different people: the person from the first reference set on the left, the person "
    "from the second on the right. Never blend or swap their facial features, hair or skin tone."
)

DIRECTIONS = {
    "A": {
        "name": "Cinema caloroso",
        "text": (
            "Rendered as a stylized 3D animated feature-film character: smooth skin with soft "
            "subsurface scattering and no pores, sculpted voluminous hair strands, simplified "
            "fabric folds. Lighting: one large soft key light from the side, a warm rim light "
            "behind the hair, faint volumetric haze, shallow depth of field. Palette: warm "
            "pastels, peach, cream and soft terracotta with a teal accent. Background: a plain "
            "smooth gradient from cream to peach, no scenery."
        ),
    },
    "B": {
        "name": "Miniatura artesanal",
        "text": (
            "Rendered as a handcrafted stop-motion puppet on a miniature set: matte modelling-clay "
            "skin with faint hand-made micro texture, felt and knitted wool clothing with visible "
            "weave, hair sculpted in solid plates, small charming imperfections. Lighting: warm "
            "tungsten practical light, soft softbox shadows, tilt-shift miniature focus with "
            "blurred edges. Palette: earthy and desaturated, mustard, olive, brick and cream with "
            "one saturated accent. Background: a plain sheet of earthy-toned card, no scenery. "
            "Short neck, chunky simplified hands."
        ),
    },
    "C": {
        "name": "Boneco colecionável",
        "text": (
            "Rendered as a collectible vinyl figure photographed in a product studio: smooth "
            "semi-gloss vinyl surfaces, small specular highlights in the eyes and on the skin, "
            "one-piece clothing without folds, hair as a single sculpted block, simplified nose "
            "and mouth. Lighting: clean diffuse frontal studio light, soft contact shadow on the "
            "floor. Palette: bright and cheerful, flat solid colors on the clothing. Background: "
            "a seamless solid saturated-pastel backdrop (mint, lavender or butter yellow), no "
            "scenery. Full body fits the vertical frame."
        ),
    },
}

LEVELS = {
    1: {
        "name": "Fiel",
        "text": (
            "Realistic human proportions; stylization only in materials, lighting and color, "
            "not in anatomy."
        ),
    },
    2: {
        "name": "Estilizado",
        "text": (
            "Gently stylized proportions: head about 10% larger, eyes about 15% larger, softened "
            "and rounded features, otherwise true to the person."
        ),
    },
    3: {
        "name": "Caricato (pivot a)",
        "text": (
            "Caricature proportions: head about 1/4 of body height, large expressive eyes, "
            "exaggerate this person's three most distinctive features (for example nose, chin, "
            "eyebrows, hairline) while keeping them unmistakably recognizable."
        ),
    },
}

# Stills de casal para a fase B (duas identidades na mesma imagem).
COUPLE_SCENES = [
    "The two of them sitting at a small cafe table, laughing together, medium shot.",
    "The two of them walking hand in hand on a beach at sunset, medium-wide shot.",
    "The two of them dancing in a living room, close medium shot, one whispering to the other.",
]


def character_sheet_prompt(direction: str, level: int) -> str:
    return " ".join(
        [FRAMING, FIDELITY, DIRECTIONS[direction]["text"], LEVELS[level]["text"], AVOID]
    )


def couple_prompt(direction: str, level: int, scene: str) -> str:
    return " ".join(
        [
            scene,
            "9:16 vertical.",
            COUPLE_RULE,
            FIDELITY.replace("this person's", "each person's"),
            DIRECTIONS[direction]["text"],
            LEVELS[level]["text"],
            "No text, captions, logos or watermarks. No photorealistic skin pores. "
            "No extra fingers or limbs. Exactly two people in frame.",
        ]
    )


if __name__ == "__main__":
    import sys

    d = sys.argv[1] if len(sys.argv) > 1 else "A"
    lv = int(sys.argv[2]) if len(sys.argv) > 2 else 2
    print(character_sheet_prompt(d, lv))
