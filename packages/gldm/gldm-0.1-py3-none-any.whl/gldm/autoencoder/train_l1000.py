from dataset import LincsDataset
from torch_geometric.loader import DataLoader
from model import BaseModel
from aae import AAE
from model_utils import get_params
from pytorch_lightning import Trainer
from torch.utils.data import ConcatDataset
from datetime import datetime
from pytorch_lightning.callbacks import ModelCheckpoint, EarlyStopping
from pytorch_lightning.loggers import TensorBoardLogger
from pytorch_lightning.callbacks import LearningRateMonitor
from model_utils import transfer_trained_weights
import argparse

# import torch.multiprocessing as mp

"""python train_l1000.py FiLMConv vae"""


if __name__ == "__main__":

    batch_size = 1
    NUM_WORKERS = 4
    train_split1 = "train_0"
    valid_split = "valid_0"
    parser = argparse.ArgumentParser()
    """
    pretrained_ckpt can be None, in which case transfer learning won't be used.

    python train_l1000.py \
    --layer_type=FiLMConv \
    --model_architecture=vae \
    --use_oclr_scheduler \
    --using_cyclical_anneal \
    --gradient_clip_val=1.0 \
    --max_lr=1e-4 \
    --gen_step_drop_probability=0.5 \
    --pretrained_ckpt=/data/ongh0068/l1000/2023-03-03_09_30_01.589479/epoch=12-val_loss=0.46.ckpt \
    --pretrained_ckpt_model_type=vae \
    
    ##### FROM SCRATCH 

    # VAE: no oclr + no kl anneal ##### LOWER LR + LOWER GRADIENT CLIP VAL + CLAMP LOG VAR DUE TO INSTABILITY and nan loss in kld
    python train_l1000.py \
    --layer_type=FiLMConv \
    --model_architecture=vae \
    --gradient_clip_val=0.1 \
    --max_lr=5e-5 \
    --gen_step_drop_probability=0.0 \
    --use_clamp_log_var

    # AAE: oclr 
    python train_l1000.py \
    --layer_type=FiLMConv \
    --model_architecture=aae \
    --gradient_clip_val=1.0 \
    --max_lr=1e-4 \
    --gen_step_drop_probability=0.0
    
    # WAE: oclr  
    python train_l1000.py \
    --layer_type=FiLMConv \
    --model_architecture=aae \
    --gradient_clip_val=0.0 \
    --max_lr=1e-4 \
    --using_wasserstein_loss --using_gp \
    --gen_step_drop_probability=0.0

    ##### FROM SCRATCH 

    # VAE: no oclr + no kl anneal + ? dropout?
    python train_l1000.py \
    --layer_type=FiLMConv \
    --model_architecture=vae \
    --gradient_clip_val=1.0 \
    --max_lr=5e-6 \
    --gen_step_drop_probability=0.0 \
    --pretrained_ckpt=/data/ongh0068/l1000/2023-03-05_14_24_55.916122/epoch=24-val_loss=0.29.ckpt \
    --pretrained_ckpt_model_type=vae 

    # /data/ongh0068/l1000/2023-03-05_14_24_55.916122/epoch=24-val_loss=0.29.ckpt
    # /data/ongh0068/l1000/2023-03-03_09_30_01.589479/epoch=12-val_loss=0.46.ckpt


    # AAE: oclr + no gen step dropout
    python train_l1000.py \
    --layer_type=FiLMConv \
    --model_architecture=aae \
    --use_oclr_scheduler \
    --gradient_clip_val=1.0 \
    --max_lr=1e-5 \
    --gen_step_drop_probability=0.0 \
    --pretrained_ckpt=/data/ongh0068/l1000/2023-03-06_16_47_15.554929/epoch=11-train_loss=0.71.ckpt \
    --pretrained_ckpt_model_type=aae 



    # WAE: oclr + no gen step dropout
    python train_l1000.py \
    --layer_type=FiLMConv \
    --model_architecture=aae \
    --use_oclr_scheduler \
    --gradient_clip_val=1.0 \
    --max_lr=1e-5 \
    --gen_step_drop_probability=0.0 \
    --pretrained_ckpt=/data/ongh0068/l1000/2023-03-07_23_24_09.367132/epoch=05-train_loss=0.23.ckpt \
    --pretrained_ckpt_model_type=aae --using_wasserstein_loss --using_gp

    """
    parser.add_argument(
        "--layer_type",
        required=True,
        type=str,
        choices=["FiLMConv", "GATConv", "GCNConv"],
    )
    parser.add_argument(
        "--model_architecture", required=True, type=str, choices=["aae", "vae"]
    )
    parser.add_argument("--use_oclr_scheduler", action="store_true")
    parser.add_argument("--using_cyclical_anneal", action="store_true")
    parser.add_argument("--using_wasserstein_loss", action="store_true")
    parser.add_argument("--use_clamp_log_var", action="store_true")
    parser.add_argument("--using_gp", action="store_true")
    parser.add_argument("--gradient_clip_val", required=True, type=float, default=1.0)
    parser.add_argument("--max_lr", required=True, type=float, default=1e-5)
    parser.add_argument(
        "--gen_step_drop_probability", required=True, type=float, default=0.5
    )
    parser.add_argument("--pretrained_ckpt", type=str)
    parser.add_argument("--pretrained_ckpt_model_type", type=str)

    args = parser.parse_args()

    raw_moler_trace_dataset_parent_folder = "data/l1000/trace_dir"
    output_pyg_trace_dataset_parent_folder = (
        "data/l1000/already_batched"
    )
    gene_exp_controls_file_path = "data/l1000/robust_normalized_controls.npz"
    gene_exp_tumour_file_path = "data/l1000/robust_normalized_tumors.npz"
    lincs_csv_file_path = "data/l1000/experiments_filtered.csv"

    train_dataset = LincsDataset(
        root="/data/ongh0068",
        raw_moler_trace_dataset_parent_folder=raw_moler_trace_dataset_parent_folder,  # "/data/ongh0068/l1000/trace_playground",
        output_pyg_trace_dataset_parent_folder=output_pyg_trace_dataset_parent_folder,
        gene_exp_controls_file_path=gene_exp_controls_file_path,
        gene_exp_tumour_file_path=gene_exp_tumour_file_path,
        lincs_csv_file_path=lincs_csv_file_path,
        split=train_split1,
        gen_step_drop_probability=args.gen_step_drop_probability,
    )

    valid_dataset = LincsDataset(
        root="/data/ongh0068",
        raw_moler_trace_dataset_parent_folder=raw_moler_trace_dataset_parent_folder,  # "/data/ongh0068/l1000/trace_playground",
        output_pyg_trace_dataset_parent_folder=output_pyg_trace_dataset_parent_folder,
        gene_exp_controls_file_path=gene_exp_controls_file_path,
        gene_exp_tumour_file_path=gene_exp_tumour_file_path,
        lincs_csv_file_path=lincs_csv_file_path,
        split=valid_split,
        gen_step_drop_probability=args.gen_step_drop_probability,
    )

    train_dataloader = DataLoader(
        train_dataset,
        batch_size=batch_size,
        shuffle=True,
        # sampler=train_sampler,
        follow_batch=[
            "correct_edge_choices",
            "correct_edge_types",
            "valid_edge_choices",
            "valid_attachment_point_choices",
            "correct_attachment_point_choice",
            "correct_node_type_choices",
            "original_graph_x",
            "correct_first_node_type_choices",
        ],
        num_workers=NUM_WORKERS,
        # prefetch_factor=0,
    )

    valid_dataloader = DataLoader(
        valid_dataset,
        batch_size=batch_size,
        shuffle=False,
        # sampler=valid_sampler,
        follow_batch=[
            "correct_edge_choices",
            "correct_edge_types",
            "valid_edge_choices",
            "valid_attachment_point_choices",
            "correct_attachment_point_choice",
            "correct_node_type_choices",
            "original_graph_x",
            "correct_first_node_type_choices",
        ],
        num_workers=NUM_WORKERS,
        # prefetch_factor=0,
    )
    print(len(train_dataloader), len(valid_dataloader))

    params = get_params(dataset=train_dataset)  # train_dataset)
    ###################################################
    params["full_graph_encoder"]["layer_type"] = args.layer_type
    params["partial_graph_encoder"]["layer_type"] = args.layer_type
    params["use_oclr_scheduler"] = args.use_oclr_scheduler
    params["using_cyclical_anneal"] = args.using_cyclical_anneal
    model_architecture = args.model_architecture
    params["max_lr"] = args.max_lr
    ###################################################

    if model_architecture == "aae":
        params["gene_exp_condition_mlp"]["input_feature_dim"] = 832 + 978 + 1
        model = AAE(
            params,
            valid_dataset,
            using_lincs=True,
            num_train_batches=len(train_dataloader),
            batch_size=batch_size,
            using_wasserstein_loss=True if args.using_wasserstein_loss else False,
            using_gp=True if args.using_gp else False,
        )
    elif model_architecture == "vae":
        model = BaseModel(
            params,
            valid_dataset,
            using_lincs=True,
            num_train_batches=len(train_dataloader),
            batch_size=batch_size,
            use_clamp_log_var = True if args.use_clamp_log_var is not None else False
        )  # train_dataset)
    else:
        raise ValueError

    if args.pretrained_ckpt is not None:
        print(f"Transfering weights from {args.pretrained_ckpt}...")
        assert args.pretrained_ckpt_model_type is not None
        if args.pretrained_ckpt_model_type == "vae":
            pretrained_model = BaseModel.load_from_checkpoint(
                args.pretrained_ckpt,
                params=params,
                dataset=valid_dataset,
                using_lincs=False,
                num_train_batches=len(train_dataloader),
                batch_size=batch_size,
            )
        elif args.pretrained_ckpt_model_type == "aae":
            pretrained_model = AAE.load_from_checkpoint(
                args.pretrained_ckpt,
                params=params,
                dataset=valid_dataset,
                using_lincs=False,
                num_train_batches=len(train_dataloader),
                batch_size=batch_size,
                using_wasserstein_loss=True if args.using_wasserstein_loss else False,
                using_gp=True if args.using_gp else False,
            )
        else:
            raise ValueError
        transferred_layer_names = transfer_trained_weights(pretrained_model, model)
        del pretrained_model
        print("Done transfering weights for layers: ", transferred_layer_names)
    ###################################################

    # Get current time for folder path.
    now = str(datetime.now()).replace(" ", "_").replace(":", "_")

    # Callbacks
    lr_monitor = LearningRateMonitor(logging_interval="step")
    tensorboard_logger = TensorBoardLogger(save_dir=f"../{now}", name=f"logs_{now}")
    early_stopping = EarlyStopping(monitor="val_loss", patience=3)
    if model_architecture == "vae":
        checkpoint_callback = ModelCheckpoint(
            save_top_k=1,
            monitor="val_loss",
            dirpath=f"../{now}",
            mode="min",
            filename="{epoch:02d}-{val_loss:.2f}",
        )
    elif model_architecture == "aae":
        checkpoint_callback = ModelCheckpoint(
            dirpath=f"../{now}",
            filename="{epoch:02d}-{train_loss:.2f}",
            monitor="epoch",
            every_n_epochs=3,
            save_on_train_epoch_end=True,
            save_top_k=-1,
        )

    callbacks = (
        [checkpoint_callback, lr_monitor, early_stopping]
        if model_architecture == "vae"
        else [checkpoint_callback, lr_monitor]
    )
    # mp.set_start_method('spawn')
    trainer = Trainer(
        accelerator="gpu",
        max_epochs=30,
        devices=[2],
        callbacks=callbacks,
        logger=tensorboard_logger,
        gradient_clip_val=args.gradient_clip_val,
        # fast_dev_run=True
        # detect_anomaly=True,
        # track_grad_norm=int(sys.argv[3]), # set to 2 for l2 norm
    )  # overfit_batches=1)
    trainer.fit(
        model,
        train_dataloaders=train_dataloader,
        val_dataloaders=valid_dataloader,
    )
