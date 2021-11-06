# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_022P4(SpellEntity):
    """
        强能奥术飞弹5
        随机对敌人发射三枚飞弹，每枚飞弹造成$15点伤害。0对生命值最低的敌人发射三枚飞弹，每枚飞弹造成$15点伤害。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0
        self.range = 1

    def play(self, game, hero, target):
        pass

