import os
import json
import requests
import endpoints


# todo: extract common request params


def get_done_items():
    bearer = os.environ.get('BEARER_SECRET')

    url = endpoints.query_database(os.environ.get('GTD_DATABASE_ID'))

    payload = json.dumps({
        "filter": {
            "or": [
                {
                    "property": "Status",
                    "status": {
                        "equals": "Done"
                    }
                }
            ]
        },
        "sorts": [
            {
                "property": "Deadline",
                "direction": "ascending"
            }
        ]
    })
    headers = {
        'Notion-Version': '2022-06-28',
        'Authorization': f'Bearer {bearer}',
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    if response.status_code != 200:
        print('WARNING items endpoint returned non-success code',
              response.status_code)
        print('CONTENT:', response.text)

    return json.loads(response.text)


def delete_entry(entry_id):
    bearer = os.environ.get('BEARER_SECRET')
    url = endpoints.delete_entry(entry_id)
    headers = {
        'Notion-Version': '2022-02-22',
        'Authorization': f'Bearer {bearer}',
    }
    response = requests.request("DELETE", url, headers=headers, data={})

    if response.status_code != 200:
        print('ERROR commenting entry', entry_id, response.text)

    return response.status_code == 200


def comment_entry(entry_id, comment):
    bearer = os.environ.get('BEARER_SECRET')
    url = endpoints.comments()
    payload = json.dumps({
        "parent": {
            "page_id": entry_id
        },
        "rich_text": [
            {
                "text": {
                    "content": comment
                }
            }
        ]
    })
    headers = {
        'Content-Type': 'application/json',
        'Notion-Version': '2022-02-22',
        'Authorization': f'Bearer {bearer}',
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    if response.status_code != 200:
        print('ERROR commenting entry', entry_id, response.text)

    return response.status_code == 200


def set_marked_for_deletion(entry_id, marked):
    bearer = os.environ.get('BEARER_SECRET')
    url = endpoints.entry_page(entry_id)

    payload = json.dumps({
        "properties": {
            "Marked for deletion": {
                "checkbox": marked
            }
        }
    })

    headers = {
        'Content-Type': 'application/json',
        'Notion-Version': '2022-02-22',
        'Authorization': 'Bearer secret_phikHjvHtW7KuQTgSnyGAzxzUD40I48S1WMy4JgjjM9',
        'Cookie': '__cf_bm=tAGkU1.59ptecBWyuHwP7RBE.xpeXWejhOJZu6U.JmY-1677462424-0-Afx7sB49lgvcMY2QsaAvf468APjl2v6WeE7/LU/6CQuxAk5TlVXXMdsBSBcztAeub/myMm0O75vFj6ABnfBJ8NI='
    }

    response = requests.request("PATCH", url, headers=headers, data=payload)

    if response.status_code != 200:
        print('ERROR marking entry', entry_id, response.text)

    return response.status_code == 200
