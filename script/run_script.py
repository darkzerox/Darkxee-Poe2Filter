import merge_file as merge_file
import os

mainGroup= [
    #----------------------
    # show items
    #----------------------
    "show/rarity_magic.filter",
    "show/rarity_rare.filter",
    "show/rarity_unique.filter",

    "show/amulets.filter",
    "show/belts.filter",
    "show/currency.filter",
    "show/gems.filter",
    "show/gold.filter",
    "show/jewel.filter",
    "show/key.filter",
    "show/relics.filter",
    "show/ring.filter",
    "show/rune_charms.filter",
    "show/salvage.filter",
    "show/scroll_of_wisdom.filter",
    "show/socketables.filter",
    "show/waystones.filter",
]

#----------------------
# hide blue white
# for hight LV.!!
#----------------------
hideBlueWhiteGroupFile = [
    "hide/scroll_of_wisdom.filter",
    "hide/rarity_normal.filter",
    "hide/rarity_magic.filter",
    "hide/rarity_rare.filter",
]
output_file_name = 'dzx-hide-blue-white'
merge_file.merge_files_from_array(hideBlueWhiteGroupFile+mainGroup, output_file_name)


#----------------------
# hide white
#----------------------
hideWhiteGroupFile = [
    "hide/scroll_of_wisdom.filter",
    "hide/rarity_normal.filter",
]
output_file_name = 'dzx-hide-white'
merge_file.merge_files_from_array(hideWhiteGroupFile+mainGroup, output_file_name)


#----------------------
# no hide
#----------------------
output_file_name = 'dzx'
merge_file.merge_files_from_array(mainGroup, output_file_name)
