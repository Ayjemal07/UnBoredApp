#This file contains routes/blueprints

from flask import Blueprint, jsonify, render_template, session, request
from flask_login import current_user  # Import current_user here
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from openai import OpenAI
import os
from random import choice
from .models import Activity

main = Blueprint('main', __name__)

# Set your OpenAI API key
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))



def get_youtube_link(activity_name):
    """
    Gets a YouTube video link for the given activity name, using broader search and ranking.
    If quota is exceeded, returns a YouTube search link.

    Args:
        activity_name: The name of the activity.

    Returns:
        A string containing the YouTube video link or a YouTube search link if quota is exceeded.
    """

    youtube_api_key = os.getenv('YOUTUBE_API_KEY')
    if not youtube_api_key:
        raise ValueError("YouTube API key not found in environment variables")

    youtube = build('youtube', 'v3', developerKey=youtube_api_key)

    search_terms = [
        activity_name,
        f"{activity_name} tutorial",
        f"{activity_name} basics"
    ]

    try:
        candidate_videos = []
        for term in search_terms:
            request = youtube.search().list(
                q=term,
                part='snippet',
                maxResults=5  # Increase results for broader search
            )
            response = request.execute()
            if response['items']:
                for item in response['items']:
                    video_id = item['id'].get('videoId')
                    if not video_id:
                        continue
                    view_count = int(item['snippet'].get('viewCount', 0))
                    like_count = int(item['snippet'].get('likeCount', 0))
                    score = view_count + like_count
                    candidate_videos.append((video_id, score))

        if candidate_videos:
            candidate_videos.sort(key=lambda x: x[1], reverse=True)
            return f'https://www.youtube.com/watch?v={candidate_videos[0][0]}'

        print(f"No suitable video found for '{activity_name}'.")
        return ''

    except HttpError as e:
        if e.resp.status == 403 and 'quotaExceeded' in e.content.decode():
            print("YouTube quota exceeded.")
            return f'https://www.youtube.com/results?search_query=what+is+{activity_name}'

        raise



# Function to get Google search link
def get_google_link(activity_name,):
    query = f"{activity_name} near me"
    return f"https://www.google.com/search?q={query.replace(' ', '+')}"

# Function to get Meetup search link
def get_meetup_link(activity_name):
    query = f"{activity_name} near me"
    return f"https://www.meetup.com/find/?keywords={query.replace(' ', '%20')}"

# Function to get random activity details
def get_chatgpt_activity(exclude_activities,user_exists=False):

    exclude_list = ', '.join(exclude_activities) if exclude_activities else ''


    if user_exists:
        user_info={
            'interests': current_user.interests,
            'physical limitations': current_user.limitations,
            'user"s age': current_user.age,
            'types of activities interested':current_user.activity_types,
            'physical effort levels interested':current_user.physical_levels,
            'budget':current_user.budget,
            }
                                       
        prompt1 = f"""You are an expert in recommending activities and hobbies. 
        Based on the following user profile:{user_info},
        Suggest a single activity that fits the user's preferences and constraints. 
        Exclude activities from this list: {exclude_list}. 
        Ensure the activity name is concise and does not exceed 31 characters. 
        Provide only the activity name."""
        print(user_info)

    else:
        prompt1=f"""You are an expert in recommending activities and hobbies. 
        Suggest one activity that is enjoyable and worth trying. 
        Exclude activities from this list: {exclude_list}. 
        Ensure the activity name is concise and does not exceed 31 characters. 
        Provide only the activity name."""

        
    response1 = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[
            {"role": "system", "content": "You are an assistant providing activity and hobby suggestions."},
            {"role": "user", "content": prompt1},
        ],
        temperature=0.5,
        top_p=0.8
    )

    name = response1.choices[0].message.content.strip()

    # Second prompt to get the activity description
    prompt2 = f"""Double check your work before you reply.
    Provide a one-sentence description of what is {name}. 
    Character limit is strictly less than 130"""

    response2 = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[
            {"role": "system", "content": "You are an assistant providing activity and hobby suggestions."},
            {"role": "user", "content": prompt2},
        ],
        temperature=0.3,
    )

    description = response2.choices[0].message.content.strip()

    # Third prompt to get the reason why it's worth trying
    prompt3 = f"""Double check your work before you reply. 
    Explain in one-sentence why {name} is worth trying.
    Character limit for the sentence is strictly less than 130"""

    response3 = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[
            {"role": "system", "content": "You are an assistant providing activity and hobby suggestions."},
            {"role": "user", "content": prompt3},
        ],
        temperature=0.3,
    )

    why_worth = response3.choices[0].message.content.strip()

    # Get YouTube, Google, and Meetup links
    youtube_link = get_youtube_link(name)
    google_link = get_google_link(name)
    meetup_link = get_meetup_link(name)


    print("chatgpt suggestion")

    return {
        "name": name,
        "description": description,
        "why_worth": why_worth,
        "youtube": youtube_link,
        "google": google_link,
        "meetup": meetup_link
    }

@main.route('/')
def index():
    return render_template('home.html')


@main.route('/profile')
def profile():
    return render_template('profile.html')

@main.route('/suggest_activity', methods=['GET'])
def suggest_activity():
    click_count = int(request.args.get('clickCount', 0))
    user_exists = current_user.is_authenticated  # Adjust based on your user authentication method
    print(user_exists)


    if 'seen_activities' not in session:
        session['seen_activities'] = []
    
    seen_activities = session['seen_activities']

    cherry_pick_activities = Activity.query.filter_by(cherry_picked=True).all()
    cherry_pick_activities = [activity for activity in cherry_pick_activities if activity.name not in seen_activities]

    selected_activity = None

    if click_count < 3:
        if cherry_pick_activities:
            selected_activity = choice(cherry_pick_activities)
            seen_activities.append(selected_activity.name)
            print(seen_activities)

    else:
        print("here")
        selected_activity = get_chatgpt_activity(seen_activities,user_exists)
        seen_activities.append(selected_activity['name'])
        print(seen_activities)
    
    #save the updated seen activities to session
    session['seen_activities'] = seen_activities


    if isinstance(selected_activity, Activity):
        # Serialize the activity and return as JSON response
        serialized_activity = {
            "id": selected_activity.id,
            "name": selected_activity.name,
            "description": selected_activity.description,
            "why_worth": selected_activity.why_worth,
            "youtube": selected_activity.youtube_link,
            "google": selected_activity.google_link,
            "meetup": selected_activity.meetup_link,
            "cherry_picked": selected_activity.cherry_picked
        }
        return jsonify(serialized_activity)
    
    else:
        # If selected_activity is not an instance of Activity, handle accordingly
        return jsonify(selected_activity)
    
@main.route('/reset_session', methods=['GET'])
def reset_session():
    session.pop('click_count', None)
    session.pop('seen_activities', None)
    print("Session after reset:", session)
    return jsonify({"message": "Session reset"})
