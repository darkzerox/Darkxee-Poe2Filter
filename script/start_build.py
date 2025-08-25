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

# Available sound effect types
SOUND_EFFECT_TYPES = ['type-01']

# Main filter group - core filters for regular gameplay
MAIN_GROUP = [
    # Gacha/Crafting Items
    "gacha.filter",
    "crafting.filter",
    
    # Essential Items
    "gold.filter",
    "uncut_gems.filter", 
    "scroll_of_wisdom.filter",
    "salvage.filter",
    
    # Equipment
    "amulets.filter",
    "belts.filter", 
    "jewel.filter",
    "ring.filter",
    
    # Special Items
    "key.filter",
    "relics.filter", 
    "rune.filter",
    "talisman.filter",
    "soul_core.filter",
    "waystones.filter",
    "flasks.filter",
    "charms.filter",
    
    # Currency
    "currency.filter",
    
    # Rarity-based filters (order matters - most specific first)
    "rarity_unique.filter", 
    "rarity_rare.filter",
    "rarity_magic.filter",
]

# Breach-specific filter group - optimized for Breach league content
BREACH_GROUP = [
    # High priority items for Breach
    "gacha.filter",
    "crafting.filter", 
    "gold.filter",
    "amulets.filter",
    "jewel.filter", 
    "ring.filter",
    
    # Breach-specific content
    "map_breach.filter",
    
    # Standard items (lower priority in Breach)
    "uncut_gems.filter",
    "scroll_of_wisdom.filter",
    "salvage.filter",
    "belts.filter",
    "key.filter", 
    "relics.filter",
    "rune.filter",
    "talisman.filter",
    "soul_core.filter", 
    "waystones.filter",
    "flasks.filter",
    "charms.filter",
    
    # Currency  
    "currency.filter",
    
    # Rarity filters
    "rarity_unique.filter",
    "rarity_rare.filter", 
    "rarity_magic.filter",
]

# Filter variants configuration
FILTER_VARIANTS = [
    {
        'name': 'dzx-poe2',
        'description': 'Main filter with all features',
        'group': MAIN_GROUP,
        'sound_type': 'type-01',
        'platforms': ['pc'],
        'no_hide_variant': True,
    },
    {
        'name': 'dzx-poe2-breach', 
        'description': 'Optimized for Breach league',
        'group': BREACH_GROUP,
        'sound_type': 'type-01',
        'platforms': ['pc', 'ps5'],
        'no_hide_variant': False,
    },
    {
        'name': 'dzx-poe2-PS5',
        'description': 'PS5 optimized version', 
        'group': MAIN_GROUP,
        'sound_type': 'type-01',
        'platforms': ['ps5'],
        'no_hide_variant': True,
    },
]

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
    """Build special filter variants (color-only, divine-mirror)"""
    print_step("Building Special Variants", "Creating specialized filters")
    
    success_count = 0
    total_builds = 0
    
    # Color-Only variant (PC only, no sounds)
    print("   Building dzx-poe2-Color-Only.filter...")
    total_builds += 1
    try:
        if merge_file.merge_files_from_array(
            MAIN_GROUP, "dzx-poe2-Color-Only", 'type-01',
            removeSoundEffect=True, hideItem=False
        ):
            success_count += 1
            print("   ✅ dzx-poe2-Color-Only.filter created successfully")
        else:
            print_error("Failed to create dzx-poe2-Color-Only.filter")
    except Exception as e:
        print_error(f"Error building Color-Only variant: {e}")
    
    # Divine-Mirror variant (high-value items only)
    divine_mirror_group = [
        "currency.filter",
        "rarity_unique.filter",
        "gacha.filter",
        "key.filter",
        "waystones.filter"
    ]
    
    print("   Building dzx-poe2-Divine-Mirror.filter...")
    total_builds += 1
    try:
        if merge_file.merge_files_from_array(
            divine_mirror_group, "dzx-poe2-Divine-Mirror", 'type-01',
            removeSoundEffect=False, hideItem=False
        ):
            success_count += 1
            print("   ✅ dzx-poe2-Divine-Mirror.filter created successfully")
        else:
            print_error("Failed to create dzx-poe2-Divine-Mirror.filter")
    except Exception as e:
        print_error(f"Error building Divine-Mirror variant: {e}")
    
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
