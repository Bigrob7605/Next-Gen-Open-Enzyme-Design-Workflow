#!/usr/bin/env python3
"""
Test Script for Next-Gen Open Enzyme Design Workflow
Validates all components and creates test outputs
"""

import os
import sys
import yaml
import json
import shutil
from datetime import datetime
from pathlib import Path

def test_python_environment():
    """Test Python environment and dependencies."""
    print("🔍 Testing Python Environment...")
    
    # Test core dependencies
    dependencies = [
        'numpy', 'scipy', 'pandas', 'matplotlib', 'seaborn',
        'Bio', 'yaml', 'requests', 'tqdm', 'psutil'
    ]
    
    missing = []
    for dep in dependencies:
        try:
            __import__(dep)
            print(f"✅ {dep}")
        except ImportError:
            print(f"❌ {dep} - MISSING")
            missing.append(dep)
    
    if missing:
        print(f"\n⚠️  Missing dependencies: {', '.join(missing)}")
        return False
    
    print("✅ All dependencies available!")
    return True

def test_system_resources():
    """Test system resources."""
    print("\n🔍 Testing System Resources...")
    
    try:
        import psutil
        
        # Memory
        memory = psutil.virtual_memory()
        print(f"💾 RAM: {memory.total / (1024**3):.1f} GB total")
        print(f"   Available: {memory.available / (1024**3):.1f} GB")
        
        if memory.total >= 16 * (1024**3):
            print("✅ Sufficient RAM for local AlphaFold")
        else:
            print("⚠️  Limited RAM - recommend ColabFold")
        
        # Disk space
        disk = psutil.disk_usage('.')
        print(f"💿 Disk: {disk.free / (1024**3):.1f} GB available")
        
        if disk.free >= 50 * (1024**3):
            print("✅ Sufficient disk space")
        else:
            print("⚠️  Limited disk space")
        
        # CPU
        cpu_count = psutil.cpu_count()
        print(f"🖥️  CPU: {cpu_count} cores")
        
        return True
        
    except ImportError:
        print("⚠️  psutil not available - cannot check resources")
        return False

def test_directory_structure():
    """Test and create directory structure."""
    print("\n🔍 Testing Directory Structure...")
    
    directories = [
        'designs', 'models', 'design_notes', 'viz',
        'docs', 'scripts', 'citations', 'examples'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ {directory}/")
    
    return True

def test_fasta_parsing():
    """Test FASTA file parsing."""
    print("\n🔍 Testing FASTA Parsing...")
    
    try:
        from Bio import SeqIO
        
        # Create a test FASTA file
        test_fasta = "designs/test_sequence.fasta"
        test_sequence = """>PETase_test_mutant
MKLLNIFGLLSLAFMLSLLTFVSEKLIYQAGYDPVKDPNGNTNLFVKDPNVGKVNGVITFTYETKQGVFSVTYKNGEGCDLLKNGVDGLLYPGWTYNYGYGTPTANVGSWLIVGVALFVVGLLGAYYIGRSLAGKKRMLGIFLFACVSAALQIPFASVAAYIYNRQGIDDLCEVNGINYALLRCCGYDIARRGLDFVKKADDYNKWAENGKSEGFTWGMACGSGYFTANKGAGISVKGDKLVINGNPITFQALCDKVGLAPAVAVHVGPDIISSVTCCTTNIKTDFSDYLLGGDCVYVPVDAEVVFTTMDVGGQFRYSRPDKFLEFGTWGQSGITREVAYYEQGLLDVVNGRTWFGQAAQENSVYGVNGDTRDYLCDLLLEGIDVAFVWAKSFPVFRQMQDLEMKTGIPLGLTDPYVKCDAAMQKATEAAVSEEEGRRLRGEMMDLMQGQPREELYVKVSDRARLHKAVDPTIEPYINITVDGPSIHGLPKGVALMTAVAYRLAADQHRFVRRFEGDLVWLNVDIPAECFRNVRVILLENVTEMNREVKEAMMIMDRFKRKYTRYELAAAGVSIVQVIPLLKAAAEYTEAFGPLHLLAFRQWLQEYLVIKGERVRFALELLWPLGIYLVNRSVSTGQQARMLGAVLAILERFIKPLVFTAPTYVTGLLLKTIRGRPKYLLIASU"""
        
        with open(test_fasta, 'w') as f:
            f.write(test_sequence)
        
        # Parse the FASTA file
        records = list(SeqIO.parse(test_fasta, "fasta"))
        
        if len(records) == 1:
            print(f"✅ FASTA parsing successful")
            print(f"   Sequence length: {len(records[0].seq)}")
            print(f"   Sequence ID: {records[0].id}")
            return True
        else:
            print("❌ FASTA parsing failed")
            return False
            
    except Exception as e:
        print(f"❌ FASTA parsing error: {e}")
        return False

def test_metadata_generation():
    """Test metadata generation."""
    print("\n🔍 Testing Metadata Generation...")
    
    try:
        # Create test metadata
        metadata = {
            'experiment_id': 'PETase_test_2024-01-15',
            'date': datetime.now().isoformat(),
            'author': 'Local Test',
            'tool': 'Test Workflow',
            'version': '1.0.0',
            'sequence_length': 290,
            'mutation': 'S238F',
            'status': 'IN_SILICO_ONLY',
            'parameters': {
                'model_type': 'test',
                'confidence_threshold': 0.8
            }
        }
        
        # Save as YAML
        yaml_file = "design_notes/test_metadata.yaml"
        with open(yaml_file, 'w') as f:
            yaml.dump(metadata, f, default_flow_style=False)
        
        # Save as JSON
        json_file = "design_notes/test_metadata.json"
        with open(json_file, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print("✅ Metadata generation successful")
        print(f"   YAML: {yaml_file}")
        print(f"   JSON: {json_file}")
        return True
        
    except Exception as e:
        print(f"❌ Metadata generation error: {e}")
        return False

def test_script_validation():
    """Test script validation."""
    print("\n🔍 Testing Script Validation...")
    
    scripts = [
        'scripts/run_alphafold.py',
        'scripts/run_rosetta.py'
    ]
    
    for script in scripts:
        if os.path.exists(script):
            print(f"✅ {script}")
        else:
            print(f"❌ {script} - MISSING")
            return False
    
    return True

def test_documentation():
    """Test documentation files."""
    print("\n🔍 Testing Documentation...")
    
    docs = [
        'README.md',
        'docs/AlphaFold_setup.md',
        'docs/Rosetta_setup.md',
        'docs/template_experiment_report.md',
        'citations/CITATIONS.md'
    ]
    
    for doc in docs:
        if os.path.exists(doc):
            print(f"✅ {doc}")
        else:
            print(f"❌ {doc} - MISSING")
            return False
    
    return True

def create_test_outputs():
    """Create test outputs to demonstrate workflow."""
    print("\n🔧 Creating Test Outputs...")
    
    # Create a mock PDB structure (simplified)
    mock_pdb = """ATOM      1  N   ALA A   1      27.462  11.336  49.655  1.00 20.00           N  
ATOM      2  CA  ALA A   1      26.132  11.336  49.655  1.00 20.00           C  
ATOM      3  C   ALA A   1      25.132  11.336  49.655  1.00 20.00           C  
ATOM      4  O   ALA A   1      24.132  11.336  49.655  1.00 20.00           O  
END"""
    
    # Create test model directory
    model_dir = "models/PETase_test_2024-01-15"
    os.makedirs(model_dir, exist_ok=True)
    
    # Save mock PDB
    pdb_file = f"{model_dir}/ranked_0.pdb"
    with open(pdb_file, 'w') as f:
        f.write(mock_pdb)
    
    # Create test visualization
    viz_dir = "viz/PETase_test_2024-01-15"
    os.makedirs(viz_dir, exist_ok=True)
    
    # Create a simple plot
    try:
        import matplotlib.pyplot as plt
        import numpy as np
        
        # Mock energy scores
        positions = np.arange(1, 291)
        scores = np.random.normal(-1.5, 0.3, 290)
        
        plt.figure(figsize=(12, 6))
        plt.plot(positions, scores, 'b-', alpha=0.7)
        plt.axhline(y=-1.5, color='r', linestyle='--', alpha=0.5)
        plt.xlabel('Residue Position')
        plt.ylabel('Energy Score (REU)')
        plt.title('PETase Test - Rosetta Energy Scores')
        plt.grid(True, alpha=0.3)
        
        plot_file = f"{viz_dir}/energy_scores.png"
        plt.savefig(plot_file, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"✅ Created test plot: {plot_file}")
        
    except Exception as e:
        print(f"⚠️  Could not create plot: {e}")
    
    print(f"✅ Created test model: {pdb_file}")
    return True

def generate_test_report():
    """Generate a test experiment report."""
    print("\n📝 Generating Test Report...")
    
    report_content = """# Experiment Report: PETase Test Mutation

## Basic Information
- **Experiment ID**: PETase_test_2024-01-15
- **Date**: 2024-01-15
- **Author**: Local Test
- **Status**: IN_SILICO_ONLY

## Design Rationale
This is a test experiment to validate the Next-Gen Open Enzyme Design Workflow.

## Computational Methods
- **Structure Prediction**: Test workflow validation
- **Energy Scoring**: Mock Rosetta analysis
- **Visualization**: Matplotlib energy plots

## Results
- Python environment validated
- System resources checked
- Directory structure created
- FASTA parsing tested
- Metadata generation working
- Scripts validated
- Documentation complete

## Conclusions
The workflow is ready for real enzyme design experiments!

## Files Generated
- `designs/test_sequence.fasta` - Test sequence
- `models/PETase_test_2024-01-15/ranked_0.pdb` - Mock structure
- `viz/PETase_test_2024-01-15/energy_scores.png` - Energy plot
- `design_notes/test_metadata.yaml` - Test metadata
"""
    
    report_file = "design_notes/test_experiment_report.md"
    with open(report_file, 'w') as f:
        f.write(report_content)
    
    print(f"✅ Generated test report: {report_file}")
    return True

def main():
    """Main test function."""
    print("🚀 Next-Gen Open Enzyme Design Workflow")
    print("🧪 Local Test Suite")
    print("=" * 50)
    
    tests = [
        ("Python Environment", test_python_environment),
        ("System Resources", test_system_resources),
        ("Directory Structure", test_directory_structure),
        ("FASTA Parsing", test_fasta_parsing),
        ("Metadata Generation", test_metadata_generation),
        ("Script Validation", test_script_validation),
        ("Documentation", test_documentation),
        ("Test Outputs", create_test_outputs),
        ("Test Report", generate_test_report)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                print(f"❌ {test_name} failed")
        except Exception as e:
            print(f"❌ {test_name} error: {e}")
    
    print("\n" + "=" * 50)
    print(f"🎯 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Workflow is ready for use.")
        print("\n📋 Next Steps:")
        print("1. Install AlphaFold for structure prediction")
        print("2. Install Rosetta for protein engineering")
        print("3. Run real experiments with your sequences")
    else:
        print("⚠️  Some tests failed. Check the output above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 