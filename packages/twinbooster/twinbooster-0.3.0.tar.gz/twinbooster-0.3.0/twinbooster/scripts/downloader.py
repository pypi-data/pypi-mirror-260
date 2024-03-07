import os
import tarfile
from urllib.request import urlretrieve


# alternatively: wget -qO- <url> | tar xvz -C </target/directory>


def download_models(
        lgbm_save_path: str = "./twinbooster/scripts/lgbm/best_model",
        barlow_twins_save_path: str = "./twinbooster/scripts/barlow_twins/best_model"
):
    """Download pretrained models."""
    # Create the paths and directories if they don't exist
    os.makedirs(lgbm_save_path, exist_ok=True)
    os.makedirs(barlow_twins_save_path, exist_ok=True)

    # Download the tar and extract it in the save path
    lgbm_model_url = "https://syncandshare.lrz.de/dl/fiMSWXFeRgsSkQjyCnrihe/lgbm_model.tar.xz"
    barlow_twins_model_url = "https://syncandshare.lrz.de/dl/fi9dFf1krBH2X6x1kmi3JM/bt_model.tar.xz"
    lgbm_tar_path = os.path.join(lgbm_save_path, "lgbm_model.tar.xz")
    barlow_twins_tar_path = os.path.join(barlow_twins_save_path, "bt_model.tar.xz")

    # Download the tar files
    if not os.path.exists(lgbm_tar_path):
        print("Downloading LightGBM model...")
        urlretrieve(lgbm_model_url, lgbm_tar_path)
    if not os.path.exists(barlow_twins_tar_path):
        print("Downloading Barlow Twins model...")
        urlretrieve(barlow_twins_model_url, barlow_twins_tar_path)

    # Extract the tar files and set permissions
    print("Extracting LightGBM model...")
    with tarfile.open(lgbm_tar_path, "r:xz") as tar:
        tar.extractall(lgbm_save_path)
        for member in tar.getmembers():
            filepath = os.path.join(lgbm_save_path, member.name)
            if member.isfile():  # Only change permissions of files, not directories
                os.chmod(filepath, 0o644)  # Read and write for owner, read for others

    print("Extracting Barlow Twins model...")
    with tarfile.open(barlow_twins_tar_path, "r:xz") as tar:
        tar.extractall(barlow_twins_save_path)
        for member in tar.getmembers():
            filepath = os.path.join(barlow_twins_save_path, member.name)
            if member.isfile():  # Only change permissions of files, not directories
                os.chmod(filepath, 0o644)  # Read and write for owner, read for others

    # Remove the tar files
    os.remove(lgbm_tar_path)
    os.remove(barlow_twins_tar_path)


def download_data(save_path: str = "./twinbooster/datasets/fs-mol"):
    """Download the data."""
    # Create the save path if it doesn't exist
    os.makedirs(save_path, exist_ok=True)

    # Download the tar and extract it in the save path
    data_url = "https://syncandshare.lrz.de/getlink/fiJ317U1asvtQJC5npSVkn/fsmol_data.tar"
    tar_path = os.path.join(save_path, "fsmol_data.tar")

    # Download the tar file
    if not os.path.exists(tar_path):
        print("Downloading data...")
        urlretrieve(data_url, tar_path)

    # Extract the tar file
    print("Extracting tar file...")
    with tarfile.open(tar_path, "r:tar") as tar:
        tar.extractall(save_path)

    # Remove the tar file
    os.remove(tar_path)


def download_pretraining_data(save_path: str = "./twinbooster/pretraining"):
    """Download the pretraining data."""
    raise NotImplementedError("This function is not implemented yet, due to file size >30GB.")
    # Create the save path if it doesn't exist
    os.makedirs(save_path, exist_ok=True)

    # Download the tar and extract it in the save path
    data_url = ""
    tar_path = os.path.join(save_path, "pretraining_data.tar")

    # Download the tar file
    if not os.path.exists(tar_path):
        print("Downloading pretraining data...")
        urlretrieve(data_url, tar_path)

    # Extract the tar file
    print("Extracting tar file...")
    with tarfile.open(tar_path, "r:tar") as tar:
        tar.extractall(save_path)

    # Remove the tar file
    os.remove(tar_path)
