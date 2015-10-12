#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    DB = connect()
    cur = DB.cursor()
    sql_statement = "TRUNCATE match_results;"
    cur.execute(sql_statement)
    DB.commit()
    DB.close


def deletePlayers():
    """Remove all the player records from the database."""
    DB = connect()
    cur = DB.cursor()
    sql_statement = "TRUNCATE players;"
    cur.execute(sql_statement)
    DB.commit()
    DB.close


def countPlayers():
    """Returns the number of players currently registered."""
    DB = connect()
    cur = DB.cursor()
    sql_statement = "select count(*) from players"
    cur.execute(sql_statement)
    count = cur.fetchall()[0][0]
    DB.close
    return count


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    DB = connect()
    cur = DB.cursor()
    cur.execute("INSERT INTO players (name) VALUES (%s)", (name,))
    DB.commit()
    DB.close


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a
    player tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    DB = connect()
    cur = DB.cursor()
    cur.execute("SELECT players.id,players.name,\
                CAST(count(match_results.winner) AS INTEGER) AS wins,\
                (SELECT cast(count(*) AS INTEGER) FROM match_results \
                    WHERE players.id=match_results.winner \
                    OR players.id=match_results.loser) AS matches \
                FROM players LEFT JOIN match_results \
                ON players.id=match_results.winner \
                GROUP BY players.id \
                ORDER BY wins DESC;")
    standings = cur.fetchall()
    # print standings
    DB.close
    return standings


def reportMatch(winner, loser, draw=False):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    DB = connect()
    cur = DB.cursor()
    # cur.execute("UPDATE players set wins=wins+1,matches=matches+1 \
    #             where id=%s", (winner,))
    # cur.execute("UPDATE players set matches=matches+1 where id=%s",
    #             (loser,))
    if draw:
        cur.execute("INSERT INTO match_results (winner,loser) VALUES (%s,%s)",
                    (winner, 0))
        cur.execute("INSERT INTO match_results (winner,loser) VALUES (%s,%s)",
                    (loser, 0))
    else:
        cur.execute("INSERT INTO match_results (winner,loser) VALUES (%s,%s)",
                    (winner, loser))
    DB.commit()
    DB.close


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """

    standings = playerStandings()
    print standings

swissPairings()
