from TikTokApi import TikTokApi
import asyncio
import os
import pandas as pd
import datetime
import json
import json
import sys
ms_token = os.environ.get(
    "ms_token", None
)  # set your own ms_token, think it might need to have visited a profile

sys.setrecursionlimit(1200)
async def get_video_example(url="https://vt.tiktok.com"):
    async with TikTokApi() as api:
        await api.create_sessions(ms_tokens=[ms_token], num_sessions=1, sleep_after=3)
        video = api.video(
            url=url
        )
        
        video_info = await video.info()
        return video_info['stats']


async def process_urls(url_list, index=0):
    try:
        if index >= len(url_list):
            return
        
        url = url_list[index]
        if os.path.exists(f'TikiToko/result.json'):
            try:
                with open(f'TikiToko/result.json', 'r') as f:
                    current_list = json.load(f)
                urls_checked = [current_list[key]['url'] for key in current_list.keys()]
                NEW_INDEX = max([int(key) for key in current_list.keys()]) + 1
                
                with open(f'TikiToko/result - Copy.json','w') as f:
                    json.dump(current_list, f)
            
                if url in urls_checked:
                    await process_urls(url_list, index + 1)
                    return
            except:
                current_list = {}
                NEW_INDEX = 1
        else:
            current_list = {}
            NEW_INDEX = 1
            
        try :
            res = await get_video_example(url)
            # Process the result here (e.g., store in a database, append to a list, etc.)
            views, like, share, comment = res['playCount'], res['diggCount'], res['shareCount'], res['commentCount']
            
            result = {
                'url': url,
                'views': views,
                'likes': like,
                'shares': share,
                'comments': comment,
                'error' : ''
            }
            
            with open(f'TikiToko/result.json','w') as f:
                current_list[NEW_INDEX] = result
                json.dump(current_list, f)
        except :
            
            result = {
                'url': url,
                'views': -1,
                'likes': -1,
                'shares': -1,
                'comments': -1,
                'error' : 'error'
            }
            
            with open(f'TikiToko/result.json','w') as f:
                current_list[NEW_INDEX] = result
                json.dump(current_list, f)
        
        await process_urls(url_list, index + 1)
    except Exception as e:
        print(e)
        print(f'Error processing {url} at index {index}')


if __name__ == "__main__":
    data_url = pd.read_excel('TikiToko\Data List.xlsx',sheet_name='data')
    url_list = data_url['Link video tiktok anda '].tolist()
    # url_list = url_list[:10]
    if len(url_list) > 0:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(process_urls(url_list))
    else:
        print('No URLs to process')
    

