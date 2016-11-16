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


    def current_state (self, state):
        prev_state = None

        near_target = self.get_near_target()

        while(prev_state != state):

            if state == StrategyState.MOVE:
                if (self.me.life < self.me.max_life * 0.2):
                    state = StrategyState.LOW_HP
                elif (near_target != None):
                    state = StrategyState.VISIBLE_ENEMY
                
            if state == StrategyState.LOW_HP:
                state = StrategyState.MOVE_BACK
                
                
            if state == StrategyState.VISIBLE_ENEMY:
                dist = self.me.get_distance_to_unit(near_target)

                if (self.me.cast_range >= dist):
                    state = StrategyState.CAN_CAST
                                    
            if state == StrategyState.CAN_CAST:
                
                angle = self.me.get_angle_to_unit(near_target)
                if (abs(angle) < self.me.cast_range):
                    state = StrategyState.TURN_TO_TARGET
                else:
                    state = StrategyState.ATTACK_TARGET
               
            if state == StrategyState.TURN_TO_TARGET:
                pass
                
            if state == StrategyState.ATTACK_TARGET:
                pass
                
            if state == StrategyState.MOVE_BACK:
                pass

            prev_state = state

        return state


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

