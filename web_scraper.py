import requests
import sys
from bs4 import BeautifulSoup
from datetime import date
from datetime import timedelta

# -d -> games from how many days ago (up to 5) -----------------done
# -s -> standings ----------------------------------------------done
# -g -> game number (e.g. -g 1, -g 2, etc)
# -bs -> basic stats
# -adv -> advanced stats
# -h -> help message
# -bs and -adv must be used in association with -g
# e.g. "python web_scraper.py -g 3 -adv" gives the advanced stats of game number 3

team_names = {
    "Atlanta": "Atlanta Hawks",
    "Boston": "Boston Celtics",
    "Brooklyn": "Brooklyn Nets",
    "Charlotte": "Charlotte Hornets",
    "Chicago": "Chicago Bulls",
    "Cleveland": "Cleveland Cavaliers",
    "Dallas": "Dallas Mavericks",
    "Denver": "Denver Nuggets",
    "Detroit": "Detroit Pistons",
    "Golden State": "Golden State Warriors",
    "Houston": "Houston Rockets",
    "Indiana": "Indiana Pacers",
    "LA Clippers": "Los Angeles Clippers",
    "LA Lakers": "Los Angeles Lakers",
    "Memphis": "Memphis Grizzlies",
    "Miami": "Miami Heat",
    "Milwaukee": "Milwaukee Bucks",
    "Minnesota": "Minnesota Timberwolves",
    "New Orleans": "New Orleans Pelicans",
    "New York": "New York Knicks",
    "Oklahoma City": "Oklahoma City Thunder",
    "Orlando": "Orlando Magic",
    "Philadelphia": "Philadelphia 76ers",
    "Phoenix": "Phoenix Suns",
    "Portland": "Portland Trailblazers",
    "Sacramento": "Sacramento Kings",
    "San Antonio": "San Antonio Spurs",
    "Toronto": "Toronto Raptors",
    "Utah": "Utah Jazz",
    "Washington": "Washington Wizards"
}

def games(URL):
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    winners = soup.find_all("tr", class_="winner")
    losers = soup.find_all("tr", class_="loser")

    matchups = {}
    for i in range(len(winners)):
        w_team = (winners[i].find("a")).get_text()
        w_score = (winners[i].find(class_="right")).get_text()
        l_team = (losers[i].find("a")).get_text()
        l_score = (losers[i].find(class_="right")).get_text()
        matchups[w_team] = l_team, w_score, l_score
    return matchups



def standings():
    EC = {}
    WC = {}
    standings_URL = "https://www.basketball-reference.com/leagues/NBA_2024_standings.html"
    s_page = requests.get(standings_URL)
    s_soup = BeautifulSoup(s_page.content, "html.parser")
    teams = s_soup.find_all("th",class_="left")
    records = s_soup.find_all("td", class_="right")
    for i in range(32):  # 30 teams plus 2 conferences
        r_index = (7*i) - 7
        wins = records[r_index].get_text()   # adjusting for "Eastern Conference" taking up an index
        losses = records[r_index + 1].get_text()
        gb = records[r_index + 3].get_text()
        if i > 0 and i < 16:
            if i < 10:
                EC[teams[i].get_text()[:-5]] = (wins, losses, gb)
            else:
                EC[teams[i].get_text()[:-6]] = (wins, losses, gb)
        elif i > 16:
            wins = records[r_index - 7].get_text()       # adjusting again but for "Western Conference"
            losses = records[r_index - 6].get_text()
            gb = records[r_index - 4].get_text()
            if i < 26:
                WC[teams[i].get_text()[:-5]] = (wins, losses, gb)
            else:
                WC[teams[i].get_text()[:-6]] = (wins, losses, gb)
    return EC, WC


def format_standings():
    ec, wc = standings()
    e_teams = list(ec.keys())
    w_teams = list(wc.keys())
    print("-------------Eastern Conference-------------" + 20 * " " + "-------------Western Conference-------------")
    print(28 * " " + "W     L     GB" + 52 * " " + "W     L     GB")
    for i in range(15):
        E = e_teams[i]
        W = w_teams[i]
        ew_space = " " * (28 - len(str(i+1) + " - " + E))  # space between team name and win column (east)
        ew = ec[E][0]   # east wins
        el = ec[E][1]   # east losses
        egb = ec[E][2]  # east games behind
        ww = wc[W][0]   # west wins
        wl = wc[W][1]   # west losses
        wgb = wc[W][2]  # west games behind
        ww_space = " " * (30 - len(str(i+1) + " - " + W))  # space between team name and win column (west)
        s_space = " " * (20 + (4-len(egb)))
        print(str(i+1) + " - " + E + ew_space + ew + 4 * " " + el + 4 * " " + egb +
              s_space + str(i+1) + " - " + W + ww_space + ww + 4 * " " + wl + 4 * " " + wgb)


def format_games(d = None):
    if d == None or d == 1:
        url = "https://www.basketball-reference.com/boxscores/?"
    elif d >= 2 and d <=5:
        g_date = date.today() - timedelta(days=d)
        m = g_date.month
        d = g_date.day
        y = g_date.year
        url = "https://www.basketball-reference.com/boxscores/?" + "month=" + str(m) + "&day=" + str(d) + "&year=" + str(y)
    else:
        sys.exit("ValueError: the -d flag only takes numbers 1 through 5 as arguments")


    matchups = games(url)
    for matches in matchups:
        winner = '\033[4m' + '\033[1m' + team_names[matches] + '\033[0m' + " - " + matchups[matches][1]
        loser = matchups[matches][0] + " - " + matchups[matches][2]
        spaces = 45 - len(winner)  # align the right column
        print(winner + (" " * spaces) + loser)
        print("\n")


def box_score():
    pass

def help_message():
    # print("")
    pass



def main():
    args = sys.argv[1:]
    if len(args) == 0:
        format_games()
    elif args[0] == "-s":
        format_standings()
    elif args[0] == "-d" and len(args) == 1:
        format_games()
    elif args[0] == "-d":
        format_games(int(args[1]))
    elif args[0] == "-bs":
        pass  # game_stats()






if __name__ == "__main__":
    main()













