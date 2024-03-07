import torch
import os
import einops
import rasterio
from rasterio.windows import Window
from torchvision import transforms
import random
import json
import numpy as np


class sen2_test(torch.utils.data.Dataset):
    def __init__(self,data_folder = "/data2/simon/test_s2/S2A_MSIL2A_20230729T100031_N0509_R122_T33TUG_20230729T134559.SAFE",amount=25,band_selection="R10m",apply_norm=False):
        # settings for band selection
        assert band_selection in ["R10m","R20m"]
        self.band_selection = band_selection

        # init transforms
        self.apply_norm=apply_norm
        
        # def window return size
        self.image_size=128
        # get location of image data
        for dirpath, dirnames, _ in os.walk(data_folder):
            if "IMG_DATA" in dirnames:
                folder_path = os.path.join(dirpath, "IMG_DATA")
        folder_path = os.path.join(folder_path,self.band_selection)
        file_paths = os.listdir(folder_path)

        # get image file paths for selected bands
        if self.band_selection == "R10m":
            self.image_files = {"R":os.path.join(folder_path,[file for file in file_paths if "B04" in file][0]),
                        "G":os.path.join(folder_path,[file for file in file_paths if "B03" in file][0]),
                        "B":os.path.join(folder_path,[file for file in file_paths if "B02" in file][0]),
                        "NIR":os.path.join(folder_path,[file for file in file_paths if "B08" in file][0])}
        if self.band_selection == "R20m":
            self.image_files = {"B05":os.path.join(folder_path,[file for file in file_paths if "B05" in file][0]),
                        "B06":os.path.join(folder_path,[file for file in file_paths if "B06" in file][0]),
                        "B07":os.path.join(folder_path,[file for file in file_paths if "B07" in file][0]),
                        "B8A":os.path.join(folder_path,[file for file in file_paths if "B8A" in file][0]),
                        "B11":os.path.join(folder_path,[file for file in file_paths if "B11" in file][0]),
                        "B12":os.path.join(folder_path,[file for file in file_paths if "B12" in file][0])}
        
        # extract keys from image files
        self.band_names = list(self.image_files.keys())
        
        # get iamge shape
        with rasterio.open(self.image_files[self.band_names[0]]) as src:
            self.image_width = src.width
            self.image_height = src.height
        
        # create list of coordinates
        self.windows = []
        for i in range(amount):
            rand_x = random.randint(0 ,self.image_width -self.image_size)
            rand_y = random.randint(0,self.image_height-self.image_size)
            window_ = Window(rand_x, rand_y, self.image_size, self.image_size)
            self.windows.append(window_)

    def __len__(self):
        return len(self.windows)
    
    def apply_transforms(self,im):
        from opensr_dataloaders.linear_transforms import linear_transform
        im = linear_transform(im.unsqueeze(0),stage="norm").squeeze(0)
        #im = einops.rearrange(im,"C W H -> W H C")
        return(im)
    
    def __getitem__(self,idx):
        # get current window
        window = self.windows[idx]
        
        # read bands iteratively
        image=[]
        for band in self.band_names:
            with rasterio.open(self.image_files[band]) as src:
                window_data = src.read(1, window=window)                
                image.append(window_data)
        image = np.stack(image)/10000
        
        # apply normalization
        if self.apply_norm:
            image = self.apply_transforms(torch.Tensor(image))

        image = torch.Tensor(image).float()
        return(image)
                

"""
ds = sen2_test(band_selection="R20m",apply_norm=False)
im = ds.__getitem__(20)
import matplotlib.pyplot as plt
plt.figure(figsize=(10, 6))
colors = ['b', 'g', 'r', 'c', 'm', 'y']
num_bins = 10
# print min, mean, std,max for all image bands
for i in range(im.shape[0]):
    band = im[i]
    min_val = band.min().item()
    mean_val = band.mean().item()
    std_val = band.std().item()
    max_val = band.max().item()
    print(f"Band {i+1}: Min={min_val}, Mean={mean_val}, Std={std_val}, Max={max_val}")
    band = im[i].flatten()
    plt.hist(band, bins=30, color=colors[i], alpha=0.5, label=f'Band {ds.band_names[i]}')
    # plot line at max value
    plt.axvline(x=band.max(), color=colors[i], linestyle='dashed', linewidth=1)
    #band = im[i].flatten().numpy()  # Convert to NumPy array for histogram calculation
    #hist, bin_edges = np.histogram(band, bins=num_bins)
    #bin_centers = 0.5 * (bin_edges[:-1] + bin_edges[1:])  # Calculate bin centers
    #plt.plot(bin_centers, hist, color=colors[i], label=f'Band {ds.band_names[i]}')
plt.title('Histograms of Each Band')
plt.xlabel('Value')
plt.ylabel('Frequency')
plt.legend()
plt.savefig("hist.png")
plt.close()
"""