# import random

# from django.http import JsonResponse
# from django.shortcuts import redirect, render

# # ==== Main Views ====


# def index(request):
#     """Landing page – initializes session variables."""
#     request.session.setdefault('gold', 0)
#     request.session.setdefault('activities', [])
#     request.session.setdefault('used_buildings', [])
#     request.session.setdefault('casino_visits', 0)

#     # Pop the sound so it only plays once
#     sound_to_play = request.session.pop('sound_to_play', None)

#     return render(request, 'index.html', {
#         'sound_to_play': sound_to_play  # ✅ Pass it to the template!
#     })


# def ninja_gold_game(request):
#     """Render the main game page with building info."""
#     building_descriptions = {
#         'farm': {
#             'name': 'Farm',
#             'earn_message': 'Earns 50-100 ounces of gold',
#             'visited_message': "You've searched on a Farm.",
#         },
#         'cave': {
#             'name': 'Cave',
#             'earn_message': 'Earns 100-250 ounces of gold',
#             'visited_message': "You've searched in a Cave.",
#         },
#         'house': {
#             'name': 'House',
#             'earn_message': 'Earns 20-50 ounces of gold',
#             'visited_message': "You stole from a House.",
#         },
#         'casino': {
#             'name': 'Casino',
#             'earn_message': 'Earn/lose 0-50 ounces of gold',
#             'visited_message': "You've been to the Casino.",
#         }
#     }

#     return render(request, 'ninja_gold.html', {
#         'building_descriptions': building_descriptions
#     })


# def get_gold_value(request):
#     """Return current gold amount in session."""
#     return JsonResponse({'gold': request.session.get('gold', 0)})


# def reset(request):
#     """Clear all session data."""
#     request.session.clear()
#     return redirect('/')


# # ==== Core Game Logic ====

# def process_money(request):
#     """Process the result of clicking a building button."""
#     if request.method != 'POST':
#         return redirect('/')

#     building = request.POST.get('building')
#     if not building:
#         return redirect('/')

#     # Initialize missing session keys
#     session_defaults = {
#         'used_buildings': [],
#         'casino_visits': 0,
#         'activities': [],
#         'gold': 0,
#     }
#     for key, default in session_defaults.items():
#         request.session.setdefault(key, default)

#     logic = {
#         'farm': {
#             'range': (50, 100),
#             'message': "You found {gold} ounces of Gold on a Farm! Yay!",
#             'sound': 'static/sounds/farm.wav',
#         },
#         'cave': {
#             'range': (75, 150),
#             'message': "You found {gold} ounces of Gold in a Cave! Yay!",
#             'sound': 'static/sounds/cave.wav',
#         },
#         'house': {
#             'range': (20, 50),
#             'message': "You stole {gold} ounces of Gold from a House! Yay!",
#             'sound': 'static/sounds/house.wav',
#         },
#         'casino': {
#             'range': (-50, 50),
#             'messages': {
#                 'win': "You won {gold} ounces of Gold at the Casino! Yay!",
#                 'loss': "You lost {gold} ounces of Gold at the Casino! Boooo!!",
#                 'neutral': "You won nothing at the Casino. Oh well...",
#             },
#             'sounds': {
#                 'win': 'static/sounds/ka-ching.mp3',
#                 'loss': 'static/sounds/loss.wav',
#                 'neutral': 'static/sounds/ohwell.wav',
#             },
#         }
#     }

#     # Prevent duplicate building use (except casino)
#     if building != 'casino' and building in request.session['used_buildings']:
#         msg = f"Nothing more to find at the {building.capitalize()}."
#         request.session['activities'].append(msg)
#         request.session['sound_to_play'] = logic['casino']['sounds']['neutral']
#         return redirect('/')

#     # Handle casino rules
#     if building == 'casino':
#         if request.session['casino_visits'] >= 15:
#             request.session['activities'].append(
#                 "You reached the Casino visit limit (15). Take the GOLD and run!")
#             return redirect('/')
#         if request.session['gold'] <= 0:
#             request.session['activities'].append(
#                 "No Gold! No Casino! Search another area.")
#             return redirect('/')
#         request.session['casino_visits'] += 1

#     # Calculate and update gold
#     if building in logic:
#         if building != 'casino':
#             gold = random.randint(*logic[building]['range'])
#             request.session['gold'] += gold
#             request.session['used_buildings'].append(building)
#             request.session['activities'].append(
#                 logic[building]['message'].format(gold=gold))
#             request.session['sound_to_play'] = logic[building]['sound']
#         else:
#             gold = random.choices(
#                 [random.randint(-50, -1), random.randint(1, 50), 0],
#                 weights=[80, 13, 7], k=1
#             )[0]
#             request.session['gold'] += gold

#             if gold > 0:
#                 msg = logic['casino']['messages']['win'].format(gold=gold)
#                 sound = logic['casino']['sounds']['win']
#             elif gold == 0:
#                 msg = logic['casino']['messages']['neutral']
#                 sound = logic['casino']['sounds']['neutral']
#             else:
#                 msg = logic['casino']['messages']['loss'].format(
#                     gold=abs(gold))
#                 sound = logic['casino']['sounds']['loss']

#             request.session['activities'].append(msg)
#             request.session['sound_to_play'] = sound

#     # Check win/loss conditions
#     buildings_used = set(request.session['used_buildings'])
#     negative_gold = request.session['gold'] < 0
#     max_casino = request.session['casino_visits'] >= 15

#     request.session['all_lost_conditions_met'] = (
#         {'farm', 'cave', 'house'}.issubset(buildings_used) and negative_gold
#     )
#     request.session['win_condition_met'] = max_casino
#     # Placeholder for future use
#     request.session['broke_even_condition_met'] = 0

#     request.session.modified = True
#     return redirect('/')


import random

from django.http import JsonResponse
from django.shortcuts import redirect, render

LOCATIONS = {
    "farm": (50, 100),
    "cave": (75, 150),
    "house": (20, 50),
}

MAX_CASINO_VISITS = 15


def new_player(number):
    return {
        "name": f"Player {number}",
        "gold": 0,
        "used_buildings": [],
        "casino_visits": 0,
    }


def player_finished(player):
    # Players finish after 15 casino visits, or when they have
    # no gold left after searching all three locations.
    return (
        player["casino_visits"] >= MAX_CASINO_VISITS
        or (
            len(player["used_buildings"]) == 3
            and player["gold"] <= 0
        )
    )


def initialize_game(request):
    if "players" not in request.session:
        request.session["players"] = [new_player(1)]
        request.session["active_player"] = 0
        request.session["activities"] = []


def sync_current_player(request):
    """Keep the existing template working for the active player."""
    players = request.session["players"]
    player = players[request.session["active_player"]]

    request.session["gold"] = player["gold"]
    request.session["used_buildings"] = player["used_buildings"]
    request.session["casino_visits"] = player["casino_visits"]

    game_over = all(player_finished(p) for p in players)

    request.session["game_over"] = game_over

    # Existing sound/confetti flags apply to single-player mode.
    request.session["all_lost_conditions_met"] = (
        len(players) == 1
        and game_over
        and player["gold"] <= 0
    )
    request.session["win_condition_met"] = (
        len(players) == 1
        and game_over
        and player["gold"] > 0
    )
    request.session["broke_even_condition_met"] = False

    result = ""

    if game_over:
        if len(players) == 2:
            first, second = players

            if first["gold"] == second["gold"]:
                result = (
                    f"It's a tie! Both players finished with "
                    f"{first['gold']} ounces of gold."
                )
            else:
                winner = max(players, key=lambda p: p["gold"])
                result = (
                    f"{winner['name']} wins with "
                    f"{winner['gold']} ounces of gold!"
                )
        else:
            result = (
                f"Game over! You finished with "
                f"{player['gold']} ounces of gold."
            )

    request.session["game_result"] = result
    request.session.modified = True


def index(request):
    initialize_game(request)
    sync_current_player(request)

    sound_to_play = request.session.pop("sound_to_play", None)

    return render(request, "index.html", {
        "sound_to_play": sound_to_play,
    })


def start_game(request):
    if request.method != "POST":
        return redirect("/")

    count = request.POST.get("player_count")

    if count not in ("1", "2"):
        return redirect("/")

    request.session["players"] = [
        new_player(number)
        for number in range(1, int(count) + 1)
    ]
    request.session["active_player"] = 0
    request.session["mode_selected"] = True

    request.session["activities"] = []
    request.session.pop("sound_to_play", None)

    sync_current_player(request)
    return redirect("/")


def reset(request):
    """Reset the game and show the player choices again."""
    initialize_game(request)
    count = len(request.session["players"])

    request.session["players"] = [
        new_player(number)
        for number in range(1, count + 1)
    ]
    request.session["active_player"] = 0
    request.session["activities"] = []
    request.session["mode_selected"] = False
    request.session.pop("sound_to_play", None)

    sync_current_player(request)
    return redirect("/")


def get_gold_value(request):
    initialize_game(request)
    sync_current_player(request)
    return JsonResponse({"gold": request.session["gold"]})


def ninja_gold_game(request):
    return index(request)


def process_money(request):
    if request.method != "POST":
        return redirect("/")

    initialize_game(request)

    building = request.POST.get("building")

    if building not in (*LOCATIONS, "casino"):
        return redirect("/")

    players = request.session["players"]
    active = request.session["active_player"]
    player = players[active]
    activities = request.session["activities"]

    if player_finished(player):
        return redirect("/")

    if building in LOCATIONS:
        if building in player["used_buildings"]:
            return redirect("/")

        gold = random.randint(*LOCATIONS[building])
        player["gold"] += gold
        player["used_buildings"].append(building)

        actions = {
            "farm": "found {gold} ounces of Gold on a Farm! Yay!",
            "cave": "found {gold} ounces of Gold in a Cave! Yay!",
            "house": "stole {gold} ounces of Gold from a House! Yay!",
        }

        message = actions[building].format(gold=gold)
        sound = f"static/sounds/{building}.wav"

    else:
        if player["gold"] <= 0:
            activities.append(
                f"{player['name']}: No Gold! Search another area."
            )
            request.session["activities"] = activities
            return redirect("/")

        gold = random.choices(
            [
                random.randint(-50, -1),
                random.randint(1, 50),
                0,
            ],
            weights=[80, 13, 7],
            k=1,
        )[0]

        # A player cannot lose more gold than they have.
        gold = max(gold, -player["gold"])

        player["gold"] += gold
        player["casino_visits"] += 1

        if gold > 0:
            message = (
                f"won {gold} ounces of Gold at the Casino! Yay!"
            )
            sound = "static/sounds/ka-ching.mp3"
        elif gold < 0:
            message = (
                f"lost {abs(gold)} ounces of Gold "
                "at the Casino! Boooo!!"
            )
            sound = "static/sounds/loss.wav"
        else:
            message = "won nothing at the Casino. Oh well..."
            sound = "static/sounds/ohwell.wav"

    activities.append(f"{player['name']} {message}")

    # Keep the current player active until their game is finished.
    if player_finished(player):
        for next_player in range(active + 1, len(players)):
            if not player_finished(players[next_player]):
                request.session["active_player"] = next_player
                break

    request.session["players"] = players
    request.session["activities"] = activities
    request.session["sound_to_play"] = sound

    sync_current_player(request)
    return redirect("/")
