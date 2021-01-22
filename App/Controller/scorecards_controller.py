from App.Data.Repository import scorecards_repo as sr


def get_scorecard(**kwargs):
    return sr.get_scorecard(kwargs)
