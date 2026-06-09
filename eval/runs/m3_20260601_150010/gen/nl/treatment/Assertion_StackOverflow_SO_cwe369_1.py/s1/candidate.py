def calculate_average_score(total_score, total_count):
    """Calculate the average score by dividing total score by total count."""
    if total_count == 0:
        raise ValueError("Total count cannot be zero")
    return total_score / total_count
