from flask import Blueprint, jsonify
from app.auth_decorators import role_required
from flask_jwt_extended import get_jwt, get_jwt_identity
from app.models.user import User 
# Pls import the Event and Ticket models once they are created
# something like from app.models.event import Event


user_bp = Blueprint('user_bp', __name__, url_prefix='/users')

# This route is for organizers
@user_bp.route('/organizer-dashboard', methods=['GET'])
@role_required(['organizer'])
def organizer_dashboard():
    return jsonify(message="Welcome to the Organizer Dashboard!"), 200

# This is the shared dashboard route
@user_bp.route('/dashboard', methods=['GET'])
@role_required(['organizer', 'attendee'])
def dashboard():
    # Get the claims and user identity from the JWT token
    claims = get_jwt()
    user_role = claims.get('role')
    user_id = get_jwt_identity()
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Return different data based on the user's role
    if user_role == 'organizer':
        # TODO: TASK 5 
        return jsonify(
            message=f"Welcome to your Organizer Dashboard, {user.username}!",
            role=user_role,
            # Example data for an organizer
            events_created=12, # I've used hardcoded data for testing. Replace with: Event.query.filter_by(organizer_id=user_id).count()
            total_tickets_sold=450 # Same as above. Replace with your logic
        ), 200
    
    elif user_role == 'attendee':
        # TODO: TASK 5 - Implement data fetching for the attendee dashboard.
        return jsonify(
            message=f"Welcome to your Attendee Dashboard, {user.username}!",
            role=user_role,
            # Example data for an attendee
            tickets_purchased=5, # I've used hardcoded data for testing. Replace with: Ticket.query.filter_by(user_id=user_id).count()
            upcoming_events=2 # Same as above. Replace with your logic
        ), 200


# ----------  HOW TO ADD NEW ROUTES TO THIS FILE  ------------------------------- #

# This file will hold all routes related to user actions and data, such as viewing dashboards.

# Logic of the App's Routing:
# 1. Blueprint Setup: I've used a Flask Blueprint (user_bp) to organize the routes.
#    This keeps should helpfully keep our code clean by grouping related endpoints together. The url_prefix='/users' means that every route defined here will start with /users. For example, @user_bp.route('/dashboard') becomes accessible at `http://127.0.0.1:5555/users/dashboard`. But this can be changed.
#
# 2. Authorization: The routes are protected to ensure only the right users can access them.
#    - @jwt_required(): I'm using a decorator that makes sure the user has sent a valid JSON Web Token in their request header.
#    - @role_required([...]): This is the custom decorator from auth_decorators.py that will check the role claim inside the JWT. If the user's role is not in the list (e.g., ['organizer']), it should denies access. I've tested this. But please make sure it works as expected in your pages.
#
# How to Add Your Own Route:
#Let's say you want to create an endpoint for users to view their own dash.
#
# STEP 1: Define the Route Signature
#   - Use the @user_bp.route() decorator to define the URL path and the HTTP method.
#   - For a user dash, it would likely be a GET request.
#
#     @user_bp.route(/profile, methods=[GET])
#
# STEP 2: Add Authorization
#   - Add the necessary decorators to protect the route. A user must be logged in to
#     see their dash, so we need @jwt_required().
#
#     @user_bp.route('/dashboard', methods=[GET])
#     @jwt_required()
#
# STEP 3: Write the Function Logic
#   - Define the Python function that will execute when this endpoint is called.
#   - Inside the function, get the user's ID from the JWT token using get_jwt_identity().
#   - Use the ID to query the database for that user's information.
#   - Return the data as a JSON response. use jsonify().
#
#     @user_bp.route(/dashboard, methods=[GET])
#     @jwt_required()
#     def view_dashboard():
#         user_id = get_jwt_identity()
#         user = User.query.get(user_id)
#         if user:
#             # The to_dict() method is a custom method in the User model to serialize data
#             return jsonify(user.to_dict()), 200
#         return jsonify({"error": "User not found"}), 404