#  ██╗░░░░░██╗███╗░░██╗░██████╗░░░░██████╗░██╗░░░░░░█████╗░░█████╗░██╗░░██╗
#  ██║░░░░░██║████╗░██║██╔════╝░░░░██╔══██╗██║░░░░░██╔══██╗██╔══██╗██║░██╔╝
#  ██║░░░░░██║██╔██╗██║██║░░██╗░░░░██████╦╝██║░░░░░███████║██║░░╚═╝█████═╝░
#  ██║░░░░░██║██║╚████║██║░░╚██╗░░░██╔══██╗██║░░░░░██╔══██║██║░░██╗██╔═██╗░
#  ███████╗██║██║░╚███║╚██████╔╝░░░██████╦╝███████╗██║░░██║╚█████╔╝██║░╚██╗
#  ╚══════╝╚═╝╚═╝░░╚══╝░╚═════╝░░░░╚═════╝░╚══════╝╚═╝░░╚═╝░╚════╝░╚═╝░░╚═╝
#
#  Developed by Yakov V. Panov (C) Ling • Black 2020
#  @site http://ling.black
import datetime
from math import floor

from wow.blizzard.core import blizzard_db
from wow.database.models import CharacterModel, MythicRaceMembersModel, MythicRaceModel


class PlayersActivityUpdater:

    @staticmethod
    def update_player(name):
        db = blizzard_db()
        ch = db.query(CharacterModel).filter(CharacterModel.name == name).first()
        team_races = db.query(MythicRaceMembersModel).filter(MythicRaceMembersModel.name == ch.name).all()
        print('Races found: ' + len(team_races).__str__())
        points = 0
        for team_race in team_races:
            races = db.query(MythicRaceModel).filter(MythicRaceModel.mythic_hash == team_race.mythic_hash).all()
            for race in races:
                print("+ -------------------------------------------+")
                print(f"|           {ch.name}")
                print("+ -------------------------------------------+")
                print(f"| -> {race.name} ({race.level})")
                print(f"| Guild race: {race.guild_race} / 5")
                level_for_race = race.level * race.guild_race
                print(f"| This race score: {level_for_race}")
                points = points + level_for_race
        print("+ -------------------------------------------+")
        print(f"| Mythic score: {points}")

        # time counting
        later_time = datetime.datetime.utcnow()
        time_scores = floor(((later_time - ch.created).total_seconds() / 60.0) / 10000)
        points = points + time_scores

        print(f"| Time score: {time_scores}")
        print(f"| Total score: {points}")
        db.query(CharacterModel).filter(CharacterModel.name == ch.name).update({'activity': points})
        db.commit()

    @staticmethod
    def update():
        db = blizzard_db()
        players = db.query(CharacterModel).all()
        for player in players:
            PlayersActivityUpdater.update_player(player.name)
