from flask import Blueprint, jsonify, render_template, request, redirect, url_for, flash

from .models import Activity, User, db
import os
from googleapiclient.discovery import build
from werkzeug.security import check_password_hash

from flask_login import login_user, logout_user, LoginManager, current_user, login_required

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
    youtube_link = data.get('youtube_link')
    google_link = data.get('google_link')
    meetup_link = data.get('meetup_link')
    tags = data.get('tags', [])  # Default to empty list if not provided

    if not all([name, description, why_worth]):
        return jsonify({'error': 'Missing required fields'}), 400

    # Ensure tags is a list
    if not isinstance(tags, list):
        return jsonify({'error': 'Tags should be a list'}), 400

    new_activity = Activity(
        name=name,
        description=description,
        why_worth=why_worth,
        youtube_link=youtube_link,
        google_link=google_link,
        meetup_link=meetup_link,
        tags=tags
    )

    db.session.add(new_activity)
    db.session.commit()

    return jsonify({'message': 'Activity added successfully', 'id': new_activity.id}), 201


@crud.route('/activities/<int:id>', methods=['PUT'])
def update_activity(id):
    activity = Activity.query.get_or_404(id)
    data = request.json

    # Check for at least one field to be updated
    if not any(key in data for key in ['name', 'description', 'why_worth', 'youtube_link', 'google_link', 'meetup_link', 'tags']):
        return jsonify({'error': 'No fields to update'}), 400

    # Update fields if provided
    activity.name = data.get('name', activity.name)
    activity.description = data.get('description', activity.description)
    activity.why_worth = data.get('why_worth', activity.why_worth)
    activity.youtube_link = data.get('youtube_link', activity.youtube_link)
    activity.google_link = data.get('google_link', activity.google_link)
    activity.meetup_link = data.get('meetup_link', activity.meetup_link)

    # Handle the tags update
    tags = data.get('tags')
    if tags is not None:
        if not isinstance(tags, list):
            return jsonify({'error': 'Tags should be a list'}), 400
        activity.tags = tags

    db.session.commit()

    return jsonify({'message': 'Activity updated successfully'}), 200


@crud.route('/activities/<int:id>', methods=['DELETE'])
def delete_activity(id):
    activity = Activity.query.get_or_404(id)

    db.session.delete(activity)
    db.session.commit()

    return jsonify({'message': 'Activity deleted successfully'}), 200

#USER CRUDS start here

# Get all users
@crud.route('/users', methods=['GET'])
@login_required
def get_all_users():
    users = User.query.all()
    return jsonify([user.serialize() for user in users])

# Get one user by ID
@crud.route('/user/<user_id>', methods=['GET'])
@login_required
def get_user_by_id(user_id):
    user = User.query.get(user_id)
    if user:
        return jsonify(user.serialize())
    else:
        return jsonify({'error': 'User not found'}), 404

# Get one user by token
@crud.route('/user/<token>', methods=['GET'])
@login_required
def get_user_by_token(token):
    user = User.query.filter_by(token=token).first()
    if user:
        return jsonify(user.serialize())
    else:
        return jsonify({'error': 'User not found'}), 404

# Update a user
@crud.route('/user/<token>', methods=['POST'])
@login_required
def update_user(token):
    user = User.query.filter_by(token=token).first()
    if user:
        user.customer_name = request.form.get('customer_name')
        user.age = request.form.get('age')
        user.location = request.form.get('location')
        user.interests = request.form.get('interests')
        user.activity_types = request.form.get('activityTypes')
        user.physical_levels = request.form.get('physicalLevel')
        user.limitations = request.form.get('limitations')
        user.primary_goals = request.form.get('primaryGoal')
        user.budget = request.form.get('budget')
        user.available_time = request.form.get('available_time')
        db.session.commit()
        flash('Profile updated successfully', 'success')
        return redirect(url_for('main.profile'))
    else:
        return jsonify({'error': 'User not found'}), 404

# Delete a user
@crud.route('/user/<user_id>', methods=['DELETE'])
@login_required
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'User deleted successfully'})
    else:
        return jsonify({'error': 'User not found'}), 404

# Add a new user
@crud.route('/user', methods=['PUT'])
@login_required
def add_user():
    email = request.form.get('email')
    password = request.form.get('password')
    customer_name = request.form.get('customer_name')
    age = request.form.get('age')
    location = request.form.get('location')
    interests = request.form.get('interests')
    activity_types = request.form.get('activityTypes')
    physical_levels = request.form.get('physicalLevel')
    limitations = request.form.get('limitations')
    primary_goals = request.form.get('primaryGoal')
    budget = request.form.get('budget')
    available_time = request.form.get('available_time')

    new_user = User(
        email=email,
        password=password,
        customer_name=customer_name,
        age=age,
        location=location,
        interests=interests,
        activity_types=activity_types,
        physical_levels=physical_levels,
        limitations=limitations,
        primary_goals=primary_goals,
        budget=budget,
        available_time=available_time
    )

    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User added successfully'})




    