import thop
import torch


def get_model_info(model, input: tuple):
  flops, params = thop.profile(model,inputs=input)
  flops, params = thop.clever_format([flops, params], "%.3f")
  print(f'params:{params}, flops:{flops}')
  print(f"Total number of param  is ", sum(x.numel() for x in model.parameters()))

if __name__ == '__main__':
  pass