import pandas as pd
from http import HTTPStatus
from dashscope import VideoSynthesis
import time

def batch_generate_videos(excel_path):
    
    df = pd.read_excel(excel_path)
    
    video_urls = []
    status_list = []

    df['combined_prompt'] = df['prompt'].astype(str) + ',' + df['camera_angle'].astype(str)
    df['combined_prompt'] = df['prompt'].fillna('') + ',' + df['camera_angle'].fillna('')
    
    for index, combined_prompt in enumerate(df['combined_prompt']):
    # enumerate is a built-in function that is used to convert an iterable object (such as a list, tuple, string, or Pandas column) into an indexed sequence so that both the index and the value of an element can be obtained when iterating.
        print('----sync call, please wait a moment----')
        rsp = ImageSynthesis.call(api_key=os.getenv("DASHSCOPE_API_KEY"),
                                  model="wanx2.1-t2i-turbo",
                                  prompt=combined_prompt,
                                  n=1,
                                  size='1024*1024')
        print('response: %s' % rsp)
        if rsp.status_code == HTTPStatus.OK:

            for result in rsp.output.results:
                file_name = PurePosixPath(unquote(urlparse(result.url).path)).parts[-1]
                with open('./%s' % file_name, 'wb+') as f:
                    f.write(requests.get(result.url).content)
        else:
            print('sync_call Failed, status_code: %s, code: %s, message: %s' %
                  (rsp.status_code, rsp.code, rsp.message))

        time.sleep(300) 

if __name__ == '__main__':
    batch_generate_videos(r"xxx.xlsx")