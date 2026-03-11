# Model Checkpoints

This directory should contain the Stack foundation model checkpoints.

## Required Files

1. **Stack-Large checkpoint** (`bc_large.ckpt`)
   - Download from: https://huggingface.co/arcinstitute/Stack-Large
   - File: `bc_large.ckpt`
   - Size: ~2.5 GB

2. **Gene list** (`basecount_1000per_15000max.pkl`)
   - Download from: https://huggingface.co/arcinstitute/Stack-Large
   - File: `basecount_1000per_15000max.pkl`
   - Size: ~900 KB

## Download Commands

```bash
# Using huggingface_hub Python package
from huggingface_hub import hf_hub_download

ckpt_path = hf_hub_download(
    repo_id="arcinstitute/Stack-Large",
    filename="bc_large.ckpt",
    local_dir="."
)

gene_list_path = hf_hub_download(
    repo_id="arcinstitute/Stack-Large",
    filename="basecount_1000per_15000max.pkl",
    local_dir="."
)
```

## Alternative Models

For other Stack variants, see: https://huggingface.co/collections/arcinstitute/stack

- `Stack-Large-Aligned` - Aligned version
- `ST-HVG-Tahoe` - HVG subset trained on Tahoe-100M
- `ST-SE-Tahoe` - SE variant trained on Tahoe-100M