#!/usr/bin/env python3
"""
DZX Filter Merge Module
======================

This module handles merging individual filter files into complete filter configurations
for Path of Exile 2. It supports various platform configurations and processing options.

Author: Darkxee
License: MIT
"""

import os
import sys
from pathlib import Path
from typing import List, Optional, Union
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Path configuration
script_dir = Path(__file__).parent
project_path = script_dir.parent
filter_group_path = project_path / "dzx_filter" / "filter_group"

class FilterMerger:
    """Handle merging of filter files with various processing options"""
    
    def __init__(self, project_path: Path, filter_group_path: Path):
        self.project_path = project_path
        self.filter_group_path = filter_group_path
        self.stats = {
            'files_processed': 0,
            'files_missing': 0,
            'lines_processed': 0,
            'sounds_removed': 0,
            'hide_to_show_converted': 0
        }
    
    def _process_sound_effects(self, content: str, effect_type: str, remove_sound: bool = False) -> str:
        """Process sound effect lines in filter content"""
        if not content:
            return content
            
        lines = content.split('\n')
        processed_lines = []
        
        for line in lines:
            if 'CustomAlertSound' in line:
                if remove_sound:
                    # Skip this line (remove sound effect)
                    self.stats['sounds_removed'] += 1
                    continue
                elif 'dzx_filter/soundeffect/type-01/' in line:
                    # Replace sound effect type
                    line = line.replace('dzx_filter/soundeffect/type-01/', 
                                      f'dzx_filter/soundeffect/{effect_type}/')
            
            processed_lines.append(line)
        
        return '\n'.join(processed_lines)
    
    def _process_hide_items(self, content: str, hide_to_show: bool = False) -> str:
        """Process Hide/Show directives in filter content"""
        if not content or not hide_to_show:
            return content
            
        lines = content.split('\n')
        processed_lines = []
        
        for line in lines:
            if line.strip() == 'Hide':
                processed_lines.append('Show')
                self.stats['hide_to_show_converted'] += 1
            else:
                processed_lines.append(line)
        
        return '\n'.join(processed_lines)
    
    def _validate_filter_file(self, file_path: Path) -> bool:
        """Validate that a filter file exists and is readable"""
        if not file_path.exists():
            logger.warning(f"Filter file not found: {file_path}")
            self.stats['files_missing'] += 1
            return False
            
        if not file_path.is_file():
            logger.warning(f"Path is not a file: {file_path}")
            self.stats['files_missing'] += 1
            return False
            
        try:
            # Try to read a small portion to verify it's readable
            with open(file_path, 'r', encoding='utf-8') as f:
                f.read(100)
            return True
        except (IOError, UnicodeDecodeError) as e:
            logger.warning(f"Cannot read filter file {file_path}: {e}")
            self.stats['files_missing'] += 1
            return False
    
    def _read_filter_file(self, file_path: Path) -> Optional[str]:
        """Read and return the content of a filter file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                self.stats['lines_processed'] += len(content.split('\n'))
                return content
        except Exception as e:
            logger.error(f"Error reading file {file_path}: {e}")
            return None
    
    def merge_files(self, 
                   file_paths: List[str], 
                   output_file_name: str,
                   effect_type: str = 'type-01',
                   remove_sound_effect: bool = False,
                   hide_to_show: bool = False) -> bool:
        """
        Merge multiple filter files into a single output file
        
        Args:
            file_paths: List of filter file names to merge
            output_file_name: Name of output file (without .filter extension)
            effect_type: Sound effect type to use
            remove_sound_effect: Whether to remove all sound effects
            hide_to_show: Whether to convert Hide directives to Show
            
        Returns:
            bool: True if merge was successful, False otherwise
        """
        
        # Reset stats
        self.stats = {
            'files_processed': 0,
            'files_missing': 0, 
            'lines_processed': 0,
            'sounds_removed': 0,
            'hide_to_show_converted': 0
        }
        
        output_file = self.project_path / f"{output_file_name}.filter"
        
        logger.info(f"Starting merge: {len(file_paths)} files -> {output_file.name}")
        
        try:
            with open(output_file, 'w', encoding='utf-8') as outfile:
                # Write header comment
                header = f"""# DZX Filter for Path of Exile 2
# Generated filter file: {output_file_name}
# Sound Effect Type: {effect_type}
# Remove Sounds: {remove_sound_effect}
# Show Hidden Items: {hide_to_show}
# Components: {len(file_paths)} files
# 
# Generated by DZX Filter Build System
# https://github.com/darkzerox/Darkxee-Poe2Filter

"""
                outfile.write(header)
                
                for file_path in file_paths:
                    # Clean up file path
                    file_path = str(file_path).lstrip(os.sep)
                    full_path = self.filter_group_path / file_path
                    
                    # Validate file
                    if not self._validate_filter_file(full_path):
                        continue
                    
                    # Read file content
                    content = self._read_filter_file(full_path)
                    if content is None:
                        continue
                    
                    # Process content
                    content = self._process_sound_effects(content, effect_type, remove_sound_effect)
                    content = self._process_hide_items(content, hide_to_show)
                    
                    # Write to output with section header
                    section_header = f"\n# ============================================\n# {file_path}\n# ============================================\n\n"
                    outfile.write(section_header)
                    outfile.write(content)
                    outfile.write('\n\n')
                    
                    self.stats['files_processed'] += 1
                    logger.debug(f"Processed: {file_path}")
                
                # Write footer
                footer = f"\n# End of filter file: {output_file_name}\n"
                outfile.write(footer)
            
            # Log results
            logger.info(f"Merge completed successfully: {output_file}")
            logger.info(f"Files processed: {self.stats['files_processed']}/{len(file_paths)}")
            if self.stats['files_missing'] > 0:
                logger.warning(f"Missing files: {self.stats['files_missing']}")
            if self.stats['sounds_removed'] > 0:
                logger.info(f"Sound effects removed: {self.stats['sounds_removed']}")
            if self.stats['hide_to_show_converted'] > 0:
                logger.info(f"Hide->Show conversions: {self.stats['hide_to_show_converted']}")
            
            return True
            
        except Exception as e:
            logger.error(f"Error during merge: {e}")
            return False
    
    def get_stats(self) -> dict:
        """Return merge statistics"""
        return self.stats.copy()

# Global merger instance
_merger = FilterMerger(project_path, filter_group_path)

def merge_files_from_array(file_paths: List[str], 
                          output_file_name: str,
                          effect_type: str = 'type-01', 
                          removeSoundEffect: bool = False, 
                          hideItem: bool = False) -> bool:
    """
    Legacy function for backward compatibility
    
    Args:
        file_paths: List of filter file names to merge
        output_file_name: Output file name (without .filter extension)  
        effect_type: Sound effect type to use
        removeSoundEffect: Whether to remove sound effects
        hideItem: Whether to convert Hide to Show
        
    Returns:
        bool: True if successful, False otherwise
    """
    return _merger.merge_files(
        file_paths=file_paths,
        output_file_name=output_file_name,
        effect_type=effect_type,
        remove_sound_effect=removeSoundEffect,
        hide_to_show=hideItem
    )

def run_tests():
    """Run basic tests of the merge functionality"""
    print("🧪 Running merge_file tests...")
    
    # Test files that should exist
    test_files = [
        "rarity_magic.filter",
        "rarity_rare.filter", 
        "currency.filter"
    ]
    
    # Clean up any existing test file
    test_output = project_path / "test_merge.filter"
    if test_output.exists():
        try:
            test_output.unlink()
            print("   Cleaned up previous test file")
        except Exception as e:
            print(f"   Warning: Could not remove previous test file: {e}")
    
    # Test 1: Basic merge
    print("\n   Test 1: Basic merge")
    success = merge_files_from_array(test_files, "test_merge")
    if success:
        print("   ✅ Basic merge test passed")
    else:
        print("   ❌ Basic merge test failed")
        return False
    
    # Test 2: Merge with sound removal
    print("\n   Test 2: Merge with sound removal")
    success = merge_files_from_array(test_files, "test_merge_no_sound", 
                                   removeSoundEffect=True)
    if success:
        print("   ✅ Sound removal test passed")
    else:
        print("   ❌ Sound removal test failed")
        return False
    
    # Test 3: Merge with hide->show conversion
    print("\n   Test 3: Merge with hide->show conversion")
    success = merge_files_from_array(test_files, "test_merge_show_all",
                                   hideItem=True)
    if success:
        print("   ✅ Hide->Show conversion test passed")
    else:
        print("   ❌ Hide->Show conversion test failed")
        return False
    
    # Clean up test files
    for test_file in ["test_merge.filter", "test_merge_no_sound.filter", "test_merge_show_all.filter"]:
        test_path = project_path / test_file
        if test_path.exists():
            try:
                test_path.unlink()
                print(f"   Cleaned up {test_file}")
            except Exception as e:
                print(f"   Warning: Could not clean up {test_file}: {e}")
    
    print("\n🎉 All merge tests passed!")
    return True

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="DZX Filter Merge Module")
    parser.add_argument('--test', action='store_true', help='Run tests')
    parser.add_argument('--merge', nargs='+', help='Merge specific files')
    parser.add_argument('--output', default='manual_merge', help='Output file name')
    parser.add_argument('--no-sound', action='store_true', help='Remove sound effects')
    parser.add_argument('--show-all', action='store_true', help='Convert Hide to Show')
    
    args = parser.parse_args()
    
    if args.test:
        run_tests()
    elif args.merge:
        print(f"Merging files: {args.merge}")
        success = merge_files_from_array(
            args.merge, 
            args.output,
            removeSoundEffect=args.no_sound,
            hideItem=args.show_all
        )
        if success:
            print(f"✅ Merge completed: {args.output}.filter")
        else:
            print("❌ Merge failed")
            sys.exit(1)
    else:
        print("Use --test to run tests or --merge to merge files")
        parser.print_help()
