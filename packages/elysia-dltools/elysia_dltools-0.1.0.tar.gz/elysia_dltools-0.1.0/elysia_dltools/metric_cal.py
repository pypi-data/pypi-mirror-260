import pyiqa
import lpips
import numpy as np
import torch
from skimage.metrics import peak_signal_noise_ratio as PSNR
from skimage.metrics import structural_similarity as SSIM


class Measure():
  def __init__(self,device=torch.device('cuda:0'),psnr=False,ssim=False,lpips=False,niqe=False,pi=False,net='vgg'):
    if psnr:
      self.psnr_metric = pyiqa.create_metric('psnr').to(device)
    if ssim:
      self.ssim_metric = pyiqa.create_metric('ssim').to(device)
    if lpips:
      self.lpips_metric = pyiqa.create_metric('lpips').to(device)
    if niqe:
      self.niqe_metric = pyiqa.create_metric('niqe').to(device)
    if pi:
      self.pi_metric = pyiqa.create_metric('pi').to(device)
    self.model = lpips.LPIPS(net=net)
    self.device = device

  def get_psnr(self,gt,src):
    psnr_score = self.psnr_metric(gt,src)
    return psnr_score
  
  def get_ssim(self,gt,src):
    ssim_score = self.ssim_metric(gt,src) 
    return ssim_score
  
  def get_lpips(self,gt,src):
    lpips_score = self.lpips_metric(gt,src)
    return lpips_score
  
  def get_niqe(self,src):
    niqe_score = self.niqe_metric(src) 
    return niqe_score
  
  def get_pi(self,src):
    pi_score = self.pi_metric(src)
    return pi_score
  
  def ssim(self, output, target):
    y_input = output.data.cpu().numpy()
    y_target = target.cpu().numpy()

    N, C, H, W = y_input.shape
    assert (C == 1 or C == 3)
    # N x C x H x W -> N x W x H x C -> N x H x W x C
    y_input = np.swapaxes(y_input, 1, 3)
    y_input = np.swapaxes(y_input, 1, 2)
    y_target = np.swapaxes(y_target, 1, 3)
    y_target = np.swapaxes(y_target, 1, 2)
    sum_structural_similarity_over_batch = 0.
    for i in range(N):
      if C == 3:
        sum_structural_similarity_over_batch += SSIM(
            y_input[i, :, :, :], y_target[i, :, :, :], multichannel=True)
      else:
        sum_structural_similarity_over_batch += SSIM(
          y_input[i, :, :, 0], y_target[i, :, :, 0])

    return sum_structural_similarity_over_batch / float(N)

  def psnr(self, output, target):
    with torch.no_grad():
      output_ = output.data.cpu().numpy()
      target_ = target.cpu().numpy()
      res = 0
      for i in range(target.shape[0]):
          res += PSNR(output_[i], target_[i])
      return res / target.shape[0]
  
  def lpips(self, imgA, imgB, model=None):
    device = next(self.model.parameters()).device

    imgA = imgA.to(device)
    imgB = imgB.to(device)
    dist01 = self.model.forward(imgA, imgB).item()
    return dist01
  
  def measure(self, imgA, imgB, img_lr=None):
        """
        参数:
            imgA: [C, H, W] uint8 or torch.FloatTensor [-1,1]
            imgB: [C, H, W] uint8 or torch.FloatTensor [-1,1]
            img_lr: [C, H, W] uint8  or torch.FloatTensor [-1,1]
            sr_scale:

        Returns: dict of metrics
        """
        psnr = self.psnr(imgA, imgB)

        ssim = self.ssim(imgA, imgB)

        lpips = self.lpips(imgA, imgB)

        return psnr, ssim, lpips