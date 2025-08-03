# Example Workflow: PETase S238F Mutation

This example demonstrates the complete workflow for designing and analyzing a PETase mutant.

## Step 1: Design Rationale

**Target Enzyme**: PETase (Polyethylene Terephthalate Hydrolase)
**Mutation**: S238F (Serine to Phenylalanine at position 238)
**Rationale**: Active site optimization for improved PET binding and catalysis

## Step 2: Sequence Preparation

1. Create FASTA file: `designs/PETase_S238F.fasta`
2. Use the provided example: `examples/PETase_S238F_example.fasta`

## Step 3: Structure Prediction

### Using ColabFold (Recommended for beginners)
```bash
# Upload to ColabFold
# 1. Visit: https://colab.research.google.com/github/sokrypton/ColabFold/blob/main/AlphaFold2.ipynb
# 2. Upload PETase_S238F.fasta
# 3. Run the notebook
# 4. Download results
```

### Using Local AlphaFold
```bash
python scripts/run_alphafold.py designs/PETase_S238F.fasta --author "Your Name" --colabfold
```

### Expected Output
- `models/PETase_S238F_2024-01-15/ranked_0.pdb`
- `models/PETase_S238F_2024-01-15/metadata.yaml`

## Step 4: Rosetta Analysis

### Energy Scoring
```bash
python scripts/run_rosetta.py models/PETase_S238F_2024-01-15/ranked_0.pdb --protocol FastRelax --author "Your Name"
```

### Mutation Analysis
```bash
python scripts/run_rosetta.py models/PETase_S238F_2024-01-15/ranked_0.pdb --protocol Mutation --mutation S238F --author "Your Name"
```

### Expected Output
- `models/PETase_S238F_2024-01-15/PETase_S238F_2024-01-15_scores.sc`
- Energy scores and structural analysis

## Step 5: Visualization

### ChimeraX Commands
```python
# Open ChimeraX and run:
open models/PETase_S238F_2024-01-15/ranked_0.pdb
color bychain
surface
# Save session: viz/PETase_S238F_2024-01-15_session.cxs
```

### PyMOL Commands
```python
# Open PyMOL and run:
load models/PETase_S238F_2024-01-15/ranked_0.pdb
show cartoon
show surface
# Save session: viz/PETase_S238F_2024-01-15_session.pse
```

## Step 6: Documentation

### Create Experiment Report
Use the template: `docs/template_experiment_report.md`

### Example Report Structure
```yaml
experiment_id: PETase_S238F_2024-01-15
date: 2024-01-15
author: Your Name
status: IN_SILICO_ONLY

design_rationale:
  target_enzyme: PETase
  mutation: S238F
  rationale: Active site optimization for improved PET binding

results:
  alphafold_confidence: 0.85
  rosetta_energy: -1248.2 REU
  structural_changes: "Residue 238 side chain reorientation"
```

## Step 7: Analysis and Conclusions

### Key Findings
1. **Structure Quality**: pLDDT score 0.85 (Good)
2. **Energy Analysis**: ΔΔG = +2.3 REU (Acceptable penalty)
3. **Structural Changes**: Active site optimization achieved

### Recommendations
- **Priority**: High (promising active site optimization)
- **Next Steps**: Experimental validation recommended
- **Additional Mutations**: Consider S238W, S238Y variants

## Step 8: File Organization

```
PETase_S238F_2024-01-15/
├── designs/
│   └── PETase_S238F.fasta
├── models/
│   └── PETase_S238F_2024-01-15/
│       ├── ranked_0.pdb
│       ├── metadata.yaml
│       └── scores.sc
├── design_notes/
│   └── PETase_S238F_2024-01-15_design.yaml
└── viz/
    ├── PETase_S238F_2024-01-15_session.cxs
    └── PETase_S238F_2024-01-15_active_site.png
```

## Validation Checklist

- [ ] Structure prediction completed
- [ ] Energy analysis performed
- [ ] Visualization generated
- [ ] Documentation completed
- [ ] Citations included
- [ ] Metadata tracked
- [ ] Next steps identified

## Troubleshooting

### Common Issues
1. **ColabFold timeout**: Use smaller sequences or local AlphaFold
2. **Rosetta errors**: Check license and database paths
3. **Memory issues**: Reduce sequence length or use cloud resources

### Performance Tips
- Use ColabFold for quick prototyping
- Run Rosetta on high-performance systems
- Save intermediate results frequently

## Next Steps

1. **Experimental Validation**
   - Synthesize mutant gene
   - Express and purify protein
   - Measure PET degradation activity

2. **Additional Analysis**
   - Test multiple mutations
   - Compare to wild-type structure
   - Analyze binding site changes

3. **Publication**
   - Write up results
   - Include all tool citations
   - Share data and code

---

**Remember**: This is a computational prediction. Experimental validation is required for any real-world applications. 