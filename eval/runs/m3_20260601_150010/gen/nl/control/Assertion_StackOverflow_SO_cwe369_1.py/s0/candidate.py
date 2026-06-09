def calculate_average_score(total_score, total_count):
    """Calculate the average score by dividing the total score by the total count."""
    if total_count == 0:
        return 0
    return total_score / total_count
