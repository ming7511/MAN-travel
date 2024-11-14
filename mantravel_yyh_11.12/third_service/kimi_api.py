from bs4 import BeautifulSoup
from openai import OpenAI
import re
import requests
import json
import settings
import os

# 初始化 OpenAI 客户端
client = OpenAI(
    api_key=settings.KIMI_API_KEY,
    base_url=settings.KIMI_MODEL_URL,
)


# 定义网页解析工具函数
def crawl_webpage_content(url: str) -> str:
    payload = {
        'api_key': settings.SCRAPE_API_KEY,
        'url': url,
        'follow_redirect': 'false'
    }
    response = requests.get('https://api.scraperapi.com/', params=payload)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        if url.startswith("https://www.xiaohongshu.com/"):
            span = soup.find('span', class_='note-text')
            content = span.get_text(strip=True) if span else "没有找到匹配的内容"

        elif url.startswith("https://www.dianping.com/"):
            content = [div.get_text(strip=True) for div in soup.find_all('div', class_='content-text')]

        else:
            content = "URL 不符合规定的解析条件。"

        return content
    else:
        return f"无法获取网页内容，状态码: {response.status_code}"


# 定义工具
tools = [
    {
        "type": "function",
        "function": {
            "name": "crawl_webpage_content",
            "description": """
                通过给定的网址获取网页内容。支持小红书和大众点评的链接。
                如果工具返回的结果为空或者是URL 不符合解析条件，请告知用户该网页不支持解析。
            """,
            "parameters": {
                "type": "object",
                "required": ["url"],
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "需要解析内容的网址（URL）"
                    }
                }
            }
        }
    }
]

# 定义工具映射
tool_map = {
    "crawl_webpage_content": crawl_webpage_content
}

file_path = os.path.join(os.path.dirname(__file__), 'promt.txt')
with open(file_path, "r", encoding="utf-8") as f:
    prompt = f.read()

# 定义对话函数
def multi_turn_chat(query: str, history=None, reset=False):
    if reset or history is None:
        history = [
            {
                "role": "system",
                "content": (
                    "你是 Kimi，由 Moonshot AI 提供的人工智能助手，专注于旅行和地理方面的知识。"
                    "请用简洁的语言提供有帮助的解答。确保回答准确、友好、易于理解。如果用户需要旅游建议，"
                    "请避免涉及恐怖主义、种族歧视、暴力等敏感话题，并确保回答内容安全、适当。"
                    f"{prompt}"
                )
            }
        ]

    url_pattern = r'(https://www\.xiaohongshu\.com/[^\s]+|https://www\.dianping\.com/[^\s]+)'
    match = re.search(url_pattern, query)

    if match:
        url = match.group(0)
        history.append({"role": "user", "content": query})

        # 调用模型以使用工具
        finish_reason = None
        while finish_reason is None or finish_reason == "tool_calls":
            response = client.chat.completions.create(
                model="moonshot-v1-128k",
                messages=history,
                temperature=0.3,
                tools=tools,
            )
            choice = response.choices[0]
            finish_reason = choice.finish_reason

            if finish_reason == "tool_calls":
                history.append(choice.message)
                for tool_call in choice.message.tool_calls:
                    tool_name = tool_call.function.name
                    tool_arguments = json.loads(tool_call.function.arguments)
                    tool_function = tool_map[tool_name]
                    tool_result = tool_function(tool_arguments["url"])

                    history.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "name": tool_name,
                        "content": json.dumps({"content": tool_result})
                    })

        return choice.message.content, history
    else:
        response = client.chat.completions.create(
            model="moonshot-v1-128k",
            messages=history + [{"role": "user", "content": query}],
            temperature=0.3,
        )

        result = response.choices[0].message.content
        history.append({
            "role": "assistant",
            "content": result
        })
        return result, history
<<<<<<< Updated upstream:mantravel_yyh_11.12/third_service/kimi_api.py
=======


# 测试调用
query1 = "我想以轻松的风格在福州市进行三天的旅游"
# query1 = 'https://www.xiaohongshu.com/explore/6724a4e100000000190143ef?xsec_token=ABMlds0Bsm02wq2HcmMj7O7UfMYamM1IdrX_JpEWJB5mw=&xsec_source=pc_search&source=unknown'
response, history = multi_turn_chat(query1)
print(response)
>>>>>>> Stashed changes:mantravel/third service/kimi_api.py
