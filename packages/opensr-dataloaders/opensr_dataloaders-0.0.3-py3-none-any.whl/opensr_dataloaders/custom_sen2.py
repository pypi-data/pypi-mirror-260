import os
from PIL import Image
import torch
from torch.utils.data import Dataset, DataLoader
import imageio.v2 as imageio
import cv2
import numpy as np

import json
from einops import rearrange
from torchvision import transforms

class s2_dataset(Dataset):
    def __init__(self, directory,phase="train",bands=4):
        # set properties and directories
        self.directory = directory
        self.lr_path = os.path.join(self.directory,"lr")
        self.hr_path = os.path.join(self.directory,"hr")
        self.bands = bands
        self.phase = phase
        
        # read files
        self.file_list_hr = os.listdir(self.hr_path)
        self.file_list_lr = os.listdir(self.lr_path)
        # keep only files in both lists
        self.files = list(set(self.file_list_hr).intersection(self.file_list_lr))
        
        # apply phase filtering
        phase_percentages = {"train":0.995,"val":0.0025,"test":0.0025}
        total_images = len(self.files)
        train_count = int(total_images * phase_percentages["train"])
        val_count = int(total_images * phase_percentages["val"])
        test_count = int(total_images * phase_percentages["test"])

        # Split the list into train, validation, and test sets
        if phase == "train":
            self.files = self.files[:train_count]
        if phase == "val":
            self.files = self.files[train_count:train_count + val_count]
        if phase == "test":
            self.files = self.files[train_count + val_count:]
            
            
            
    def __len__(self):
        return len(self.files)
    
    def linear_transform(self,t,stage="norm"):
        assert stage in ["norm","denorm"]    

        # define constants
        self.rgb_c = 3.
        self.nir_c = 5.

        if stage == "norm":
            # divide according to conventions
            t[:,:,0] = t[:,:,0] * (10.0 / self.rgb_c) # R
            t[:,:,1] = t[:,:,1] * (10.0 / self.rgb_c) # G
            t[:,:,2] = t[:,:,2] * (10.0 / self.rgb_c) # B
            t[:,:,3] = t[:,:,3] * (10.0 / self.nir_c) # NIR
            # clamp to get rid of outlier pixels
            t = t.clamp(0,1)
            # bring to -1..+1
            t = (t*2)-1
        if stage == "denorm":
            # bring to 0..1
            t = (t+1)/2
            # divide according to conventions
            t[:,:,0] = t[:,:,1] * (self.rgb_c / 10.0) # R
            t[:,:,1] = t[:,:,1] * (self.rgb_c / 10.0) # G
            t[:,:,2] = t[:,:,2] * (self.rgb_c / 10.0) # B
            t[:,:,3] = t[:,:,3] * (self.nir_c / 10.0) # NIR
            # clamp to get rif of outlier pixels
            t = t.clamp(0,1)

        # return image
        return(t)


    def apply_augmentations(self,im):
        smoothen_liklelihood = 1.0
        jitter_liklelihood   = 0.0
        
        if self.phase=="train" or self.phase=="val":
            import random
            smoothen_rand = random.uniform(0, 1)
            jitter_rand = random.uniform(0, 1)

            # denormalize and rearrange
            im = (im+1)/2
            im = rearrange(im,"w h c -> c w h")

            # perform color jitter
            if jitter_rand<jitter_liklelihood:
                # Define the color jitter transformation
                color_jitter = transforms.ColorJitter(brightness=0.5, contrast=0.3, saturation=0.3, hue=0.3)
                # Apply the transformation
                band_ls = []
                for band in im:
                    band = torch.unsqueeze(band,0)
                    #print(band.shape)
                    band = color_jitter(band)
                    band = torch.squeeze(band,0)
                    band_ls.append(band)
                im = torch.stack(band_ls)
            
            # perform smoothen
            if smoothen_rand<smoothen_liklelihood:
                # Define Kernel
                sigma_rand = random.uniform(0.7, 1.5)
                sigma_rand = 0.4
                gaussian_blur = transforms.GaussianBlur(kernel_size=5, sigma=sigma_rand)
                # Apply the blur to the image tensor
                band_ls = []
                for band in im:
                    band = torch.unsqueeze(band,0)
                    band = gaussian_blur(band)
                    band = torch.squeeze(band,0)
                    band_ls.append(band)
                im = torch.stack(band_ls)
                # perform jitter

            # normalize and rearrange
            im = (im*2)-1
            im = rearrange(im,"c w h -> w h c")
        
        # return im regardless of train,test,val
        return(im)


    def __getitem__(self, index):
        # set file paths
        file_name = self.files[index]
        file_path_hr = os.path.join(self.hr_path, file_name)
        file_path_lr = os.path.join(self.lr_path, file_name)
        
        # PIL
        hr = Image.open(file_path_hr)
        lr = Image.open(file_path_lr)
        
        hr = np.array(hr)
        lr = np.array(lr)
        
        
        # change to no of bands wanted
        hr = hr[:,:,:self.bands]
        lr = lr[:,:,:self.bands]
        
        # Convert image to tensor
        hr = torch.Tensor(hr) / 255.0
        lr = torch.Tensor(lr) / 255.0

        # apply blur
        lr = self.apply_augmentations(lr)

        # apply convention norm
        hr = self.linear_transform(hr,stage="norm")
        lr = self.linear_transform(lr,stage="norm")

        images = {"LR_image":lr,"image":hr}
        
        return images


"""
ds = s2_dataset(directory="/data2/simon/S2_images/",phase="train",bands=4)
dl = DataLoader(ds,batch_size=1,shuffle=True,num_workers=16,pin_memory=True)

from ldm.helper_functions.linear_transforms import linear_transform
from ldm.helper_functions.stretching import convention_stretch_sen2
import matplotlib.pyplot as plt
batch = next(iter(dl))
batch["LR_image"] = linear_transform(batch["LR_image"],stage="denorm")
batch["image"] = linear_transform(batch["image"],stage="denorm")
batch["LR_image"] = convention_stretch_sen2(batch["LR_image"])
batch["image"] = convention_stretch_sen2(batch["image"])
# plot HR and LR image from batch dictionary
plt.figure(figsize=(20,10))
plt.subplot(1,2,1)
plt.imshow(batch["image"][0][:,:,:3].cpu().numpy())
plt.title("HR image")
plt.subplot(1,2,2)
plt.imshow(batch["LR_image"][0][:,:,:3].cpu().numpy())
plt.title("LR image")
plt.savefig("S2_ds.png")
plt.close()
"""