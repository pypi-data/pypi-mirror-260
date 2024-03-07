import os
import cv2

def makeVideo(path, fps=10, size = (640, 360)):
    filelist = os.listdir(path)
    filelist2 = sorted([os.path.join(path, i) for i in filelist])
    
    video_path = os.path.join('/Users/tiumo/Desktop/SETS/tempcode', 'Video_{}.avi'.format(path.split('/')[-1]))

    video = cv2.VideoWriter(video_path, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), fps,
                            size) 

    for item in filelist2:
        print(item)
        if item.endswith('._'):
            continue
        if item.endswith('.jpg'):
            print(item)
            img = cv2.imread(item)
            video.write(img)

    video.release()
    cv2.destroyAllWindows()
    print('视频合成生成完成啦')


if __name__ == '__main__':
    data_path = r'/Volumes/T7/#datasets/VAD-datasets/avenue/testing/frames/'
    frames_paths = os.listdir(data_path)
    for p in frames_paths:
        if '._' in p:
            continue
        path = os.path.join(data_path, p)
        makeVideo(path, 10)
