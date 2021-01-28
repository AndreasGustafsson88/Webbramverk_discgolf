from App.Data.Repository import scorecards_repo as sr


def get_scorecard(**kwargs):
    return sr.get_scorecard(kwargs)


def delete_scorecard(scorecard):
    sr.delete_scorecard(scorecard)


def create_scorecard(course, players, multi, rated):

    round_summary = {'course_id': str(course._id),
                     'course': course.name,
                     'course_holes': course.holes,
                     'rated': rated,
                     'players': [{'user_name': player.user_name,
                                  'full_name': player.full_name,
                                  'hcp': player.hcp,
                                  'stats': {f'hole{i + 1}{v}': "" for i in range(course.holes[0] * multi)
                                            for v in ['_points', '_par', '_throws']}} for player in players],
                     'active': True,
                     'multi': multi
                     }
    return sr.create_scorecard(round_summary)
