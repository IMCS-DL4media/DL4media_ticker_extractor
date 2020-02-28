def concatenate_news_stories(l, char = '\n'):
    """
    Concatenates news stories into one string, with newlines seperating stories.

    Takes a list of dictionaries with fields
        text - string corresponding to news story.

    Returns string.
    """

    result = ''
    for story in l:
        if len(result) != 0:
            result+= char
        result+= story['text']

    return result