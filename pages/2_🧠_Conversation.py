import asyncio
import base64
import json
import os
import sys

sys.path.append('../venv')

import pyaudio
import websockets
from open_ai import ai_completion
from tts import speak
import streamlit as st
from utils import keyword_check

# Initialize session_state for 
if 'run' not in st.session_state:
    st.session_state['run'] = False

def start_recording():
    st.session_state['run'] = True


def stop_recording():
    st.session_state['run'] = False

st.set_page_config(page_title='Parlom', page_icon=':bulb:',
                   layout="wide", initial_sidebar_state="auto", menu_items=None)

with st.container():
    st.title('Parlom')
    st.markdown("""---""")
    st.write('Click the button to begin a conversation!')

start, stop = st.columns(2)

start.button('Begin Conversation', on_click=start_recording)

stop.button('End Conversation', on_click=stop_recording)

FRAMES_PER_BUFFER = 3200
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
p = pyaudio.PyAudio()

# starts recording
stream = p.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    frames_per_buffer=FRAMES_PER_BUFFER
)


# the AssemblyAI endpoint we're going to hit
URL = "wss://api.assemblyai.com/v2/realtime/ws?sample_rate=16000"

# Retrieve API key from environment
AA_API_KEY = os.environ.get('AA_API_KEY')

if not AA_API_KEY:
    print('ERROR: AssemblyAI API key not set')
    sys.exit(1)


async def send_receive():

    print(f'Connecting websocket to url ${URL}')

    async with websockets.connect(
            URL,
            extra_headers=(("Authorization", AA_API_KEY),),
            ping_interval=80,
            ping_timeout=60
    ) as _ws:

        r = await asyncio.sleep(0.1)
        print("Receiving SessionBegins ...")

        session_begins = await _ws.recv()
        print(session_begins)
        print("Sending messages ...")

        async def send():
            while st.session_state['run']:
                try:
                    data = stream.read(FRAMES_PER_BUFFER,
                                       exception_on_overflow=False)
                    data = base64.b64encode(data).decode("utf-8")
                    json_data = json.dumps({"audio_data": str(data)})
                    r = await _ws.send(json_data)

                except websockets.exceptions.ConnectionClosedError as e:
                    print(e)
                    assert e.code == 4008
                    break

                except Exception as e:
                    assert False, "Not a websocket 4008 error"

                r = await asyncio.sleep(0.01)

            return True

        async def receive():
            while st.session_state['run']:
                try:
                    result_str = await _ws.recv()
                    if json.loads(result_str)['message_type'] == 'FinalTranscript':
                        prompt = json.loads(result_str)['text'].strip()
                        if prompt:
                            res = keyword_check(prompt.lower())
                            
                            if res:
                                ai_response = res
                            else:
                                ai_response = ai_completion(prompt).strip()
            
                            st.markdown('**Human:** ' + prompt)
                            st.markdown('**AI:** ' + ai_response)
                            speak(ai_response)

                except websockets.exceptions.ConnectionClosedError as e:
                    print(e)
                    assert e.code == 4008
                    break

                except Exception as e:
                    assert False, "Not a websocket 4008 error"

        send_result, receive_result = await asyncio.gather(send(), receive())

try:
    asyncio.run(send_receive())

except AssertionError:
    asyncio.run(send_receive())
