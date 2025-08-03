# 🚀 Local Test Setup Guide - Windows

## Quick Start for Your Powerful System

With your **64GB RAM, RTX 4070, 4TB SSD, Windows 11** setup, you're perfectly positioned to run the full workflow locally!

## 📋 Step 1: Install Python

### Option A: Microsoft Store (Recommended)
1. Open Microsoft Store
2. Search for "Python 3.11" or "Python 3.12"
3. Install the latest version
4. Restart PowerShell

### Option B: Official Python.org
1. Go to https://www.python.org/downloads/
2. Download Python 3.11 or 3.12
3. **IMPORTANT**: Check "Add Python to PATH" during installation
4. Restart PowerShell

## 📋 Step 2: Verify Installation

```powershell
python --version
# Should show: Python 3.x.x

pip --version
# Should show: pip x.x.x
```

## 📋 Step 3: Install Dependencies

```powershell
# Navigate to your project directory
cd "C:\My Projects\Gene Folding And Creation"

# Install required packages
pip install -r requirements.txt

# Install additional packages for system monitoring
pip install psutil
```

## 📋 Step 4: Run Setup Script

```powershell
python setup_local_test.py
```

This will:
- ✅ Check your system resources
- ✅ Verify Python installation
- ✅ Install missing dependencies
- ✅ Create test directories
- ✅ Copy example files

## 📋 Step 5: Install AlphaFold (Optional for Full Test)

### Option A: ColabFold (Easiest - Cloud-based)
- No local installation needed
- Uses Google Colab
- Perfect for testing

### Option B: Local AlphaFold (Full Power)
```powershell
# Install AlphaFold dependencies
pip install alphafold

# Download AlphaFold databases (requires ~3TB space)
# See docs/AlphaFold_setup.md for detailed instructions
```

## 📋 Step 6: Install Rosetta (Optional)

```powershell
# Download Rosetta from: https://www.rosettacommons.org/software/license-and-download
# Extract to a directory
# Add to PATH or configure in scripts
```

## 🎯 Ready to Test!

Once setup is complete, you can run:

```powershell
# Test with ColabFold (recommended for first test)
python scripts/run_alphafold.py designs/PETase_S238F.fasta --colabfold

# Test with local AlphaFold (if installed)
python scripts/run_alphafold.py designs/PETase_S238F.fasta

# Test Rosetta (if installed)
python scripts/run_rosetta.py models/PETase_S238F_*/ranked_0.pdb --protocol FastRelax
```

## 🚀 Your System Advantages

With your **64GB RAM, RTX 4070, 4TB SSD**:

- ✅ **Local AlphaFold**: Can run full AlphaFold locally
- ✅ **GPU Acceleration**: RTX 4070 will speed up predictions
- ✅ **Large Models**: Can handle multiple protein structures
- ✅ **Fast Storage**: SSD will accelerate I/O operations
- ✅ **Parallel Processing**: Can run multiple jobs simultaneously

## 🔧 Troubleshooting

### Python not found:
```powershell
# Check if Python is in PATH
where python

# If not found, reinstall with "Add to PATH" checked
```

### Permission errors:
```powershell
# Run PowerShell as Administrator
# Or use user installation
pip install --user -r requirements.txt
```

### Memory issues:
- Close other applications
- Use ColabFold for cloud processing
- Monitor with Task Manager

## 📊 Expected Performance

With your system specs:
- **AlphaFold prediction**: ~30-60 minutes per protein
- **Rosetta refinement**: ~5-15 minutes per structure
- **Memory usage**: ~8-16GB during peak operations
- **Storage**: ~2-5GB per protein structure

Ready to revolutionize enzyme design! 🧬✨ 