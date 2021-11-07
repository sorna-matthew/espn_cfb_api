import sys
sys.path.insert(0,'..')

import espn_cfb_api as cfb
import numpy as np
from matplotlib import pyplot as plt, lines

week_num = 10

fbs = cfb.FBS()
tp25 = fbs.getTop25Teams(weekNumber=week_num, rankingType = 'cfp')
tp25Ids = [team.teamId for team in tp25]
for conference in fbs.getConferences():
    matchupLines = list()
    matchupText = list()
    fig = plt.figure(figsize=(14,8), dpi = 120)
    matchups = conference.getMatchups(weekNumber = week_num)
    for matchup in matchups:
        homeColor = matchup.homeTeam.hexColor
        awayColor = matchup.awayTeam.hexColor
        
        homeWinProb = matchup.homeTeam.getSchedule(weekNumber = week_num).getWinProbability()
        if len(homeWinProb) > 1:
            xvals = np.array([x for x in range(len(homeWinProb))])/(len(homeWinProb)-1)*100
            if homeWinProb[-1] != 50:
                plt.plot(xvals, homeWinProb, '-', color=homeColor, linewidth = 3)
                plt.plot(xvals, homeWinProb, '--', color=awayColor, linewidth = 3)
                dotted_line1 = lines.Line2D([], [], linewidth=2, linestyle="--", dashes=(6, 1), color=homeColor)
                dotted_line2 = lines.Line2D([], [], linewidth=2, linestyle="-", dashes=(3, 4), color=awayColor)
                matchupLines.append((dotted_line1, dotted_line2))
            if homeWinProb[-1] > 50:
                awayText = f'{matchup.awayTeam.displayName}'
                if matchup.awayTeam.teamId in tp25Ids:
                    awayText = f'#{str(tp25Ids.index(matchup.awayTeam.teamId)+1)} ' + awayText
                homeText = f'$\\bf{matchup.homeTeam.location}$ $\\bf{matchup.homeTeam.name}$'
                if matchup.homeTeam.teamId in tp25Ids:
                    homeText = f'#{str(tp25Ids.index(matchup.homeTeam.teamId)+1)} ' + homeText
                matchupText.append(awayText+' vs. '+homeText)
            if homeWinProb[-1] < 50:
                awayText = f'$\\bf{matchup.awayTeam.location}$ $\\bf{matchup.awayTeam.name}$'
                if matchup.awayTeam.teamId in tp25Ids:
                    awayText = f'#{str(tp25Ids.index(matchup.awayTeam.teamId)+1)} ' + awayText
                homeText = f'{matchup.homeTeam.displayName}'
                if matchup.homeTeam.teamId in tp25Ids:
                    homeText = f'#{str(tp25Ids.index(matchup.homeTeam.teamId)+1)} ' + homeText
                matchupText.append(awayText+' vs. '+homeText)

    plt.title(conference.conferenceName + f' [Week {week_num}]')
    plt.ylabel('Home Team Win Probability [%]')
    plt.xlabel('Game Progression [%]')
    plt.legend(matchupLines, matchupText, loc = 'lower left', fontsize=6)
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
    
    filename = conference.conferenceName.replace(' ', '_') + '_week_' + str(week_num) + '.png'
    fig.savefig(filename, facecolor = 'lightgray')
    plt.close(fig)