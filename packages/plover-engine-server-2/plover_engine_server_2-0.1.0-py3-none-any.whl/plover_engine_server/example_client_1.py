#!/bin/python3
# https://github.com/ftobia/aiohttp-websockets-example/blob/master/client.py

import asyncio
import os

import aiohttp

#HOST = os.getenv('HOST', '0.0.0.0')
#PORT = int(os.getenv('PORT', 8080))

#URL = f'http://{HOST}:{PORT}/ws'

URL = f'http://localhost:8087/websocket'

async def main():
    async with aiohttp.ClientSession() as session:
        try:
            async with session.ws_connect(URL) as ws:
                if 1:
                    while True:
                        await asyncio.sleep(1)
                        await ws.send_str(r'{"zero_last_stroke_length": true, "translation": "{PLOVER:toggle}"}')
                    return
                #await asyncio.sleep(1)
                ##await ws.send_str(r'{"translation": "abc"}')
                ##await ws.send_str(r'{"stroke": ["P-", "H-", "R-", "O-", "-L", "-G"]}')
                #await ws.send_str(r'{"translation": "{PLOVER:toggle}"}')
                #await ws.send_str(r'{"translation": "abc"}')
                #return

                await prompt_and_send(ws)
                async for msg in ws:
                    print('Message received from server:', msg)
                    await prompt_and_send(ws)

                    if msg.type in (aiohttp.WSMsgType.CLOSED,
                                    aiohttp.WSMsgType.ERROR):
                        break

        except asyncio.CancelledError:
            return
        finally:
            await ws.close()


async def prompt_and_send(ws):
    new_msg_to_send = input('Type a message to send to the server: ')
    if new_msg_to_send == 'exit':
        print('Exiting!')
        raise SystemExit(0)
    await ws.send_str(new_msg_to_send)


if __name__ == '__main__':
    print('Type "exit" to quit')
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
