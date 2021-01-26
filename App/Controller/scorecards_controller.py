from App.Data.Repository import scorecards_repo as sr


def get_scorecard(**kwargs):
    return sr.get_scorecard(kwargs)


def delete_scorecard(scorecard):
    sr.delete_scorecard(scorecard)
