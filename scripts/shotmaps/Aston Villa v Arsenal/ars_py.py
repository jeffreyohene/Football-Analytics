# Libraries
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib
from matplotlib.cm import get_cmap
import matplotlib.pyplot as plt
from urllib.request import urlopen
from PIL import Image
from mplsoccer import VerticalPitch, FontManager, add_image


# Loading font
fm = FontManager()
fm_rubik = FontManager('https://raw.githubusercontent.com/google/fonts/main/ofl/rubikmonoone/'
                       'RubikMonoOne-Regular.ttf')

# Loading Arsenal logo
ars_url = 'https://upload.wikimedia.org/wikipedia/en/thumb/5/53/Arsenal_FC.svg/1743px-Arsenal_FC.svg.png'
ars_logo = Image.open(urlopen(ars_url))

# Importing data
df = pd.read_csv('ars.csv')

#df_shots = df[df.result == 'Shot'].copy()
df_team1 = df[df.home_away == 'a'].copy()
shots1 = df_team1[df_team1.result=='Shot'].copy()
gols1 = df_team1[df_team1.result=='Goal'].copy()

# setting up pitch
pitch = VerticalPitch(pad_bottom=0.5,  
                      half=True, 
                      goal_type='box',
                      goal_alpha=0.8)  
fig, ax = pitch.draw(figsize=(12, 10))

# Plotting shots
sc = pitch.scatter(shots1.X_old*120, shots1.Y_old*80,
                   s=(shots1.xG * 900) + 100,
                   c='red', alpha=.7,edgecolors='#383838',# for other markers types see: https://matplotlib.org/api/markers_api.html
                   marker='o',
                   ax=ax)

# Plotting goals
s2 = pitch.scatter(gols1.X_old*120, gols1.Y_old*80,
                   s=(gols1.xG * 900) + 100,
                   c='green',
                   edgecolors='#383838',
                   marker='*',
                   ax=ax)  

# Inverting axis to match exact goal and shot locations    
plt.gca().invert_xaxis() 


# Adding plot text
txt = ax.text(x=40, y=75, s='Arsenal shots & goals\nv. Aston Villa',
              size=30,c='maroon',
              fontproperties=fm_rubik.prop, color=pitch.line_color,
              va='center', ha='center')

# Adding Arsenal logo
ax_image = add_image(ars_logo, fig, left=0.10, bottom=0.6, width=0.08,
                     alpha=0.9)            
        