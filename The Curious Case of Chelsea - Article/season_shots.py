# Libraries
import pandas as pd
import matplotlib.pyplot as plt
from urllib.request import urlopen
from PIL import Image
from mplsoccer import Pitch, FontManager, add_image


# setting up pitch. nb - statsbomb
pitch = Pitch(pad_top=0.05, pad_right=0.05, pad_bottom=0.05, pad_left=0.05, line_zorder=2)


# reading shot data
che_shots = pd.read_csv('che_shots.csv',encoding='iso-8859-1')
agn_che = pd.read_csv('agn_che.csv',encoding='iso-8859-1')

# subsetting shots
shots = che_shots[che_shots.result == 'Shot'].copy()
gols_che = che_shots[che_shots.result == 'Goal'].copy()

shots_con = agn_che[agn_che.result == 'Shot'].copy()
gols_agn = agn_che[agn_che.result == 'Goal'].copy()

#shifting coordinates for shots against
shots_con['X'] = pitch.dim.right - shots_con.X
gols_agn['X'] = pitch.dim.right - gols_agn.X

# setting up plot
fig, axs = pitch.jointgrid(figheight=10,  # the figure is 10 inches high
                           left=None,  # joint grid center-aligned
                           bottom=0.075,  # grid starts 7.5% in from the bottom of the figure
                           marginal=0.1,  # marginal axes heights are 10% of grid height
                           space=0,  # 0% of the grid height reserved for space between axes
                           grid_width=0.9,  # the grid width takes up 90% of the figure width
                           title_height=0,  # plot without a title axes
                           axis=False,  # turn off title/ endnote/ marginal axes
                           endnote_height=0,  # plot without an endnote axes
                           grid_height=0.8)  # grid takes up 80% of the figure height

# Shot maps
sc_t1 = pitch.scatter(shots.X * 120, shots.Y * 80, s=shots.xG * 600,
                         ec='black', color='red',alpha=0.3,ax=axs['pitch'])
sc_t2 = pitch.scatter(gols_che.X* 120,gols_che.Y* 80, s=gols_che.xG * 600,
                         ec='black', color='green',marker='*',alpha=0.85, ax=axs['pitch'])


s1 = pitch.scatter(shots_con.X* 120, shots_con.Y* 80, s=shots_con.xG * 600,
                         ec='black', color='red',alpha=0.3,ax=axs['pitch'])
s2 = pitch.scatter(gols_agn.X* 120,gols_agn.Y* 80, s=gols_agn.xG * 600,
                         ec='black', color='green',marker='*',alpha=0.85, ax=axs['pitch'])


plt.gca().invert_xaxis()


# importing font
fm = FontManager()
fm_rubik = FontManager('https://github.com/google/fonts/blob/main/ofl/arsenal/Arsenal-Regular.ttf')


# importing club logos
che_url = 'https://upload.wikimedia.org/wikipedia/en/thumb/c/cc/Chelsea_FC.svg/480px-Chelsea_FC.svg.png'
logo = Image.open(urlopen(che_url))



txt1 = axs['pitch'].text(x=25, y=8, s='Chelsea Shots & Goals', fontproperties=fm.prop, color='maroon',
                         ha='center', va='center', fontsize=13)
txt2 = axs['pitch'].text(x=95, y=8, s='Conceded Shots & Goals', fontproperties=fm.prop, color='maroon',
                         ha='center', va='center', fontsize=13)

ax_image = add_image(logo, fig, left=0.57, bottom=0.6, width=0.08,
                     alpha=0.9)
                                                            



axs['pitch'].text(x=60, y=-2, s="CHELSEA SEASON SHOTMAP", color='maroon', fontsize=20, ha='center', va='center')

axs['pitch'].text(1, 78, '@jeffrstats', ha='right', va='center',color='grey',fontsize=15)

plt.show()