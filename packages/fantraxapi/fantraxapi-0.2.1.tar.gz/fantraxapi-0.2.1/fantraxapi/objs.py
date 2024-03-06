from datetime import datetime, timedelta


class Team:
    """ Represents a single Team.

        Attributes:
            team_id (str): Team ID.
            name (str): Team Name.
            short (str): Team Short Name.

    """
    def __init__(self, api, team_id, name, short):
        self._api = api
        self.team_id = team_id
        self.name = name
        self.short = short

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.name


class Matchup:
    """ Represents a single Matchup.

        Attributes:
            matchup_key (int): Team ID.
            away (:class:`~Team`): Away Team.
            away_score (float): Away Team Score.
            home (:class:`~Team`): Home Team.
            home_score (float): Home Team Score.

    """
    def __init__(self, api, matchup_key, data):
        self._api = api
        self.matchup_key = matchup_key
        self.away = api.team(data[0]["teamId"])
        self.away_score = float(data[1]["content"])
        self.home = api.team(data[2]["teamId"])
        self.home_score = float(data[3]["content"])

    def winner(self):
        if self.away_score > self.home_score:
            return self.away, self.away_score, self.home, self.home_score
        elif self.away_score < self.home_score:
            return self.home, self.home_score, self.away, self.away_score
        else:
            return None, None, None, None

    def difference(self):
        if self.away_score > self.home_score:
            return self.away_score - self.home_score
        elif self.away_score < self.home_score:
            return self.home_score - self.away_score
        else:
            return 0

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f"{self.away} ({self.away_score}) vs {self.home} ({self.home_score})"


class ScoringPeriod:
    """ Represents a single Scoring Period.

        Attributes:
            name (str): Name.
            week (int): Week Number.
            start (datetime): Start Date of the Period.
            end (datetime): End Date of the Period.
            next (datetime): Next Day after the Period.
            complete (bool): Is the Period Complete?
            current (bool): Is it the current Period?
            future (bool): Is the Period in the future?
            matchups (List[:class:`~Matchup`]): List of Matchups.

    """
    def __init__(self, api, data):
        self._api = api
        self.name = data["caption"]
        self.week = int(self.name[15:])
        dates = data["subCaption"][1:-1].split(" - ")
        self.start = datetime.strptime(dates[0], "%a %b %d, %Y")
        self.end = datetime.strptime(dates[1], "%a %b %d, %Y")
        self.next = self.end + timedelta(days=1)
        now = datetime.now()
        self.complete = now > self.next
        self.current = self.start < now < self.next
        self.future = now < self.start

        self.matchups = []
        for i, matchup in enumerate(data["rows"], 1):
            self.matchups.append(Matchup(self._api, i, matchup["cells"]))

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        output = f"{self.name}: {self.start}-{self.end}"
        if self.complete:
            output += "\nComplete"
        elif self.current:
            output += "\nCurrent"
        else:
            output += "\nFuture"
        for matchup in self.matchups:
            output += f"\n{matchup}"
        return output


class Standings:
    """ Represents a single Standings.

        Attributes:
            week (int): Week Number.
            ranks (Dict[int, :class:`~Record`]): Team Ranks and their Records.

    """
    def __init__(self, api, data, week=None):
        self._api = api
        self.week = week
        self.ranks = {}
        for obj in data:
            team_id = obj["fixedCells"][1]["teamId"]
            rank = obj["fixedCells"][0]["content"]
            self.ranks[int(rank)] = Record(self._api, team_id, rank, obj["cells"])

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        output = f"Standings"
        if self.week:
            output += f" Week {self.week}"
        for rank, record in self.ranks.items():
            output += f"\n{record}"
        return output


class Record:
    """ Represents a single Record of a :class:`~Standings`.

        Attributes:
            team (:class:`~Team`): Team.
            rank (int): Standings Rank.
            win (int): Number of Wins.
            loss (int): Number of Losses.
            tie (int): Number of Ties.
            points (int): Number of Points.
            win_percentage (float): Win Percentage.
            games_back (int): Number of Games Back.
            wavier_wire_order (int): Wavier Wire Claim Order.
            points_for (float): Fantasy Points Against.
            streak (str): Streak.

    """
    def __init__(self, api, team_id, rank, data):
        self._api = api
        self.team = self._api.team(team_id)
        self.rank = int(rank)
        self.win = int(data[0]["content"])
        self.loss = int(data[1]["content"])
        self.tie = int(data[2]["content"])
        self.points = int(data[3]["content"])
        self.win_percentage = float(data[4]["content"])
        self.games_back = int(data[5]["content"])
        self.wavier_wire_order = int(data[6]["content"])
        self.points_for = float(data[7]["content"].replace(",", ""))
        self.points_against = float(data[8]["content"].replace(",", ""))
        self.streak = data[9]["content"]

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f"{self.rank}: {self.team} ({self.win}-{self.loss}-{self.tie})"
