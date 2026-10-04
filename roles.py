from enum import Enum

class Role(Enum):
    MIRNY = "mirny"
    DON = "don"
    MAFIA = "mafia"
    KOMISSAR = "komissar"
    SERZHANT = "serzhant"
    DOKTOR = "doktor"
    MANYAK = "manyak"
    LYUBOVNITSA = "lyubovnitsa"
    ADVOKAT = "advokat"
    SAMOUBIYTSA = "samoubiytsa"
    BOMZH = "bomzh"
    SCHASTLIVCHIK = "schastlivchik"
    KAMIKADZE = "kamikadze"

ROLE_KEYS = {
    Role.MIRNY: "role_mirny", Role.DON: "role_don", Role.MAFIA: "role_mafia",
    Role.KOMISSAR: "role_komissar", Role.SERZHANT: "role_serzhant",
    Role.DOKTOR: "role_doktor", Role.MANYAK: "role_manyak",
    Role.LYUBOVNITSA: "role_lyubovnitsa", Role.ADVOKAT: "role_advokat",
    Role.SAMOUBIYTSA: "role_samoubiytsa", Role.BOMZH: "role_bomzh",
    Role.SCHASTLIVCHIK: "role_schastlivchik", Role.KAMIKADZE: "role_kamikadze",
}

def get_roles_for_player_count(count: int) -> list:
    roles = [Role.DON, Role.MAFIA, Role.DOKTOR]
    if count >= 6: roles.append(Role.KOMISSAR)
    if count >= 8: roles += [Role.KAMIKADZE, Role.BOMZH]
    if count >= 10: roles.append(Role.LYUBOVNITSA)
    if count >= 12: roles.append(Role.SERZHANT)
    if count >= 14: roles.append(Role.MANYAK)
    if count >= 16: roles.append(Role.ADVOKAT)
    while len(roles) < count:
        roles.append(Role.MIRNY)
    return roles[:count]
