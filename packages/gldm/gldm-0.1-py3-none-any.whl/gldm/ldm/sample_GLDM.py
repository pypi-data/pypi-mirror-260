import sys 
sys.path.append('ldm/')
sys.path.append('../autoencoder/')
import os
os.environ["CUDA_DEVICE_ORDER"]="PCI_BUS_ID"  
os.environ["CUDA_VISIBLE_DEVICES"]="1"
import argparse
import pandas as pd
import pickle
from moler_ldm import LatentDiffusion
import torch
from dataset import LincsDataset, MolerDataset
from torch_geometric.loader import DataLoader
from omegaconf import OmegaConf
from model_utils import get_params
from tqdm import tqdm
from pytorch_lightning.trainer import Trainer
from pytorch_lightning.callbacks import ModelCheckpoint, EarlyStopping
from pytorch_lightning.loggers import TensorBoardLogger
from pytorch_lightning.callbacks import LearningRateMonitor
from datetime import datetime
from ldm.models.diffusion.ddim import DDIMSampler
from ldm.modules.diffusionmodules.util import make_ddim_sampling_parameters, make_ddim_timesteps, noise_like
from DDIM import MolSampler
from rdkit import Chem
from rdkit.Chem import Draw
from rdkit.Chem.Draw import IPythonConsole
IPythonConsole.drawOptions.addAtomIndices = False
IPythonConsole.drawOptions.addStereoAnnotation = True
IPythonConsole.drawOptions.baseFontSize = 0.5
IPythonConsole.ipython_useSVG=False

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--ckpt_path', '-m', type=str, default='model_ckpt/GLDM_WAE_uncond.ckpt', help='Path to the checkpoint file')
    parser.add_argument('--config_file', '-c', type=str, default='config/ldm_uncon+wae_uncon.yml', help='Path to the configuration file')
    parser.add_argument('--raw_data', '-r', type=str, default="/data/ongh0068/guacamol/trace_dir", help='Path to the raw data file')
    parser.add_argument('--trace_data', '-t', type=str, default="/data/ongh0068/l1000/already_batched", help='Path to processed data')
    parser.add_argument('--num_samples', '-n', type=int, default=10, help='Number of samples to generate')
    parser.add_argument('--gene_expr', '-g', type=str, default=None, help='Path to gene expression file')
    parser.add_argument('--output', '-o', type=str, default='samples.pkl', help='Path to output file')
    parser.add_argument('--save_img', '-s', type=str, default=None, help='Path to output image file')

    args = parser.parse_args()

    ckpt_path = args.ckpt_path
    checkpoint = torch.load(ckpt_path, map_location = device)
    config_file = args.config_file
    config = OmegaConf.load(config_file)
    ldm_params = config['model']['params']
    num_samples = args.num_samples
    save_img = args.save_img

    # args
    batch_size = 1
    NUM_WORKERS = 4
    train_split1 = "train_0"
    valid_split = "valid_0"

    layer_type = "FiLMConv"
    model_architecture = 'aae'
    gradient_clip_val = 1.0
    max_lr = 1e-5
    gen_step_drop_probability = 0
    use_oclr_scheduler = True
    using_cyclical_anneal = False
    use_clamp_log_var = False

    raw_moler_trace_dataset_parent_folder = args.raw_data
    # raw_moler_trace_dataset_parent_folder = "/data/ongh0068/l1000/TRACE_DIR"
    output_pyg_trace_dataset_parent_folder = args.trace_data
    do_constrained_generation = True if args.gene_expr is not None else False

    dataset = MolerDataset(
        root="/data/ongh0068",
        raw_moler_trace_dataset_parent_folder=raw_moler_trace_dataset_parent_folder,  # "/data/ongh0068/l1000/trace_playground",
        output_pyg_trace_dataset_parent_folder=output_pyg_trace_dataset_parent_folder,
        split="valid_0",
        gen_step_drop_probability=0.0
    )

    first_stage_params = get_params(dataset)
    first_stage_config = config['model']['first_stage_config']
    ldm_params = config['model']['params']
    unet_params = config['model']['unet_config']['params']
    first_stage_params["gene_exp_condition_mlp"]["input_feature_dim"] = 832 + 978 + 1

    if do_constrained_generation:
        gene_expr = torch.load(args.gene_expr, map_location=device)

    ldm_model = LatentDiffusion(
        first_stage_config,
        config['model']['cond_stage_config'],
        dataset, 
        gen_step_drop_probability,
        batch_size,
        first_stage_params,
        first_stage_config['ckpt_path'],
        unet_config = config['model']['unet_config'],
        **ldm_params
    )
    ldm_model.load_state_dict(checkpoint['state_dict'])
    ldm_model.to(device=device)
    ldm_model.eval()

    sampler = MolSampler(ldm_model)
    ddim_steps=500
    ddim_eta=1.0
    size = (1, 512)

    samples, _ = sampler.sample(
        S = ddim_steps,
        batch_size = num_samples,  # not batch size
        conditioning = gene_expr if do_constrained_generation else None,
        shape = size,
        ddim_eta = ddim_eta, 
        verbose = False
    )

    decoding_samples = samples.view((num_samples, unet_params.image_size))
    decoding_res = ldm_model.first_stage_model.decode(decoding_samples)
    output_mols = [decoding_res[i].molecule for i in range(len(decoding_res))]

    if args.output is not None:
        with open(args.output, 'wb') as f:
            pickle.dump(output_mols, f)
    if save_img is not None:
        if '.png' in save_img:
            img = Draw.MolsToGridImage(output_mols, subImgSize=(200,200), maxMols = 1000, molsPerRow=5, returnPNG=False)
            img.save(save_img)
        elif '.svg' in save_img:
            img = Draw.MolsToGridImage(output_mols, subImgSize=(200,200), maxMols = 1000, molsPerRow=5, useSVG=True, returnPNG=False)
            # with open(save_img, 'wb') as f:
            #     f.write(img.data)
            img.save(save_img)
        else:
            raise ValueError("Invalid file format")