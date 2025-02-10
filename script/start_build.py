import merge_file as merge_file
from build_css import filter_to_css
from build_html import write_html_to_file

soundEffectType = ['type-01']

mainGroup= [
    #----------------------
    # Gacha group
    #---------------------- 

    "gacha.filter",

    #----------------------
    # Item group
    #---------------------- 

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
    "charms.filter",

    #----------------------
    # Currency group
    #---------------------- 
    
    "currency.filter",

    #----------------------
    # Rarity group
    #----------------------
    
    "rarity_unique.filter",
    "rarity_rare.filter",
    "rarity_magic.filter",
]

breachGroup= [

    "gacha.filter",
    "amulets.filter",
    "jewel.filter",
    "ring.filter",

    "map_breach.filter",

    "uncut_gems.filter",
    "scroll_of_wisdom.filter",
    "salvage.filter",
    "belts.filter",
    "key.filter",
    "relics.filter",
    "rune_charms.filter",
    "soul_core.filter",
    "waystones.filter",
    "flasks.filter",
    "charms.filter",

    #----------------------
    # Currency group
    #---------------------- 
    
    "currency.filter",

    #----------------------
    # Rarity group
    #----------------------
    
    "rarity_unique.filter",
    "rarity_rare.filter",
    "rarity_magic.filter",
]

#----------------------
# merge all filter
#----------------------
for sound_type in soundEffectType:
    if sound_type == 'type-01': 
        output_file_name = f'dzx-poe2'
    else:
        output_file_name = f'dzx-poe2-{sound_type}'
    merge_file.merge_files_from_array(mainGroup, output_file_name ,sound_type)


#----------------------
# merge all filter - Show all items
#----------------------
for sound_type in soundEffectType:
    if sound_type == 'type-01': 
        output_file_name = 'dzx-poe2-no-hide'
    else:
        output_file_name = f'dzx-poe2-{sound_type}-no-hide'
    merge_file.merge_files_from_array(mainGroup, output_file_name,'type-01',False, True)

#----------------------
# For breach map
#----------------------
output_file_name = 'dzx-poe2-breach'
merge_file.merge_files_from_array(breachGroup, output_file_name ,'type-01')




#----------------------
# merge all filter for PS5
#----------------------
output_file_name = 'dzx-poe2-PS5'
merge_file.merge_files_from_array(mainGroup, output_file_name ,'type-01', True)


#----------------------
# merge all filter for PS5 - Show all items
#----------------------
output_file_name = 'dzx-poe2-PS5-no-hide'
merge_file.merge_files_from_array(mainGroup, output_file_name ,'type-01', True, True)


#----------------------
# merge all filter for PS5 -Breach
#----------------------
output_file_name = 'dzx-poe2-PS5-breach'
merge_file.merge_files_from_array(breachGroup, output_file_name ,'type-01', True)






#----------------------
# create css file
filter_to_css(mainGroup, "filter_styles.css")
#----------------------

#----------------------
# create html preview
write_html_to_file(mainGroup, "index.html")
#----------------------
