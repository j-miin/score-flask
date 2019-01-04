from flask import Flask, jsonify, Blueprint, request, render_template, make_response
from score_keeping.users.models import User
from score_keeping.game.models import Game, GameLog
from score_keeping import db, app
from sqlalchemy.exc import IntegrityError
from score_keeping.helpers.auth import generate_token, requires_auth, verify_token


users_api_blueprint = Blueprint('users_api',
                                __name__,
                                template_folder='templates')

@users_api_blueprint.route('/games', methods=['GET'])
def list_games():
    games = Game.query.all()

    games = [{
        "id": int(game.id),
        "gameName": game.gameName,
        "scorePerPoint": game.scorePerPoint,
        "timerChecked": game.timerChecked,
        "timerMinPerRound": game.timerMinPerRound,
        "timerMinPerGame": game.timerMinPerGame
    } for game in games]

    return jsonify(games), 200



@users_api_blueprint.route('/signup', methods=['POST'])
def create_user():

    post_data = request.get_json()

    try:
        user = User(
            name=post_data['user']["name"],
            email=post_data['user']["email"],
            password=post_data['user']["password"]
        )

        db.session.add(user)
        db.session.commit()

# the problem with this is that the user doesnt know what they did wrong.
# FIX!!!
    except IntegrityError:
        return jsonify(message="User with that email already exists"), 409

    new_user = User.query.filter_by(email=post_data['user']["email"]).first()

    return jsonify(
        id=user.id,
        token=generate_token(new_user)
    )


@users_api_blueprint.route('/gamelog', methods=['POST'])
def game_log():

    post_data = request.get_json()

    gamelog = GameLog(
        game_id=post_data['gamelog']["game_id"],
        scores=post_data['gamelog']["scores"],
    )

    db.session.add(gamelog)
    db.session.commit()

    return jsonify(
        message="Game log added"
    )

@users_api_blueprint.route('/pastgames', methods=['GET'])
def past_games():

    past_game = Gamelog.query.filter_by(id)    

@users_api_blueprint.route('/login', methods=['POST'])
def login():
    post_data = request.get_json()
    user = User.query.filter_by(email=post_data['user']["email"]).first()

    if user and user.check_password(str(post_data['user']["password"])):
        auth_token = user.encode_auth_token(user.id)

        responseObject = {
            'status': 'success',
            'message': 'Successfully signed in.',
            'auth_token': auth_token.decode()
        }

        return make_response(jsonify(responseObject)), 201

    else:
        responseObject = {
            'status': 'fail',
            'message': 'Some error occurred. Please try again.'
        }

        return make_response(jsonify(responseObject)), 401
    #     return jsonify(token=generate_token(user))
    # else:
    #     return jsonify(error=True), 403

# @users_api_blueprint.route("/api/is_token_valid", methods=["POST"])
# def is_token_valid():
#     incoming = request.get_json()
#     is_valid = verify_token(incoming["token"])

#     if is_valid:
#         return jsonify(token_is_valid=True)
#     else:
#         return jsonify(token_is_valid=False), 403


@users_api_blueprint.route('/newgame', methods=['POST'])
def create_game():
    post_data = request.get_json()

    jwt = request.headers.get('Authorization')

    if jwt:
        auth_token = jwt.split(" ")[1]
    else:
        responseObject = {
            'status': 'failed',
            'message': 'No authorization header found'
        }

        return jsonify(responseObject), 401

    user_id = User.decode_auth_token(auth_token)

    user = User.query.get(user_id)

    if user:
        game = Game(
            gameName=post_data['game']["gameName"],
            user_id=user_id,
            scorePerPoint=post_data['game']["scorePerPoint"],
            timerChecked=post_data['game']["timerChecked"],
            timerMinPerRound=post_data['game']["timerMinPerRound"],
            timerMinPerGame=post_data['game']["timerMinPerGame"]
        )
        db.session.add(game)
        db.session.commit()

        return jsonify(
            id=game.id,
        )
    else:
        responseObject = {
            'status': 'failed',
            'message': 'Authentication failed'
        }
