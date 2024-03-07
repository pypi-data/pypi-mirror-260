import torch
import numpy as np
import random
import albumentations as A
from einops import rearrange 


def init_color_transform(brightness=0.2,contrast=0.2,saturation=0.2,hue=0.2):
    transform = A.ReplayCompose([A.ColorJitter(brightness=brightness, contrast=contrast, saturation=saturation, hue=hue, always_apply=True)])
    return(transform)


def augment_bands(lr, hr, transform):
    """
    Applies augmentation to three randomly selected bands of 4-band (W, H, 4 or 6) tensors using Albumentations.

    Parameters:
    lr (torch.Tensor): Low-resolution input tensor.
    hr (torch.Tensor): High-resolution input tensor.
    transform (albumentations.core.composition.Compose): Albumentations transformation.

    Returns:
    Tuple[torch.Tensor, torch.Tensor]: Augmented low-resolution and high-resolution tensors.

    Note:
    - Assumes last dimension represents bands.
    - Converts tensors to/from NumPy arrays for augmentation.
    """
    
    # convert to Numpy
    lr = lr.numpy()
    hr = hr.numpy()

    rearrange_needed = False
    if lr.shape[-1]>lr.shape[0]:
        rearrange_needed = True
        lr = rearrange(lr,"c h w -> h w c")
        hr = rearrange(hr,"c h w -> h w c")

    assert lr.shape[-1]==4 or lr.shape[-1]==6,"Augmentation Shape invalid"
    assert hr.shape[-1]==4 or lr.shape[-1]==6,"Augmentation Shape invalid"
    
    # Select 3 random indices from the 4 bands
    bands = range(lr.shape[-1])
    selected_indices = random.sample(bands, 3)
    
    # Extract the selected bands
    lr_selected = lr[:, :, selected_indices]
    hr_selected = hr[:, :, selected_indices]
    
    # Apply augmentation
    lr_augmented = transform(image=lr_selected)
    hr_augmented = A.ReplayCompose.replay(lr_augmented['replay'], image=hr_selected)["image"]
    lr_augmented = lr_augmented["image"]

    # Reconstruct the original 4-band tensor
    lr[:, :, selected_indices] = lr_augmented
    hr[:, :, selected_indices] = hr_augmented

    if rearrange_needed==True:
        lr = rearrange(lr,"h w c -> c h w")
        hr = rearrange(hr,"h w c -> c h w")
    
    # convert back to Tensor
    lr = torch.Tensor(lr)
    hr = torch.Tensor(hr)

    return lr, hr




def add_black_spots(images,mean_amount=15,mean_size=8):
    """
    Add black spots of varying sizes and amounts to all bands of the input image.
    
    Parameters:
    - image: A PyTorch tensor of shape (batch,channels, height, width).
    - mean_amount: mean of notm. distribution for amount of black spots
    - mean_size: mean of norm. distribution of black spot's size
    
    Returns:
    - Modified image with black spots.
    """
    
    
    if len(images.shape)==3:
        images = images.unsqueeze(0)
        three_band = False
    else:
        three_band = True
    
    final_result = []
    for image in images:
        # get random number of spots form normal distribution
        mean = mean_amount
        std = 3  # Adjust this as needed
        num_spots_f = torch.normal(mean, std, size=(1,))
        num_spots = max(0, round(num_spots_f.item()))

        channels, height, width = image.shape
        for _ in range(num_spots):
            # Randomly determine the center of the spot
            center_x, center_y = torch.randint(0, width, (1,)), torch.randint(0, height, (1,))

            # Randomly determine the size of the spot
            std_size = 3
            rand_size = torch.normal(mean_size, std_size, size=(1,))
            rand_size = max(0, round(rand_size.item()))
            spot_size = rand_size

            # Calculate the top-left corner of the spot
            start_x = max(center_x - spot_size // 2, 0)
            start_y = max(center_y - spot_size // 2, 0)

            # Calculate the bottom-right corner of the spot
            end_x = min(start_x + spot_size, width)
            end_y = min(start_y + spot_size, height)

            # Set the pixels in this range to 0 in all bands
            image[:, start_y:end_y, start_x:end_x] = 0.0
        
        # append image with spots to list
        final_result.append(image)
    
    # stack result
    final_result = torch.stack(final_result)
    
    # back to 3D tensor if necessary
    if three_band == False:
        final_result = final_result.squeeze(0)
    return final_result



def other_augmentations(lr,hr):
    """
    Applies identical augmentations including HorizontalFlip, VerticalFlip, RandomRotate90, 
    and Transpose to all bands of both low-resolution and high-resolution images using Albumentations.
    This ensures the spatial correspondence between LR and HR images is maintained.

    Parameters:
    lr (torch.Tensor): Low-resolution input tensor.
    hr (torch.Tensor): High-resolution input tensor.

    Returns:
    Tuple[torch.Tensor, torch.Tensor]: Augmented low-resolution and high-resolution tensors.

    Note:
    - Assumes last dimension represents bands.
    - Converts tensors to/from NumPy arrays for augmentation.
    """
    
    # Define the transformation pipeline
    transform = A.ReplayCompose([
        A.HorizontalFlip(p=0.5),
        A.VerticalFlip(p=0.5),
        A.RandomRotate90(p=0.5),
        A.Transpose(p=0.5)
    ])
    
    # Convert tensors to numpy arrays
    lr_np = lr.numpy()
    hr_np = hr.numpy()

    # Check and rearrange if channels are first
    rearrange_needed = False
    if lr_np.shape[-1] > lr_np.shape[0]:
        rearrange_needed = True
        lr_np = rearrange(lr_np, "c h w -> h w c")
        hr_np = rearrange(hr_np, "c h w -> h w c")

    # Apply augmentation to the LR image and get the replay data
    augmented_lr = transform(image=lr_np)
    replay_data = augmented_lr['replay']

    # Apply the same augmentation to the HR image using the replay data
    augmented_hr = A.ReplayCompose.replay(replay_data, image=hr_np)

    # Extract augmented images
    lr_np = augmented_lr['image']
    hr_np = augmented_hr['image']

    # Rearrange back if needed
    if rearrange_needed:
        lr_np = rearrange(lr_np, "h w c -> c h w")
        hr_np = rearrange(hr_np, "h w c -> c h w")
    
    # Convert back to PyTorch tensors
    lr_tensor = torch.from_numpy(lr_np).float()
    hr_tensor = torch.from_numpy(hr_np).float()

    return lr_tensor, hr_tensor