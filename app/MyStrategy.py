# -*- coding: utf-8 -*- 

from model.ActionType import ActionType
from model.Game import Game
from model.Move import Move
from model.Wizard import Wizard
from model.World import World
from model.Faction import Faction

import math

class StrategyState:
    MOVE = 1
    LOW_HP = 2
    VISIBLE_ENEMY = 3
    CAN_CAST = 4
    TURN_TO_TARGET = 5
    ATTACK_TARGET = 6
    MOVE_BACK = 7


   



class MyStrategy:
    def move(self, me, world, game, move):

        """
        @type me: Wizard
        @type world: World
        @type game: Game
        @type move: Move
        """

        self.me = me
        self.world = world
        self.game = game



        move.speed = game.wizard_forward_speed
        move.strafe_speed = game.wizard_strafe_speed
        move.turn = game.wizard_max_turn_angle
        move.action = ActionType.MAGIC_MISSILE

        state = self.current_state(StrategyState.MOVE)

        self.make_action(move, state)

        print(state)

    def current_state (self, state):
        """Определяем текущее состояние по набору состояний"""
        prev_state = None

        print(state)
        rules = self.get_rules()
        while(state!=prev_state):

            for rule in rules:
                if (rule[0] == state):
                    # проверяем сработало правило или нет
                    if rule[3] != None:
                        result = rule[3](*rule[4])
                    else:
                        result = True

                    if rule[2] == result:
                        state = rule[1]
                        print (state)
                        
            prev_state = state 

        return state

    def make_action(self, move, state):
        """Выполняем некоторое действие """

        move.speed = 3
        
        pass

    def get_rules(self):

        near_target = self.get_near_target()

        # проверяем уровень жизни
        check_hp = lambda me: me.life < me.max_life * 0.2
        # проверяем возможность использовать заклинание
        check_cast_range = lambda me, target: abs(me.get_angle_to_unit(near_target)) < me.cast_range

        # описание таблицы переходов

        states = [
        (StrategyState.MOVE,             StrategyState.LOW_HP,             False,       check_hp, [self.me]),
        (StrategyState.MOVE,             StrategyState.VISIBLE_ENEMY,      True,        check_hp, [self.me]),
        (StrategyState.LOW_HP,           StrategyState.MOVE_BACK,          True,        None, None),
        (StrategyState.VISIBLE_ENEMY,    StrategyState.CAN_CAST,           True,        check_cast_range, [self.me, near_target] ),
        (StrategyState.CAN_CAST,         StrategyState.TURN_TO_TARGET,     False,       check_cast_range, [self.me, near_target] ),
        (StrategyState.CAN_CAST,         StrategyState.ATTACK_TARGET,      True,        check_cast_range, [self.me, near_target] ),
        (StrategyState.TURN_TO_TARGET,   None,                             True,        check_cast_range, [self.me, near_target] ),
        (StrategyState.ATTACK_TARGET,    None,                             True,        check_cast_range, [self.me, near_target] ),
        (StrategyState.MOVE_BACK,        None,                             True,        check_cast_range, [self.me, near_target] ),
        
        ]        
    
        return states


    def go_to(self, unit):
        """Простейший способ перемещения волшебника."""
        angle = self.me.get_angle_to_unit(unit)

        self.move.turn = angle

        if( abs(angle) < self.game.staff_sector/4.0):
            self.move.speed = self.game.wizard_forward_speed


    def get_near_target(self):
        """ Определяем ближащую цель"""

        min_dist = None
        near_target = None
        for target in (self.world.bonuses + self.world.minions + self.world.buildings):
            if (target.faction == Faction.NEUTRAL or target.faction == self.me.faction):
                continue

            distance = self.me.get_distance_to_unit(target)

            if (min_dist is None or distance < min_dist):
                min_dist = distance
                near_target = target
        
        return target







class Point2D:
    """Вспомогательный класс для хранения позиций на карте."""
    def __init__(self, x, y):
        """Инициали"""
        self.x = x
        self.y = y 

    def getDistanceTo(self, point):
        return math.hypot(self.x - point.x, self.y - point.y)

