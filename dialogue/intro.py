# dialogue/intro.py

def get_intro_lines():
    SG = "assets/Dialogue/Faces/Schoolgirl/"
    MY = "assets/Dialogue/Faces/Mysterious/"
    SCENE = "assets/Scenes/intro_hallway.png"

    Darkout = (0,0,0)


    return [
        # --- Wake up ---
        {
            "name": "ME",
            "face": SG + "Awkwardness.png",
            "scene": SCENE,
            "text": "…Where am I?"
        },

        {
            "name": "???",
            "face": MY + "Calm.png",
            "scene": SCENE,
            "tint": Darkout,
            "text": "Awake already."
        },

        {
            "name": "ME",
            "face": SG + "Calm.png",
            "scene": SCENE,
            "text": "No… I was in class. Then— lights out."
        },

        {
            "name": "???",
            "face": MY + "Special.png",
            "scene": SCENE,
            "tint": Darkout,
            "text": "Don’t waste time trying to remember. Not yet."
        },

        # --- Discomfort ---
        {
            "name": "ME",
            "face": SG + "Indifference.png",
            "scene": SCENE,
            "text": "My body feels heavy… like I’m stuck in a bad dream."
        },

        {
            "name": "???",
            "face": MY + "Aggression.png",
            "scene": SCENE,
            "tint": Darkout,
            "text": "You are. But dreams still bite."
        },

        # --- Regaining control ---
        {
            "name": "ME",
            "face": SG + "Calm.png",
            "scene": SCENE,
            "text": "Okay… breathe. Focus."
        },

        {
            "name": "???",
            "face": MY + "Talk.png",
            "scene": SCENE,
            "tint": Darkout,
            "text": "Waves will come. You survive, you learn."
        },

        {
            "name": "ME",
            "face": SG + "Passion.png",
            "scene": SCENE,
            "text": "So it’s that kind of place… Fine."
        },

        # --- Rules / threat ---
        {
            "name": "???",
            "face": MY + "Smile.png",
            "scene": SCENE,
            "tint": Darkout,
            "text": "Good. Then listen."
        },

        {
            "name": "???",
            "face": MY + "Special.png",
            "scene": SCENE,
            "tint": Darkout,
            "text": "Attack with LEFT CLICK or ENTER. Block with RIGHT CLICK or E."
        },

        {
            "name": "ME",
            "face": SG + "Smile.png",
            "scene": SCENE,
            "text": "Got it."
        },

        # --- Final hook ---
        {
            "name": "???",
            "face": MY + "Special.png",
            "scene": SCENE,
            "tint": Darkout,
            "text": "When the bell rings… don’t look back."
        },
    ]