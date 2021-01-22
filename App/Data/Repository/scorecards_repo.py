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
