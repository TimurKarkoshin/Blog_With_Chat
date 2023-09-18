import asyncio

from pywebio import start_server
from pywebio.input import input_group, input, actions
from pywebio.output import put_markdown, output, put_scrollable, toast, put_buttons
from pywebio.session import run_async, run_js

chat_cache = []
online_users = set()
MAX_MESSAGES_COUNT = 100


async def main():
    global chat_cache

    put_markdown("## 🌼 Обсуждалка 🌼")

    chat_box = output()
    put_scrollable(chat_box, height=350, keep_bottom=True)

    nickname = await input("Присоединиться",
                           required=True,
                           placeholder="Ваше имя",
                           validate=lambda name: "Такой ник уже используется!"
                           if name in online_users or name == '➕' else None)
    online_users.add(nickname)

    chat_cache.append(('➕', f'`{nickname}` подключился к обсуждению!'))
    chat_box.append(put_markdown(f'➕ `{nickname}` подключился к обсуждению'))

    refresh_task = run_async(refresh_msg(nickname, chat_box))

    while True:
        data = await input_group("💬 Отправить сообщение", [
            input(placeholder="Текст сообщения ...", name="msg"),
            actions(
                name="cmd",
                buttons=["Отправить", {'label': "Выйти из чата", 'type': 'cancel'}]
            )
        ], validate=lambda m: ('msg',
                               "Введите текст сообщения!") if m["cmd"] == "Отправить" and not m['msg'] else None)

        if data is None:
            break

        chat_box.append(put_markdown(f"`{nickname}`: {data['msg']}"))
        chat_cache.append((nickname, data['msg']))

    refresh_task.close()

    online_users.remove(nickname)
    toast("Вы вышли из чата!")
    chat_box.append(put_markdown(f'💔 Пользователь `{nickname}` покинул беседу!'))
    chat_cache.append(('💔', f'Пользователь `{nickname}` покинул беседу!'))

    put_buttons(['Перезайти'], onclick=lambda btn: run_js('window.location.reload()'))


async def refresh_msg(nickname, chat_box):
    global chat_cache
    last_idx = len(chat_cache)

    while True:
        await asyncio.sleep(1)

        for message in chat_cache[last_idx:]:
            if message[0] != nickname:
                chat_box.append(put_markdown(f"`{message[0]}`: {message[1]}"))

        if len(chat_cache) > MAX_MESSAGES_COUNT:
            chat_cache = chat_cache[len(chat_cache) // 2:]

        last_idx = len(chat_cache)


if __name__ == "__main__":
    start_server(main, debug=True, port=8080, cdn=False)
