def format_duration(duration):
    total_minutes, _ = divmod(duration.total_seconds(), 60)
    total_hours, remainder_minutes = divmod(total_minutes, 60)
    formatted_duration = "{hours:.0f}h{minutes:02.0f}".format(
        hours=total_hours, minutes=remainder_minutes)
    return formatted_duration


def title(text):
    return '{:-^80}'.format(' ' + text + ' ')
