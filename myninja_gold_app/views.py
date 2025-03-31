import json  # Add this to the top
import os
import random

import requests
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import HttpResponse, redirect, render


def index(request):
    if 'gold' not in request.session:
        request.session['gold'] = 0
        print(f"Current gold in session: {request.session.get('gold')}")
    if 'activites' not in request.session:
        request.session['activites'] = []
    if 'used_buildings' not in request.session:
        request.session['used_buildings'] = []
    return render(request, 'index.html')


def ninja_gold_game(request):
    # Define building descriptions
    building_descriptions = {
        'farm': {
            'name': 'Farm',
            'earn_message': 'Earns 50-100 ounces of gold',
            'visited_message': "You've searched on a Farm.",
        },
        'cave': {
            'name': 'Cave',
            'earn_message': 'Earns 100-250 ounces of gold',
            'visited_message': "You've searched in a Cave.",
        },
        'house': {
            'name': 'House',
            'earn_message': 'Earns 20-50 ounces of gold',
            'visited_message': "You stole from a House.",
        },
        'casino': {
            'name': 'Casino',
            'earn_message': 'Earn/lose 0-50 ounces of gold',
            'visited_message': "You've been to the Casino.",
        }
    }

    # Initialize session variables if they don't exist
    if 'gold' not in request.session:
        request.session['gold'] = 0
    if 'activities' not in request.session:
        request.session['activities'] = []
    if 'visited_buildings' not in request.session:
        request.session['visited_buildings'] = []

    return render(request, 'ninja_gold.html', {
        'building_descriptions': building_descriptions
    })


def get_gold_value(request):
    gold = request.session.get('gold', 0)
    return JsonResponse({'gold': gold})


def process_money(request):
    print("The form has been submitted!")
    print(request.POST)

    # Safely get the building value from POST request
    building = request.POST.get('building')

    # Initialize session variables if they don't exist
    session_defaults = {
        'used_buildings': [],
        'casino_visits': 0,
        'activites': [],
        'gold': 0,
        'visited_buildings': [],
    }
    for key, default_value in session_defaults.items():
        if key not in request.session:
            request.session[key] = default_value

    # Define building logic
    building_logic = {
        'farm': {
            'min_gold': 50,
            'max_gold': 100,
            'message': "You Found {gold} ounces of Gold on a Farm! Yay!",
            'sound': 'static/sounds/farm.wav'
        },
        'cave': {
            'min_gold': 100,
            'max_gold': 250,
            'message': "You Found {gold} ounces of Gold in a Cave! Yay!",
            'sound': 'static/sounds/cave.wav'
        },
        'house': {
            'min_gold': 20,
            'max_gold': 50,
            'message': "You Stole {gold} ounces of Gold from a House! Yay!",
            'sound': 'static/sounds/house.wav'
        },
        'casino': {
            'min_gold': -50,
            'max_gold': 50,
            'message_win': "You Won {gold} ounces of Gold at the Casino! Yay!",
            'message_loss': "You Lost {gold} ounces of Gold at the Casino! Boooo!!",
            'message_neutral': "You Won nothing at the Casino. Oh Well...",
            'sound_win': 'static/sounds/win.wav',
            'sound_loss': 'static/sounds/loss.wav',
            'sound_neutral': 'static/sounds/ohwell.wav'
        }
    }

    # Prevent reusing a building (except Casino)
    if building in request.session['used_buildings'] and building != 'casino':
        return redirect('/')

    # Handle Casino-specific conditions
    if building == 'casino':
        if request.session['casino_visits'] >= 15:
            request.session['activites'].append(
                "You have reached the maximum number of Casino visits (15). Take the GOLD and Run!"
            )
            return redirect('/')
        if request.session['gold'] <= 0:
            request.session['activites'].append(
                "No Gold! No Casino! Search another area."
            )
            return redirect('/')

    # Process gold earnings/losses for the selected building
    if building in building_logic:
        if building != 'casino':
            # Regular buildings: Farm, Cave, House
            gold = random.randint(
                building_logic[building]['min_gold'], building_logic[building]['max_gold']
            )
            message = building_logic[building]['message'].format(gold=gold)
            sound = building_logic[building]['sound']

            request.session['gold'] += gold
            request.session['used_buildings'].append(building)
            request.session['activites'].append(message)
            request.session['sound_to_play'] = sound

        elif building == 'casino':
            # Casino logic
            request.session['casino_visits'] += 1
            gold = random.choices(
                population=[random.randint(-50, -1), random.randint(1, 50), 0],
                weights=[85, 10, 5],  # 85% lose, 10% win, 5% neutral
                k=1
            )[0]
            request.session['gold'] += gold

            if gold > 0:
                message = building_logic['casino']['message_win'].format(
                    gold=gold)
                sound = building_logic['casino']['sound_win']
            elif gold == 0:
                message = building_logic['casino']['message_neutral']
                sound = building_logic['casino']['sound_neutral']
            else:
                message = building_logic['casino']['message_loss'].format(
                    gold=abs(gold))
                sound = building_logic['casino']['sound_loss']

            request.session['activites'].append(message)
            request.session['sound_to_play'] = sound

        # Check if all conditions for "loss" are met
    farm_used = 'farm' in request.session['used_buildings']
    cave_used = 'cave' in request.session['used_buildings']
    house_used = 'house' in request.session['used_buildings']
    negative_gold = request.session['gold'] < 0
    max_casino_visits_reached = request.session['casino_visits'] >= 15

    request.session['all_lost_conditions_met'] = (
        farm_used and cave_used and house_used and negative_gold
    )
    print("All Lost Conditions Met:",
          request.session['all_lost_conditions_met'])

    request.session['win_condition_met'] = max_casino_visits_reached

    # Save session changes
    request.session.modified = True

    return redirect('/')


def get_gold_value(request):
    gold = request.session.get('gold', 0)
    return JsonResponse({'gold': gold})


def reset(request):
    request.session.clear()
    return redirect('/')
