import googleapiclient.discovery
import pandas as pd

# Set your YouTube API keys
API_KEYS = [
    "AIzaSyABYBAG8OT1J0vCfdHu3XvqJbDqagOKVeI",  # ttsawsum
    "AIzaSyDbODBb34oc0vlSmzp-Cljvh717Dcxx8Yk",  # greatfirewall
    "AIzaSyD8-KDroWmAFvNMBl4rXcZ_C7cX-1ro6to"   # Brett
]
API_Count = 150
API_INDEX = 2

#Conservative Focus Group
CandaceOwens = 'UCL0u5uz7KZ9q-pe-VC8TY-w'
Peterson = 'UCL_f53ZEJxp8TtlOkHwMV9Q'
Shapiro = 'UCnQC_G5Xsjhp9fEJKuIcrSw'
DailyWire = 'UCaeO5vkdj5xOQHp4UmIN6dw'
#conservatives Video Essays
PragerU = 'UCZWlSUNDvCCS1hBiXV0zKcA'
JohnDoyle = 'UCzZpgppwC_XQMe8lFiI77-Q'
BlackPigeonSpeaks = '' # Too recent to be useful I think, only 23 videos
#Conservative news etc
MattWalsh = 'UCO01ytfzgXYy4glnPJm4PPQ'
TheQuartering = 'UCfwE_ODI1YTbdjkzuSi1Nag'
TimPool = 'UCG749Dj4V2fKa143f8sE60Q'
LaurenChen = 'UCLUrVTVTA3PnUFpYvpfMcpg'
StevenCrowder = 'UCIveFvW-ARp_B_RckhweNJw'
CharlieKirk = 'UCfaIu2jO-fppCQV_lchCRIQ'

#Liberal Video Essays
PhilosphyTube = 'UCNL8SCfixpPsU5shwmv9Kuw'
Shaun = 'UCJ6o36XL0CpYb6U5dNBiXHQ'
Contrapoints = 'UCNvsIonJdJ5E4EXMa65VYpA'
BigJoel = 'UCaN8DZdc8EHo5y1LsQWMiig'
InnuendoStudios = 'UC5fdssPqmmGhkhsJi4VcckA'
Jose = 'UCeDKIj0G5XbultKOQnacu_w'
FD_Signifier = 'UCgi2u-lGY-2i2ubLsUr6FbQ'
LeejaMiller = 'UCb3cDvWiHwRzQaK81PrISbg'
DokiDokiDisclosure = 'UCgQcWW5Tbfnv79TT41thXKQ'  # Smaller channel
# Liberal News / Shows/ Podcasts
Sam_Harris = 'UCNAxrHudMfdzNi6NxruKPL'   # ERROR
HasanAbi = 'UCtoaZpBnrd0lhycxYJ4MNOQ'
Vaush = 'UC1E-JS8L0j1Ei70D9VEFrPQ'
TheKavernacle = 'UCoG5ya-sMXNMkqkIz1sZ_Lw'
TheMajorityReportwithSamSeder = 'UC-3jIAlnQmbbVMV6gR7K8aQ'
TheDavidPakmanShow = 'UCvixJtaXuNdMPUGdOPcY8Ag' #NEED MORE IS LONG

#Controls
TSeries=''
PewDiePie='UC-lHJZR3Gqxm24_Vd_AJ5Yw'
SchaffrillasProductions = 'UC5UYMeKfZbFYnLHzoTJB1xA'
DafuqBoom = 'UCsSsgPaZ2GSmO6il8Cb5iGA'
AlternateHistoryHub = 'UClfEht64_NrzHf8Y0slKEjw'
DougDoug = 'UClyGlKOhDUooPJFy4v_mqPg'
CaptainMidnight = 'UCROQqK3_z79JuTetNP3pIXQ'
RTGame = 'UCRC6cNamj9tYAO6h_RXd5xA'
Izzzyzzz = 'UCWyRlMktpKbfefqBQk8U6Nw'
DudePerfect = 'UCRijo3ddMTht_IHyNSNXpNQ'
ToddintheShadows = 'UCaTSjmqzOO-P8HmtVW3t7sA'
AnaIsabel = 'UCZTTxoM7GT-NVe52xqP0cXw'  # Only 35 videos
ScotttheWoz = 'UC4rqhyiTs7XyuODcECvuiiQ'
NeoPunkFM = 'UCHQwadnN4MCnMpunnJxZyGQ'
MrBeast = 'UCX6OQ3DkcsbYNE6H8uQQuVA'
AdrianGrayComedy = 'UCvulgQYQPPUMwCs7tKMXO0g'
TheCosmonautVarietyHour = 'UCqTYHSnBUXZamsVcOlQf-fg'
NeverKnowsBest = 'UC1fKT0wuhchtclPqpdWEnHw'
AmandatheJedi = 'UCiHwDqiw6-2dpSJEXkaCi9Q'
MythKeeper = 'UCaMbwVTAQp3HjC35TNhQjhg'
Spice8Rack = 'UCDJACu5LRKWE7sqagICB-ew'
Geopold = 'UC5wZGwqyPawfmzpve8aJ-hw'
Cocomelon = 'UCbCmjCuTUZos6Inko4u57UQ'
Kapslash = 'UCV67sb8dmMii4Z0CgtKchmA'


CHANNEL_ID_GLOBAl = Geopold
NAME = 'Geopold'


def get_channel_videos(channel_id):
    global API_Count
        
    youtube = googleapiclient.discovery.build('youtube', 'v3', developerKey=API_KEYS[API_INDEX])
    
    videos = []
    next_page_token = None

    # while True:
    #     request = youtube.search().list(
    #         part='snippet',
    #         channelId=channel_id,
    #         maxResults=50,  # Maximum results per page
    #         order='date',   # Order by date (newest first)
    #         pageToken=next_page_token
    #     )
    #     response = request.execute()

    #     videos.extend(response['items'])
    #     next_page_token = response.get('nextPageToken')

    #     if not next_page_token:
    #         break

    # Get playlist of uploaded videos
    resp = youtube.channels().list(id=channel_id, part='contentDetails').execute()
    playlist_id = resp['items'][0]['contentDetails']['relatedPlaylists']['uploads']

    # Get videos from playlist
    while True:
        resp = youtube.playlistItems().list(
            part="snippet",
            maxResults=50,
            playlistId=playlist_id,
            pageToken=next_page_token
        ).execute()
        videos.extend(resp['items'])
        if 'nextPageToken' not in resp:
            break
        next_page_token = resp['nextPageToken']
        API_Count += 50
        youtube = googleapiclient.discovery.build('youtube', 'v3', developerKey=API_KEYS[API_INDEX])

    return videos

def get_video_data(video_id):
    global API_Count
    youtube = googleapiclient.discovery.build('youtube', 'v3', developerKey=API_KEYS[API_INDEX])

    try:
        request = youtube.videos().list(
            part='snippet,contentDetails,statistics',
            id=video_id
        )
        response = request.execute()
        return response['items'][0] if response['items'] else None
    except Exception as e:
        print("Error retrieving video data:", e)
        return None

def main():
    global API_Count
    # Ben Shapiro's Channel ID
    channel_id = CHANNEL_ID_GLOBAl

    # Get all videos from the channel
    print("Fetching videos from the channel...")
    videos = get_channel_videos(channel_id)

    # Create an empty DataFrame to store video data
    video_data_list = []

    print("Retrieving data for each video...")
    for idx, video in enumerate(videos, start=1):
        print(f"Processing video {idx} of {len(videos)}")

        # if 'id' not in video:
        #     print("Invalid video item:", video)
        #     continue

        # video_id = video['id'].get('videoId')
        # if not video_id:
        #     print("Skipping non-video item:", video)
        #     continue

        try:
            video_id = video['snippet']['resourceId']['videoId']
        except Exception:
            print('Invalid video:', video)
            continue

        video_data = get_video_data(video_id)

        if video_data:
            snippet = video_data['snippet']
            content_details = video_data['contentDetails']
            statistics = video_data['statistics']

            # Extracted variables
            title = snippet['title']
            published_at = snippet['publishedAt']
            duration = content_details['duration']
            view_count = statistics.get('viewCount', 'N/A')
            like_count = statistics.get('likeCount', 'N/A')
            dislike_count = statistics.get('dislikeCount', 'N/A')
            channel_title = snippet.get('channelTitle', 'N/A')
            channel_id = snippet.get('channelId', 'N/A')
            description = snippet.get('description', 'N/A')
            tags = ','.join(snippet.get('tags', []))
            category_id = snippet.get('categoryId', 'N/A')
            comment_count = statistics.get('commentCount', 'N/A')
            favorite_count = statistics.get('favoriteCount', 'N/A')

            # Append data to list
            video_data_list.append({
                'Title': title,
                'Published At': published_at,
                'Duration': duration,
                'View Count': view_count,
                'Like Count': like_count,
                'Dislike Count': dislike_count,
                'Channel Title': channel_title,
                'Channel ID': channel_id,
                'Description': description,
                'Tags': tags,
                'Category ID': category_id,
                'Comment Count': comment_count,
                'Favorite Count': favorite_count
            })
        else:
            print("No data found for this video.")

    # Create DataFrame from the list
    df = pd.DataFrame(video_data_list)

    # Save DataFrame to CSV
    df.to_csv(NAME + '_videos.csv', index=False)
    print("Data saved to " + NAME + 'videos.csv')
    print("API_Count: " + str(API_Count))

if __name__ == "__main__":
    main()
