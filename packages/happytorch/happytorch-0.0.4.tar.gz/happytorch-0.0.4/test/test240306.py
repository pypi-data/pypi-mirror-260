from happytorch import score_curve


data_folder = "/data/datadata/#datasets/VAD-datasets"
dataset_type = "avenue"
preds_list = ['/data/datadata/#datasets/VAD-datasets/a_preds/avenue_pro.npz', '/data/datadata/#datasets/VAD-datasets/a_preds/avenue2_pro.npz'],
save_dir = "/home/nemo/Mourn/a2pip/test/outputs"

score_curve.vis_score_curve(data_folder, dataset_type, preds_list, save_dir)