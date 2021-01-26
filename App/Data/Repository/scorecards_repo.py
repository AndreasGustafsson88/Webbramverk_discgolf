from App.Data.Models.scorecards import Scorecard


def add_scorecard(player_summary):
    e = 'success'
    try:
        Scorecard.insert_one(player_summary)

    except Exception as e:
        pass

    finally:
        return e


def get_scorecard(kwargs):
    return Scorecard.find(**kwargs).first_or_none()


def update_scorecard(mongo_object, player_summary):
    for e, player in enumerate(mongo_object.players):
        player['stats'] = player_summary['players'][e]['stats']
        mongo_object.save()


def save_scorecard(scorecard):
    scorecard.active = False
    scorecard.save()


def delete_scorecard(scorecard):
    Scorecard.delete_one(_id=scorecard._id)
