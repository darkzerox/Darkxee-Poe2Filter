import merge_file as merge_file

mainGroup= [
    #----------------------
    # show items
    #----------------------
    "rarity_magic.filter",
    "rarity_rare.filter",
    "rarity_unique.filter",

    "scroll_of_wisdom.filter",
    "salvage.filter",
    "gold.filter",
    "currency.filter",

    "amulets.filter",
    "belts.filter",
    "gems.filter",
    "jewel.filter",
    "key.filter",
    "relics.filter",
    "ring.filter",
    "rune_charms.filter",
    "soul_core.filter",
    "waystones.filter",


]

#----------------------
# hide All rare blue white
# for hight LV.!!!!
#----------------------
hideHeightLVGroupFile = [
    "hide_scroll_of_wisdom.filter",
    "hide_rarity_heightLV.filter",
    "hide_rarity_rare.filter",
    "hide_rarity_magic.filter",
]
output_file_name = 'dzx-for-hight-lv'
merge_file.merge_files_from_array(mainGroup+hideHeightLVGroupFile, output_file_name)


#----------------------
# hide blue white
# for hight LV.!!
#----------------------
hideBlueWhiteGroupFile = [
    "hide_scroll_of_wisdom.filter",
    "hide_rarity_magic.filter",
]
output_file_name = 'dzx-hide-blue-white'
merge_file.merge_files_from_array(mainGroup+hideBlueWhiteGroupFile, output_file_name)


#----------------------
# hide white
#----------------------
hideWhiteGroupFile = [
    "hide_scroll_of_wisdom.filter",
    "hide_rarity_normal.filter",
]
output_file_name = 'dzx-hide-white'
merge_file.merge_files_from_array(mainGroup+hideWhiteGroupFile, output_file_name)


#----------------------
# no hide
#----------------------
output_file_name = 'dzx'
merge_file.merge_files_from_array(mainGroup, output_file_name)
