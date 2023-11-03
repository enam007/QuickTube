import requests as r
from urllib.parse import urlparse, parse_qs
import re
import pandas as pd
from youtube_transcript_api import YouTubeTranscriptApi
import json
from pytube import YouTube



def use_global_token():
    return token

def extract_video_id(url,videoType):
    # Parse the URL
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    if videoType == 'Vimeo':
        if 'video' in query_params:
            video_id = query_params['video'][0]
    elif videoType == 'YouTube':
        if 'v' in query_params:
            video_id = query_params['v'][0]
    return video_id




def getToken():
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
        #"Cookie": "vuid=1604597071.1909810702; _abexps=%7B%223039%22%3A%2250_off%22%7D; _gcl_au=1.1.529568572.1691671393; _gid=GA1.2.707996846.1692090385; player=\"captions=en-US.subtitles\"; g_state={\"i_p\":1692098139861,\"i_l\":1}; _scid=cc08fcb8-98f8-4d98-ad9f-d03a35f7b829; _sctr=1%7C1692037800000; _tt_enable_cookie=1; _ttp=6b7xfMhe-JCUy5_hbSdC0_ava0S; afUserId=94a240af-2f63-48fe-9e26-3e778ca4ce9b-p; AF_SYNC=1692091281147; _uetvid=16df89b03b4d11ee971c27ce5ab49325; _scid_r=cc08fcb8-98f8-4d98-ad9f-d03a35f7b829; __cf_bm=KzAWTAdQTzovRLSij5INIRACBIh9zJPd_S8dpiqlc8s-1692178507-0-AY0MaxhQhgHmq5mMYUaP9lbPZ5P6i7fIcJt6Yx8ouZlc7X8du9HeBGOzPtcbGtVDrcUoTXM+AyT4x+InzwWh3WM=; OptanonConsent=isGpcEnabled=0&datestamp=Wed+Aug+16+2023+15%3A11%3A28+GMT%2B0530+(India+Standard+Time)&version=6.29.0&isIABGlobal=false&hosts=&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1&AwaitingReconsent=false&geolocation=IN%3BJH; OptanonAlertBoxClosed=2023-08-16T09:41:28.161Z; _gat_UA-76641-8=1; _ga=GA1.2.1842675939.1691671393; _ga_126VYLCXDY=GS1.1.1692178508.4.1.1692178888.59.0.0",
        "Host": "vimeo.com",
        #"Referer": "https://vimeo.com/showcase/10478752?autoplay=1",
        # "Sec-Fetch-Dest": "empty",
        # "Sec-Fetch-Mode": "cors",
        # "Sec-Fetch-Site": "same-origin",
        #"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    # "newrelic": "eyJ2IjpbMCwxXSwiZCI6eyJ0eSI6IkJyb3dzZXIiLCJhYyI6IjM5Mjg0IiwiYXAiOiI3NDQ3NDY4IiwiaWQiOiIxZjc5NzQ3MjFjOTMxZmM2IiwidHIiOiI3Y2FkZjU3NTBlYzYyNjAwNWJkNGE5MjVlNGU2MzI5MCIsInRpIjoxNjkyMTc4ODg5ODM5fX0=",
        "sec-ch-ua": "\"Not/A)Brand\";v=\"99\", \"Google Chrome\";v=\"115\", \"Chromium\";v=\"115\"",
        "sec-ch-ua-mobile": "?0",
        #"sec-ch-ua-platform": "\"Windows\"",
        #"traceparent": "00-7cadf5750ec626005bd4a925e4e63290-1f7974721c931fc6-01",
        #"tracestate": "39284@nr=0-1-39284-7447468-1f7974721c931fc6----1692178889839",
        "x-requested-with": "XMLHttpRequest"
    }
    rr = r.get("https://vimeo.com/_next/jwt",headers= headers)
    data = dict(rr.json())
    return data['token']
token=getToken()
def identify_video_service(url):
    if 'youtube.com' in url:
        return 'YouTube'
    elif 'vimeo.com' in url:
        return 'Vimeo'
    else:
        return 'Unknown'
    
def get_vimeo_captions(token,video_id):
        headers={
        "Authorization":	"jwt "+token,
    "Accept"	:"application/vnd.vimeo.*+json;version=3.4"
    }
        texttrack = r.get("https://api.vimeo.com/videos/"+video_id+"/texttracks",headers= headers)
        data = dict(texttrack.json())
        print("dataaaaa\t",data)
        dataa= r.get(data['data'][0]['link'])
        text = dataa.text
        pattern = r"(\d+)\n(\d{2}:\d{2}:\d+\.\d+) --> (\d{2}:\d{2}:\d+\.\d+)\n([\s\S]*?)(?=\n\d+\n\d{2}:\d{2}:\d+\.\d+ --> \d{2}:\d{2}:\d+\.\d+|\Z)"
        matches = re.findall(pattern, text)
        data = []
        for match in matches:
            data.append({
                "start": match[1],
                "end": match[2],
                "text": match[3].strip()
            })

        # Creating DataFrame
        df = pd.DataFrame(data)
        df["start"] = pd.to_datetime(df["start"])
        df["end"] = pd.to_datetime(df["end"])
        df.drop('end', axis=1,inplace=True)
        start = df.loc[0, 'start']
        # Set the starttime column as the index
        df.set_index("start", inplace=True)

        return df,start


def get_youtube_caption(video_id):
    lst=YouTubeTranscriptApi.get_transcript(video_id)
    df = pd.DataFrame(lst)
    df['end'] = df['start'] +df['duration']
    df['start'] = pd.to_datetime(df['start'], unit='s')
    df['end'] = pd.to_datetime(df['end'], unit='s')
    df['start_time'] = df['start'].dt.time
    df['end_time'] = df['end'].dt.time
    start = df.loc[0, 'start']
    df.set_index("start", inplace=True)
    return df,start


def get_video_caption(video_id,video_type):  
    if video_type=="Vimeo":
        token=use_global_token()

        return get_vimeo_captions(token,video_id)
    elif video_type == "YouTube":
        return get_youtube_caption(video_id)
    
def sample_data(df,interval,key):
    #df.set_index("start", inplace=True)
    grouped = df.resample(str(interval)+"T").agg({key: lambda x: " ".join(x)})
    data=grouped.reset_index()
    return data

def makeJson(df):
    df['summary_x'] = df['summary_x'].str.split("\n-")
    df['overview'] = df['overview'].str.split("\n-")
    df['start'] = pd.to_datetime(df['start'])

# Create a dictionary to store the data
    result = {}

# Iterate through each row of the DataFrame
    for _, row in df.iterrows():
        start = pd.Timestamp(row['start'])
        start_time = row['start'].strftime('%H:%M:%S')
        text = row['text']
        summary = row['summary_x']
        overview = row['overview']

        # Get the hour as an integer (0, 1, 2, ...)
        hour = start.hour

        # If the hour key doesn't exist in the result dictionary, create it
        if hour not in result:
            result[hour] = {
                'start': start_time,
                'overview': overview,
                'data': []
            }
        # if pd.notna(summary).any():  # Check if any element is not NaN
        #     summary_value = summary.tolist()
        # else:
        #     summary_value = "No summary available"
        # Append the data for the current row to the 'data' list
        result[hour]['data'].append({
            'start': start_time,
            'text': text,
            'summary': summary#if not pd.isna(summary) else "No summary available"
        })

# Serialize the dictionary to JSON
    json_result = json.dumps(result, indent=2)
    return json_result

def mergeDf(data_summary,data_overview):
    print("Columnssssssss",data_summary.columns)
    print("Columnssssssss0",data_overview.columns)
    if data_summary['start'][0].time().minute != 0:
        start = data_summary.loc[0, 'start']
        data_overview.at[0, 'start'] = start
    return pd.merge(data_summary, data_overview, on='start', how='outer')

def get_youtube_embed_code(video_id):
    embed_code = f"https://www.youtube.com/embed/{video_id}"
    return embed_code

def get_video_info(url,video_id):
    yt = YouTube(url)
    result ={"title":yt.title,
    "url": url,"video_type":"youtube"}
    return result

def get_vimeo_video_info(video_id):
    token=use_global_token()
    api_url = f'https://api.vimeo.com/videos/{video_id}'
    headers = {
        'Authorization': f'jwt {token}',
    }
    response = r.get(api_url, headers=headers)

    if response.status_code == 200:
        video_data = response.json()
        result ={"title":video_data['name'],
        "url": video_data['link'],
        "video_type":"vimeo"}
        return result
        
    
    

