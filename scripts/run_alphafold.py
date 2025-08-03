#!/usr/bin/env python3
"""
AlphaFold Structure Prediction Script
Automates structure prediction with metadata tracking for the enzyme design workflow.
"""

import os
import sys
import json
import yaml
import argparse
from datetime import datetime
from pathlib import Path
import subprocess
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AlphaFoldRunner:
    def __init__(self, config_file=None):
        """Initialize AlphaFold runner with configuration."""
        self.config = self.load_config(config_file)
        self.setup_directories()
        
    def load_config(self, config_file):
        """Load configuration from file or use defaults."""
        default_config = {
            'alphafold_version': '2.3.2',
            'max_extra_seq': 1024,
            'num_recycle': 3,
            'num_ensemble': 1,
            'output_dir': 'models',
            'design_notes_dir': 'design_notes',
            'fasta_dir': 'designs'
        }
        
        if config_file and os.path.exists(config_file):
            with open(config_file, 'r') as f:
                user_config = yaml.safe_load(f)
                default_config.update(user_config)
        
        return default_config
    
    def setup_directories(self):
        """Create necessary directories if they don't exist."""
        dirs = [
            self.config['output_dir'],
            self.config['design_notes_dir'],
            self.config['fasta_dir']
        ]
        
        for dir_path in dirs:
            Path(dir_path).mkdir(parents=True, exist_ok=True)
    
    def parse_fasta(self, fasta_file):
        """Parse FASTA file and extract sequence information."""
        sequences = {}
        current_header = None
        current_sequence = ""
        
        with open(fasta_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line.startswith('>'):
                    if current_header:
                        sequences[current_header] = current_sequence
                    current_header = line[1:]
                    current_sequence = ""
                else:
                    current_sequence += line
            
            if current_header:
                sequences[current_header] = current_sequence
        
        return sequences
    
    def generate_metadata(self, enzyme_name, mutation, sequence, author):
        """Generate metadata for the experiment."""
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        
        metadata = {
            'experiment_id': f"{enzyme_name}_{mutation}_{datetime.now().strftime('%Y-%m-%d')}",
            'date': datetime.now().strftime("%Y-%m-%d"),
            'timestamp': timestamp,
            'author': author,
            'enzyme_name': enzyme_name,
            'mutation': mutation,
            'sequence': sequence,
            'tool': 'AlphaFold',
            'version': self.config['alphafold_version'],
            'parameters': {
                'max_extra_seq': self.config['max_extra_seq'],
                'num_recycle': self.config['num_recycle'],
                'num_ensemble': self.config['num_ensemble']
            },
            'validation_status': 'IN_SILICO_ONLY',
            'input_file': f"{enzyme_name}_{mutation}.fasta",
            'output_files': []
        }
        
        return metadata
    
    def run_alphafold(self, fasta_file, author, use_colabfold=False):
        """Run AlphaFold structure prediction."""
        # Parse FASTA file
        sequences = self.parse_fasta(fasta_file)
        
        if not sequences:
            logger.error("No sequences found in FASTA file")
            return False
        
        # Extract enzyme name and mutation from filename
        fasta_path = Path(fasta_file)
        filename = fasta_path.stem
        parts = filename.split('_')
        
        if len(parts) < 2:
            logger.error("Filename should be in format: {enzyme}_{mutation}.fasta")
            return False
        
        enzyme_name = parts[0]
        mutation = '_'.join(parts[1:])
        
        # Generate metadata
        sequence = list(sequences.values())[0]  # Use first sequence
        metadata = self.generate_metadata(enzyme_name, mutation, sequence, author)
        
        # Create output directory
        output_dir = Path(self.config['output_dir']) / f"{enzyme_name}_{mutation}_{datetime.now().strftime('%Y-%m-%d')}"
        output_dir.mkdir(parents=True, exist_ok=True)
        
        if use_colabfold:
            return self.run_colabfold(fasta_file, output_dir, metadata)
        else:
            return self.run_local_alphafold(fasta_file, output_dir, metadata)
    
    def run_colabfold(self, fasta_file, output_dir, metadata):
        """Run ColabFold (cloud-based AlphaFold)."""
        logger.info("Using ColabFold for structure prediction")
        
        # Create ColabFold command
        cmd = [
            'python', '-m', 'colabfold.batch',
            fasta_file,
            str(output_dir),
            '--num-recycle', str(self.config['num_recycle']),
            '--num-ensemble', str(self.config['num_ensemble'])
        ]
        
        try:
            logger.info(f"Running ColabFold: {' '.join(cmd)}")
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            logger.info("ColabFold completed successfully")
            
            # Update metadata with output files
            self.update_metadata_with_outputs(output_dir, metadata)
            
            # Save metadata
            self.save_metadata(metadata, output_dir)
            
            return True
            
        except subprocess.CalledProcessError as e:
            logger.error(f"ColabFold failed: {e}")
            logger.error(f"Error output: {e.stderr}")
            return False
    
    def run_local_alphafold(self, fasta_file, output_dir, metadata):
        """Run local AlphaFold installation."""
        logger.info("Using local AlphaFold for structure prediction")
        
        # Create AlphaFold command
        cmd = [
            'python', '-m', 'alphafold.run_alphafold',
            '--fasta_paths', fasta_file,
            '--output_dir', str(output_dir),
            '--max_extra_seq', str(self.config['max_extra_seq']),
            '--num_recycle', str(self.config['num_recycle']),
            '--num_ensemble', str(self.config['num_ensemble'])
        ]
        
        # Add database paths if configured
        if 'data_dir' in self.config:
            cmd.extend(['--data_dir', self.config['data_dir']])
        
        try:
            logger.info(f"Running AlphaFold: {' '.join(cmd)}")
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            logger.info("AlphaFold completed successfully")
            
            # Update metadata with output files
            self.update_metadata_with_outputs(output_dir, metadata)
            
            # Save metadata
            self.save_metadata(metadata, output_dir)
            
            return True
            
        except subprocess.CalledProcessError as e:
            logger.error(f"AlphaFold failed: {e}")
            logger.error(f"Error output: {e.stderr}")
            return False
    
    def update_metadata_with_outputs(self, output_dir, metadata):
        """Update metadata with generated output files."""
        output_files = []
        
        # Look for PDB files
        for pdb_file in output_dir.glob("*.pdb"):
            output_files.append(str(pdb_file))
        
        # Look for JSON files
        for json_file in output_dir.glob("*.json"):
            output_files.append(str(json_file))
        
        metadata['output_files'] = output_files
        metadata['output_directory'] = str(output_dir)
    
    def save_metadata(self, metadata, output_dir):
        """Save metadata to file."""
        metadata_file = output_dir / "metadata.yaml"
        
        with open(metadata_file, 'w') as f:
            yaml.dump(metadata, f, default_flow_style=False)
        
        logger.info(f"Metadata saved to {metadata_file}")
    
    def create_design_note(self, metadata):
        """Create design note file."""
        design_note_file = Path(self.config['design_notes_dir']) / f"{metadata['experiment_id']}_design.yaml"
        
        design_note = {
            'experiment_id': metadata['experiment_id'],
            'date': metadata['date'],
            'author': metadata['author'],
            'enzyme_name': metadata['enzyme_name'],
            'mutation': metadata['mutation'],
            'design_rationale': 'To be filled by researcher',
            'target_properties': ['stability', 'activity'],
            'tools_used': ['AlphaFold'],
            'status': 'IN_SILICO_ONLY',
            'next_steps': [
                'Validate structure quality',
                'Run Rosetta refinement',
                'Visualize in ChimeraX/PyMOL',
                'Consider experimental validation'
            ]
        }
        
        with open(design_note_file, 'w') as f:
            yaml.dump(design_note, f, default_flow_style=False)
        
        logger.info(f"Design note created: {design_note_file}")

def main():
    parser = argparse.ArgumentParser(description='Run AlphaFold structure prediction')
    parser.add_argument('fasta_file', help='Input FASTA file')
    parser.add_argument('--author', required=True, help='Author name')
    parser.add_argument('--config', help='Configuration file (YAML)')
    parser.add_argument('--colabfold', action='store_true', help='Use ColabFold instead of local AlphaFold')
    
    args = parser.parse_args()
    
    # Check if FASTA file exists
    if not os.path.exists(args.fasta_file):
        logger.error(f"FASTA file not found: {args.fasta_file}")
        sys.exit(1)
    
    # Initialize runner
    runner = AlphaFoldRunner(args.config)
    
    # Run prediction
    success = runner.run_alphafold(args.fasta_file, args.author, args.colabfold)
    
    if success:
        logger.info("Structure prediction completed successfully!")
        logger.info("Next steps:")
        logger.info("1. Check output files in models/ directory")
        logger.info("2. Validate structure quality")
        logger.info("3. Run Rosetta refinement if needed")
        logger.info("4. Visualize in ChimeraX/PyMOL")
    else:
        logger.error("Structure prediction failed!")
        sys.exit(1)

if __name__ == "__main__":
    main() 