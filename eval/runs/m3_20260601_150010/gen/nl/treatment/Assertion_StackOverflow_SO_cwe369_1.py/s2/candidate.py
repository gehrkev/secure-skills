def calculate_average_score(total_score, total_count):
    """
    Calculate the average score by dividing the total score by the total count.

    Args:
        total_score: The sum of all scores
        total_count: The number of scores

    Returns:
        The average score as a float

    Raises:
        ValueError: If total_count is zero
    """
    if total_count == 0:
        raise ValueError("Cannot calculate average: total count cannot be zero")

    return total_score / total_count
