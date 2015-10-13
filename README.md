# udacity-tournament-results-database

# Udacity Tournament Results Database Project

What this is about?
-------------------

This is a simple database project developed as part of the Udacity Full Stack course. My objective was to setup a database schema and various python methods that would allow for the management of a tournament that uses a Swiss Style Scoring and record keeping system.


How do I use this?
------------------

Quick usage:

Note: Assumption here is that you already have psql insatlled 1.9+ installed in your environment.

1. Clone the repository
2. Use CLI to run the `psql => \i tournament.sql` command. This will setup the database and required tables.
3. Run the test file in an IDE or on CLI via `python tournament_test.py` to test that the application is running. The output should be the following
`
1. Old matches can be deleted.
2. Player records can be deleted.
3. After deleting, countPlayers() returns zero.
4. After registering a player, countPlayers() returns 1.
5. Players can be registered and deleted.
6. Newly registered players appear in the standings with no matches.
7. After a match, players have updated standings.
8. After one match, players with one win are paired.
Success!  All tests pass!`

4. The aboove output is a good indicator that the python program `tournament.py` is fully functinoal.
5. From here on you can import tournament.py into your program of choice and call the various methods to manage a Swiss Style Scoring tournament. For example
	-to add a player named Bruce Lee call the function registerPlayer('Bruce Lee'). This will add the player to the database.
	-to report a match's results, call the function reportMatch(winner, loser) where winner and loser are the players ids.
6. Use the docstrings in 
