width = 600
height = 350

scan_tab = None
create_tab = None
settings_tab = None

with open('Assets/Data/colors.txt') as f:
    colors = f.read().splitlines()

number = int(open('Assets/Data/number.txt', 'r').read())
