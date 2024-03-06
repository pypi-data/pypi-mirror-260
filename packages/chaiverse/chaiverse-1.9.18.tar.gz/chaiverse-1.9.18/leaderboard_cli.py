from chaiverse.http_client import SubmitterClient
from chaiverse.schemas import Leaderboard
from chaiverse import config


def get_leaderboard() -> Leaderboard:
    submitter_client = SubmitterClient()
    leaderboard = submitter_client.get(config.LATEST_LEADERBOARD_ENDPOINT)
    leaderboard = Leaderboard(**leaderboard)
    return leaderboard


def display_leaderboard():
    leaderboard = get_leaderboard()
    print(leaderboard.to_tabulate())
