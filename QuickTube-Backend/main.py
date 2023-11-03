from flask import Flask,jsonify,request
import summary
import videoInfo
import concurrent.futures
import g4f
import asyncio


app = Flask(__name__)

def get_summary(text):
    response = g4f.ChatCompletion.create(
        model="gpt-3.5-turbo",
        provider=g4f.Provider.DeepAi,
        messages=[{"role": "user", "content": "Summarize it in atleast 10 bullet points" + text}],
        stream=True,
    )
    result_string = " "
    for message in response:
        result_string += message
    return result_string
def process_row(text):
    #print(row)
    asyncio.set_event_loop(asyncio.new_event_loop())
    summary = get_summary(text)  # Access the 'text' column
    return summary

@app.route('/')
def hello_world():
    return 'Hello World'

@app.route('/transcribe')
def transcribe():
    url = request.args.get('url')
    result = summary.get_Summary(url)
    return result

@app.route('/video_info')
def video_info():
    url = request.args.get('url')
    result = videoInfo.getVideoInfo(url)
    return result



if __name__ == "__main__":
    app.run(debug=True, port=5000)