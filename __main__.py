#  ██╗░░░░░██╗███╗░░██╗░██████╗░░░░██████╗░██╗░░░░░░█████╗░░█████╗░██╗░░██╗
#  ██║░░░░░██║████╗░██║██╔════╝░░░░██╔══██╗██║░░░░░██╔══██╗██╔══██╗██║░██╔╝
#  ██║░░░░░██║██╔██╗██║██║░░██╗░░░░██████╦╝██║░░░░░███████║██║░░╚═╝█████═╝░
#  ██║░░░░░██║██║╚████║██║░░╚██╗░░░██╔══██╗██║░░░░░██╔══██║██║░░██╗██╔═██╗░
#  ███████╗██║██║░╚███║╚██████╔╝░░░██████╦╝███████╗██║░░██║╚█████╔╝██║░╚██╗
#  ╚══════╝╚═╝╚═╝░░╚══╝░╚═════╝░░░░╚═════╝░╚══════╝╚═╝░░╚═╝░╚════╝░╚═╝░░╚═╝
#
#  Developed by Yakov V. Panov (C) Ling • Black 2020
#  @site http://ling.black

#  ██╗░░░░░██╗███╗░░██╗░██████╗░░░░██████╗░██╗░░░░░░█████╗░░█████╗░██╗░░██╗
#  ██║░░░░░██║████╗░██║██╔════╝░░░░██╔══██╗██║░░░░░██╔══██╗██╔══██╗██║░██╔╝
#  ██║░░░░░██║██╔██╗██║██║░░██╗░░░░██████╦╝██║░░░░░███████║██║░░╚═╝█████═╝░
#  ██║░░░░░██║██║╚████║██║░░╚██╗░░░██╔══██╗██║░░░░░██╔══██║██║░░██╗██╔═██╗░
#  ███████╗██║██║░╚███║╚██████╔╝░░░██████╦╝███████╗██║░░██║╚█████╔╝██║░╚██╗
#  ╚══════╝╚═╝╚═╝░░╚══╝░╚═════╝░░░░╚═════╝░╚══════╝╚═╝░░╚═╝░╚════╝░╚═╝░░╚═╝
#
#  Developed by Yakov V. Panov (C) Ling • Black 2020
#  @site http://ling.black
import os
import time

import pyfiglet
import enquiries
import uvicorn

from config import app_server, app_port
from database import engine, Base
from wow.updater.activity import PlayersActivityUpdater
from wow.updater.mythic import MythicUpdater
from wow.updater.static import StaticUpdater
from wow.updater import MediaUpdater, CharacterUpdater
from wow.updater.guild import GuildUpdater
from wow.utils.installer import wow_install

Base.metadata.create_all(bind=engine)


def print_header():
    os.system('clear')
    print()
    print(pyfiglet.figlet_format("Prestij"))
    print('     WoW Guild Prestij (C)')
    print()


def menu_press_enter():
    print()
    input('[ Press Enter to continue... ]')


def menu_press_enter_and_back():
    input('[ Press Enter to continue... ]')
    menu_root()


def menu_updater():
    print_header()
    options = [
        'Static data, like classes, races, etc',
        'Only guild information',
        'Only guild members',
        'Only guild members mythic',
        'Only guild members activity',
        'All dynamic data'
        'Everything at all!',
        'I want to back',
    ]
    choice = enquiries.choose('What r u wanna to update?: ', options)
    print(choice)
    if choice is options[0]:
        StaticUpdater.update_classes()
        StaticUpdater.update_races()
        StaticUpdater.update_specs()
        return menu_press_enter_and_back()
    if choice is options[1]:
        GuildUpdater.update_info()
        return menu_press_enter_and_back()
    if choice is options[2]:
        CharacterUpdater.update_characters()
        return menu_press_enter_and_back()
    if choice is options[3]:
        MythicUpdater.update_characters_mythic()
        return menu_press_enter_and_back()
    if choice is options[4]:
        PlayersActivityUpdater.update()
        return menu_press_enter_and_back()
    if choice is options[5]:
        GuildUpdater.update_info()
        time.sleep(1)
        CharacterUpdater.update_characters()
        time.sleep(1)
        MythicUpdater.update_characters_mythic()
        return menu_press_enter_and_back()
    if choice is options[6]:
        return menu_press_enter_and_back()
    if choice is options[7]:
        menu_root()


def menu_downloader():
    print_header()
    options = [
        'I want to download everything!',
        'Only guild members avatar',
        'Only guild members equipment items',
        'I want to back',
    ]
    choice = enquiries.choose('What r u wanna to download?: ', options)
    print(choice)
    if choice is options[0]:
        MediaUpdater.update_characters_images()
        MediaUpdater.update_items_images()
        return menu_press_enter_and_back()
    if choice is options[1]:
        MediaUpdater.update_characters_images()
        return menu_press_enter_and_back()
    if choice is options[2]:
        MediaUpdater.update_items_images()
        return menu_press_enter_and_back()
    if choice is options[3]:
        menu_root()


def menu_single():
    print_header()
    options = [
        'I want to update ...',
        'I want to update mythic of ...',
        'I want to add guild role to ...',
        'I want to add meta to ...',
        'I want to back'
    ]
    choice = enquiries.choose('What r u wanna do?: ', options)
    name = enquiries.freetext('Character name: ')
    if choice is options[0]:
        CharacterUpdater.update_character(name)
        return menu_press_enter_and_back()
    if choice is options[1]:
        MythicUpdater.update_mythic_character(name)
        return menu_press_enter_and_back()
    if choice is options[2]:
        role = enquiries.freetext("Type guild role: ")
        CharacterUpdater.update_guild_role(name, int(role))
        return menu_press_enter_and_back()
    if choice is options[3]:
        meta = enquiries.freetext("Type meta text: ")
        CharacterUpdater.update_meta(name, meta)
        return menu_press_enter_and_back()
    if choice is options[4]:
        menu_root()
    pass


def menu_root():
    print_header()
    options = [
        'I want to update ...',
        'I want to download ...',
        'I want to do standard cron operations',
        'I see it first time (install)',
        'I want to single update',
        'I want to run web server',
        'I want to quit'
    ]
    choice = enquiries.choose('What r u wanna do?: ', options)
    print(choice)
    if choice is options[0]:
        menu_updater()
    if choice is options[1]:
        menu_downloader()
    if choice is options[4]:
        menu_single()
    if choice is options[5]:
        uvicorn.run("server:app", host=app_server, port=app_port, reload=True)
    if choice is options[6]:
        quit()


wow_install()
menu_root()
