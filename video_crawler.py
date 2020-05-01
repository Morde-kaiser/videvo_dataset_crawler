import requests
import re
from bs4 import BeautifulSoup
from tqdm import tqdm
from time import sleep
import time
import random
import os


def download_videos():
    requests.DEFAULT_RETRIES = 5  # 增加重连次数
    s = requests.session()
    s.keep_alive = False  # requsets库里面http connection 是 keep alive 的，一定要把它关了，否则就卡死了
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/'
                      '537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36'
    }
    html = requests.get('https://www.videvo.net/stock-video-footage/video/sort/random/freeclips/yes/',
                        headers=header).text
    bs = BeautifulSoup(html, 'html.parser')
    video_ids_naive = bs.find_all(['div'], {'class': 'video-thumb-inner'})
    reg = r'<a href="(.*?)">'
    video_ids = re.findall(reg, str(video_ids_naive))  # 这里以及成功找到每一个小图片的相对地址

    video_urls = []
    start_url = 'https://www.videvo.net'
    for video_id in video_ids:
        video_urls.append(start_url + video_id)  # 这里得到封面上每个视频的绝对地址的列表，我们还要再进一步点进去

    # ---------------------------下面这一部要花不少时间，因为要打开每一个页面，然后下载里面的视频----------------------- #
    downloadable_urls = []
    name_list = []
    for video_url in tqdm(video_urls):  # 第一个tqdm用于把可下载的视频的网址和名字保存下来，全部扒下来以后先sleep(3)让requests休息一下
        sleep(0.5 + random.random())  # 适当延时一会，规避网站反爬虫机制
        html = requests.get(video_url, headers=header).text  # 图片点进去的页面，我们要在里面找到视屏播放的地址， 结尾一般是mp4结构
        reg = r'<source type="video/mp4" src="(.*?)">'
        downloadable_urls.append(re.findall(reg, html)[0])  # 每个图片的下载路径确实是找到了，但是有一些还是相对路径，非常令人恼火

        reg = '<span itemprop="name">(.*?)</span>'
        name_list.append(re.findall(reg, html)[0])  # 这里把每个视频的名字也爬下来

    downloadable_urls_robust = []
    base_url = 'https://cdn.videvo.net'
    for url in downloadable_urls:
        if not str(url).startswith('https://'):
            url = base_url + url
        downloadable_urls_robust.append(url)

    for url in downloadable_urls_robust:
        print(url)

    for name in name_list:
        print(name)

    path = 'video'
    if path not in os.listdir():
        os.mkdir(path)  # 这里是视频的下载地址

    #  正式进入下载阶段
    for i in tqdm(range(min(len(name_list), len(downloadable_urls_robust)))):
        print("正在下载第 %d 个视频，视频名: %s" % (i + 1, name_list[i]))
        sleep(0.5 + random.random())  # 休息一下，反爬
        movie_url = downloadable_urls_robust[i]
        movie_name = name_list[i]
        downsize = 0
        start_time = time.time()
        req = requests.get(movie_url, headers=header, stream=True, verify=False)
        file_path = path + '/%s.mp4' % movie_name
        with(open(file_path, 'wb')) as f:
            for chunk in req.iter_content(chunk_size=10000):
                if chunk:
                    f.write(chunk)
                    downsize += len(chunk)
                    line = 'downloading %d KB/s - %.2f MB， 共 %.2f MB'
                    line = line % (
                        downsize / 1024 / (time.time() - start_time), downsize / 1024 / 1024, downsize / 1024 / 1024)
                    print(line)


download_videos()
