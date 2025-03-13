import os
import openai
import re #regular expressions module
from markupsafe import escape #protects projects against injection attacks
from megafit import app
import sys 
sys.dont_write_bytecode = True
from flask import render_template, request, Flask, Blueprint, redirect, url_for, session
from megafit.database import users_collection
from bson.objectid import ObjectId

catalog_blueprint = Blueprint('catalog', __name__)

@catalog_blueprint.route('/catalog',methods=['GET', 'POST'])
@app.route('/catalog',defaults={'route_with_name': None})
@app.route('/catalog/<route_with_name>')
def catalog(route_with_name):

  # Set default catalog me message and team member names.
    team_names = ["Biceps", "Quads", "Glutes", "Hamstrings", "Back", "Triceps", "Shoulders", "Abs", "Chest"]
    team_description = ["flexes the elbow and rotate the forearm", "hip flexor and a knee extensor",
                        "abduction and extension of the thigh", "back of the thigh that begin at the pelvis",
                        "movement of the thoracic cage and flexion of the upper vertebral column and head",
                        "on the dorsal part of the upper arm",
                        "The muscles of the shoulder play a critical role in providing stability to the shoulder joint",
                        "support the trunk, allow movement", "thick, fan-shaped muscle"]
    team_images = ["biceps.png", "quads.png", "glutes.png", "hamstrings.png", "back.png", "triceps.png", "shoulders.png", "abs.png", "chest.png"]
    bicep_exercises = [
        {"name": "Hammer Curls", 
            "favorited": False, 
            "description": "This exercise involves curling dumbbells with a neutral grip to target the biceps and forearm muscles.", 
            "video_url":"https://www.youtube.com/embed/WGTCVgCqLqM?si=P-7VAJ6rZauUIolv"},
        {"name": "Barbell Curls", 
            "favorited": False,
            "description": "Performed by curling a barbell while keeping the upper arms stationary, this exercise focuses on biceps hypertrophy.", 
            "video_url":"https://www.youtube.com/embed/dDI8ClxRS04?si=jrpD8Fhb6cTd4mwo"},
        {"name": "Reverse Curls", 
            "favorited": False, 
            "description": "Curling a barbell with an overhand grip to strengthen the brachioradialis and biceps", 
            "video_url":"https://www.youtube.com/embed/eve_ZgHapkw?si=J84vpK5xLIE1bkah&amp;start=19"},
        {"name": "Preacher Curls", 
            "favorited": False,
            "description": "Curling a barbell or dumbbell on a preacher bench isolates and enhances biceps contraction.",
            "video_url": "https://www.youtube.com/embed/Ja6ZlIDONac?si=5pHoFyflcf-0jHed"},
        {"name": "Spider Curls", 
            "favorited": False, 
            "description": "Performed prone on an incline bench, this curl variant focuses intensely on bicep peaks by limiting shoulder movement.", 
            "video_url":"https://www.youtube.com/embed/ke2shAeQ0O8?si=lINI9wC5vk_oS2Cm"},
        {"name": "Incline Curls", 
            "favorited": False, 
            "description": "Curling dumbbells while seated back on an incline bench to increase the biceps' stretch and contraction.", 
            "video_url":"https://www.youtube.com/embed/51zzhEn8DxM?si=hp_E41xHuk76MZSc&amp;start=19"}
        ]
    quad_exercises = [
        {"name": "Squats", 
            "favorited": False , 
            "description": "A compound movement targeting the quadriceps, hamstrings, and glutes with variations affecting depth and muscle focus.",
            "video_url":"https://www.youtube.com/embed/EbOPpWi4L8s?si=IDEZisTej50_oWwx&amp;start=5"}, 
        {"name": "Leg Extensions", 
            "favorited": False,
            "description": "An isolation exercise targeting the quadriceps by extending the knee against weighted resistance.",
            "video_url":"https://www.youtube.com/embed/swZQC689o9U?si=GQHr_S3HPcCuFtE1&amp"}, 
        {"name": "Lunges", 
            "favorited": False, 
            "description": "A versatile lower body workout that primarily targets the quadriceps, along with glutes and hamstrings.",
            "video_url":"https://www.youtube.com/embed/ASdqJoDPMHA?si=GC3jjVNBhtXN_ePG&amp"},
        {"name": "Goblet squats", 
            "favorited": False,
            "description": "Performed by squatting with a dumbbell held at chest level, focusing on the quads and core stabilization.",
            "video_url":"https://www.youtube.com/embed/CkFzgR55gho?si=_EOuE1-7ey5asosH&amp;start=18"},
        {"name": "Sissy squats",
            "favorited": False, 
            "description": "This exercise isolates the quadriceps by bending the knees to lean backward while bodyweight or machine provides resistance.", 
            "video_url":"https://www.youtube.com/embed/JGD_aMeKBJY?si=OJjSNcxZghhY0nHH&amp"},
        {"name": "Leg press", "favorited": False, "description": "A machine-based exercise targeting the quadriceps, hamstrings, and glutes by pressing weight away from the body.", "video_url":"https://www.youtube.com/embed/yZmx_Ac3880?si=PnWQ5Rsd7Wpd4Buz&amp"}
        ]
    glute_exercises = [
        {"name": "Hip Thrusts", 
            "favorited": False, 
            "description": "A ground-based movement that emphasizes glute activation and hip extension.", 
            "video_url":"https://www.youtube.com/embed/kkk-4_Odqtk?si=XpRMlhHO_9C77ZQW&amp"}, 
        {"name": "Glute Bridges", 
            "favorited": False, 
            "description": "A compound lift that emphasizes the hamstrings and glutes, involving a hip-hinge movement.",
            "video_url":"https://www.youtube.com/embed/XLXGydU5DdU?si=EDdymNv2RVVwfYMY&amp"},
        {"name": "RDL's", 
            "favorited": False, 
            "description": "A functional exercise targeting the glutes and thighs by stepping onto an elevated platform.",
            "video_url":"https://www.youtube.com/embed/hQgFixeXdZo?si=7GZOgmqhDXIyyskp&amp"},
        {"name": "Kickbacks",
            "favorited": False,
            "description": "This targets the glutes by kicking the leg back against resistance in a standing or hands-and-knees position.",
            "video_url":"https://www.youtube.com/embed/50uCtMJze0s?si=g3JYTiwaLkBLUyXv&amp"},
        {"name": "Step ups",
            "favorited": False, 
            "description": "A functional exercise targeting the glutes and thighs by stepping onto an elevated platform.", 
            "video_url":"https://www.youtube.com/embed/elhu-WC1qk4?si=Wja73VzfzVo5PKYU&amp"},
        {"name": "Bulganin spilt squat", 
         "favorited": False, 
         "description": "A single-leg exercise where one foot is elevated behind you on a bench, focusing on the quadriceps, hamstrings, and glutes of the front leg.", 
         "video_url":"https://www.youtube.com/embed/vgn7bSXkgkA?si=CHBxO4u8X938Ba3O&amp"}
        ]
    hamstring_exercises = [
        {"name": "Seated Leg Curls", 
            "favorited": False, 
            "description": "This exercise targets the hamstrings by curling the legs towards the buttocks while seated.", 
            "video_url":"https://www.youtube.com/embed/_qwLdYywo_A?si=qU_k4ru86DMJrCRT&amp"}, 
        {"name": "Laying Leg Curls", 
            "favorited": False, 
            "description": "Performed prone to isolate and engage the hamstrings through a curling motion.", 
            "video_url": "https://www.youtube.com/embed/SiwJ_T62l9c?si=TD7Z4_fASzHGMSIw&amp"}, 
        {"name": "Standing Leg Curls", 
            "favorited": False, 
            "description": "An isolation move that targets one hamstring at a time by curling the leg against resistance.", 
            "video_url":"https://www.youtube.com/embed/N6FVnaasdq0?si=DIQGezgPoW5FIWjY&amp"},
        {"name": "Single leg deadlift", 
            "favorited": False, 
            "description": "A balance-focused movement that engages the hamstrings and glutes of the working leg.", 
            "video_url":"https://www.youtube.com/embed/lI8-igvsnVQ?si=RbGrPD7PwDki27Qs&amp"},
        {"name": "Good-mornings", 
            "favorited": False, 
            "description": "An exercise emphasizing the lower back, hamstrings, and glutes through a hip-hinge movement.", 
            "video_url":"https://www.youtube.com/embed/OWz0f3CN_xg?si=XwJPm7AexhKik2xQ&amp;start=13"},
        {"name": "Nordic hamstring curls", 
            "favorited": False, 
            "description": "A partner-assisted or machine-supported exercise that intensely targets hamstring strength and resilience.", 
            "video_url":"https://www.youtube.com/embed/3-4pKUhkzoQ?si=9TNuPTd7EZsywHEC&amp"}
        ]
    back_exercises = [
        {"name": "Lat Pulldown", 
            "favorited": False, 
            "description": "A cable-based exercise where you pull a weighted bar down towards your chest to target the latissimus dorsi muscles of the back.", 
            "video_url":"https://www.youtube.com/embed/AOpi-p0cJkc?si=4QnfYAhJg7vikMqj"}, 
        {"name": "Seated Row", 
            "favorited": False, 
            "description": "This machine or cable-based exercise involves pulling weights towards your torso, engaging the middle back, biceps, and lats.", 
            "video_url":"https://www.youtube.com/embed/vwHG9Jfu4sw?si=wuadZhkp8KspKctN"}, 
        {"name": "Pull ups", 
            "favorited": False, 
            "description": "An upper-body strength exercise where you lift your body up while hanging from a bar, primarily targeting the latissimus dorsi.", 
            "video_url":"https://www.youtube.com/embed/p40iUjf02j0?si=ZaNd8Dm04d4aw-ci&amp;start=24"},
        {"name": "Barbell Row", 
            "favorited": False, 
            "description": "Performed by bending forward and pulling a barbell towards your stomach, it primarily works the upper and middle back muscles.", 
            "video_url":"https://www.youtube.com/embed/6jPxFjRBV9s?si=lCyS0q-P27KOGWqX&amp"},
        {"name": "Shrugs", 
            "favorited": False, 
            "description": "This exercise involves lifting the shoulders towards the ears to isolate and build the upper trapezius muscles of the neck and shoulders.", 
            "video_url":"https://www.youtube.com/embed/JatJyKQhjX4?si=Q4s5hs0-plMGRePR&amp"},
        {"name": "Austrailian pull ups", 
            "favorited": False, 
            "description": "Performed under a bar at waist height, this horizontal pull-up focuses on the upper back, shoulders, and arms, suitable for beginners or as a regression from traditional pull-ups.", 
            "video_url":"https://www.youtube.com/embed/li7pwEmEcZY?si=NMF4YHnl98rod9Lz&amp"}
        ]
    tricep_exercises = [
        {"name": "Tricep Push Down", 
            "favorited": False, 
            "description": "A cable exercise where you push a bar or rope attachment downward against resistance to target the triceps muscles.", 
            "video_url":"https://www.youtube.com/embed/JDEDaZTEzGE?si=uYyNCEle8DHzG5XV&amp"}, 
        {"name": "Skullcrushers", 
            "favorited": False, 
            "description": "An exercise performed by lying on a bench and extending weights from near the head to above by bending and straightening the elbows, focusing on the triceps.", 
            "video_url":"https://www.youtube.com/embed/9baX4-wEYx8?si=cHrVzoDOsJ3do7VZ&amp;start=18"}, 
        {"name": "Closegrip Benchpress", 
            "favorited": False, 
            "description": "A variation of the bench press where the hands are placed closer together to emphasize the triceps along with the chest.", 
            "video_url":"https://www.youtube.com/embed/wxVRe9pmJdk?si=pwqkrr3fms-cTdyN&amp;start=9"},
        {"name": "Tricep kickbacks", 
            "favorited": False, 
            "description": "Involves bending forward with one arm supporting the body and the other extending a dumbbell back and up to isolate the triceps.", 
            "video_url":"https://www.youtube.com/embed/ZO81bExngMI?si=qp951Vg7ri1m5Ms3&amp"},
        {"name": "Diamond push ups", 
            "favorited": False, 
            "description": "Performed with the hands together under the chest forming a diamond shape, targeting the triceps and the inner chest.", 
            "video_url":"https://www.youtube.com/embed/jaxbEHLC4qU?si=hNrr64DpEkBQXVki&amp;start=6"},
        {"name": "Dips", 
            "favorited": False, 
            "description": "This bodyweight exercise requires lowering and raising the body on parallel bars or rings, heavily engaging the triceps.", 
            "video_url":"https://www.youtube.com/embed/ynm9hhHJFEU?si=40tLQmFB2PkWTBWp&amp"}
        ]
    shoulder_exercises = [
        {"name": "Front raise", 
            "favorited": False, 
            "description": "This bodyweight exercise requires lowering and raising the body on parallel bars or rings, heavily engaging the triceps.", 
            "video_url":"https://www.youtube.com/embed/hRJ6tR5-if0?si=A2MTMjAXJa2x6A8h&amp"},
        {"name": "Overhead press", 
            "favorited": False,
            "description": "Performed with the hands together under the chest forming a diamond shape, targeting the triceps and the inner chest.", 
            "video_url":"https://www.youtube.com/embed/boUVD0pCGCk?si=0vYm1BUJkDJjLlbb&amp;start=75"},
        {"name": "Arnold press", 
            "favorited": False, 
            "description": "Involves bending forward with one arm supporting the body and the other extending a dumbbell back and up to isolate the triceps.", 
            "video_url":"https://www.youtube.com/embed/jeJttN2EWCo?si=auIYJux0vooYi4ki&amp"},
        {"name": "Lateral Raises", 
            "favorited": False, 
            "description": "An exercise performed by lying on a bench and extending weights from near the head to above by bending and straightening the elbows, focusing on the triceps.", 
            "video_url":"https://www.youtube.com/embed/wZnsZsMywrY?si=5-e_cm-DFjDSQOdp"}, 
        {"name": "Dumbbell Shoulderpress", 
            "favorited": False, 
            "description": "A cable exercise where you push a bar or rope attachment downward against resistance to target the triceps muscles.", 
            "video_url":"https://www.youtube.com/embed/HzIiNhHhhtA?si=S7Yg7BOW20ijx1Iv"}, 
        {"name": "Rear Delt Flies", 
            "favorited": False, 
            "description": "A variation of the bench press where the hands are placed closer together to emphasize the triceps along with the chest.", 
            "video_url":"https://www.youtube.com/embed/Y59M5fXn8bs?si=osg2i2KFUci43POg"}
        ]
    abs_exercises = [
        {"name": "Crunches", 
            "favorited": False, 
            "description": "A classic core exercise focusing on the upper abdominal muscles by lifting the shoulders off the ground.", 
            "video_url":"https://www.youtube.com/embed/O0pIQ2UqeCY?si=g8Unf85tsxu6ddoa"}, 
        {"name": "Leg Raises", 
            "favorited": False, 
            "description": "Performed by lying flat and lifting the legs to a 90-degree angle, targeting the lower abdominals and hip flexors.", 
            "video_url":"https://www.youtube.com/embed/Zr-PtqcpeWM?si=IrkUb3nXS2m9HOXL"}, 
        {"name": "Sit ups", 
            "favorited": False, 
            "description": "A full-body core exercise that involves lifting the upper body all the way to the knees, engaging the entire abdominal region.", 
            "video_url":"https://www.youtube.com/embed/onaQ0v_J5uU?si=_E9Mlgs2yVdh2CH7"},
        {"name": "Russian twist", 
            "favorited": False, 
            "description": "This exercise involves twisting the torso from side to side while seated, engaging the obliques and entire core.", 
            "video_url":"https://www.youtube.com/embed/DJQGX2J4IVw?si=7fN--8o_Q41z8tlw"},
        {"name": "Bicycle crunch", 
            "favorited": False, 
            "description": "This is not a standard exercise, but rather a humorous phrase implying that genetics play a role in one's physical traits or limitations.", 
            "video_url":"https://www.youtube.com/embed/1we3bh9uhqY?si=33lq3x4Lno69-rYE&amp;start=8"},
        {"name": "plank", 
            "favorited": False, 
            "description": "A static hold exercise where you maintain a straight body line from head to heels, focusing on the core, shoulders, and back.", 
            "video_url":"https://www.youtube.com/embed/rerKy2AEHz4?si=N4hG6vObBzfenX4O&amp"}
        ]
    chest_exercises = [
        {"name": "Dumbbell bench press", 
            "favorited": False, 
            "description": "A variation of the bench press using dumbbells, allowing a greater range of motion and balanced muscle development.", 
            "video_url":"https://www.youtube.com/embed/YQ2s_Y7g5Qk?si=ZdtMtUHnnFqw2im2&amp"},
        {"name": "Bench Press", 
            "favorited": False, 
            "description": "A fundamental compound exercise involving pressing a barbell from the chest up to strengthen the pectorals, triceps, and shoulders.", 
            "video_url":"https://www.youtube.com/embed/gRVjAtPip0Y?si=nZXS0ZqAltt8y8Y5&amp;start=34"}, 
        {"name": "Pec Flies", 
            "favorited": False, 
            "description": "Performed on a flat bench with dumbbells, this exercise involves moving the arms in an arcing motion to target the chest muscles.", 
            "video_url":"https://www.youtube.com/embed/jiitI2ma3J4?si=ERiw__sLQea-iGVq&amp"}, 
        {"name": "Incline bench press", 
            "favorited": False, 
            "description": "Similar to the bench press but performed on an inclined bench, focusing more on the upper chest and shoulders.", 
            "video_url":"https://www.youtube.com/embed/5kyLUGVq_pk?si=ovzERDb2PLt_fXxZ&amp"},
        {"name": "push ups", 
            "favorited": False, 
            "description": "A bodyweight exercise that involves lowering and raising the body using the arms, targeting the chest, shoulders, and triceps.", 
            "video_url":"https://www.youtube.com/embed/FaIpD_zfrJI?si=aWWTuNNvJCD63F1c&amp;start=5"},
        {"name": "cable flies", 
            "favorited": False, 
            "description": "This exercise uses a cable machine to perform a chest fly motion from various angles to isolate and define the chest muscles.", 
            "video_url":"https://www.youtube.com/embed/PRw7ieDBLl4?si=rWKx6uE7HAXNX0Rx&amp"}
        ]
    team_exercises = [bicep_exercises, quad_exercises, glute_exercises, hamstring_exercises, back_exercises,
                      tricep_exercises, shoulder_exercises, abs_exercises, chest_exercises]
    
    # Combine team names and descriptions, images, and exercises into a single list of dictionaries
    team_info = [{'name': name, 'description': description, 'image': image, 'exercises': exercises} for name, description, image, exercises in zip(team_names, team_description, team_images, team_exercises)]
    cleaned_name = "Megafit"
    
    user_favorites = []

    # Check if a user is logged in and fetch their favorite workouts
    if 'username' in session:
        username = session['username']
        user_doc = users_collection.find_one({'username': username})
        if user_doc and 'favorite_workouts' in user_doc:
            user_favorites = user_doc['favorite_workouts']

    # Now, update the team_info structure to mark exercises as favorited
    for team in team_info:
        for exercise in team['exercises']:
            exercise['favorited'] = exercise['name'] in user_favorites

    search_query = request.args.get('search')
    if search_query:
        search_query = escape(search_query).lower()
        filtered_team_info = [member for member in team_info 
                            if search_query in member['name'].lower()
                            or search_query in member['description'].lower()
                            or any(search_query in exercise['name'].lower() or search_query in exercise['description'].lower() for exercise in member['exercises'])]
        return render_template('catalog.html', team_info=filtered_team_info, search_query=search_query)

    if route_with_name:
        route_with_name = escape(route_with_name)  # Sanitize the input
        is_english_alphabetic = re.match("[a-zA-Z]+", route_with_name)
        if is_english_alphabetic:
            cleaned_name = is_english_alphabetic.group(0)
            if cleaned_name in team_names:
                # Pass the combined team_info to the template
                return render_template('catalog.html', catalog_name=cleaned_name, catalog_catalog=cleaned_name, team_info=team_info)

    # For the default route or if no specific team member is matched, also pass team_info
    return render_template('catalog.html', catalog_name=cleaned_name, team_info=team_info)

@catalog_blueprint.route('/add_favorite', methods=['POST'])
def add_favorite():
    username = session.get('username') #gets user from session
    
    if 'username' not in session:
            return redirect(url_for('login'))  # Redirect to login if no user is in session

    selected_favorites = request.form.getlist('favorite_workouts')

    # Update the user's document with the selected favorite workouts
    users_collection.update_one(
        {'username': username},
        {'$set': {'favorite_workouts': selected_favorites}}
    )

    return redirect(url_for('.catalog'))