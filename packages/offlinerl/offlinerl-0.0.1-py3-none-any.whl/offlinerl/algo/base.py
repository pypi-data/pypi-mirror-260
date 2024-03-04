import os
import uuid
import json
from abc import ABC, abstractmethod

import torch
from collections import OrderedDict
from loguru import logger
from offlinerl.utils.exp import init_exp_run
from offlinerl.utils.io import create_dir, download_helper, read_json
from offlinerl.utils.logger import log_path


import time
import random   

class BaseAlgo(ABC):
    def __init__(self, args):        
        logger.info('Init AlgoTrainer')
        if "exp_name" not in args.keys():
            exp_name = str(uuid.uuid1()).replace("-","")
        else:
            exp_name = args["exp_name"]
        
        if "aim_path" in args.keys():
            if os.path.exists(args["aim_path"]):
                time.sleep(random.randint(1, 5))
                repo = args["aim_path"]
            else:
                os.makedirs(args["aim_path"])
            repo = args["aim_path"]
        else:
            repo = None
        
        self.repo = repo

        # 生成 1 到 5 之间的随机整数，单位为秒
        # random_seconds = random.randint(1, 5)

        # # 等待随机生成的秒数
        # print(f"等待 {random_seconds} 秒...")
        # time.sleep(random_seconds)

        # print("等待结束，继续执行下一步操作。")

        # try:
        try:
            self.exp_run = init_exp_run(repo = repo, experiment_name = exp_name)
        except:
            time.sleep(random.randint(1, 5))
            self.exp_run = init_exp_run(repo = repo, experiment_name = exp_name)

        # except:
        #     time.sleep(2)
        #     self.exp_run = init_exp_run(repo = repo, experiment_name = exp_name)

        if self.exp_run.repo is not None:  # a naive fix of aim exp_logger.repo is None
            self.index_path = self.exp_run.repo.path
        else:
            repo = os.path.join(log_path(),"./.aim")
            if not os.path.exists(repo):
                logger.info('{} dir is not exist, create {}',repo, repo)
                os.system(str("cd " + os.path.join(repo,"../") + "&& aim init"))
            self.index_path = repo

        print(f'self.index_path/{self.index_path}')
        self.models_save_dir = os.path.join(self.index_path, "models")
        self.metric_logs = OrderedDict()
        self.metric_logs_path = os.path.join(self.index_path, "metric_logs.json")
        create_dir(self.models_save_dir)

        # self.exp_run.set_params(args, name='hparams')
        self.exp_run['hparams'] = args
    
    def log_res(self, epoch, result):
        logger.info('Epoch : {}', epoch)
        for k,v in result.items():
            logger.info('{} : {}',k, v)
            self.exp_run.track(v, name=k.split(" ")[0], epoch=epoch,)
        
        self.metric_logs[str(epoch)] = result
        with open(self.metric_logs_path,"w") as f:
            json.dump(self.metric_logs,f)

        run_id = self.exp_run.name.split( )[-1]
        tmp_dir = os.path.join(self.models_save_dir, run_id)
        if not os.path.exists(tmp_dir):
            os.makedirs(tmp_dir)
        self.save_model(os.path.join(tmp_dir, str(epoch) + ".pt"))            
    
    @abstractmethod
    def train(self, 
              history_buffer,
              eval_fn=None,):
        pass
    
    def _sync_weight(self, net_target, net, soft_target_tau = 5e-3):
        for o, n in zip(net_target.parameters(), net.parameters()):
            o.data.copy_(o.data * (1.0 - soft_target_tau) + n.data * soft_target_tau)
    
    @abstractmethod
    def get_policy(self,):
        pass
    
    #@abstractmethod
    def save_model(self, model_path):
        torch.save(self.get_policy(), model_path)
        
    #@abstractmethod
    def load_model(self, model_path):
        model = torch.load(model_path)
        
        return model