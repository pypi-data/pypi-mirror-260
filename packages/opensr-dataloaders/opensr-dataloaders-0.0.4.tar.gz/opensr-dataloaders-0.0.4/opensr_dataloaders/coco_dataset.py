import os
import torch
from PIL import Image
import numpy as np
import os
import glob
from torch.utils.data import Dataset, DataLoader
from einops import rearrange
import torchvision.transforms as transforms

import json
from einops import rearrange
from torchvision import transforms

class JpegImageDataset(Dataset):
    def __init__(self,folders,phase,image_size=512,return_type="single",channels=3,force_rescan=False,verbose=False):
        
        self.verbose=verbose
        
        # set inputs to class
        self.channels = channels
        self.folders = folders
        self.image_size = image_size # desired image dimensions
        self.return_type = return_type
        self.phase = phase
        
        # set transforms
        self.init_transforms(dataset_type="coco_dataset",
                             band_stats_path="ldm/data/band_statistics.json",
                             apply_transforms=False)

        # make sure inputs are valid
        assert self.channels in [3,4]
        assert self.return_type in ["single","pair"]
        assert self.phase in ["train","val"]
        assert len(self.folders)>0
        
        if self.verbose:
            print("Creating dataset from all png/jpeg files in directories:",self.folders,"\n")
                
        # Read files from folders, by:
        # 1. rescanning folders and check for image size & RGB
        # 2. use list with precomputed info
        self.image_files = self.read_image_file_or_scan_folders(self.folders,force_rescan=force_rescan)
        if self.verbose:
            print("Total number of suitable image files in all folders: ",len(self.image_files))
        
        # train/test split
        self.image_files = self.train_test_split(phase)
        if self.verbose:
            print("No. of images after filtering for",self.phase,"pase: ",len(self.image_files),"\n")
            print("Dataset sucessfully initialized.")
        
    
    def train_test_split(self,phase="train"):
        # perform train test split on data
        if phase=="train":
            #first_85_percent = self.image_files[:int(len(self.image_files)*0.85)]
            #image_files = first_85_percent
            image_files = self.image_files[:len(self.image_files)-5]
            #image_files = self.image_files[:100]
        if phase=="val":
            #last_15_percent = self.image_files[-int(len(self.image_files)*0.15):]
            #image_files = last_15_percent
            image_files = self.image_files[len(self.image_files)-5:]
        return(image_files)
    
    def read_image_file_or_scan_folders(self,folders,force_rescan=False):
        list_of_lists = []
        for folder in folders:
            if self.verbose:
                print("Loading from folder:",folder)
            # first, check if folder has been scanned for suitable pictures already
            suitable_pictures_file_path = os.path.join(folder, 'suitable_files.txt')
            if os.path.exists(suitable_pictures_file_path) and force_rescan==False:
                if self.verbose:
                    print('List containing suitable files found (or force_rescan is activated):',suitable_pictures_file_path)
            
                with open(suitable_pictures_file_path, 'r') as f:
                    image_files_from_folder = [line.strip() for line in f.readlines()]
            else:
                if self.verbose:
                    print('No list containing suitable images found. Scanning and creating ',suitable_pictures_file_path)
                # read all file names from folder
                image_files_from_folder = self.get_images_from_folders(folder)
                # check each image to see if they are RGB and over the size requirement
                image_files_from_folder = self.check_image_sizes(image_files_from_folder)
                # save suitable files list to text file in root directory of dataset
                with open(suitable_pictures_file_path, 'w') as f:
                    for item in image_files_from_folder:
                        f.write("%s\n" % item)
        
            
            # append list of files either loaded or scanned to self         
            list_of_lists.append(image_files_from_folder)
            if self.verbose:
                print("No. of suitable image files in this folder:",len(image_files_from_folder),"\n")
        return(self.flatten_list(list_of_lists))
            
    
    def get_images_from_folders(self,folder_path):
        image_files = glob.glob(os.path.join(folder_path, '**/*.jpg'), recursive=True)
        image_files = self.check_image_sizes(image_files)
        return(image_files)
    
    def check_image_sizes(self,image_files):
        new_ls = []
        for path in image_files:
            with Image.open(path) as image:
                width, height = image.size
                if width>self.image_size and height>self.image_size and image.mode=="RGB":
                    new_ls.append(path)
        return(new_ls)
    
    def crop_center(self,image):
        height, width = image.shape[:2]
        crop_size = self.image_size
        y_start = (height - crop_size) // 2
        x_start = (width - crop_size) // 2
        y_end = y_start + crop_size
        x_end = x_start + crop_size
        return image[y_start:y_end, x_start:x_end]
    
    def flatten_list(self,nested_list):
        flat_list = []
        for item in nested_list:
            if isinstance(item, list):
                flat_list.extend(self.flatten_list(item))
            else:
                flat_list.append(item)
        return flat_list
    
    def rgb_to_grayscale(self,img_tensor):
        r, g, b = img_tensor[0], img_tensor[1], img_tensor[2]
        gray = 0.2989 * r + 0.5870 * g + 0.1140 * b  # grayscale formula
        return torch.stack([r, g, b, gray], dim=0)

        
    def __len__(self):
        return len(self.image_files)

    def init_transforms(self,dataset_type="worldstrat_preprocessed_RGBNIR",band_stats_path="ldm/data/band_statistics.json",apply_transforms=True):

        
        if apply_transforms==False:
            self.transform_PIL = transforms.ToPILImage()
            self.transform = transforms.ToTensor()
        
        if apply_transforms==True:
            try:
                with open(band_stats_path, 'r') as file:
                    # Load the JSON data into a dictionary
                    data_dict = json.load(file)
                mean = [data_dict["norm_dict"][dataset_type]["mean"]["0"],
                        data_dict["norm_dict"][dataset_type]["mean"]["1"],
                        data_dict["norm_dict"][dataset_type]["mean"]["2"],
                        data_dict["norm_dict"][dataset_type]["mean"]["3"]]

                std = [data_dict["norm_dict"][dataset_type]["std"]["0"],
                        data_dict["norm_dict"][dataset_type]["std"]["1"],
                        data_dict["norm_dict"][dataset_type]["std"]["2"],
                        data_dict["norm_dict"][dataset_type]["std"]["3"]]
                transform_ = transforms.Compose([
                        transforms.ToTensor(),
                        transforms.Normalize(mean=mean, std=std),
                         ])
                self.transform_PIL = transforms.ToPILImage()
                self.transform = transform_

            except:
                self.transform_PIL = transforms.ToPILImage()
                self.transform = transforms.ToTensor()

    def apply_transforms(self,im):
        """
        in: - torch tensor of shape W H C
        out: normalized tensor
        """
        # check if we need transpose at this place
        if im.shape[-1]<im.shape[0]: # True if W H B
            transpose_needed = True
        else:
            transpose_needed = False
        
        # apply transpose if needed, then apply transform
        if transpose_needed:
            im = rearrange(im,"w h b -> b w h")
        im = self.transform_PIL(im)
        im = self.transform(im)
        if transpose_needed:
            im = rearrange(im,"b w h -> w h b")
        return(im)
    
    
    def __getitem__(self, index):
        image_path = self.image_files[index]
        image = Image.open(image_path)
        image = np.array(image)
        image = torch.Tensor(image)
        
        image = self.crop_center(image)
        image = image/255.0
        
        # get 4th band from grayscale
        if self.channels==4:
            # turn to RGB if wanted
            image = rearrange(image,"w h c -> c w h")
            image = self.rgb_to_grayscale(image)
            image = rearrange(image,"c w h -> w h c")
            # apply transformation/normalization
            image = self.apply_transforms(image)
        
        # get interpolated version and return
        if self.return_type =="pair":
            # rearrange hr image
            image = rearrange(image,"w h c -> c w h")
            # interpolate hr to lr
            image_lr = torch.nn.functional.interpolate(image.unsqueeze(0),
                                                    size=(128,128), mode='bilinear', align_corners=False).squeeze(0)
            # bring images back to wanted shape
            image    = rearrange(image,"c w h -> w h c")
            image_lr = rearrange(image_lr,"c w h -> w h c")

            # stretch to -1..+1
            image = (image*2)-1
            image_lr = (image_lr*2)-1

            # return images as dict
            return {"image":image,"LR_image":image_lr}
            
        if self.return_type =="single":
            # stretch to -1..+1
            #image = (image*2)-1
            return {"image":image}