import settings
import requests
from openai import OpenAI

client = OpenAI(
    api_key=settings.KIMI_API_KEY,
    base_url=settings.KIMI_MODEL_URL,
)

with open(r"D:\软件工程\团队作业\2\promt.txt", "r", encoding="utf-8") as f:
    prompt = f.read()

def multi_turn_chat(query, history=None, reset=False):
    if reset or history is None:
        history = [
            {
                "role": "system",
                "content": (
                    "你是 Kimi，由 Moonshot AI 提供的人工智能助手，专注于旅行和地理方面的知识。"
                    "请用简洁的语言提供有帮助的解答。确保回答准确、友好、易于理解。如果用户需要旅游建议，"
                    "请避免涉及恐怖主义、种族歧视、暴力等敏感话题，并确保回答内容安全、适当。"
                    # f"{prompt}"
                )
            }
        ]

    # 添加用户问题并生成响应
    history.append({
        "role": "user",
        "content": query
    })

    completion = client.chat.completions.create(
        model="moonshot-v1-128k",
        messages=history,
        temperature=0.3,
        response_format={"type": "text"},

    )

    result = completion.choices[0].message.content
    history.append({
        "role": "assistant",
        "content": result
    })

    return result, history



# test

query1 = '访问https://www.xiaohongshu.com/explore/6724a4e100000000190143ef?xsec_token=ABMlds0Bsm02wq2HcmMj7O7UfMYamM1IdrX_JpEWJB5mw=&xsec_source=pc_search&source=unknown，对此总结并作出旅游规划'

response2, history = multi_turn_chat(query1)

print(response2)
