# dialogue/intro.py

def get_intro_lines():
    F = "assets/Schoolgirl/Faces/"
    S = "assets/Scenes/"

    return [
        {
            "scene": S + "intro_hallway.png",
            "name": "Schoolgirl",
            "face": F + "Calm.png",
            "text": "…So you really woke up here."
        },

        {
            "scene": S + "intro_hallway.png",
            "name": "Schoolgirl",
            "face": F + "Indifference.png",
            "text": "Interesting. Most of them stay asleep."
        },

        {
            "name": "Schoolgirl",
            "face": F + "Smile.png",
            "text": "Relax. If this were a dream, you'd already be gone."
        },

        {
            "name": "Schoolgirl",
            "face": F + "Calm.png",
            "text": "This place used to be loud. Bells. Footsteps. Voices."
        },

        {
            "name": "Schoolgirl",
            "face": F + "Awkwardness.png",
            "text": "Now it only responds to movement… and fear."
        },

        {
            "name": "Schoolgirl",
            "face": F + "Indifference.png",
            "text": "They will come in waves. They always do."
        },

        {
            "name": "Schoolgirl",
            "face": F + "Passive aggression.png",
            "text": "Timing matters more than strength. Swing wildly and you won’t last."
        },

        {
            "name": "Schoolgirl",
            "face": F + "Calm.png",
            "text": "Defend when you must. Hesitate when you can."
        },

        {
            "name": "Schoolgirl",
            "face": F + "Passion.png",
            "text": "Coins fall from mistakes. Collect them. Mistakes have value here."
        },

        {
            "name": "Schoolgirl",
            "face": F + "Smile.png",
            "text": "Don’t bother looking for exits."
        },

        {
            "name": "Schoolgirl",
            "face": F + "Calm.png",
            "text": "When the bell rang… no one left."
        },

        {
            "name": "Schoolgirl",
            "face": F + "Passion.png",
            "text": "Stay alive long enough… and maybe you’ll understand why."
        },
    ]