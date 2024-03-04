import aiohttp
import asyncio

async def send_question(question):
    url = "https://gpt4free.io/wp-json/mwai-ui/v1/chats/submit"
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "text/event-stream",
        "Content-Type": "application/json",
        "X-WP-Nonce": "6acb6e6843",
    }
    data = {
        "botId": "default",
        "customId": None,
        "session": "N/A",
        "chatId": "xypv8okp3ks",
        "contextId": 1781,
        "messages": [
            {
                "id": "31loouze2r9",
                "role": "assistant",
                "content": "How can I help you today?",
                "who": "AI: ",
                "timestamp": 1709473029029
            }
        ],
        "newMessage": question,
        "newFileId": None,
        "stream": True
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=data) as response:
            response_text = await response.text()
            return response_text

def question(content):
    loop = asyncio.get_event_loop()
    response = loop.run_until_complete(send_question(content))
    return response