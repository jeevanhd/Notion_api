import sys
import requests
import os
from dotenv import load_dotenv


# -- Loading Env---
load_dotenv()

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
DATABASE_ID = os.getenv("DATABASE_ID")

if not NOTION_TOKEN or not DATABASE_ID:
    print(f"Missing Notion token or Database id")
    sys.exit(1)


# ---- HEADERS ----
headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

def saveToNotion(topic_name, topic_content):
    """
    Save a topic to Notion database
    
    Args:
        topic_name (str): The title of the topic
        topic_content (str): The content of the topic
    
    Returns:
        dict: Success/error response with status and message
    """
    try:
        # ---- DATA ----
        data = {
            "parent": {"database_id": DATABASE_ID},
            "properties": {
                "Name": {"title": [{"text": {"content": topic_name}}]}
            },
            "children": [
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {"content": topic_content}
                            }
                        ]
                    }
                }
            ]
        }

        # ---- API CALL ----
        response = requests.post("https://api.notion.com/v1/pages", headers=headers, json=data)
        
        if response.status_code in [200, 201]:
            page_data = response.json()
            return {
                "success": True,
                "status_code": response.status_code,
                "message": "Page created successfully!",
                "page_id": page_data.get("id"),
                "url": page_data.get("url")
            }
        else:
            return {
                "success": False,
                "status_code": response.status_code,
                "message": f"Failed to create page: {response.text}",
                "error_details": response.json() if response.content else None
            }
            
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "status_code": 500,
            "message": f"Network error occurred: {str(e)}",
            "error_type": "NetworkError"
        }
    except Exception as e:
        return {
            "success": False,
            "status_code": 500,
            "message": f"Unexpected error occurred: {str(e)}",
            "error_type": "UnexpectedError"
        }


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python notion_service.py \"Topic Name\" \"Topic Content\"")
        sys.exit(1)

    topic_name = sys.argv[1]
    topic_content = sys.argv[2]
    
    result = saveToNotion(topic_name=topic_name, topic_content=topic_content)
    
    if result["success"]:
        print(f"✅ {result['message']}")
        if result.get("url"):
            print(f"🔗 Page URL: {result['url']}")
    else:
        print(f"❌ {result['message']}")
        sys.exit(1)