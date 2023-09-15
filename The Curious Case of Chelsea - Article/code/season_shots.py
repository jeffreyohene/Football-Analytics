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
shots = che_shots[che_shots.outcome == 'Shot'].copy()
gols_che = che_shots[che_shots.outcome == 'Goal'].copy()

shots_con = agn_che[agn_che.outcome == 'Shot'].copy()
gols_agn = agn_che[agn_che.outcome == 'Goal'].copy()

#shifting coordinates for shots against
shots_con['X'] = pitch.dim.right - shots_con.X
gols_agn['X'] = pitch.dim.right - gols_agn.X

# Optional to run: Use for debugging if coordinates exhibit unusual behavior
#print(shots_con['X'])
#shots_con['X'] = pitch.dim.right - shots_con['X']
#print(shots_con['X'])

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
sc_t1 = pitch.scatter(shots.X, shots.Y, s=shots.xG * 600,
                         ec='black', color='red',alpha=0.5,ax=axs['pitch'])
sc_t2 = pitch.scatter(gols_che.X,gols_che.Y, s=gols_che.xG * 600,
                         ec='black', color='green',marker='*',alpha=0.85, ax=axs['pitch'])


s1 = pitch.scatter(shots_con.X, shots_con.Y, s=shots_con.xG * 600,
                         ec='black', color='red',alpha=0.5,ax=axs['pitch'])
s2 = pitch.scatter(gols_agn.X,gols_agn.Y, s=gols_agn.xG * 600,
                         ec='black', color='green',marker='*',alpha=0.85, ax=axs['pitch'])


plt.gca().invert_xaxis()


# importing font
fm = FontManager()
fm_rubik = FontManager('https://github.com/google/fonts/blob/main/ofl/arsenal/Arsenal-Regular.ttf')


# importing club logos
url = 'https://upload.wikimedia.org/wikipedia/en/thumb/c/cc/Chelsea_FC.svg/480px-Chelsea_FC.svg.png'
logo = Image.open(urlopen(url))


ax_image = add_image(logo, fig,left=0.22,bottom=0.81,width=0.1)

txt1 = axs['pitch'].text(x=25, y=8, s='Conceded Shots & Goals', fontproperties=fm.prop, color='#034694',
                         ha='center', va='center', fontsize=13)
txt2 = axs['pitch'].text(x=95, y=8, s='Chelsea Shots & Goals', fontproperties=fm.prop, color='#034694',
                         ha='center', va='center', fontsize=13)
                                                            

axs['pitch'].text(x=60, y=-9, s="CHELSEA SEASON SHOTMAP", color='#034694', fontsize=28, ha='center', va='center')

axs['pitch'].text(1, 78, '@jeffrstats', ha='right', va='center',color='grey',fontsize=15)

plt.show()