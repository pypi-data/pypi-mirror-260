import numpy as np
import os 
from glob import glob

preds = np.load('/data/datadata/#datasets/VAD-datasets/a_preds/avenue2.npz')

save_name = '/data/datadata/#datasets/VAD-datasets/a_preds/avenue2_pro.npz'

# length_list = [1439, 1211, 923, 947, 1007, 1283, 605, 36, 1175, 842, 472, 1271, 549, 507, 1001, 740, 427, 294, 249, 273, 76]
a = np.array([1439, 1211, 923, 947, 1007, 1283, 605, 36, 1175, 841, 472, 1271, 549, 507, 1001, 740, 426, 294, 248, 273, 76])

# print(sum(length_list))


# test_dir = '/data/datadata/#datasets/VAD-datasets/avenue/testing/frames'

# videos_list = sorted(glob(os.path.join(test_dir, "*")))

# print(len(videos_list))


# temp_list = []
# for video in videos_list:
#     temp_list.append(len(glob(os.path.join(video, "*.jpg"))))

# print(temp_list)
# print(sum(temp_list))

# gt = np.load('/data/datadata/#datasets/VAD-datasets/data/frame_labels_avenue.npy')
# print(gt.shape)


print(preds['arr_0'].shape)

preds = preds['arr_0']
a = a-4
print(sum(a))
start = 0
end = 0

new_preds = []
for aaa in a:
    end += aaa
    temp = preds[start:end]
    temp2 = np.concatenate((np.array([1,1,1,1]), temp))
    new_preds.append(temp2)
    start = end
    print(temp.shape)
    
pred_pro = np.concatenate(new_preds, axis=0)
np.savez(save_name, pred_pro)
print(pred_pro.shape)