import pandas as pd
import matplotlib.pyplot as plt
from urllib.request import urlopen
from PIL import Image
from mplsoccer import Pitch, FontManager, add_image


# pitch setup
pitch = Pitch(pad_top=0.05, pad_right=0.05, pad_bottom=0.05, pad_left=0.05, line_zorder=2)

# importing club logos - wikipedia logos because it's open source
home_url = 'https://upload.wikimedia.org/wikipedia/en/thumb/7/7a/Manchester_United_FC_crest.svg/474px-Manchester_United_FC_crest.svg.png'
home_logo = Image.open(urlopen(home_url))

away_url = 'https://upload.wikimedia.org/wikipedia/en/thumb/f/fd/Brighton_%26_Hove_Albion_logo.svg/480px-Brighton_%26_Hove_Albion_logo.svg.png'
away_logo = Image.open(urlopen(away_url))


# reading shot data
home = pd.read_csv('home.csv',encoding='iso-8859-1')
away = pd.read_csv('away.csv',encoding='iso-8859-1')

# team names
h = home.at[0, 'home_team'].split()[0]
a = away.at[0, 'away_team'].split()[0]

# statistics: goals, shots and xG
h1_gols = home.at[0, 'home_goals']
a1_gols = away.at[0, 'away_goals']

h1_shots = (home['outcome'] == 'shot').count()
a1_shots = (away['outcome'] == 'shot').count()

h_xg = round(home['xG'].sum(), 2)
a_xg = round(away['xG'].sum(), 2)


# subsetting shots
home_shots = home[home.outcome == 'Shot'].copy()
home_gols = home[home.outcome == 'Goal'].copy()

away_shots = away[away.outcome == 'Shot'].copy()
away_gols = away[away.outcome == 'Goal'].copy()

# shift coordinates for away team
away_shots['X'] = pitch.dim.right - away_shots.X
away_gols['X'] = pitch.dim.right - away_gols.X

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
h_shots = pitch.scatter(home_shots.X, home_shots.Y, s=home_shots.xG * 1300,
                         ec='black', color='#6BDBC7',alpha=0.3,ax=axs['pitch'])
h_gols = pitch.scatter(home_gols.X,home_gols.Y, s=home_gols.xG * 1300,
                         ec='black', color='#6BDBC7',marker='*',alpha=0.5, ax=axs['pitch'])


a_shots = pitch.scatter(away_shots.X, away_shots.Y, s=away_shots.xG * 1300,
                         ec='black', color='#DBBD56',alpha=0.3,ax=axs['pitch'])
a_gols = pitch.scatter(away_gols.X,away_gols.Y, s=away_gols.xG * 1300,
                         ec='black', color='#DBBD56',marker='*',alpha=0.5, ax=axs['pitch'])


plt.gca().invert_xaxis()                        


# importing font
fm = FontManager()
fm_rubik = FontManager('https://github.com/google/fonts/blob/main/ofl/arsenal/Arsenal-Regular.ttf')


#txt1 = axs['pitch'].text(x=10, y=70, s=f"{a}", fontproperties=fm.prop, color='#6BDBC7',
#                         ha='center', va='center', fontsize=25)
#txt2 = axs['pitch'].text(x=105, y=70, s=f"{h}", fontproperties=fm.prop, color='#DBBD56',
#                         ha='center', va='center', fontsize=25)

ax_image = add_image(home_logo, fig, left=0.42, bottom=0.6, width=0.08,
                     alpha=0.9)

ax_image = add_image(away_logo, fig, left=0.50, bottom=0.6, width=0.08,
                     alpha=0.9)



txt3 =axs['pitch'].text(x=60.3,y=58,s='Total Shots',fontproperties=fm.prop, fontweight='bold', color='#5D6466',
                         ha='center', va='center', fontsize=15)

txt4 =axs['pitch'].text(x=63,y=61,s=f"{h1_shots}",fontproperties=fm.prop, fontweight='bold', color='#6BDBC7',
                         ha='center', va='center', fontsize=14)

txt5 =axs['pitch'].text(x=57,y=61,s=f"{a1_shots}",fontproperties=fm.prop, fontweight='bold', color='#DBBD56',
                         ha='center', va='center', fontsize=14)



txt6 =axs['pitch'].text(x=60,y=70,s='Expected Goals',fontproperties=fm.prop, fontweight='bold',color='#5D6466',
                       ha='center', va='center', fontsize=15)

txt7 =axs['pitch'].text(x=64,y=73,s=f"{h_xg}",fontproperties=fm.prop, fontweight='bold', color='#6BDBC7',
                         ha='center', va='center', fontsize=14)

txt8 =axs['pitch'].text(x=56,y=73,s=f"{a_xg}",fontproperties=fm.prop, fontweight='bold',color='#DBBD56',
                       ha='center', va='center', fontsize=14)



txt9 =axs['pitch'].text(x=59.7,y=64,s='Scoreline',fontproperties=fm.prop, fontweight='bold', color='#5D6466',
                         ha='center', va='center', fontsize=15)

txt10 =axs['pitch'].text(x=63,y=67,s=f"{h1_gols}",fontproperties=fm.prop, fontweight='bold',color='#6BDBC7',
                         ha='center', va='center', fontsize=14)

txt11 =axs['pitch'].text(x=57,y=67,s=f"{a1_gols}",fontproperties=fm.prop, fontweight='bold', color='#DBBD56',
                        ha='center', va='center', fontsize=14)





axs['pitch'].text(x=87, y=-3, s=f"{h} United", color='#6BDBC7', fontweight='bold', fontsize=20, ha='center', va='center')
axs['pitch'].text(x=63.5, y=-3, s="v", color='#5D6466', fontsize=16, fontweight='bold', ha='center', va='center')
axs['pitch'].text(x=35, y=-3, s=f"{a} & Hove Albion", color='#DBBD56', fontweight='bold', fontsize=20, ha='center', va='center')


axs['pitch'].text(1, 78, '@jeffrstats', ha='right', va='center',color='grey',fontsize=6)

plt.show()