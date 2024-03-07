import numpy as np
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from matplotlib.patches import FancyArrowPatch, Rectangle
from matplotlib.gridspec import GridSpec

from glob import glob
import os
from collections import OrderedDict
from PIL import Image, ImageOps
import cv2

from tqdm import tqdm

from .src_imgs import movie_picture


def load_test_data(dataset_type, data_folder, preds_list=None):
    labels = np.load(
        os.path.join(data_folder, 'data',
            "frame_labels_" + dataset_type + ".npy",
        )
    ).squeeze()
    
    datadata = np.load(preds_list[0][0])
    preds_1 = datadata['arr_0']
    
    datadata2 = np.load(preds_list[0][1])
    preds_2 = datadata2['arr_0']
    

    videos = OrderedDict()
    test_folder = os.path.join(data_folder, dataset_type, "testing/frames")
    videos_list = sorted(glob(os.path.join(test_folder, "*")))

    label_length = 0

    for xxx, video in enumerate(videos_list):
        video_name = video.split("/")[-1]
        videos[video_name] = {}
        videos[video_name]["path"] = video
        videos[video_name]["frame"] = glob(os.path.join(video, "*.jpg"))
        videos[video_name]["frame"].sort()
        videos[video_name]["length"] = len(videos[video_name]["frame"])
        # -------------------------------------------------------------
        temp2 = labels[  
                    label_length : videos[video_name]["length"] + label_length
                ]
        videos[video_name]["label"] = temp2
        # -------------------------------------------------------------
        temp = preds_1[label_length: videos[video_name]["length"] + label_length]
        videos[video_name]['pred'] = temp
        # -------------------------------------------------------------
        
        temp1 = preds_2[label_length: videos[video_name]["length"] + label_length]
        videos[video_name]['pred2'] = temp1
        
                        
        label_length += videos[video_name]["length"] 
    
    return labels, videos, videos_list



def add_semi_transparent_border(image, border_size=40, transparency=0.2):

    w, h = (image.shape[1], image.shape[0])
    
    # 在图像上画一个半透明的矩形
    cv2.rectangle(image, (border_size//2, border_size//2), (w-border_size//2, h-border_size//2), (68, 131, 222, int(255 * transparency)), border_size)

    return image

def open_image(image_path):
    image = np.array(cv2.imread(image_path))
# 创建一个具有透明度的图像，使用BGRA格式
    image_with_alpha = np.zeros((image.shape[0], image.shape[1], 4), dtype=np.uint8)
    image_with_alpha[:, :, :3] = image  # 复制BGR通道
    image_with_alpha[:, :, 3] = 255  # 设置Alpha通道为255（不透明）
    return image_with_alpha


def img_movies(img):
    movies = movie_picture()
        
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
                img_array= add_semi_transparent_border(np.array(img_array), border_size=15, transparency=0.5)
        else:
            img_array2 = open_image(v)
            img_array2 = img_movies(img_array2)
            if idx in abnormals:
                img_array2 = add_semi_transparent_border(np.array(img_array2), border_size=15, transparency=0.5)

            img_array = np.concatenate((img_array, img_array2), axis=1)  # 横向拼接
            # img_array = np.concatenate((img_array, img_array2), axis=0)  # 纵向拼接
    return Image.fromarray(cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB))


def vis_score_curve(data_folder, dataset_type, preds_list, save_dir, prefix_name='vis', save_format="png"):
    
    
    labels, videos, videos_list = load_test_data(dataset_type, data_folder, preds_list)
    
    for video in tqdm(videos_list):
        video_name = video.split("/")[-1]
        
        y = videos[video_name]["label"]
        p = videos[video_name]["pred"]
        p2 = videos[video_name]["pred2"]
        
        x = range(0, len(y))
        abnormals = np.where(y == 1)[0]
        start_a = np.where(np.diff(y) == 1)[0]
        end_a = np.where(np.diff(y) == -1)[0]

        images = concat_images(videos[video_name]["frame"], [i for i in range(0, len(y), len(y)//6)], abnormals)
        
        fig = plt.figure(figsize=(20, 7))
        gs = GridSpec(5, 1, figure=fig)
        # 设置字体为 Times New Roman
        plt.rcParams['font.family'] = 'Times New Roman'
        
        plt.subplots_adjust(hspace=0.05, wspace=0) 
        
        # -----------------------------------------------------------------------------------------
        ax_img = fig.add_subplot(gs[0:2, 0]) 
        ax_1 = fig.add_subplot(gs[2, 0])
        ax_2 = fig.add_subplot(gs[3, 0])
        ax_3 = fig.add_subplot(gs[4, 0])
        ax_1.set_ylabel('GT')
        ax_2.set_ylabel('Baseline')
        ax_3.set_ylabel('Proposed')
        
        ax_img.imshow(images)
        ax_img.axis('off')  # 关闭坐标轴
        
        # -----------------------------------------------------------------------------------------
        
        for s,e in zip(start_a, end_a):
            ax_1.axvspan(s, e, alpha=1.0, color='#a0c789')
        ax_1.set_xlim(0, len(y))
        
        ax_1.tick_params(axis='both', which='both', bottom=False, top=False, left=False, right=False, labelbottom=True, labelleft=False)
        
        x_tricks = np.sort(np.concatenate([np.insert(start_a, 0, 0), np.append(end_a, len(y))]))
        plt.sca(ax_1)  # 设置当前活动的Axes对象为ax_3
        plt.xticks(x_tricks)
        ax_1.xaxis.set_ticks_position('top')
        ax_1.tick_params(axis='x', direction='inout', pad=0, rotation=90)
        # -----------------------------------------------------------------------------------------
        
        ax_2.plot(x, p, color='#001bf8')
        for s,e in zip(start_a, end_a):
            ax_2.axvspan(s, e, alpha=1.0, color='#b9cae7')
        
        ax_2.set_ylim(0, 1)
        ax_2.set_xlim(0, len(y))
        
        ax_2.tick_params(axis='both', which='both', bottom=False, top=False, left=False, right=False, labelbottom=False, labelleft=False)
        
        # -----------------------------------------------------------------------------------------

        ax_3.plot(x, p2, color='#001bf8')
        for s,e in zip(start_a, end_a):
            ax_3.axvspan(s, e, alpha=1.0, color='#b9cae7')
        
        ax_3.set_ylim(0, 1)
        ax_3.set_xlim(0, len(y))
        
        ax_3.tick_params(axis='both', which='both', bottom=False, top=False, left=False, right=False, labelbottom=False, labelleft=False)

        # -----------------------------------------------------------------------------------------
        fig.savefig(os.path.join(save_dir, prefix_name + "_" + video_name + "." + save_format))
        
        plt.close()
        plt.close()
        plt.close()
        plt.close() # 一个close对应一个子图
        
    
    return None

if __name__ == "__main__":
    data_folder = "/data/datadata/#datasets/VAD-datasets"
    dataset_type = "avenue"
    preds_list = ['/data/datadata/#datasets/VAD-datasets/a_preds/avenue_pro.npz', '/data/datadata/#datasets/VAD-datasets/a_preds/avenue2_pro.npz'],
    save_dir = "/home/nemo/Mourn/a2pip/test/outputs"

    vis_score_curve(data_folder, dataset_type, preds_list, save_dir)
    