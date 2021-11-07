import espn_cfb_api as cfb
import matplotlib.pyplot as plt
import numpy as np

conferenceId = 175
c = cfb.Conference(conferenceId = conferenceId)

for team in c.getTeams():
    fig = plt.figure(figsize=(12,6), dpi = 120)
    for game in team.getSchedule():
        if game.weekNumber <= 8:
            if team.teamId == game.homeTeam.teamId:
                wp = game.getWinProbability(key = 'home')
                if len(wp) > 0:
                    opp = game.awayTeam
            else:
                wp = game.getWinProbability(key = 'away')
                if len(wp) > 0:
                    opp = game.homeTeam
            
            if len(wp) > 0:
                xvals = np.array([x for x in range(len(wp))])/(len(wp)-1)*100
                plt.plot(xvals, wp, color = opp.hexColor, label=opp.displayName)
    
    plt.legend(loc = 'lower left')
    plt.ylabel('Win Probability [%]')
    plt.xlabel('Game Duration [%]')
    plt.title(team.displayName + f' {team.record}')
    plt.xlim([-1,101])
    plt.ylim([-1,101])
    plt.grid()
    filename = 'ASUN-WAC/conference_{}_team_{}.png'.format(c.conferenceId, team.teamId)
    plt.savefig(filename)
    plt.close(fig)