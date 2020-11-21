#  ██╗░░░░░██╗███╗░░██╗░██████╗░░░░██████╗░██╗░░░░░░█████╗░░█████╗░██╗░░██╗
#  ██║░░░░░██║████╗░██║██╔════╝░░░░██╔══██╗██║░░░░░██╔══██╗██╔══██╗██║░██╔╝
#  ██║░░░░░██║██╔██╗██║██║░░██╗░░░░██████╦╝██║░░░░░███████║██║░░╚═╝█████═╝░
#  ██║░░░░░██║██║╚████║██║░░╚██╗░░░██╔══██╗██║░░░░░██╔══██║██║░░██╗██╔═██╗░
#  ███████╗██║██║░╚███║╚██████╔╝░░░██████╦╝███████╗██║░░██║╚█████╔╝██║░╚██╗
#  ╚══════╝╚═╝╚═╝░░╚══╝░╚═════╝░░░░╚═════╝░╚══════╝╚═╝░░╚═╝░╚════╝░╚═╝░░╚═╝
#
#  Developed by Yakov V. Panov (C) Ling • Black 2020
#  @site http://ling.black
import math
from hashlib import md5

from blizzard.mythic import blizzard_character_mythic_keystone_profile_season
from wow.utils.character import roles, CharactersSorter


class MythicHashUtils:
    @staticmethod
    def affixes(afs):
        """
        Creates affixes hash
        :param afs:
        :return:
        """
        s = ''
        for a in afs:
            s += (str(a['wow_id']) + a['name'])
        return md5(s.encode()).hexdigest()

    @staticmethod
    def team(members):
        """
        Creates team hash
        :param members:
        :return:
        """
        s = ''
        sorted_members = CharactersSorter.by_name(members)
        for a in sorted_members:
            s += (str(a['wow_id']) + a['name'])
        return md5(s.encode()).hexdigest()

    @staticmethod
    def mythic(mythic):
        """
        Creates mythic hash
        :param mythic:
        :return:
        """
        return md5((
                           str(mythic['wow_dung_id']) +
                           mythic['hashes']['team'] +
                           mythic['hashes']['affixes'] +
                           str(mythic['keystone_level']) +
                           str(mythic['completed'])
                   ).encode()).hexdigest()


def reformat_profile_mythic_time(time):
    duration_in_seconds = time / 1000
    dur = ''

    days = math.floor(duration_in_seconds / 86400)
    duration_in_seconds -= days * 86400

    hours = math.floor(duration_in_seconds / 3600)
    duration_in_seconds -= hours * 3600

    minutes = math.floor(duration_in_seconds / 60)
    seconds = duration_in_seconds - minutes * 60
    seconds = math.floor(seconds)

    dur += ('0' + str(hours) if hours < 10 else str(hours)) + ':'
    dur += ('0' + str(minutes) if minutes < 10 else str(minutes)) + ':'
    dur += ('0' + str(seconds) if seconds < 10 else str(seconds))

    return dur


def reformat_profile_mythic(data):
    best = []
    if 'best_runs' in data:
        best = data['best_runs']
    arr = []
    for item in best:
        res = {
            'wow_dung_id': item['dungeon']['id'],
            'name': item["dungeon"]["name"],
            'keystone_level': item["keystone_level"],
            'keystone_affixes': list(map(lambda a: {'wow_id': a['id'], 'name': a['name']}, item['keystone_affixes'])),
            'completed': item['completed_timestamp'],
            'duration': {
                'time': item['duration'],
                'format': reformat_profile_mythic_time(item['duration'])
            },
            'members': list(map(lambda a: {
                'wow_id': a["character"]["id"],
                'name': a["character"]["name"],
                'spec': {
                    'wow_id': a["specialization"]["id"],
                },
                'role_id': roles[a["specialization"]["id"]],
            }, item['members'])),
            'done_in_time': item['is_completed_within_time'],
            'hashes': {
                'affixes': '',
                'team': '',
                'mythic': '',
            }
        }
        res['hashes']['affixes'] = MythicHashUtils.affixes(res['keystone_affixes'])
        res['hashes']['team'] = MythicHashUtils.team(res['members'])
        res['hashes']['mythic'] = MythicHashUtils.mythic(res)

        res['members'] = CharactersSorter.by_role_id(res['members'])
        arr.append(res)
    return arr


class MythicUtils:

    @staticmethod
    def get_profile_mythic(
            name: str
    ):
        data = blizzard_character_mythic_keystone_profile_season(name=name, season=4)
        return reformat_profile_mythic(data)
