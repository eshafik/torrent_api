def check_title(query, data):
    match = query.split("+")
    if (len(match) >= 2) and match[0].lower() in data.get("title") and match[1].lower() in data.get("title"):
        print("query: ", query, "title:", data.get("title"))
        return True
    if (len(match) == 1) and match[0].lower() in data.get("title"):
        print("single string")
        return True
    return False
