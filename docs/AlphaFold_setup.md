# AlphaFold Setup Guide

## Overview
AlphaFold is a deep learning system that predicts protein 3D structures from amino acid sequences. This guide covers both local installation and ColabFold usage.

## Option 1: ColabFold (Recommended for Beginners)

### Quick Start
1. Visit [ColabFold](https://colab.research.google.com/github/sokrypton/ColabFold/blob/main/AlphaFold2.ipynb)
2. Upload your FASTA sequence
3. Run the notebook
4. Download results

### Advantages
- No local installation required
- Free GPU access
- Pre-configured environment
- Easy to use interface

## Option 2: Local AlphaFold Installation

### Prerequisites
- Python 3.8+
- CUDA-compatible GPU (recommended)
- 16GB+ RAM
- 100GB+ disk space

### Installation Steps

#### 1. Create Conda Environment
```bash
conda create -n alphafold python=3.8
conda activate alphafold
```

#### 2. Install AlphaFold
```bash
pip install alphafold
```

#### 3. Download Genetic Databases
```bash
# Download databases (this may take several hours)
wget https://storage.googleapis.com/alphafold-databases/casp14_sequences.fasta
wget https://storage.googleapis.com/alphafold-databases/pdb70_2021Mar03.tar.gz
# ... (additional database downloads)
```

#### 4. Set Environment Variables
```bash
export ALPHAFOLD_DATA_DIR=/path/to/your/alphafold/data
export ALPHAFOLD_DB_DIR=/path/to/your/alphafold/databases
```

### Usage

#### Basic Command
```bash
python -m alphafold.run_alphafold \
  --fasta_paths=/path/to/sequences.fasta \
  --output_dir=/path/to/output \
  --data_dir=/path/to/alphafold/data \
  --uniref90_database_path=/path/to/uniref90.fasta \
  --mgnify_database_path=/path/to/mgy_clusters.fa \
  --pdb70_database_path=/path/to/pdb70 \
  --uniclust30_database_path=/path/to/uniclust30.fasta \
  --bfd_database_path=/path/to/bfd \
  --template_mmcif_dir=/path/to/pdb_mmcif/mmcif_files \
  --obsolete_pdbs_path=/path/to/pdb_mmcif/obsolete.dat
```

#### Python API
```python
import alphafold
from alphafold.data import pipeline
from alphafold.model import config
from alphafold.model import model

# Load your sequence
with open('sequence.fasta', 'r') as f:
    sequence = f.read().strip()

# Run prediction
result = alphafold.predict_structure(sequence)
```

## Output Files
- `ranked_0.pdb` - Best predicted structure
- `ranked_1.pdb` - Second best structure
- `ranking_debug.json` - Confidence scores
- `scores.json` - Detailed scoring information

## Integration with Workflow

### File Naming Convention
```
{enzyme_name}_{mutation}_{date}_{tool_version}.pdb
```

### Example
```
PETase_S238F_2024-01-15_alphafold_v2.3.2.pdb
```

### Metadata Template
```yaml
sequence: MKLLNIFGLLSLAFMLSLLTFVSEKLI...
tool: AlphaFold
version: 2.3.2
date: 2024-01-15
author: researcher_name
confidence_score: 0.85
parameters:
  max_extra_seq: 1024
  num_recycle: 3
  num_ensemble: 1
validation_status: IN_SILICO_ONLY
```

## Troubleshooting

### Common Issues
1. **Out of Memory**: Reduce `max_extra_seq` parameter
2. **Slow Performance**: Use GPU acceleration
3. **Database Errors**: Verify database paths and integrity

### Performance Tips
- Use GPU acceleration when available
- Limit sequence length for faster processing
- Use ColabFold for quick prototyping

## Citations
- Jumper, J., et al. (2021). Highly accurate protein structure prediction with AlphaFold. Nature, 596(7873), 583-589.
- Mirdita, M., et al. (2022). ColabFold: making protein folding accessible to all. Nature Methods, 19(6), 679-682.

## Next Steps
After structure prediction:
1. Validate model quality using pLDDT scores
2. Run Rosetta refinement if needed
3. Visualize in ChimeraX/PyMOL
4. Document in `/design_notes/` 