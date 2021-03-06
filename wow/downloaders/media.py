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

from logzero import logger

from progress.bar import Bar

from blizzard.character import blizzard_character_media
from blizzard.core import blizzard_media
from core.url import LSAURL
from config import default_items_images_path, default_characters_images_path


class MediaDownloader:
    """
    Downloads media data from existsing models

    """

    @staticmethod
    def download_items_images(
            items,
            path=default_items_images_path,
            connector=None,
    ):
        """
        Downloads all items images and saves it to the directory
        :param connector:
        :param items:
        :param path:
        :return:
        """
        logger.info("Starting downloading items...")
        logger.info(f"Total count: {len(items)}")
        bar = Bar('Items downloading', max=len(items), fill='█')

        for model in items:
            resp = blizzard_media(f"item/{model.wow_id}")
            url = resp['assets'][0]['value']
            file_data_id = resp['assets'][0]['file_data_id']
            file_path = f'{path}/{file_data_id}.jpg'

            if connector is not None:
                connector(wow_id=model.wow_id, image_id=file_data_id)

            if not os.path.isfile(file_path):
                LSAURL(url).download_file(file_path)
            bar.next()

    @staticmethod
    def download_characters_images(
            characters,
            path=default_characters_images_path,
    ):
        """
        Downloads the character images
        :param characters:
        :param path:
        :return:
        """
        logger.info("Starting downloading characters...")
        logger.info(f"Total count: {len(characters)}")
        bar = Bar('Characters downloading', max=len(characters), fill='█')

        for model in characters:
            try:
                resp = blizzard_character_media(model.name)
                image_avatar = resp['assets'][1]['value']
                image_main = resp['assets'][3]['value']
                save_name = str(model.name).lower()
                LSAURL(image_avatar).download_file(f'{path}/{save_name}_avatar.png')
                LSAURL(image_main).download_file(f'{path}/{save_name}_main.png')
            except KeyError:
                logger.error(model.name + ' not found')
            bar.next()
