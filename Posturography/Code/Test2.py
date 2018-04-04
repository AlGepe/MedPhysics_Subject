from obci_readmanager.signal_processing import read_manager as read
from obci_readmanager.signal_processing.balance.wii_preprocessing import *
from obci_readmanager.signal_processing.balance.wii_analysis import *

# file_name = 'still_eyes_closed_eyes_open'
file_name = 'sway_forward'
wbr = read.ReadManager(file_name+'.obci.xml', file_name+'.obci.raw', file_name + '.obci.tag')
smart_tags = wii_cut_fragments(wbr, start_tag_name='ss_start', end_tags_names=['ss_stop'])
TL = smart_tags[0].get_samples()[0,:]
TR = smart_tags[0].get_samples()[1,:]
BR = smart_tags[0].get_samples()[2,:]
BL = smart_tags[0].get_samples()[3,:]

x = ((TR+BR) - (TL+BL)) / (TR+TL+BR+BL)
y = ((TR+TL) - (BR+BL)) / (TR+TL+BR+BL)

x = x * 22.5 # Convert to cm
y = y * 22.5 # Convert to cm
print(min(x))
print(max(x))
print(min(y))
print(max(y))
print(type(x))
print(type(y))
