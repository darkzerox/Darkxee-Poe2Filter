#!/usr/bin/env python3
"""
DZX Filter Build System
======================

Main build script for generating Path of Exile 2 filter files.
This script merges individual filter components into complete filter files
for different platforms and configurations.

Author: Darkxee
License: MIT
"""

import sys
import os
import time
import argparse
import json
from pathlib import Path
from typing import List, Dict, Optional

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    import merge_file
    from build_css import filter_to_css
    from build_html import write_html_to_file
except ImportError as e:
    print(f"❌ Error importing required modules: {e}")
    print("Please ensure all required Python files are present in the script directory.")
    sys.exit(1)

# ==============================================================================
# CONFIGURATION
# ==============================================================================

def load_config() -> Dict:
    """Load configuration from config.json"""
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    config_path = project_root / "config.json"
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        print(f"✅ Configuration loaded from {config_path}")
        return config
    except FileNotFoundError:
        print(f"⚠️ Config file not found at {config_path}, using default configuration")
        return get_default_config()
    except json.JSONDecodeError as e:
        print(f"❌ Error parsing config.json: {e}")
        print("Using default configuration")
        return get_default_config()

def get_default_config() -> Dict:
    """Get default configuration if config.json is not available"""
    return {
        "sound_effects": {"available_types": ["type-01"], "default_type": "type-01"},
        "filter_groups": {
            "MAIN_GROUP": [
                "gacha.filter", "crafting.filter", "gold.filter", "uncut_gems.filter", 
                "scroll_of_wisdom.filter", "salvage.filter", "amulets.filter", "belts.filter", 
                "jewel.filter", "ring.filter", "key.filter", "relics.filter", "rune.filter", 
                "talisman.filter", "soul_core.filter", "waystones.filter", "flasks.filter", 
                "charms.filter", "currency.filter", "rarity_unique.filter", 
                "rarity_rare.filter", "rarity_magic.filter"
            ],
            "BREACH_GROUP": [
                "gacha.filter", "crafting.filter", "gold.filter", "amulets.filter", 
                "jewel.filter", "ring.filter", "map_breach.filter", "uncut_gems.filter", 
                "scroll_of_wisdom.filter", "salvage.filter", "belts.filter", "key.filter", 
                "relics.filter", "rune.filter", "talisman.filter", "soul_core.filter", 
                "waystones.filter", "flasks.filter", "charms.filter", "currency.filter", 
                "rarity_unique.filter", "rarity_rare.filter", "rarity_magic.filter"
            ]
        },
        "filter_variants": [
            {"name": "dzx-poe2", "description": "Main filter", "group": "MAIN_GROUP", 
             "platforms": ["pc"], "no_hide_variant": True},
            {"name": "dzx-poe2-breach", "description": "Breach optimized", "group": "BREACH_GROUP", 
             "platforms": ["pc", "ps5"], "no_hide_variant": False},
            {"name": "dzx-poe2-PS5", "description": "PS5 version", "group": "MAIN_GROUP", 
             "platforms": ["ps5"], "no_hide_variant": True}
        ]
    }

# Load configuration
CONFIG = load_config()

# Extract values from config for backwards compatibility
SOUND_EFFECT_TYPES = CONFIG.get("sound_effects", {}).get("available_types", ["type-01"])

# Get filter groups from config
MAIN_GROUP = CONFIG.get("filter_groups", {}).get("MAIN_GROUP", [])
BREACH_GROUP = CONFIG.get("filter_groups", {}).get("BREACH_GROUP", [])

# Get filter variants from config
def get_filter_variants():
    """Get filter variants from config, converting group names to actual groups"""
    variants = []
    for variant_config in CONFIG.get("filter_variants", []):
        if not variant_config.get("enabled", True):
            continue
            
        variant = variant_config.copy()
        
        # Convert group name to actual group
        group_name = variant.get("group", "MAIN_GROUP")
        if group_name == "MAIN_GROUP":
            variant["group"] = MAIN_GROUP
        elif group_name == "BREACH_GROUP":
            variant["group"] = BREACH_GROUP
        else:
            # If it's already a list, keep it as is
            if isinstance(group_name, list):
                variant["group"] = group_name
            else:
                print(f"⚠️ Unknown group '{group_name}', using MAIN_GROUP")
                variant["group"] = MAIN_GROUP
        
        # Set default sound type if not specified
        if "sound_type" not in variant:
            variant["sound_type"] = CONFIG.get("sound_effects", {}).get("default_type", "type-01")
            
        variants.append(variant)
    
    return variants

FILTER_VARIANTS = get_filter_variants()

# ==============================================================================
# UTILITY FUNCTIONS
# ==============================================================================

def print_banner():
    """Print a nice banner for the build system"""
    banner = """
    ╔═══════════════════════════════════════════════════════════════╗
    ║                     DZX Filter Build System                   ║
    ║                   Path of Exile 2 Item Filters               ║
    ╚═══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def print_step(step: str, description: str):
    """Print a build step with formatting"""
    print(f"\n🔨 {step}: {description}")
    print("─" * 60)

def print_success(message: str):
    """Print success message"""
    print(f"✅ {message}")

def print_error(message: str):
    """Print error message"""
    print(f"❌ {message}")

def print_warning(message: str):
    """Print warning message"""
    print(f"⚠️  {message}")

def validate_filter_files(group: List[str]) -> List[str]:
    """Validate that all filter files exist"""
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    filter_group_path = project_root / "dzx_filter" / "filter_group"
    
    missing_files = []
    for filter_file in group:
        filter_path = filter_group_path / filter_file
        if not filter_path.exists():
            missing_files.append(str(filter_path))
    
    return missing_files

# ==============================================================================
# BUILD FUNCTIONS  
# ==============================================================================

def build_filter_variant(variant: Dict, args: argparse.Namespace) -> bool:
    """Build a specific filter variant"""
    name = variant['name']
    description = variant['description']
    group = variant['group']
    sound_type = variant['sound_type']
    platforms = variant['platforms']
    no_hide_variant = variant.get('no_hide_variant', False)
    
    print(f"\n📦 Building variant: {name}")
    print(f"   Description: {description}")
    print(f"   Platforms: {', '.join(platforms)}")
    print(f"   Files: {len(group)} filter components")
    
    success_count = 0
    total_builds = 0
    
    # Build for each platform
    for platform in platforms:
        is_ps5 = platform == 'ps5'
        
        # Main variant
        output_name = f"{name}" if not is_ps5 or 'PS5' in name else f"{name}-PS5"
        total_builds += 1
        
        print(f"   Building {output_name}.filter...")
        try:
            if merge_file.merge_files_from_array(
                group, output_name, sound_type, 
                removeSoundEffect=is_ps5, hideItem=False
            ):
                success_count += 1
                print(f"   ✅ {output_name}.filter created successfully")
            else:
                print_error(f"Failed to create {output_name}.filter")
        except Exception as e:
            print_error(f"Error building {output_name}.filter: {e}")
        
        # No-hide variant (if enabled)
        if no_hide_variant:
            no_hide_name = f"{output_name}-no-hide" 
            total_builds += 1
            
            print(f"   Building {no_hide_name}.filter...")
            try:
                if merge_file.merge_files_from_array(
                    group, no_hide_name, sound_type,
                    removeSoundEffect=is_ps5, hideItem=True
                ):
                    success_count += 1
                    print(f"   ✅ {no_hide_name}.filter created successfully")
                else:
                    print_error(f"Failed to create {no_hide_name}.filter")
            except Exception as e:
                print_error(f"Error building {no_hide_name}.filter: {e}")
    
    return success_count == total_builds

def build_special_variants(args: argparse.Namespace) -> bool:
    """Build special filter variants from config"""
    print_step("Building Special Variants", "Creating specialized filters")
    
    special_variants = CONFIG.get("special_variants", [])
    if not special_variants:
        print("   No special variants configured")
        return True
    
    success_count = 0
    total_builds = len([v for v in special_variants if v.get("enabled", True)])
    
    for variant in special_variants:
        if not variant.get("enabled", True):
            continue
            
        name = variant.get("name", "unknown")
        description = variant.get("description", "")
        group_raw = variant.get("group", "MAIN_GROUP")
        remove_sounds = variant.get("remove_sounds", False)
        hide_items = variant.get("hide_items", False)
        sound_type = variant.get("sound_type", CONFIG.get("sound_effects", {}).get("default_type", "type-01"))
        
        # Convert group name to actual group
        if isinstance(group_raw, str):
            if group_raw == "MAIN_GROUP":
                group = MAIN_GROUP
            elif group_raw == "BREACH_GROUP":
                group = BREACH_GROUP
            else:
                print(f"      ⚠️ Unknown group '{group_raw}', using MAIN_GROUP")
                group = MAIN_GROUP
        elif isinstance(group_raw, list):
            group = group_raw
        else:
            group = MAIN_GROUP
        
        print(f"   Building {name}.filter...")
        print(f"      {description}")
        
        try:
            if merge_file.merge_files_from_array(
                group, name, sound_type,
                removeSoundEffect=remove_sounds, 
                hideItem=hide_items
            ):
                success_count += 1
                print(f"   ✅ {name}.filter created successfully")
            else:
                print_error(f"Failed to create {name}.filter")
        except Exception as e:
            print_error(f"Error building {name} variant: {e}")
    
    return success_count == total_builds

def build_css_and_html(args: argparse.Namespace) -> bool:
    """Build CSS styles and HTML preview"""
    success = True
    
    if not args.skip_css:
        print_step("Building CSS", "Generating filter styles")
        try:
            filter_to_css(MAIN_GROUP, "filter_styles.css")
            print_success("CSS file generated successfully")
        except Exception as e:
            print_error(f"Error generating CSS: {e}")
            success = False
    
    if not args.skip_html:
        print_step("Building HTML Preview", "Generating web preview")
        try:
            if write_html_to_file(MAIN_GROUP, "index.html"):
                print_success("HTML preview generated successfully")
            else:
                print_error("Failed to generate HTML preview")
                success = False
        except Exception as e:
            print_error(f"Error generating HTML: {e}")
            success = False
    
    return success

def main():
    """Main build function"""
    parser = argparse.ArgumentParser(
        description="DZX Filter Build System - Generate Path of Exile 2 item filters",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python start_build.py                    # Build all filters
  python start_build.py --skip-css         # Skip CSS generation
  python start_build.py --skip-html        # Skip HTML preview
  python start_build.py --validate-only    # Only validate filter files
        """
    )
    
    parser.add_argument('--skip-css', action='store_true',
                       help='Skip CSS generation')
    parser.add_argument('--skip-html', action='store_true', 
                       help='Skip HTML preview generation')
    parser.add_argument('--validate-only', action='store_true',
                       help='Only validate filter files, do not build')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Enable verbose output')
    
    args = parser.parse_args()
    
    # Print banner
    print_banner()
    
    start_time = time.time()
    
    # Validate filter files
    print_step("Validation", "Checking filter files")
    all_files = list(set(MAIN_GROUP + BREACH_GROUP))  # Remove duplicates
    missing_files = validate_filter_files(all_files)
    
    if missing_files:
        print_error("Missing filter files:")
        for file in missing_files:
            print(f"   - {file}")
        return 1
    else:
        print_success(f"All {len(all_files)} filter files found")
    
    if args.validate_only:
        print("\n🎉 Validation complete - all files present!")
        return 0
    
    # Build all variants
    print_step("Building Filter Variants", f"Creating {len(FILTER_VARIANTS)} variants")
    
    total_success = 0
    for variant in FILTER_VARIANTS:
        if build_filter_variant(variant, args):
            total_success += 1
    
    # Build special variants
    special_success = build_special_variants(args)
    
    # Build CSS and HTML
    web_success = build_css_and_html(args)
    
    # Summary
    end_time = time.time()
    duration = end_time - start_time
    
    print(f"\n{'='*60}")
    print("📊 BUILD SUMMARY")
    print(f"{'='*60}")
    print(f"✅ Filter variants built: {total_success}/{len(FILTER_VARIANTS)}")
    print(f"✅ Special variants: {'Success' if special_success else 'Failed'}")
    print(f"✅ Web assets: {'Success' if web_success else 'Failed'}")
    print(f"⏱️  Build time: {duration:.2f} seconds")
    
    if total_success == len(FILTER_VARIANTS) and special_success and web_success:
        print("\n🎉 All builds completed successfully!")
        return 0
    else:
        print(f"\n⚠️  Some builds failed. Check the output above for details.")
        return 1

# ==============================================================================
# ENTRY POINT
# ==============================================================================

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n⚠️ Build cancelled by user")
        sys.exit(130)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        if '--verbose' in sys.argv or '-v' in sys.argv:
            import traceback
            traceback.print_exc()
        sys.exit(1)
