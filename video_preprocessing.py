'''
首先把video这个视频数据集下载下来，再运行这段代码  
作用是对video文件夹里面的116个视频的每一个视频逐帧裁剪成640*360的格式以后放到相应的文件夹，图片格式为jpg，这样文件大小会小一些
裁剪格式和图片格式都可以在下面代码自行调整

有一个问题就是116个视频里面有5个视频竟然播放不了，其对应的文件夹都是空的，我就自己再定义了一个函数，把空目录全部删了

'''
import os
import cv2


def del_emp_dir(path):
    for (root, dirs, files) in os.walk(path):
        for item in dirs:
            dir = os.path.join(root, item)
            try:
                os.rmdir(dir)  # os.rmdir() 方法用于删除指定路径的目录。仅当这文件夹是空的才可以, 否则, 抛出OSError。
                print(dir)
            except Exception as e:
                print('Exception', e)


data_path = 'video'
video_list = [file for file in os.listdir(data_path) if file[0] != "."]  # 所有视频的名称
video_list.sort()
frame_path = 'Frames'  # 这个文件夹里面就是把所有视频的帧都拿出来，裁剪成640*360, 再逐帧保存回去
if frame_path not in os.listdir():
    os.mkdir(frame_path)

video_num = len(video_list)  # 这里有116个视频，但是有5个视频好像读不出来，所以只有111个视频的帧数

for i in range(video_num):
    video = cv2.VideoCapture(os.path.join(data_path, video_list[i]))  # 打开所有视频的绝对路径
    clean_video_name = video_list[i].rstrip('.mp4')  # 这样文件名好看一点
    os.mkdir('Frames/' + clean_video_name)  # 做好每个视频的文件夹，里面要放该视频的所有帧数

    frames = []

    framecount = 0
    while video.isOpened():
        ret, frame = video.read()

        if ret:
            framecount += 1
            each_frame_path = 'Frames/' + clean_video_name + '/' + str(framecount) + '.jpg'  # 每一帧的图片的绝对路径
            res = cv2.resize(frame, (640, 360), interpolation=cv2.INTER_AREA)
            # cv2.imshow("Image", res)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()
            cv2.imwrite(each_frame_path, res)
        else:
            video.release()

del_emp_dir('Frames')
