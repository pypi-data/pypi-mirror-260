BASE_SUBMITTER_URL = "https://guanaco-submitter.chai-research.com"
BASE_FEEDBACK_URL = "https://guanaco-feedback.chai-research.com"

LATEST_LEADERBOARD_ENDPOINT = "/latest_leaderboard"
LEADERBOARDS_ENDPOINT = "/leaderboards"
LEADERBOARD_ENDPOINT = "/leaderboard"
CHAT_ENDPOINT = "/models/{submission_id}/chat"
FEEDBACK_SUMMARY_ENDPOINT = "/feedback"
FEEDBACK_ENDPOINT = "/feedback/{submission_id}"

SUBMISSION_ENDPOINT = "/models/submit"
BLEND_SUBMISSION_ENDPOINT = "/models/submit_blend"
REWARD_BLEND_SUBMISSION_ENDPOINT = "/models/submit_reward_blend"
ROUTED_BLEND_SUBMISSION_ENDPOINT = "/models/submit_routed_blend"
ALL_SUBMISSION_STATUS_ENDPOINT = "/models/"
SEARCH_SUBMISSIONS_ENDPOINT = "/models/search"
INFO_ENDPOINT = "/models/{submission_id}"
DEACTIVATE_ENDPOINT = "/models/{submission_id}/deactivate"
REDEPLOY_ENDPOINT = "/models/{submission_id}/redeploy"
EVALUATE_ENDPOINT = "/models/{submission_id}/evaluate"
TEARDOWN_ENDPOINT = "/models/{submission_id}/teardown"

COMPETITIONS_ENDPOINT = '/competitions'
COMPETITION_ENDPOINT = '/competitions/{competition_id}'
COMPETITION_ENROLLED_SUBMISSION_IDS_ENDPOINT = '/competitions/{competition_id}/enrolled_submission_ids/{submission_id}'

DEFAULT_BEST_OF = 4
DEFAULT_REWARD_REPO = "ChaiML/reward_models_100_170000000_cp_498032"
DEFAULT_MAX_INPUT_TOKENS = 512
