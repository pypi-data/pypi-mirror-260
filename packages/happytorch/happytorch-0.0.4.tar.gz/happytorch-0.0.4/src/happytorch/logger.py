import os
import logging
import time


class htLogger:
    def __init__(self, args):
        # path init
        if "/auto" in args.output_dir:
            file_name = os.path.basename(args.config_file)[:-5]  # 使用配置文件名称
            args.output_dir = args.output_dir.replace("/auto", "/{}".format(file_name))
            if not os.path.exists(args.output_dir):
                os.makedirs(args.output_dir)

        # logger init
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

        sh = logging.StreamHandler()

        # 创建处理器：sh为控制台处理器，fh为文件处理器,log_file为日志存放的文件夹
        if "_time" or "_test" in args.output_dir:
            log_file = os.path.join(
                args.output_dir,
                "{}.log".format(time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())),
            )
        else:
            log_file = os.path.join(args.output_dir, "eval.log")
        fh = logging.FileHandler(log_file, encoding="UTF-8")

        formator = logging.Formatter(
            fmt="%(asctime)s %(levelname)s: %(message)s",  # "%(asctime)s %(filename)s %(levelname)s %(message)s"
            datefmt="%m/%d-%Y %H:%M:%S",
        )
        sh.setFormatter(formator)
        fh.setFormatter(formator)

        self.logger.addHandler(sh)
        self.logger.addHandler(fh)

        self.logger.info(args)
        self.logger.info("-" * 100)
        
def init_logger(args):
    return htLogger(args).logger
