# 日志类
from datetime import datetime
import pytz
import wandb

class Logger():
  def __init__(self, log_path, mode='a', use_wandb=False, wandb_config=None, wandb_project='EDNet', wandb_name='demo',wandb_jobtype='training'):
    print(f'日志文件已经创建,位于{log_path}')
    self.log_path = log_path
    self.file = open(self.log_path, mode)
    self.file.write(f'-*'*30+'\n')
    self.file.write(f'日志文件已经创建,位于{log_path} \n')

    if use_wandb:
      # wandb_config: dict
      # wand.log()  : dict
      wandb.init(config = wandb_config, project = wandb_project, name = wandb_name, job_type = wandb_jobtype)

    
  def write_info(self, info):
    info_to_write = f'[{self.current_time()}]  {info}\n'
    self.file.write(info_to_write)
    self.file.flush()

  def print_info(self, info):
    info_to_print = f'[{self.current_time()}]  {info}\n'
    print(info_to_print)
  
  def write_and_print_info(self, info):
    info_to_write = f'[{self.current_time()}]  {info}\n'
    self.file.write(info_to_write)
    self.file.flush()
    print(info_to_write)

  def current_time(self):
    beijing_tz = pytz.timezone('Asia/Shanghai')  # 创建北京时间（亚洲/上海）时区对象
    beijing_time = datetime.now(beijing_tz)      # 获取当前的北京时间
    beijing_time = beijing_time.strftime("%Y/%m/%d %H:%M:%S")# date.datetime类型转str
    return beijing_time
  
  def wandb_log(self,info):
    wandb.log(info)

  def finish(self):
    self.file.close()



if __name__ == '__main__':
  pass