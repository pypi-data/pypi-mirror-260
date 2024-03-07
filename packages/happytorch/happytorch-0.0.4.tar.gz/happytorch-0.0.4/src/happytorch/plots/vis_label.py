import numpy as np
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from matplotlib.patches import FancyArrowPatch, Rectangle
from glob import glob
import os
from collections import OrderedDict
from PIL import Image, ImageOps
import cv2

from tqdm import tqdm

def load_test_data(label_dir, dataset_type, data_folder):
    labels = np.load(
        os.path.join(label_dir,
            "frame_labels_" + dataset_type + ".npy",
        )
    ).squeeze()
    
    
    videos = OrderedDict()
    test_folder = os.path.join(data_folder, dataset_type, "testing/frames")
    videos_list = sorted(glob(os.path.join(test_folder, "*")))

    label_length = 0
    
    for video in videos_list:
        video_name = video.split("/")[-1]
        videos[video_name] = {}
        videos[video_name]["path"] = video
        videos[video_name]["frame"] = glob(os.path.join(video, "*.jpg"))
        videos[video_name]["frame"].sort()
        videos[video_name]["length"] = len(videos[video_name]["frame"])
        
        videos[video_name]["label"] = labels[label_length: videos[video_name]["length"] + label_length]
                
        label_length += videos[video_name]["length"] 
    
    return labels, videos, videos_list

def add_semi_transparent_border(image, border_size=40, transparency=0.2):

    w, h = (image.shape[1], image.shape[0])
    
    # 在图像上画一个半透明的矩形
    cv2.rectangle(image, (border_size//2, border_size//2), (w-border_size//2, h-border_size//2), (0, 0, 255, int(255 * transparency)), border_size)

    return image

def open_image(image_path):
    image = np.array(cv2.imread(image_path))
     # 创建一个具有透明度的图像，使用BGRA格式
    image_with_alpha = np.zeros((image.shape[0], image.shape[1], 4), dtype=np.uint8)
    image_with_alpha[:, :, :3] = image  # 复制BGR通道
    image_with_alpha[:, :, 3] = 255  # 设置Alpha通道为255（不透明）
    return image_with_alpha


def img_movies(img):
    movies = cv2.imread("/userHome/nemo/projects/sorting/visualize/movie1.png", cv2.IMREAD_UNCHANGED)
    
    h1, w1 = img.shape[:2]
    h2, w2 = movies.shape[:2]
    
    movies = cv2.resize(movies, (w1, h2*w1//w2))
    img_array = np.concatenate((movies, img, movies), axis=0)  # 纵向拼接
    return img_array
    

def concat_images(frames, i_list, abnormals):
    for i, idx in enumerate(i_list):
        v = frames[idx]
        if i == 0:
            img_array = open_image(v)  # 打开图片
            img_array = img_movies(img_array)
            
            if idx in abnormals:
                # img = ImageOps.expand(img, border=n, fill='red')
                # img = img.resize((x, y))
                img_array= add_semi_transparent_border(np.array(img_array), border_size=20, transparency=0.5)
        else:
            img_array2 = open_image(v)
            img_array2 = img_movies(img_array2)
            if idx in abnormals:
                img_array2 = add_semi_transparent_border(np.array(img_array2), border_size=20, transparency=0.5)

            img_array = np.concatenate((img_array, img_array2), axis=1)  # 横向拼接
            # img_array = np.concatenate((img_array, img_array2), axis=0)  # 纵向拼接
    return Image.fromarray(cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB))


if __name__ == "__main__":
    labels, videos, videos_list = load_test_data(
        "/userHome/nemo/projects/sorting/data",
        "avenue",
        "/userHome/nemo/datasets/",
    )

    for video in tqdm(videos_list):
        video_name = video.split("/")[-1]
        ax = plt.figure()
        y = videos[video_name]["label"]
        x = range(0, len(y))
        
        abnormals = np.where(y == 1)[0]
        
        start_a = np.where(np.diff(y) == 1)[0]+1
        end_a = np.where(np.diff(y) == -1)[0]+1

        images = concat_images(videos[video_name]["frame"], [i for i in range(0, len(y), len(y)//6)], abnormals)
        # 然后【采样】标识异常帧
            
        ## 画图
        
        fig = plt.figure(figsize=(15,7))
        
        ax1 = plt.subplot(211)
        
        plt.imshow(images)
                
        plt.xticks([])  # 去掉x轴
        plt.yticks([])  # 去掉y轴
        plt.axis('off')  # 去掉坐标轴
        
        ax2 = plt.subplot(212)
        plt.plot(x, y)
        for s,e in zip(start_a, end_a):
            plt.axvspan(s, e, alpha=0.1, color='red')
            
            img_index = np.random.choice(range(s,e))
            random_number = np.random.uniform(0.4, 0.9)

            img = Image.open(videos[video_name]["frame"][img_index])

            imagebox =OffsetImage(img, zoom=0.15)
            ab = AnnotationBbox(imagebox, (img_index, random_number), frameon=False, pad=0)
            ax2.add_artist(ab) 
            
            arrow = FancyArrowPatch((img_index, 1), (img_index, random_number), arrowstyle='<-', mutation_scale=15, color='gray')
            ax2.add_patch(arrow)   
            
        plt.xlim(0, len(y))
        x_tricks = np.sort(np.concatenate([np.insert(start_a, 0, 0), np.append(end_a, len(y))]))
        plt.xticks(x_tricks, rotation=45)
        # plt.ylim(-0.1, 1)
        
        fig.tight_layout()
        fig.savefig('/userHome/nemo/projects/sorting/visualize/figs/label_{}.png'.format(video_name))
        plt.close()
        plt.close()
        