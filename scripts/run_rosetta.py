#!/usr/bin/env python3
"""
Rosetta Protein Engineering Script
Automates Rosetta protocols with metadata tracking for the enzyme design workflow.
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

class RosettaRunner:
    def __init__(self, config_file=None):
        """Initialize Rosetta runner with configuration."""
        self.config = self.load_config(config_file)
        self.setup_directories()
        
    def load_config(self, config_file):
        """Load configuration from file or use defaults."""
        default_config = {
            'rosetta_version': '2021.16',
            'score_function': 'ref2015',
            'protocol': 'FastRelax',
            'iterations': 5,
            'output_dir': 'models',
            'design_notes_dir': 'design_notes',
            'scripts_dir': 'scripts/rosetta_scripts'
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
            self.config['scripts_dir']
        ]
        
        for dir_path in dirs:
            Path(dir_path).mkdir(parents=True, exist_ok=True)
    
    def generate_metadata(self, enzyme_name, mutation, protocol, author):
        """Generate metadata for the experiment."""
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        
        metadata = {
            'experiment_id': f"{enzyme_name}_{mutation}_{datetime.now().strftime('%Y-%m-%d')}",
            'date': datetime.now().strftime("%Y-%m-%d"),
            'timestamp': timestamp,
            'author': author,
            'enzyme_name': enzyme_name,
            'mutation': mutation,
            'tool': 'Rosetta',
            'version': self.config['rosetta_version'],
            'protocol': protocol,
            'parameters': {
                'score_function': self.config['score_function'],
                'iterations': self.config['iterations'],
                'protocol': protocol
            },
            'validation_status': 'IN_SILICO_ONLY',
            'output_files': []
        }
        
        return metadata
    
    def create_fastrelax_script(self, output_file):
        """Create FastRelax RosettaScript."""
        script_content = f"""<ROSETTASCRIPTS>
    <SCOREFXNS>
        <ScoreFunction name="{self.config['score_function']}" weights="{self.config['score_function']}"/>
    </SCOREFXNS>
    
    <TASKOPERATIONS>
        <RestrictToRepacking name="repack_only"/>
    </TASKOPERATIONS>
    
    <MOVERS>
        <FastRelax name="relax" scorefxn="{self.config['score_function']}" task_operations="repack_only" repeats="{self.config['iterations']}"/>
    </MOVERS>
    
    <PROTOCOLS>
        <Add mover="relax"/>
    </PROTOCOLS>
</ROSETTASCRIPTS>"""
        
        with open(output_file, 'w') as f:
            f.write(script_content)
        
        logger.info(f"Created FastRelax script: {output_file}")
    
    def create_mutation_script(self, output_file, mutation_spec):
        """Create mutation RosettaScript."""
        # Parse mutation specification (e.g., "238S>F" for S238F)
        if '>' in mutation_spec:
            position, mutation = mutation_spec.split('>')
            position = position[:-1]  # Remove the wild-type amino acid
            wild_type = mutation_spec[len(position)]
            mutant = mutation
        else:
            # Assume format like "S238F"
            import re
            match = re.match(r'([A-Z])(\d+)([A-Z])', mutation_spec)
            if match:
                wild_type, position, mutant = match.groups()
            else:
                logger.error(f"Invalid mutation format: {mutation_spec}")
                return False
        
        script_content = f"""<ROSETTASCRIPTS>
    <SCOREFXNS>
        <ScoreFunction name="{self.config['score_function']}" weights="{self.config['score_function']}"/>
    </SCOREFXNS>
    
    <TASKOPERATIONS>
        <OperateOnResidueSubset name="mutate_res" selector="residue_{position}">
            <MutateResidue target="{mutant}"/>
        </OperateOnResidueSubset>
    </TASKOPERATIONS>
    
    <MOVERS>
        <PackRotamersMover name="pack" scorefxn="{self.config['score_function']}" task_operations="mutate_res"/>
    </MOVERS>
    
    <PROTOCOLS>
        <Add mover="pack"/>
    </PROTOCOLS>
</ROSETTASCRIPTS>"""
        
        with open(output_file, 'w') as f:
            f.write(script_content)
        
        logger.info(f"Created mutation script: {output_file}")
        return True
    
    def run_rosetta(self, pdb_file, protocol, mutation_spec=None, author=None):
        """Run Rosetta protocol."""
        # Extract enzyme name and mutation from filename
        pdb_path = Path(pdb_file)
        filename = pdb_path.stem
        
        # Try to parse filename for enzyme and mutation info
        parts = filename.split('_')
        if len(parts) >= 2:
            enzyme_name = parts[0]
            mutation = '_'.join(parts[1:])
        else:
            enzyme_name = "unknown"
            mutation = "unknown"
        
        # Generate metadata
        metadata = self.generate_metadata(enzyme_name, mutation, protocol, author or "unknown")
        
        # Create output directory
        output_dir = Path(self.config['output_dir']) / f"{enzyme_name}_{mutation}_{datetime.now().strftime('%Y-%m-%d')}"
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Create RosettaScript
        script_file = output_dir / f"{protocol}.xml"
        
        if protocol == "FastRelax":
            self.create_fastrelax_script(script_file)
        elif protocol == "Mutation":
            if not mutation_spec:
                logger.error("Mutation specification required for Mutation protocol")
                return False
            if not self.create_mutation_script(script_file, mutation_spec):
                return False
        else:
            logger.error(f"Unknown protocol: {protocol}")
            return False
        
        # Run Rosetta
        return self.execute_rosetta(pdb_file, script_file, output_dir, metadata)
    
    def execute_rosetta(self, pdb_file, script_file, output_dir, metadata):
        """Execute Rosetta command."""
        # Create Rosetta command
        cmd = [
            'rosetta_scripts.default.linuxgccrelease',
            '-s', pdb_file,
            '-parser:protocol', str(script_file),
            '-out:path:all', str(output_dir),
            '-out:file:scorefile', f"{metadata['experiment_id']}_scores.sc",
            '-out:file:silent', f"{metadata['experiment_id']}_results.silent",
            '-out:file:silent_struct_type', 'binary',
            '-nstruct', '1'
        ]
        
        try:
            logger.info(f"Running Rosetta: {' '.join(cmd)}")
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            logger.info("Rosetta completed successfully")
            
            # Update metadata with output files
            self.update_metadata_with_outputs(output_dir, metadata)
            
            # Save metadata
            self.save_metadata(metadata, output_dir)
            
            # Parse energy scores
            self.parse_energy_scores(output_dir, metadata)
            
            return True
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Rosetta failed: {e}")
            logger.error(f"Error output: {e.stderr}")
            return False
    
    def update_metadata_with_outputs(self, output_dir, metadata):
        """Update metadata with generated output files."""
        output_files = []
        
        # Look for PDB files
        for pdb_file in output_dir.glob("*.pdb"):
            output_files.append(str(pdb_file))
        
        # Look for score files
        for score_file in output_dir.glob("*.sc"):
            output_files.append(str(score_file))
        
        # Look for silent files
        for silent_file in output_dir.glob("*.silent"):
            output_files.append(str(silent_file))
        
        metadata['output_files'] = output_files
        metadata['output_directory'] = str(output_dir)
    
    def parse_energy_scores(self, output_dir, metadata):
        """Parse energy scores from Rosetta output."""
        score_files = list(output_dir.glob("*.sc"))
        
        if not score_files:
            logger.warning("No score files found")
            return
        
        # Read the first score file
        score_file = score_files[0]
        
        try:
            with open(score_file, 'r') as f:
                lines = f.readlines()
            
            # Parse header and first data line
            if len(lines) >= 2:
                header = lines[0].strip().split()
                data = lines[1].strip().split()
                
                # Create score dictionary
                scores = {}
                for i, field in enumerate(header):
                    if i < len(data):
                        try:
                            scores[field] = float(data[i])
                        except ValueError:
                            scores[field] = data[i]
                
                metadata['energy_scores'] = scores
                logger.info(f"Energy scores parsed: {scores.get('total_score', 'N/A')}")
        
        except Exception as e:
            logger.error(f"Error parsing score file: {e}")
    
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
            'protocol': metadata['protocol'],
            'design_rationale': 'To be filled by researcher',
            'target_properties': ['stability', 'activity'],
            'tools_used': ['Rosetta'],
            'status': 'IN_SILICO_ONLY',
            'energy_scores': metadata.get('energy_scores', {}),
            'next_steps': [
                'Compare energy scores to wild-type',
                'Visualize structural changes',
                'Consider experimental validation',
                'Test additional mutations if needed'
            ]
        }
        
        with open(design_note_file, 'w') as f:
            yaml.dump(design_note, f, default_flow_style=False)
        
        logger.info(f"Design note created: {design_note_file}")

def main():
    parser = argparse.ArgumentParser(description='Run Rosetta protein engineering')
    parser.add_argument('pdb_file', help='Input PDB file')
    parser.add_argument('--protocol', required=True, choices=['FastRelax', 'Mutation'], 
                       help='Rosetta protocol to run')
    parser.add_argument('--mutation', help='Mutation specification (e.g., S238F or 238S>F)')
    parser.add_argument('--author', required=True, help='Author name')
    parser.add_argument('--config', help='Configuration file (YAML)')
    
    args = parser.parse_args()
    
    # Check if PDB file exists
    if not os.path.exists(args.pdb_file):
        logger.error(f"PDB file not found: {args.pdb_file}")
        sys.exit(1)
    
    # Check mutation specification for Mutation protocol
    if args.protocol == 'Mutation' and not args.mutation:
        logger.error("Mutation specification required for Mutation protocol")
        sys.exit(1)
    
    # Initialize runner
    runner = RosettaRunner(args.config)
    
    # Run Rosetta
    success = runner.run_rosetta(args.pdb_file, args.protocol, args.mutation, args.author)
    
    if success:
        logger.info("Rosetta analysis completed successfully!")
        logger.info("Next steps:")
        logger.info("1. Check output files in models/ directory")
        logger.info("2. Compare energy scores to wild-type")
        logger.info("3. Visualize structural changes in ChimeraX/PyMOL")
        logger.info("4. Consider experimental validation")
    else:
        logger.error("Rosetta analysis failed!")
        sys.exit(1)

if __name__ == "__main__":
    main() 