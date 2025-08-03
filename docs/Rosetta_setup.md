# Rosetta Setup Guide

## Overview
Rosetta is a comprehensive software suite for macromolecular modeling, protein design, and structure prediction. This guide covers PyRosetta installation and basic usage for enzyme engineering.

## Installation Options

### Option 1: PyRosetta (Recommended for Python Users)

#### Prerequisites
- Python 3.7-3.9
- 8GB+ RAM
- Linux/macOS (Windows via WSL)

#### Installation Steps

##### 1. Create Conda Environment
```bash
conda create -n rosetta python=3.8
conda activate rosetta
```

##### 2. Install PyRosetta
```bash
# For academic users (free license required)
pip install pyrosetta

# Alternative: Install from conda
conda install -c conda-forge pyrosetta
```

##### 3. Download Rosetta Database
```bash
# Download Rosetta database (required for PyRosetta)
wget https://www.rosettacommons.org/downloads/rosetta_bin_mac_2021.16.61629_bundle.tgz
tar -xzf rosetta_bin_mac_2021.16.61629_bundle.tgz
export ROSETTA_DB=/path/to/rosetta_database
```

### Option 2: Rosetta Binaries

#### Download and Install
1. Visit [Rosetta Commons](https://www.rosettacommons.org/software/license-and-download)
2. Request academic license
3. Download appropriate version for your OS
4. Extract and add to PATH

## Basic Usage

### PyRosetta Examples

#### 1. Load and Analyze Structure
```python
import pyrosetta
from pyrosetta import pose_from_pdb

# Initialize PyRosetta
pyrosetta.init()

# Load structure
pose = pose_from_pdb("protein.pdb")

# Basic analysis
print(f"Sequence: {pose.sequence()}")
print(f"Number of residues: {pose.total_residue()}")
print(f"Secondary structure: {pose.secstruct()}")
```

#### 2. Point Mutation
```python
from pyrosetta.rosetta.protocols.simple_moves import MutateResidue

# Create mutation protocol
mutate = MutateResidue()
mutate.set_target(238)  # Residue position
mutate.set_res_name("PHE")  # New amino acid

# Apply mutation
mutate.apply(pose)

# Save mutated structure
pose.dump_pdb("mutated_protein.pdb")
```

#### 3. Energy Scoring
```python
from pyrosetta import create_score_function

# Create scoring function
scorefxn = create_score_function("ref2015")

# Score the pose
score = scorefxn(pose)
print(f"Total energy: {score}")

# Per-residue energies
for i in range(1, pose.total_residue() + 1):
    res_score = scorefxn(pose, i)
    print(f"Residue {i}: {res_score}")
```

#### 4. Docking (if ligand present)
```python
from pyrosetta.rosetta.protocols.docking import DockMCMProtocol

# Setup docking
docking = DockMCMProtocol()
docking.set_scorefxn(scorefxn)

# Run docking
docking.apply(pose)

# Save docked structure
pose.dump_pdb("docked_protein.pdb")
```

### RosettaScripts Examples

#### 1. FastRelax Protocol
```xml
<ROSETTASCRIPTS>
    <SCOREFXNS>
        <ScoreFunction name="ref2015" weights="ref2015"/>
    </SCOREFXNS>
    
    <TASKOPERATIONS>
        <RestrictToRepacking name="repack_only"/>
    </TASKOPERATIONS>
    
    <MOVERS>
        <FastRelax name="relax" scorefxn="ref2015" task_operations="repack_only"/>
    </MOVERS>
    
    <PROTOCOLS>
        <Add mover="relax"/>
    </PROTOCOLS>
</ROSETTASCRIPTS>
```

#### 2. Point Mutation Protocol
```xml
<ROSETTASCRIPTS>
    <SCOREFXNS>
        <ScoreFunction name="ref2015" weights="ref2015"/>
    </SCOREFXNS>
    
    <TASKOPERATIONS>
        <OperateOnResidueSubset name="mutate_res" selector="residue_238">
            <MutateResidue target="PHE"/>
        </OperateOnResidueSubset>
    </TASKOPERATIONS>
    
    <MOVERS>
        <PackRotamersMover name="pack" scorefxn="ref2015" task_operations="mutate_res"/>
    </MOVERS>
    
    <PROTOCOLS>
        <Add mover="pack"/>
    </PROTOCOLS>
</ROSETTASCRIPTS>
```

## Integration with Workflow

### File Naming Convention
```
{enzyme_name}_{mutation}_{date}_{tool_version}_{protocol}.pdb
```

### Example
```
PETase_S238F_2024-01-15_rosetta_v2021.16_fastrelax.pdb
```

### Metadata Template
```yaml
sequence: MKLLNIFGLLSLAFMLSLLTFVSEKLI...
tool: Rosetta
version: 2021.16
protocol: FastRelax
date: 2024-01-15
author: researcher_name
energy_score: -1250.5
parameters:
  score_function: ref2015
  iterations: 5
  repack_only: true
validation_status: IN_SILICO_ONLY
```

## Common Protocols

### 1. Structure Refinement
- **FastRelax**: Quick structure optimization
- **Relax**: Thorough structure refinement
- **Minimize**: Energy minimization

### 2. Design Protocols
- **Fixbb**: Fixed backbone design
- **Backrub**: Backbone flexibility design
- **Loop modeling**: Loop region design

### 3. Docking Protocols
- **Rigid body docking**: Initial docking
- **Flexible docking**: Refined docking
- **High-resolution docking**: Final refinement

## Performance Tips

### Optimization
- Use multiple CPU cores when available
- Run protocols in parallel for multiple mutations
- Use appropriate scoring functions for your task

### Memory Management
- Process structures one at a time for large datasets
- Use `-out:file:silent` for efficient output
- Monitor memory usage for large proteins

## Troubleshooting

### Common Issues
1. **License Errors**: Ensure academic license is properly installed
2. **Database Errors**: Verify ROSETTA_DB environment variable
3. **Memory Issues**: Reduce number of iterations or use smaller proteins

### Debugging
```python
# Enable verbose output
pyrosetta.init("-out:level 100")

# Check pose validity
if pose.is_fullatom():
    print("Pose is full atom")
else:
    print("Pose is centroid")
```

## Citations
- Leaver-Fay, A., et al. (2011). ROSETTA3: an object-oriented software suite for the simulation and design of macromolecules. Methods in Enzymology, 487, 545-574.
- Alford, R. F., et al. (2017). The Rosetta all-atom energy function for macromolecular modeling and design. Journal of Chemical Theory and Computation, 13(6), 3031-3048.

## Next Steps
After Rosetta analysis:
1. Compare energy scores between wild-type and mutants
2. Visualize structural changes in ChimeraX/PyMOL
3. Document findings in `/design_notes/`
4. Consider wet-lab validation for promising designs 