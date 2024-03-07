import os
import yaml
import argparse
import sys


def merge_data(data_1, data_2):
    """
    使用 data_2 和 data_1 合成一个新的字典。
    对于 data_2 和 data_1 都有的 key, 如果data_2为None, 则用data_1, 否则用data_2。
    :param data_1:
    :param data_2:
    :return:
    """
    if isinstance(data_1, dict) and isinstance(data_2, dict):
        new_dict = {}
        d2_keys = list(data_2.keys())
        for d1k in data_1.keys():
            if d1k in d2_keys:  # d1,d2都有。去往深层比对
                d2_keys.remove(d1k)
                new_dict[d1k] = merge_data(data_1.get(d1k), data_2.get(d1k))
            else:
                new_dict[d1k] = data_1.get(d1k)  # d1有d2没有的key
        for d2k in d2_keys:  # d2有d1没有的key
            new_dict[d2k] = data_2.get(d2k)
        return new_dict
    else:
        if data_2 == None: #d2为空使用d1
            return data_1
        else:              #d2不为空使用d2
            return data_2

def loadyaml(file_path):
    with open(file_path, mode="r", encoding="utf-8") as f:
        yamlConf = yaml.load(f.read(), Loader=yaml.FullLoader)
    if "__BASE__" in yamlConf.keys():
        (filedir, _) = os.path.split(file_path) 
        temp_list = yamlConf["__BASE__"] if type(yamlConf["__BASE__"]) is list else [yamlConf["__BASE__"]] 
        for base_config in temp_list:
            yamlConf = merge_data(loadyaml(os.path.join(filedir, base_config)), yamlConf)
    return yamlConf


class Struct:   # 未用到  
    def __init__(self, **entries): 
        self.__dict__.update(entries)

def yaml2object(file_path):   # 未用到   
    yamlConf = loadyaml(file_path)
    args = Struct(**yamlConf)
    return args

def get_parser():
    parser = argparse.ArgumentParser(description = 'A method to update parser parameters using yaml files') 
    
    parser.add_argument("-c", "--config-file", metavar="FILE", help="path to config file")
    parser.add_argument('--gpus', nargs='+', type=str, help='gpus')
    
    parser.add_argument(
        "--resume",
        action="store_true",
        help="Whether to attempt to resume from the checkpoint directory. "
        "See documentation of `DefaultTrainer.resume_or_load()` for what it means.",
    )
    parser.add_argument("--eval-only", action="store_true", help="perform evaluation only")
    parser.add_argument("--num-gpus", type=int, default=1, help="number of gpus *per machine*")
    parser.add_argument("--num-machines", type=int, default=1, help="total number of machines")
    
    return parser 

class Dict(dict):
    __setattr__ = dict.__setitem__
    __getattr__ = dict.__getitem__
    
def dictToObj(dictObj):
    if not isinstance(dictObj, dict):
        return dictObj
    d = Dict()
    for k, v in dictObj.items():
        d[k] = dictToObj(v)
    return d

def get_args(config_file):
    default_args = get_parser().parse_args()
    default_args.config_file = config_file
    args = merge_data(loadyaml(config_file), vars(default_args))
    
    return dictToObj(args)

if __name__ == "__main__":
    args = get_args('/userHome/nemo/projects/MNAD_jigsaw/configs/rank.yaml')

    print(args.gpus, type(args.gpus))   