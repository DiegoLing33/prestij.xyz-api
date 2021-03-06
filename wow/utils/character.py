#  ██╗░░░░░██╗███╗░░██╗░██████╗░░░░██████╗░██╗░░░░░░█████╗░░█████╗░██╗░░██╗
#  ██║░░░░░██║████╗░██║██╔════╝░░░░██╔══██╗██║░░░░░██╔══██╗██╔══██╗██║░██╔╝
#  ██║░░░░░██║██╔██╗██║██║░░██╗░░░░██████╦╝██║░░░░░███████║██║░░╚═╝█████═╝░
#  ██║░░░░░██║██║╚████║██║░░╚██╗░░░██╔══██╗██║░░░░░██╔══██║██║░░██╗██╔═██╗░
#  ███████╗██║██║░╚███║╚██████╔╝░░░██████╦╝███████╗██║░░██║╚█████╔╝██║░╚██╗
#  ╚══════╝╚═╝╚═╝░░╚══╝░╚═════╝░░░░╚═════╝░╚══════╝╚═╝░░╚═╝░╚════╝░╚═╝░░╚═╝
#
#  Developed by Yakov V. Panov (C) Ling • Black 2020
#  @site http://ling.black

roles = {
    577: 3,
    581: 1,
    102: 4,
    103: 3,
    104: 1,
    105: 2,
    253: 4,
    254: 4,
    255: 4,
    62: 4,
    63: 4,
    64: 4,
    65: 2,
    66: 1,
    70: 3,
    265: 4,
    266: 4,
    267: 4,
    262: 4,
    263: 4,
    264: 2,
    256: 2,
    257: 2,
    258: 4,
    259: 3,
    260: 3,
    261: 3,
    268: 1,
    270: 2,
    269: 3,
    250: 1,
    251: 3,
    252: 3,
    71: 3,
    72: 3,
    73: 1,
    0: 0,
}

role_names = {
    1: 'Tank',
    2: 'Healer',
    3: 'Millie',
    4: 'Range',
}


def get_role_by_spec_id(spec_id):
    return roles[spec_id]


def get_role_name_by_id(role_type):
    return role_names[role_type]


class CharactersSorter:
    """
    Characters sorter utility
    """

    @staticmethod
    def by_name(characters):
        return sorted(characters, key=lambda x: x['name'])

    @staticmethod
    def by_role_id(characters):
        return sorted(characters, key=lambda x: x['role_id'])
