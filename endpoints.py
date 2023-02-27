def query_database(database_id):
    return f"https://api.notion.com/v1/databases/{database_id}/query"


def delete_entry(entry_id):
    return f"https://api.notion.com/v1/blocks/{entry_id}"


def comments():
    return "https://api.notion.com/v1/comments"


def entry_page(entry_id):
    return f"https://api.notion.com/v1/pages/{entry_id}"
