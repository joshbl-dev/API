REDIRECT_URL = "https://joshbl.dev"


def rejected_perms():
	return REDIRECT_URL + "/403"


def invalid_request():
	return REDIRECT_URL + "/404"