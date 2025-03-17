import pandas as pd
from http import HTTPStatus
from dashscope import VideoSynthesis
import time

def batch_generate_videos(excel_path):
    
    df = pd.read_excel(excel_path)
    
    video_urls = []
    status_list = []

    df['combined_prompt'] = df['prompt'].astype(str) + ',' + df['camera_angle'].astype(str)
    
    for index, combined_prompt in enumerate(df['combined_prompt']):

        try:
            print(f'Generating the {index+1}/{len(df)}th video...')
            
            rsp = VideoSynthesis.call(
                model='wanx2.1-t2v-turbo',
                prompt=combined_prompt,
                size='1280*720'
            )

            print(rsp)
            
            if rsp.status_code == HTTPStatus.OK:
                print(rsp.output.video_url)
                video_urls.append(rsp.output.video_url)
                print(f'The {index+1}/{len(df)}th video has been generated')
                status_list.append('Success')
            else:
                 print('Failed, status_code: %s, code: %s, message: %s' %
                      (rsp.status_code, rsp.code, rsp.message))
            
        except Exception as e:
            video_urls.append('')
            status_list.append(f'异常：{str(e)}')
            continue
            
        time.sleep(1800) 
    
    df['video_url'] = video_urls
    df['status'] = status_list

    df.to_excel(excel_path, index=False)
    print(f'All text generation videos have been completed!')


if __name__ == '__main__':
    batch_generate_videos(r"xxx.xlsx")

