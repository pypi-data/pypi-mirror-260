import torch


def select_dataset(dataloader_type="worldstrat_preprocessed_RGBNIR",train_batch_size=2,val_batch_size=2,num_workers=0,revisits=1,prefetch_factor=0,**kwargs):
    """
    Creates training and validation data loaders from a specified dataset.

    The function supports multiple datasets and the returned data loaders
    are ready for use in a training loop.

    Args:
        dataloader_type (str, optional): Specifies the type of dataset to use. Options include "worldstrat_preprocessed", 
        "NAIP", "worldstrat_preprocessed_RGBNIR", "coco_dataset", "worldstrat_spot6", and "s2_dataset". 
        Default is "worldstrat_preprocessed_RGBNIR".

        train_batch_size (int, optional): Number of samples per batch to load for training data. Default is 2.

        val_batch_size (int, optional): Number of samples per batch to load for validation data. Default is 2.

        num_workers (int, optional): Number of subprocesses to use for data loading. Default is 1.

    Returns:
        tuple: Consisting of (train_loader, val_loader, ds_train, ds_val) where train_loader and val_loader are 
        torch.utils.data.DataLoader instances for the training and validation datasets respectively, and ds_train, ds_val
        are the corresponding dataset instances.
    """
    
    # get and control datalaoder
    assert dataloader_type in ["S2NAIP_v4","sen2_test"]

    # Each conditional block sets up data loaders for a different dataset
    # Loaders are configured according to specific dataset require
    
    if dataloader_type == "S2NAIP_v4":
        import pathlib
        from opensr_dataloaders.S2NAIP_v4 import S2NAIP_v4
        from torch.utils.data import DataLoader
        csv_path = "/data3/landcover_s2naip/csvs/train_metadata_landcover.csv"
        ds_train = S2NAIP_v4(phase="train",csv_path=csv_path)
        ds_val =  S2NAIP_v4(phase="val",csv_path=csv_path)
        train_loader = torch.utils.data.DataLoader(ds_train,batch_size=train_batch_size,num_workers=num_workers,
                                                   drop_last=True,prefetch_factor=prefetch_factor,
                                                   sampler = ds_train.sampler)
        val_loader = torch.utils.data.DataLoader(ds_val,batch_size=val_batch_size,num_workers=num_workers,
                                                 drop_last=True,prefetch_factor=prefetch_factor,
                                                 sampler = ds_val.sampler)

    if dataloader_type == "worldstrat_MISR":
        import pathlib
        from ldm.data.worldstrat_MISR import worldstrat_MISR
        from torch.utils.data import DataLoader
        revisits = 4
        csv_path = "/data3/landcover_s2naip/csvs/train_metadata_landcover.csv"
        ds_train = worldstrat_MISR(root_dir="/data3/worldstrat_misr_saved_2",phase="train",revisits=revisits,stddev_noise=0.1,noise=False)
        ds_val =  worldstrat_MISR(root_dir="/data3/worldstrat_misr_saved_2",phase="val",revisits=revisits,stddev_noise=0.1,noise=False)
        train_loader = torch.utils.data.DataLoader(ds_train,batch_size=train_batch_size,num_workers=num_workers,
                                                   drop_last=True,prefetch_factor=prefetch_factor)
        val_loader = torch.utils.data.DataLoader(ds_val,batch_size=val_batch_size,num_workers=num_workers,
                                                 drop_last=True,prefetch_factor=prefetch_factor)

    if dataloader_type == "S2NAIP":
        import pathlib
        from ldm.data.S2NAIP import S2NAIP
        from torch.utils.data import DataLoader
        ds_train = S2NAIP(phase="train",data_folder="/data2/simon/S2NAIP_saved/train/",apply_norm=True)
        ds_val =  S2NAIP(phase="val",data_folder="/data2/simon/S2NAIP_saved/train/",apply_norm=True)
        train_loader = torch.utils.data.DataLoader(ds_train,batch_size=train_batch_size,num_workers=num_workers,
                                                   shuffle=True,drop_last=True,prefetch_factor=prefetch_factor)
        val_loader = torch.utils.data.DataLoader(ds_val,batch_size=val_batch_size,num_workers=num_workers,
                                                 drop_last=True,shuffle=True,prefetch_factor=prefetch_factor)
    
    if dataloader_type == "S2NAIP_v2":
        import pathlib
        from ldm.data.S2NAIP_v2 import S2NAIP_v2
        from torch.utils.data import DataLoader
        ds_train = S2NAIP_v2(phase="train")
        ds_val =  S2NAIP_v2(phase="val")
        train_loader = torch.utils.data.DataLoader(ds_train,batch_size=train_batch_size,num_workers=num_workers,
                                                   shuffle=True,drop_last=True,prefetch_factor=prefetch_factor)
        val_loader = torch.utils.data.DataLoader(ds_val,batch_size=val_batch_size,num_workers=num_workers,
                                                 drop_last=True,shuffle=True,prefetch_factor=prefetch_factor)
        
    if dataloader_type == "S2NAIP_v2_MISR":
        import pathlib
        from ldm.data.S2NAIPv2_MISR_fake import S2NAIPv2_MISR_fake
        from torch.utils.data import DataLoader
        ds_train = S2NAIPv2_MISR_fake(phase="train")
        ds_val =  S2NAIPv2_MISR_fake(phase="val")
        train_loader = torch.utils.data.DataLoader(ds_train,batch_size=train_batch_size,num_workers=num_workers,
                                                   shuffle=True,drop_last=True,prefetch_factor=prefetch_factor)
        val_loader = torch.utils.data.DataLoader(ds_val,batch_size=val_batch_size,num_workers=num_workers,
                                                 drop_last=True,shuffle=True,prefetch_factor=prefetch_factor)

    if dataloader_type == "S2NAIP_v2_20m":
        import pathlib
        from ldm.data.S2NAIP_v2_6b_20m import S2NAIP_v2_6b_20m
        from torch.utils.data import DataLoader
        ds_train = S2NAIP_v2_6b_20m(phase="train",data_folder = "/data2/simon/S2NAIP_v2_b6_20m/",apply_norm=True,augmentation=True)
        ds_val =  S2NAIP_v2_6b_20m(phase="val",data_folder = "/data2/simon/S2NAIP_v2_b6_20m/",apply_norm=True,augmentation=True)
        train_loader = torch.utils.data.DataLoader(ds_train,batch_size=train_batch_size,num_workers=num_workers,
                                                   shuffle=True,drop_last=True,prefetch_factor=prefetch_factor)
        val_loader = torch.utils.data.DataLoader(ds_val,batch_size=val_batch_size,num_workers=num_workers,
                                                 drop_last=True,shuffle=False,prefetch_factor=prefetch_factor)
        
    
    if dataloader_type == "sen2_test":
        import pathlib
        from opensr_dataloaders.sen2_test import sen2_test
        from torch.utils.data import DataLoader
        ds_test = sen2_test(data_folder = "/data2/simon/test_s2/S2A_MSIL2A_20230729T100031_N0509_R122_T33TUG_20230729T134559.SAFE",
                            amount=24,band_selection=kwargs["band_selection"],apply_norm=kwargs["apply_norm"])
        test_loader = torch.utils.data.DataLoader(ds_test,batch_size=val_batch_size,num_workers=num_workers,
                                                   shuffle=False,drop_last=True,prefetch_factor=prefetch_factor)
        return(test_loader)
        
    if dataloader_type == "S2NAIP_int":
        import pathlib
        from ldm.data.S2NAIP_int import S2NAIP_int
        from torch.utils.data import DataLoader
        ds_train = S2NAIP_int(phase="train",data_folder="/data2/simon/S2NAIP_saved/train/")
        ds_val =  S2NAIP_int(phase="val",data_folder="/data2/simon/S2NAIP_saved/train/")
        train_loader = torch.utils.data.DataLoader(ds_train,batch_size=train_batch_size,num_workers=num_workers,
                                                   shuffle=True,drop_last=True,prefetch_factor=prefetch_factor)
        val_loader = torch.utils.data.DataLoader(ds_val,batch_size=val_batch_size,num_workers=num_workers,
                                                 drop_last=True,shuffle=True,prefetch_factor=prefetch_factor)

    if dataloader_type == "worldstrat_spot6":
        from ldm.data.custom_data import ImageDataset
        from torch.utils.data import DataLoader

        dataset_root = "/data2/simon/worldstrat_SISR_preprocessed/"
        ds_train = ImageDataset(phase="train",dataset_type="worldstrat",return_type="pair",
                            lr_res=128,hr_res=256,return_res="interpolated",val_range="0..1")
        ds_val = ImageDataset(phase="val",dataset_type="worldstrat",return_type="pair",
                            lr_res=128,hr_res=256,return_res="interpolated",val_range="0..1")

        train_loader = DataLoader(ds_train,batch_size=train_batch_size,num_workers=num_workers,shuffle=True,drop_last=True)
        val_loader = DataLoader(ds_val,batch_size=val_batch_size,num_workers=num_workers,drop_last=True)

    if dataloader_type == "worldstrat_preprocessed":
        from ldm.data.custom_data_worldstrat_preprocessed import worldstrat_SISR
        from torch.utils.data import DataLoader

        dataset_root = "/data2/simon/worldstrat_SISR_preprocessed/"
        ds_train = worldstrat_SISR(dataset_root,phase="train")
        ds_val = worldstrat_SISR(dataset_root,phase="val")

        train_loader = DataLoader(ds_train,batch_size=train_batch_size,num_workers=num_workers,shuffle=True,drop_last=True)
        val_loader = DataLoader(ds_val,batch_size=val_batch_size,num_workers=num_workers,drop_last=True,shuffle=True)

    if dataloader_type == "worldstrat_preprocessed_RGBNIR":
        from ldm.data.custom_data_worldstrat_preprocessed import worldstrat_SISR
        from torch.utils.data import DataLoader

        dataset_root = "/data2/simon/worldstrat_SISR_RGBNIR_preprocessed/"
        ds_train = worldstrat_SISR(dataset_root,phase="train",lr_type="interpolated")
        ds_val = worldstrat_SISR(dataset_root,phase="val",lr_type="interpolated",)

        train_loader = DataLoader(ds_train,batch_size=train_batch_size,num_workers=num_workers,drop_last=True,shuffle=True)
        val_loader = DataLoader(ds_val,batch_size=val_batch_size,num_workers=num_workers,drop_last=True,shuffle=True)


    if dataloader_type == "s2_dataset":
        from opensr_dataloaders.custom_sen2 import s2_dataset
        from torch.utils.data import DataLoader
        #directory_path = '/data3/S2_images/'  # Replace with the actual directory path
        directory_path = '/data2/simon/S2_images/'  # Replace with the actual directory path 
        ds_train = s2_dataset(directory_path,phase="train",bands=4)
        ds_val = s2_dataset(directory_path,phase="val",bands=4)
        train_loader = DataLoader(ds_train, batch_size=train_batch_size, drop_last=True,shuffle=True,num_workers=num_workers)
        val_loader = DataLoader(ds_val, batch_size=val_batch_size, drop_last=True,shuffle=True,num_workers=num_workers)
        
    if dataloader_type == "coco_dataset":
        from ldm.data.coco_dataset import JpegImageDataset as coco_dataset
        from torch.utils.data import DataLoader

        folders = ["/data2/simon/cv_datasets/COCO","/data2/simon/cv_datasets/ADE20K","/data2/simon/cv_datasets/OpenImages"]
        ds_train = coco_dataset(folders=folders,phase="train",image_size=512,return_type="pair",channels=4,force_rescan=False)
        ds_val = coco_dataset(folders=folders,phase="val",image_size=512,return_type="pair",channels=4,force_rescan=False)

        train_loader = DataLoader(ds_train,batch_size=train_batch_size,num_workers=num_workers,shuffle=True,persistent_workers=True)
        val_loader = DataLoader(ds_val,batch_size=val_batch_size,num_workers=num_workers,persistent_workers=True,drop_last=True,shuffle=True)

    if dataloader_type == "worldstrat_MISR_fake":
        from ldm.data.worldstrat_MISR_fake import worldstrat_MISR_fake as worldstrat_MISR_fake
        from torch.utils.data import DataLoader
        
        ds_train = worldstrat_MISR_fake(phase="train",revisits=revisits,noise=False)
        ds_val = worldstrat_MISR_fake(phase="val",revisits=revisits,noise=False)
        
        train_loader = DataLoader(ds_train,batch_size=train_batch_size,num_workers=num_workers,shuffle=True,persistent_workers=True)
        val_loader = DataLoader(ds_val,batch_size=val_batch_size,num_workers=num_workers,persistent_workers=True,drop_last=True,shuffle=True)


    if dataloader_type == "worldstrat_r":
        from ldm.data.worldstrat_r import worldstrat_DataSet
        from torch.utils.data import DataLoader
        
        ds_train = worldstrat_DataSet("/data1/worldstrat_r",ftype="train",revisits=revisits)
        ds_val = worldstrat_DataSet("/data1/worldstrat_r",ftype="val",revisits=revisits)
        
        train_loader = DataLoader(ds_train,batch_size=train_batch_size,num_workers=num_workers,shuffle=True,persistent_workers=True)
        val_loader = DataLoader(ds_val,batch_size=val_batch_size,num_workers=num_workers,persistent_workers=True,drop_last=True,shuffle=True)

        
        
        
    # FINAL RETURN
    return train_loader,val_loader,ds_train,ds_val
        


def create_pl_datamodule(train_loader,val_loader,test_loader=None):
    import pytorch_lightning as pl
    class pl_datamodule(pl.LightningDataModule):
        def __init__(self, train_loader, val_loader):
            super().__init__()
            self.train_loader = train_loader
            self.val_loader = val_loader
            self.test_loader = test_loader
        def train_dataloader(self):
            return self.train_loader
        def val_dataloader(self):
            return self.val_loader
        def test_dataloader(self):
            if self.test_loader!=None:
                return self.test_loader
        def prepare_data(self):
            pass
        def setup(self, stage=None):
            pass
        

    datamodule = pl_datamodule(train_loader,val_loader)
    return(datamodule)


"""
Copy of prev method in case sth goes wrong

# get and control datalaoder
dataloader_type = "worldstrat_preprocessed_RGBNIR"

batch_size = 2

assert dataloader_type in ["worldstrat_preprocessed","NAIP",
                           "worldstrat_preprocessed_RGBNIR",
                           "coco_dataset","worldstrat_spot6",]


if dataloader_type == "NAIP":
    from ldm.data.custom_data_naip import NAIP
    from torch.utils.data import DataLoader
    ds_train = NAIP(pathlib.Path("/data3/S2NAIP/train"), type="train", scale=4)
    ds_val =  NAIP(pathlib.Path("/data3/S2NAIP/val"), type="val", scale=4)
    ds_val = torch.utils.data.Subset(ds_val,list(range(20)))
    train_loader = torch.utils.data.DataLoader(ds_train,batch_size=16,shuffle=True)
    val_loader = torch.utils.data.DataLoader(ds_val,batch_size=5,drop_last=True)

if dataloader_type == "worldstrat_spot6":
    from ldm.data.custom_data import ImageDataset
    from torch.utils.data import DataLoader
    
    dataset_root = "/data2/simon/worldstrat_SISR_preprocessed/"
    ds_train = ImageDataset(phase="train",dataset_type="worldstrat",return_type="pair",
                        lr_res=128,hr_res=256,return_res="interpolated",val_range="0..1")
    ds_val = ImageDataset(phase="val",dataset_type="worldstrat",return_type="pair",
                        lr_res=128,hr_res=256,return_res="interpolated",val_range="0..1")
    
    train_loader = DataLoader(ds_train,batch_size=batch_size,num_workers=16,shuffle=True)
    val_loader = DataLoader(ds_val,batch_size=10,num_workers=batch_size)

if dataloader_type == "worldstrat_preprocessed":
    from ldm.data.custom_data_worldstrat_preprocessed import worldstrat_SISR
    from torch.utils.data import DataLoader
    
    dataset_root = "/data2/simon/worldstrat_SISR_preprocessed/"
    ds_train = worldstrat_SISR(dataset_root,phase="train")
    ds_val = worldstrat_SISR(dataset_root,phase="val")
    
    train_loader = DataLoader(ds_train,batch_size=batch_size,num_workers=16,shuffle=True)
    val_loader = DataLoader(ds_val,batch_size=10,num_workers=batch_size)
    
if dataloader_type == "worldstrat_preprocessed_RGBNIR":
    from ldm.data.custom_data_worldstrat_preprocessed import worldstrat_SISR
    from torch.utils.data import DataLoader
    
    dataset_root = "/data2/simon/worldstrat_SISR_RGBNIR_preprocessed/"
    ds_train = worldstrat_SISR(dataset_root,phase="train",lr_type="interpolated")
    ds_val = worldstrat_SISR(dataset_root,phase="val",lr_type="interpolated",)
    
    train_loader = DataLoader(ds_train,batch_size=batch_size,num_workers=16,shuffle=True)
    val_loader = DataLoader(ds_val,batch_size=batch_size,num_workers=1)
    
    
if dataloader_type == "coco_dataset":
    from ldm.data.coco_dataset import JpegImageDataset as coco_dataset
    from torch.utils.data import DataLoader
    
    folders = ["/data2/simon/cv_datasets/COCO","/data2/simon/cv_datasets/ADE20K","/data2/simon/cv_datasets/OpenImages"]
    ds_train = coco_dataset(folders=folders,phase="train",image_size=512,return_type="single",channels=4,force_rescan=False)
    ds_val = coco_dataset(folders=folders,phase="val",image_size=512,return_type="single",channels=4,force_rescan=False)
    
    train_loader = DataLoader(ds_train,batch_size=batch_size,num_workers=16,shuffle=True,persistent_workers=True)
    val_loader = DataLoader(ds_val,batch_size=1,num_workers=1,persistent_workers=True)
"""
