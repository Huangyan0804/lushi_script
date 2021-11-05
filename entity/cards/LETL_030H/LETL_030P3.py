# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_030P3(SpellEntity):
    """
        热力迸发
        造成12点伤害。下回合你的火焰技能速度值加快（1）点
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 12
        self.range = 1

    def play(self, hero, target):
        power = self.game_entity.get_spell_power(self.spell_school, hero.own)

        target.got_damage((self.damage + power) * self.damage_advantage[self.lettuce_role][target.lettuce_role])
