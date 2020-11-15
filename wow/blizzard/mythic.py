#  ██╗░░░░░██╗███╗░░██╗░██████╗░░░░██████╗░██╗░░░░░░█████╗░░█████╗░██╗░░██╗
#  ██║░░░░░██║████╗░██║██╔════╝░░░░██╔══██╗██║░░░░░██╔══██╗██╔══██╗██║░██╔╝
#  ██║░░░░░██║██╔██╗██║██║░░██╗░░░░██████╦╝██║░░░░░███████║██║░░╚═╝█████═╝░
#  ██║░░░░░██║██║╚████║██║░░╚██╗░░░██╔══██╗██║░░░░░██╔══██║██║░░██╗██╔═██╗░
#  ███████╗██║██║░╚███║╚██████╔╝░░░██████╦╝███████╗██║░░██║╚█████╔╝██║░╚██╗
#  ╚══════╝╚═╝╚═╝░░╚══╝░╚═════╝░░░░╚═════╝░╚══════╝╚═╝░░╚═╝░╚════╝░╚═╝░░╚═╝
#
#  Developed by Yakov V. Panov (C) Ling • Black 2020
#  @site http://ling.black
from urllib.parse import quote

from wow.blizzard.core import default_params, blizzard_request
from config import server_slug, mythic_season


def blizzard_character_mythic_keystone_profile(
        name: str,
        server: str = server_slug,
        data=default_params,
        sleep: int = 10
):
    """
    Returns the character equipment information
    :param name:
    :param server:
    :param data:
    :param sleep:
    :return:
    """
    name = quote(name.lower())
    return blizzard_request(
        f"profile/wow/character/{server}/{name}/mythic-keystone-profile",
        data,
        sleep
    )


def blizzard_character_mythic_keystone_profile_season(
        name: str,
        server: str = server_slug,
        data=default_params,
        season=mythic_season,
        sleep: int = 10
):
    """
    Returns the character equipment information
    :param season:
    :param name:
    :param server:
    :param data:
    :param sleep:
    :return:
    """
    name = quote(name.lower())
    return blizzard_request(
        f"profile/wow/character/{server}/{name}/mythic-keystone-profile/season/{season}",
        data,
        sleep
    )
