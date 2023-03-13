# Loading libraries
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib
from matplotlib.cm import get_cmap
import matplotlib.pyplot as plt
from urllib.request import urlopen
from PIL import Image
from mplsoccer import Pitch, VerticalPitch, FontManager, add_image


# Importing font
fm = FontManager()
fm_rubik = FontManager('https://raw.githubusercontent.com/google/fonts/main/ofl/rubikmonoone/'
                       'RubikMonoOne-Regular.ttf')

# Importing Aston Villa Logo
avl_url = 'https://upload.wikimedia.org/wikipedia/en/thumb/f/f9/Aston_Villa_FC_crest_%282016%29.svg/724px-Aston_Villa_FC_crest_%282016%29.svg.png'
avl_logo = Image.open(urlopen(avl_url))

# Aston Villa shot data
df = pd.read_csv('avl.csv')

# Separating shots from goals
#df_shots = df[df.result == 'Shot'].copy()
df_team1 = df[df.home_away == 'h'].copy()
shots1 = df_team1[df_team1.result=='Shot'].copy()
gols1 = df_team1[df_team1.result=='Goal'].copy()

# Setting up pitch
pitch = VerticalPitch(pad_bottom=0.5,  
                      half=True,  # gonna use a half pitch
                      goal_type='box',
                      goal_alpha=0.8)  
fig, ax = pitch.draw(figsize=(12, 10))

# Plotting shots
sc = pitch.scatter(shots1.X_old*120, shots1.Y_old*80,
                   # size varies between 100 and 1000 (points squared)
                   s=(shots1.xG * 900) + 100,
                   c='red', alpha=.7,  # color for scatter in hex format
                   edgecolors='#383838',  # give the markers a charcoal border
                   # for other markers types see: https://matplotlib.org/api/markers_api.html
                   marker='o',
                   ax=ax)

# Plotting goals
s2 = pitch.scatter(gols1.X_old*120, gols1.Y_old*80,
                   # size varies between 100 and 1000 (points squared)
                   s=(gols1.xG * 900) + 200,
                   c='green',  # color for scatter in hex format
                   edgecolors='#383838',  # give the markers a charcoal border
                   # for other markers types see: https://matplotlib.org/api/markers_api.html
                   marker='*',
                   ax=ax) 


# Inverting axis to match exact goal and shot locations
plt.gca().invert_xaxis()  

# Adding plot text
txt = ax.text(x=40, y=70, s='Aston Villa shots & goals\nv. Arsenal',
              size=30,
              c='blue',
              # here i am using a downloaded font from google fonts instead of passing a fontdict
              fontproperties=fm_rubik.prop, color=pitch.line_color,
              va='center', ha='center')

# Adding Villa logo
ax_image = add_image(avl_logo, fig, left=0.10, bottom=0.6, width=0.08,
                     alpha=0.9) 