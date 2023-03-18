import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.cm import get_cmap
import matplotlib.pyplot as plt
from urllib.request import urlopen
from PIL import Image
from mplsoccer import Pitch, VerticalPitch, FontManager, add_image


# setting up pitch. nb - statsbomb
pitch = Pitch(pitch_color='grass',
              line_color = 'white', 
              stripe = True, 
              pad_top=0.05, 
              pad_right=0.05, 
              pad_bottom=0.05, 
              pad_left=0.05, 
              line_zorder=2)


# reading shot data
df = pd.read_csv('spez.csv',encoding='iso-8859-1')

# subsetting shots
df_shots = df[df.result == 'Shot'].copy()
df_gols = df[df.result == 'Goal'].copy()
# subset the shots for each team
t1, t2 = df_shots.team_name.unique()
df_t1 = df_shots[df_shots.team_name == t1].copy()
df_t2 = df_shots[df_shots.team_name == t2].copy()

# subsetting goals
df_g1 = df_gols[df_gols.team_name == t1].copy()
df_g2 = df_gols[df_gols.team_name == t2].copy()

#shifting coordinates for Madrid
df_t1['X'] = pitch.dim.right - df_t1.X
df_g1['X'] = pitch.dim.right - df_g1.X

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
sc_t1 = pitch.scatter(df_t1.X, df_t1.Y, s=df_t1.xG * 600,
                         ec='black', color='red',alpha=0.8,ax=axs['pitch'])
sc_t2 = pitch.scatter(df_g1.X,df_g1.Y, s=df_g1.xG * 600,
                         ec='black', color='gold',marker='*',alpha=0.85, ax=axs['pitch'])


s1 = pitch.scatter(df_t2.X, df_t2.Y, s=df_t2.xG * 600,
                         ec='black', color='red',alpha=0.8,ax=axs['pitch'])
s2 = pitch.scatter(df_g2.X,df_g2.Y, s=df_g2.xG * 600,
                         ec='black', color='gold',marker='*',alpha=0.85, ax=axs['pitch'])


plt.gca().invert_xaxis()                        


# importing font
fm = FontManager()
fm_rubik = FontManager('https://github.com/google/fonts/blob/main/ofl/arsenal/Arsenal-Regular.ttf')


# importing club logos
t1_url = 'https://upload.wikimedia.org/wikipedia/en/thumb/1/1c/US_Sassuolo_Calcio_logo.svg/220px-US_Sassuolo_Calcio_logo.svg.png'
t1_logo = Image.open(urlopen(t1_url))

t2_url = 'https://upload.wikimedia.org/wikipedia/commons/thumb/a/aa/Spezia_Calcio.svg/241px-Spezia_Calcio.svg.png'
t2_logo = Image.open(urlopen(t2_url))


txt1 = axs['pitch'].text(x=25, y=8, s='Sassuolo Shots', fontproperties=fm.prop, color='black',
                         ha='center', va='center', fontsize=13)
txt2 = axs['pitch'].text(x=95, y=8, s='Spezia Shots', fontproperties=fm.prop, color='black',
                         ha='center', va='center', fontsize=13)

ax_image = add_image(t1_logo, fig, left=0.27, bottom=0.8, height=0.08, width=0.08,
                     alpha=0.9)

ax_image = add_image(t2_logo, fig, left=0.69, bottom=0.8, height=0.08, width=0.08,
                     alpha=0.9)

txt3 =axs['pitch'].text(x=60.3,y=58,s='Tiro',fontproperties=fm.prop, color='black',
                         ha='center', va='center', fontsize=15)

txt4 =axs['pitch'].text(x=57,y=61,s='22',fontproperties=fm.prop, color='black',
                         ha='center', va='center', fontsize=14)

txt5 =axs['pitch'].text(x=63,y=61,s='7',fontproperties=fm.prop, color='black',
                         ha='center', va='center', fontsize=14)

txt6 =axs['pitch'].text(x=60,y=70,s='xG',fontproperties=fm.prop, color='black',
                       ha='center', va='center', fontsize=15)

txt7 =axs['pitch'].text(x=57,y=73,s='2.01',fontproperties=fm.prop, color='black',
                       ha='center', va='center', fontsize=14)

txt8 =axs['pitch'].text(x=63,y=73,s='0.71',fontproperties=fm.prop, color='black',
                         ha='center', va='center', fontsize=14)

txt9 =axs['pitch'].text(x=59.7,y=64,s='Gol',fontproperties=fm.prop, color='black',
                         ha='center', va='center', fontsize=15)  

txt10 =axs['pitch'].text(x=57,y=67,s='1',fontproperties=fm.prop, color='black',
                        ha='center', va='center', fontsize=14)

txt11 =axs['pitch'].text(x=63,y=67,s='1',fontproperties=fm.prop, color='black',
                         ha='center', va='center', fontsize=14)                                                                



axs['pitch'].text(x=60, y=-2, s="SASSUOLO vs SPEZIA SHOTMAP", color='black', fontsize=20, ha='center', va='center')

axs['pitch'].text(1, 78, '@jeffrstats', ha='right', va='center',color='black',fontsize=15)

plt.show()