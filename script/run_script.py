import merge_file as merge_file
from build_css import filter_to_css
from build_html import write_html_to_file

mainGroup= [
    "gold.filter",
    "uncut_gems.filter",
    "scroll_of_wisdom.filter",
    "salvage.filter",
    "amulets.filter",
    "belts.filter",
    "jewel.filter",
    "key.filter",
    "relics.filter",
    "ring.filter",
    "rune_charms.filter",
    "soul_core.filter",
    "waystones.filter",
    "flasks.filter",

    #----------------------
    # Currency group
    #---------------------- 
    
    "currency.filter",

    #----------------------
    # Rarity group
    #----------------------

    "rarity_magic.filter",
    "rarity_rare.filter",
    "rarity_unique.filter",

]

#----------------------
# merge all filter
#----------------------
output_file_name = 'dzx-poe2'
merge_file.merge_files_from_array(mainGroup, output_file_name)


#----------------------
# merge all filter
#----------------------
output_file_name = 'dzx-poe2-PS5'
merge_file.merge_files_from_array(mainGroup, output_file_name , True)


#----------------------
# create css file
filter_to_css(mainGroup, "filter_styles.css")
#----------------------

#----------------------
# create html preview
write_html_to_file(mainGroup, "index.html")
#----------------------
