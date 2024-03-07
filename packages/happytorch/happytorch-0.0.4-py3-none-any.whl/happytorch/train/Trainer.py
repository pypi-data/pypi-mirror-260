import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import time
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import torch.utils.data as data
import torchvision.transforms as transforms
from torch.autograd import Variable

from collections import OrderedDict
from tqdm import tqdm
import numpy as np
import glob
import random
import os

from itertools import permutations

from ..logger import init_logger
from .utils import setup_seed
from .data import htDataLoader as myDL


class novaArgs:
    def __init__(self, args):
        self.args = self.init_args(args)
        self.seed = self.setup_seed()
        self.logger = self.build_logger()
    
    def init_args(self, args):
        args.train_folder = args.dataset_path+"/"+args.dataset_type+"/training/frames"
        args.test_folder = args.dataset_path+"/"+args.dataset_type+"/testing/frames"    
        return args
    
    def setup_seed(self):
        torch.manual_seed(self.args.seed)
        torch.cuda.manual_seed_all(self.args.seed)
        np.random.seed(self.args.seed)
        random.seed(self.args.seed)
        # torch.backends.cudnn.deterministic = True # 加了会变慢
        return self.args.seed
        
    def build_logger(self):
        return init_logger(self.args)
    

class novaData(novaArgs):
    def __init__(self, args):
        super().__init__(args)
        self.train_batch = self.build_train_batch()
        self.test_batch = self.build_test_batch()
        
    def build_train_batch(self):
        train_dataset = myDL(
            self.args,
            self.args.train_folder,
            transforms.Compose(
                [
                    transforms.ToTensor(),
                ]
            ),
            resize_height=self.args.h,
            resize_width=self.args.w,
            time_step=self.args.t_length - 1,
        )
        self.args.train_size = len(train_dataset)
        train_batch = data.DataLoader(
            train_dataset,
            batch_size=self.args.batch_size,
            shuffle=True,
            num_workers=self.args.num_workers,
            drop_last=True,
        )
        return train_batch

    def build_test_batch(self):
        test_dataset = myDL(
            self.args.test_folder,
            transforms.Compose(
                [
                    transforms.ToTensor(),
                ]
            ),
            resize_height=self.args.h,
            resize_width=self.args.w,
            time_step=self.args.t_length - 1,
        )

        self.args.test_size = len(test_dataset)

        test_batch = data.DataLoader(
            test_dataset,
            batch_size=self.args.test_batch_size,
            shuffle=False,
            num_workers=self.args.num_workers_test,
            drop_last=False,
        )
        return test_batch

    def save_checkpoint(self):
        self.logger.info("now: {}, pre_best: {}".format(self.now_acc, self.best_acc))
        if self.now_acc > self.best_acc:
            self.best_acc = self.now_acc
            self.logger.info("Epoch {}, Best checkpoint is saved at {}".format(self.epoch, self.args.output_dir))
            torch.save(self.model.state_dict(), os.path.join(self.args.output_dir, "model_best.pth"))
            torch.save(self.m_items, os.path.join(self.args.output_dir, "keys_best.pt"))
        else:
            torch.save(self.model.state_dict(), os.path.join(self.args.output_dir, "model.pth"))
            torch.save(self.m_items, os.path.join(self.args.output_dir, "keys.pt"))
            
            self.logger.info(f"Epoch {self.epoch} | Training checkpoint saved at {self.args.output_dir}")
            

class novaModel(novaData):
    def __init__(self, args):
        super().__init__(args)
        
        self.model = self.build_model()
        self.optimizer = self.build_optimizer()
        self.scheduler = self.build_scheduler()
        self.loss_func = self.build_loss_fun()

    def build_model(self):
        return torch.hub.load('pytorch/vision:v0.10.0', 'vgg11')

    def build_optimizer(self):
        return torch.optim.Adam(self.model.parameters(), lr=self.args.lr)
    
    def build_scheduler(self):
        return optim.lr_scheduler.CosineAnnealingLR(
            self.optimizer, T_max=self.args.epochs
        )

    def build_loss_fun(self):
        return nn.MSELoss(reduction="none")


class novaEvaluator(novaModel):
    def __init__(self, args):
        super().__init__(args)

    def test(self):
        pass

class novaTrainer(novaModel):
    def __init__(self, args):
        super().__init__(args)
        self.now_acc = 0
        self.best_acc = -1

    def _run_batch(self, inputs):
        images, clip_feas = inputs
        imgs, imgs_r, gt_r = self.inputs2imgs(images)
        clip_feas = clip_feas.cuda()
        
        # semantic_p  = self._clip(inputs[-2])
        # semantic_f = self._clip(inputs[-1])

        # context_p = semantic_p.view(-1, 512, 1, 1).expand(-1, 512, 32, 32)

        out_list, seq, pred_sem, non_sem = self.model.forward(
            imgs[:, 0 : 3 * (self.args.t_length - 1)],
            self.m_items,
            imgs_r,
            clip_feas[:, :4],
            True)

        (   outputs,
            _,
            _,
            m_items,
            softmax_score_query,
            softmax_score_memory,
            separateness_loss,
            compactness_loss,
        ) = out_list


        loss_pixel = torch.mean(
            self.loss_func_mse(outputs, imgs[:, 3 * (self.args.t_length - 1) :])
        )

        loss_r = self.compute_loss(seq, gt_r)
        loss_semantic = self.bak_compute_semantic_loss(pred_sem, clip_feas[:, -1])
        # loss_semantic = self.compute_semantic_loss(pred_sem, clip_feas[:, -1], non_sem)
        

        loss = (
            loss_pixel
            + self.args.loss_compact * compactness_loss
            + self.args.loss_separate * separateness_loss  
            + loss_r * self.args.loss_w_sorting
            + loss_semantic * self.args.loss_w_semantic
        )

        if self.iters is not None:
            self.logger.info(
                "iter: {} / Loss: Prediction {:.6f} / Compact: {:.6f} / Separate: {:.6f} / Sort: {:.6f} / Semantic: {:.6f}".format(
                    self.iters,
                    loss_pixel.item(),
                    separateness_loss.item(),
                    compactness_loss.item(),
                    loss_r.item(),
                    loss_semantic.item()
                )
            )

        self.optimizer.zero_grad()
        loss.backward(retain_graph=True)
        self.optimizer.step()

    def _run_epoch(self):
        with tqdm(total=len(self.train_batch)) as pbar:
            pbar.set_description("Epoch {} / {}".format(self.epoch, self.args.epochs))
            for i, inputs in enumerate(self.train_batch):
                self.iters = i + self.epoch * len(self.train_batch) 
                # self.iters = i 

                self.iters = self.iters if self.iters % self.args.logger_iters == 0 else None

                self.model.train()
                self._run_batch(inputs)

                pbar.update(1)
            pbar.close()
        self.scheduler.step()

    def train(self):
        self.model.train()
        
        self.logger.info("Training dataset {}~".format(self.args.dataset_type))
        self.logger.info("The output directory is {}".format(self.args.output_dir))
        
        if self.args.load_best_dir != '':
            print('*'*30)
            print('loading pre-trained weights:', self.args.load_best_dir)
            print('*'*30)
    
            model_path = os.path.join(self.args.load_best_dir, 'model_best.pth')
            m_items_path = os.path.join(self.args.load_best_dir, 'keys_best.pt')
            
            state_dict = torch.load(model_path)
            # model = STLN(self.args).cuda()
            self.model.load_state_dict(state_dict, strict=False)
            self.m_items = torch.load(m_items_path).cuda().clone()

        for epoch in range(self.args.epochs):
            self.epoch = epoch
            self.logger.info(
                "Epoch: {} & Totol epochs: {}".format(self.epoch, self.args.epochs)
            )

            self.model.train()
            self._run_epoch()

            if ((self.epoch + 1) % self.args.eval_epochs == 0) or (
                self.epoch == self.args.epochs - 1
            ):
                # self.evaluate()
                self.test()
                self._save_checkpoint()
                

        self.logger.info("Training is finished")
