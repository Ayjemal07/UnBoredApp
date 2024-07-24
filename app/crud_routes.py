from flask import Blueprint, request, jsonify
from .models import Activity, User, db
import os
from googleapiclient.discovery import build
from werkzeug.security import check_password_hash
crud = Blueprint('crud', __name__)

#pagination fetching of activities
@crud.route('/activityset', methods=['GET'])
def get_activities():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 6, type=int)

    # Paginate the query results
    activities = Activity.query.paginate(page=page, per_page=per_page, error_out=False)
    serialized_activities = [activity.serialize() for activity in activities.items]

    return jsonify(serialized_activities)

@crud.route('/activities', methods=['GET'])
def get_all_activities():
    activities = Activity.query.all()
    serialized_activities = []
    for activity in activities:
        serialized_activity = activity.serialize()
        serialized_activities.append(serialized_activity)
    return jsonify(serialized_activities)

@crud.route('/activities/<int:id>', methods=['GET'])
def get_activity(id):
    activity = Activity.query.get_or_404(id)
    serialized_activity = activity.serialize()
    return jsonify(serialized_activity)

@crud.route('/activities', methods=['POST'])
def add_activity():
    data = request.json
    name = data.get('name')
    description = data.get('description')
    why_worth = data.get('why_worth')
    youtube_link=data.get('youtube_link')
    google_link=data.get('google_link')
    meetup_link=data.get('meetup_link')

    if not all([name, description, why_worth]):
        return jsonify({'error': 'Missing required fields'}), 400

    new_activity = Activity(name=name, description=description, why_worth=why_worth,youtube_link=youtube_link,google_link=google_link,meetup_link=meetup_link)

    db.session.add(new_activity)
    db.session.commit()

    return jsonify({'message': 'Activity added successfully', 'id': new_activity.id}), 201

@crud.route('/activities/<int:id>', methods=['PUT'])
def update_activity(id):
    activity = Activity.query.get_or_404(id)
    data = request.json

    activity.name = data.get('name', activity.name)
    activity.description = data.get('description', activity.description)
    activity.why_worth = data.get('why_worth', activity.why_worth)
    activity.youtube_link=data.get('youtube_link',activity.youtube_link)
    activity.google_link=data.get('google_link',activity.google_link)
    activity.meetup_link=data.get('meetup_link',activity.meetup_link)


    db.session.commit()

    return jsonify({'message': 'Activity updated successfully'}), 200

@crud.route('/activities/<int:id>', methods=['DELETE'])
def delete_activity(id):
    activity = Activity.query.get_or_404(id)

    db.session.delete(activity)
    db.session.commit()

    return jsonify({'message': 'Activity deleted successfully'}), 200

# Functions to generate YouTube, Google, and Meetup links

def get_youtube_link(activity_name):
    youtube_api_key = os.getenv('YOUTUBE_API_KEY')
    if not youtube_api_key:
        raise ValueError("YouTube API key not found in environment variables")

    youtube = build('youtube', 'v3', developerKey=youtube_api_key)
    
    request = youtube.search().list(
        q=activity_name,
        part='snippet',
        maxResults=1
    )
    response = request.execute()
    
    if response['items']:
        first_item = response['items'][0]
        if 'id' in first_item and 'videoId' in first_item['id']:
            video_id = first_item['id']['videoId']
            return f'https://www.youtube.com/watch?v={video_id}'
    
    return ''


def get_google_link(activity_name):
    query = f"{activity_name} near me"
    return f"https://www.google.com/search?q={query.replace(' ', '+')}"

# Function to get Meetup search link
def get_meetup_link(activity_name):
    query = f"{activity_name} near me"
    return f"https://www.meetup.com/find/?keywords={query.replace(' ', '%20')}"


@crud.route('/login', methods = ['POST'])
def get_token():
    data=request.json
    email=data['email']
    password=data['password']

    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400

    logged_user = User.query.filter(User.email == email).first()
    if logged_user and check_password_hash(logged_user.password, password):
        return jsonify({'token': logged_user.token}), 200
    
    else:
        return jsonify({'error': 'Invalid email or password'}), 401
    