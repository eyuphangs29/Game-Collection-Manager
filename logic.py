def validate_game_entry(title, rating):
    """Business logic that checks the accuracy of game data."""
    if not title or title.strip() == "":
        return False
    try:
        r = int(rating)
        if r < 0 or r > 5:
            return False
    except (ValueError, TypeError):
        return False
    return True