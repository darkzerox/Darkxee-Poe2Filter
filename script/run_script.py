import merge_file as merge_file
import os

mainGroup= [
    #----------------------
    # show items
    #----------------------
    "show/scroll_of_wisdom.filter",
    "show/salvage.filter",
    "show/gold.filter",
    "show/currency.filter",

    "show/amulets.filter",
    "show/belts.filter",
    "show/gems.filter",
    "show/jewel.filter",
    "show/key.filter",
    "show/relics.filter",
    "show/ring.filter",
    "show/rune_charms.filter",
    "show/soul_core.filter",
    "show/waystones.filter",

    "show/rarity_magic.filter",
    "show/rarity_rare.filter",
    "show/rarity_unique.filter",
]

#----------------------
# hide blue white
# for hight LV.!!
#----------------------
hideBlueWhiteGroupFile = [
    # "hide/rarity_rare.filter",
    "hide/rarity_magic.filter",
    "hide/rarity_normal.filter",
    "hide/scroll_of_wisdom.filter",
]
output_file_name = 'dzx-hide-blue-white'
merge_file.merge_files_from_array(hideBlueWhiteGroupFile+mainGroup, output_file_name)


#----------------------
# hide white
#----------------------
hideWhiteGroupFile = [
    "hide/rarity_normal.filter",
    "hide/scroll_of_wisdom.filter",
]
output_file_name = 'dzx-hide-white'
merge_file.merge_files_from_array(hideWhiteGroupFile+mainGroup, output_file_name)


#----------------------
# no hide
#----------------------
output_file_name = 'dzx'
merge_file.merge_files_from_array(mainGroup, output_file_name)
