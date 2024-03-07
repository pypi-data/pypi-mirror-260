# import dataset utilities
import torch
import os
import pandas as pd
import torch
import random
from einops import rearrange
from torchvision import transforms
import numpy as np
from tqdm import tqdm
from torch.utils.data import Dataset, DataLoader, WeightedRandomSampler


# Step 2: Custom Dataset Class
class S2NAIP_v4(Dataset):
    def __init__(self, csv_path, phase="train"):
        self.phase = phase

        # read and clean DF
        self.dataframe = pd.read_csv(csv_path)
        self.dataframe = self.dataframe.fillna(0)
        self.dataframe = self.dataframe[self.dataframe["SuperClass"]!=0]

        # enable FAKE VAL while it is not available
        #if self.phase=="val":
        #    self.dataframe = self.dataframe[:100000]
        #    self.dataframe = self.dataframe.sample(n=100)
        #    self.phase = "train"

        # set paths
        self.input_dir = "/data3/final_s2naip_simon/"
        self.hr_input_path = os.path.join(self.input_dir,self.phase,"HR")
        self.lr_input_path = os.path.join(self.input_dir,self.phase,"LR")
        self.degradations = ["none","gaussian","bell","sigmoid"]

        # initialize sampler
        self.define_sampler()
        # initialize norm
        from opensr_dataloaders.linear_transforms import linear_transform
        self.linear_transform = linear_transform
        # init albumentations
        from opensr_dataloaders.image_augmentations import init_color_transform
        self.color_transform = init_color_transform(brightness=0.5,contrast=0.5,saturation=0.5,hue=0.5)
        from opensr_dataloaders.image_augmentations import augment_bands
        self.augment_bands = augment_bands
        from opensr_dataloaders.image_augmentations import add_black_spots
        self.add_black_spots = add_black_spots
        from opensr_dataloaders.image_augmentations import other_augmentations
        self.other_augmentations = other_augmentations

    def __len__(self):
        return len(self.dataframe)
    
    def normalization(self, im, stage="norm"):
        im = im.unsqueeze(0)
        im = self.linear_transform(im,stage=stage)
        im = im.squeeze(0)
        return(im)
    
    def apply_augmentations(self,lr,hr):
        lr,hr = lr.float(),hr.float()

        # set probabilities
        smoothen_liklelihood   = 0.80 # 0.75
        jitter_liklelihood     = 0.40 # 0.75
        black_spots_likelihood = 0.00

        # get random numbers
        smoothen_rand = random.uniform(0, 1)
        jitter_rand = random.uniform(0, 1)
        black_spots_rand = random.uniform(0, 1)

        # perform color jitter
        if jitter_rand<jitter_liklelihood:
            lr,hr = self.augment_bands(lr,hr,self.color_transform)

        # perform other augmentations
        lr,hr = self.other_augmentations(lr,hr)

        # perform smoothen
        if smoothen_rand<smoothen_liklelihood:
            # Define Kernel
            sigma_rand = random.uniform(0.65, 1.2)
            gaussian_blur = transforms.GaussianBlur(kernel_size=5, sigma=sigma_rand)
            # Apply the blur to the image tensor
            band_ls = []
            for band in lr:
                band = torch.unsqueeze(band,0)
                band = gaussian_blur(band)
                band = torch.squeeze(band,0)
                band_ls.append(band)
            lr = torch.stack(band_ls)
        
        if black_spots_likelihood<black_spots_rand:
            lr = self.add_black_spots(lr)
            
                
        return(lr,hr)
    
    def define_sampler(self):
        # stratiefied Sampling with weights - ideally it sums up to 1
        class_weights = {
            'Rural': 0.30,  
            'Forest': 0.25, 
            'Water': 0.05,  
            'Developed': 0.4, }
        
        # 1. clean dataset
        data = self.dataframe
        # 2. define sampler
        class_counts = data['SuperClass'].value_counts()
        base_weights = [1.0 / class_counts[i] for i in data['SuperClass'].values]
        adjusted_weights = [base_weights[i] * class_weights[class_label] for i, class_label in enumerate(data['SuperClass'].values)] 
        # 3. set sampler
        self.sampler = WeightedRandomSampler(adjusted_weights, len(adjusted_weights),replacement=True)
    
    def __getitem__(self, idx):
        # get random degradation, get input paths
        random_degradation = np.random.choice(self.degradations)
        lr_input_path = os.path.join(self.input_dir,self.phase,"LR",random_degradation)
        lr_input_path = os.path.join(lr_input_path,self.dataframe.iloc[idx]["name"] + ".pt")
        hr_input_path = os.path.join(self.hr_input_path,self.dataframe.iloc[idx]["name"] + ".pt")

        # check if files exist
        if not os.path.exists(lr_input_path) or not os.path.exists(hr_input_path):
            # if files arent yet on disk, load another random example
            idx = np.random.randint(0,len(self))
            return self.__getitem__(idx) # recursive call

       # Load iamges from disk
        lr_image = torch.load(lr_input_path)
        hr_image = torch.load(hr_input_path)
        lr_image = lr_image.float()
        lr_image = lr_image.float()

        # bring to value range. Check since they are mixed while writing to disk is ongoing
        if hr_image.max()>10:
            hr_image = hr_image/10000
        if lr_image.max()>10:
            lr_image = lr_image/10000

        # perform augmentations
        if self.phase=="train":
            #print(lr_image.shape,hr_image.shape)
            lr_image,hr_image = self.apply_augmentations(lr_image,hr_image)
            
        # apply norm
        apply_norm = True
        if apply_norm:
            lr_image,hr_image = lr_image.unsqueeze(0),hr_image.unsqueeze(0)
            lr_image = self.linear_transform(lr_image,stage="norm")
            hr_image = self.linear_transform(hr_image,stage="norm")
            lr_image,hr_image = lr_image.squeeze(0),hr_image.squeeze(0)

        hr_image = rearrange(hr_image,"c h w -> h w c")
        lr_image = rearrange(lr_image,"c h w -> h w c")

        # return images
        return {"image":hr_image,"LR_image":lr_image}

if False:
    ds = S2NAIP_v4(phase="train",csv_path="/data3/landcover_s2naip/csvs/train_metadata_landcover.csv")
    dl = DataLoader(ds,batch_size=1,shuffle=False,num_workers=0)
    lr_means = []
    hr_means = []
    for batch in tqdm(dl):
        lr_means.append(batch["LR_image"].max().item())
        hr_means.append(batch["image"].max().item())

        if batch["LR_image"].max().item()>10 or batch["image"].max().item()>10:
            print("Unusual: ",batch["LR_image"].max().item(),batch["image"].max().item())
    


if False:
    # create objects
    ds = S2NAIP_v4(csv_path="/data3/landcover_s2naip/csvs/train_metadata_landcover.csv")
    print("Lenght: ",len(ds))
    batch = ds.__getitem__(5679)
    hr,lr = batch["image"],batch["LR_image"]
    # show lr and hr images
    import matplotlib.pyplot as plt
    from ldm.helper_functions.stretching import convention_stretch_sen2
    fig,ax = plt.subplots(1,2,figsize=(20,10))
    lr_viz,hr_viz = lr,hr
    lr_viz = ds.linear_transform(lr_viz,stage="denorm")
    hr_viz = ds.linear_transform(hr_viz,stage="denorm")
    #lr_viz,hr_viz = (lr_viz+1)/2,(hr_viz+1)/2
    hr_viz = rearrange(hr_viz,"c h w -> h w c")
    lr_viz = rearrange(lr_viz,"c h w -> h w c")
    hr_viz = convention_stretch_sen2(hr_viz)
    lr_viz = convention_stretch_sen2(lr_viz)
    ax[0].imshow(hr_viz[:,:,:3])
    ax[1].imshow(lr_viz[:,:,:3])
    plt.savefig("test.png")





