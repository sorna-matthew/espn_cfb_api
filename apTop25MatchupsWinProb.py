import espn_cfb_api as cfb
import numpy as np
from matplotlib import pyplot as plt, lines

week_num = 10

fbs = cfb.FBS()
ap = fbs.getAPTop25Teams(weekNumber=week_num)
apIds = [team.teamId for team in ap]
top25matchups = list()
includedIds = list()
fig = plt.figure(figsize=(18,10), dpi = 240)
for conference in fbs.getConferences():
    matchupLines = list()
    matchupText = list()
    matchups = conference.getMatchups(weekNumber = week_num)
    
    for matchup in matchups:
        if ((matchup[0].teamId in apIds) or (matchup[1].teamId in apIds)) and ((matchup[0].teamId not in includedIds) and (matchup[1].teamId not in includedIds)):
            top25matchups.append(matchup)
            includedIds.append(matchup[0].teamId)
            includedIds.append(matchup[1].teamId)
    
for matchup in top25matchups:
    homeColor = matchup[0].hexColor
    awayColor = matchup[1].hexColor
    
    homeWinProb = matchup[0].getSchedule(weekNumber = week_num).getWinProbability()
    if len(homeWinProb) > 1:
        xvals = np.array([x for x in range(len(homeWinProb))])/(len(homeWinProb)-1)*100
        if homeWinProb[-1] != 50:
            plt.plot(xvals, homeWinProb, '-', color=homeColor, linewidth = 2)
            plt.plot(xvals, homeWinProb, '--', color=awayColor, linewidth = 2)
            dotted_line1 = lines.Line2D([], [], linewidth=3, linestyle="--", dashes=(6, 1), color=homeColor)
            dotted_line2 = lines.Line2D([], [], linewidth=3, linestyle="-", dashes=(3, 4), color=awayColor)
            matchupLines.append((dotted_line1, dotted_line2))
        if homeWinProb[-1] > 50:
            awayText = f'{matchup[1].displayName}'
            if matchup[1].teamId in apIds:
                awayText = f'#{str(apIds.index(matchup[1].teamId)+1)} ' + awayText
            homeText = f'$\\bf{matchup[0].location}$ $\\bf{matchup[0].name}$'
            if matchup[0].teamId in apIds:
                homeText = f'#{str(apIds.index(matchup[0].teamId)+1)} ' + homeText
            matchupText.append(awayText+' vs. '+homeText)
        if homeWinProb[-1] < 50:
            awayText = f'$\\bf{matchup[1].location}$ $\\bf{matchup[1].name}$'
            if matchup[1].teamId in apIds:
                awayText = f'#{str(apIds.index(matchup[1].teamId)+1)} ' + awayText
            homeText = f'{matchup[0].displayName}'
            if matchup[0].teamId in apIds:
                homeText = f'#{str(apIds.index(matchup[0].teamId)+1)} ' + homeText
            matchupText.append(awayText+' vs. '+homeText)

plt.title(f'AP Top 25 [Week {week_num}]')
plt.ylabel('Home Team Win Probability [%]')
plt.xlabel('Game Progression [%]')
plt.legend(matchupLines, matchupText, loc = 'lower left', fontsize = 6)
plt.xlim([-1,101])
plt.ylim([-1, 101])

# Major ticks every 25, minor ticks every 5
ax = fig.axes[0]
major_ticks = np.arange(0, 101, 25)
minor_ticks = np.arange(0, 101, 5)

ax.set_xticks(major_ticks)
ax.set_xticks(minor_ticks, minor=True)
ax.set_yticks(major_ticks)
ax.set_yticks(minor_ticks, minor=True)

# And a corresponding grid
ax.grid(which='both')

# Or if you want different settings for the grids:
ax.grid(which='minor', alpha=0.2)
ax.grid(which='major', alpha=0.5)

filename = f'WEEK {week_num}/AP_TOP25_week_' + str(week_num) + '.png'
fig.savefig(filename, facecolor = 'lightgray')
plt.close(fig)