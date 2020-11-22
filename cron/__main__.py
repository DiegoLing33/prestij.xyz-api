#  ██╗░░░░░██╗███╗░░██╗░██████╗░░░░██████╗░██╗░░░░░░█████╗░░█████╗░██╗░░██╗
#  ██║░░░░░██║████╗░██║██╔════╝░░░░██╔══██╗██║░░░░░██╔══██╗██╔══██╗██║░██╔╝
#  ██║░░░░░██║██╔██╗██║██║░░██╗░░░░██████╦╝██║░░░░░███████║██║░░╚═╝█████═╝░
#  ██║░░░░░██║██║╚████║██║░░╚██╗░░░██╔══██╗██║░░░░░██╔══██║██║░░██╗██╔═██╗░
#  ███████╗██║██║░╚███║╚██████╔╝░░░██████╦╝███████╗██║░░██║╚█████╔╝██║░╚██╗
#  ╚══════╝╚═╝╚═╝░░╚══╝░╚═════╝░░░░╚═════╝░╚══════╝╚═╝░░╚═╝░╚════╝░╚═╝░░╚═╝
#
#  Developed by Yakov V. Panov (C) Ling • Black 2020
#  @site http://ling.black
import logging
import time
import sys
from datetime import datetime

import logzero

from wow.updater import GuildUpdater, CharacterUpdater, MediaUpdater, PlayersActivityUpdater
from wow.updater.mythic import MythicUpdater


def has_arg(a: str):
    return a in sys.argv


def run_cron_operation():
    """
    Operation what needs to do every hour min
    :return:
    """

    logzero.logfile(f"static/logs/{datetime.now().strftime('%d.%m.%Y-%H:%M:%S')}-rotating.log", maxBytes=1e6, backupCount=3)

    # Update info first
    if has_arg('info') or has_arg('guild') or has_arg('force__all'):
        GuildUpdater.update_info()
        time.sleep(1)

    # Then update players
    if has_arg('characters') or has_arg('guild') or has_arg('force__all'):
        CharacterUpdater.update_characters()
        time.sleep(1)

    # Then update players mythic
    if has_arg('mythic') or has_arg('guild') or has_arg('force__all'):
        MythicUpdater.update_characters_mythic()
        time.sleep(1)

    # Then update players activity
    if has_arg('activity') or has_arg('guild') or has_arg('force__all'):
        PlayersActivityUpdater.update()
        time.sleep(1)

    # And for the end update images
    if has_arg('avatars') or has_arg('media') or has_arg('force__all'):
        MediaUpdater.update_characters_images()
        time.sleep(1)

    if has_arg('items') or has_arg('media') or has_arg('force__all'):
        MediaUpdater.update_items_images()
        time.sleep(1)


if __name__ == "__main__":
    run_cron_operation()
    pass
