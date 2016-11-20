# -*- coding: utf-8 -*- 

from model.ActionType import ActionType
from model.Game import Game
from model.Move import Move
from model.Wizard import Wizard
from model.World import World
from model.Faction import Faction

import math

class StrategyState:
    MOVE = 10
    LOW_HP = 20
    VISIBLE_ENEMY = 30
    CAN_CAST = 40
    TURN_TO_TARGET = 50
    ATTACK_TARGET = 60
    MOVE_BACK = 70
    MOVE_TO_WAYPOINT = 80

    @staticmethod
    def desc(state):
        """Описание методов, которые """
        r = {
        StrategyState.MOVE             : ("MOVE", "Шаг вперед"),
        StrategyState.LOW_HP           : ("LOW_HP", "Мало жизни"),
        StrategyState.VISIBLE_ENEMY    : ("VISIBLE_ENEMY", "Видим врага"),
        StrategyState.CAN_CAST         : ("CAN_CAST", "Могу колдавать"),
        StrategyState.TURN_TO_TARGET   : ("TURN_TO_TARGET", "Поворачиваемся к врагу"),
        StrategyState.ATTACK_TARGET    : ("ATTACK_TARGET", "Аттакуем цель"),
        StrategyState.MOVE_BACK        : ("MOVE_BACK", "Двигаемся назад"),
        StrategyState.MOVE_TO_WAYPOINT : ("MOVE_TO_WAYPOINT", "Двигаемся к башне"),
        }

        return r[state] if state in r else ("","")

    @staticmethod
    def print_state(state, tab = ""):
        """Выводим на экран описание метода """
        print ((tab + "%20s: %s") % StrategyState.desc(state) )


class MyStrategy:
    
    WAYPOINT_RADIUS = 100.0
    LOW_HP_FACTOR = 0.25


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

        state = self.current_state(StrategyState.MOVE)

        self.make_action(move, state)

    def current_state (self, state):
        """Определяем текущее состояние по набору состояний"""
        prev_state = None

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
                        
            prev_state = state 

        return state

    def make_action(self, move, state):
        StrategyState.print_state(state)        
#            move.speed = self.game.wizard_forward_speed
#            move.strafe_speed = self.game.wizard_strafe_speed
#            move.turn = self.game.wizard_max_turn_angle
#            move.action = ActionType.MAGIC_MISSILE



        """Выполняем некоторое действие """

        if StrategyState.MOVE_TO_WAYPOINT == state:
            next_viewpoint = self.get_next_waypoint()
            map_size = self.game.map_size
            angle = self.me.get_angle_to_unit(next_viewpoint)
            move.turn = angle
            if( abs(angle) < self.game.staff_sector/4.0):
                move.speed = self.game.wizard_forward_speed

        else:
            print ("movements not found")
        pass

    def get_rules(self):

        near_target = self.get_near_target()

        # проверяем уровень жизни
        check_hp = lambda me: me.life < me.max_life * 0.2

        # есть ли враг рядом
        check_target = lambda t: t != None

        # можем ли мы его аттаковать
        check_cast_range = lambda me, target: me.get_distance_to_unit(near_target) < me.cast_range

        # проверяем возможность использовать заклинание
        check_cast_angle = lambda me, target: abs(me.get_angle_to_unit(near_target)) < me.cast_range

        # описание таблицы переходов

        states = [
        (StrategyState.MOVE,             StrategyState.LOW_HP,             True,        check_hp, [self.me]),
        (StrategyState.MOVE,             StrategyState.VISIBLE_ENEMY,      True,        check_cast_range, [self.me, near_target]),
        (StrategyState.MOVE,             StrategyState.MOVE_TO_WAYPOINT,   True,        None, None),
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


    def lane(self):
        map_size = self.game.map_size
        # LaneType.Middle
        l = [
        Point2D(80.0, map_size - 100.0),
        Point2D(120.0, map_size - 400.0),
        Point2D(200.0, map_size - 800.0),
        Point2D(200.0, map_size * 0.75),
        Point2D(200.0, map_size * 0.5),
        Point2D(200.0, map_size * 0.25),
        Point2D(200.0, 200.0),
        Point2D(map_size * 0.25, 200.0),
        Point2D(map_size * 0.5, 200.0),
        Point2D(map_size * 0.75, 200.0),
        Point2D(map_size - 200.0, 200.0)        
        ] 
        return l

    def get_next_waypoint(self):
        waypoints = self.lane()

        for waypoint_index in range(0,len(waypoints) - 1):
            
            if(self.me.get_distance_to_unit(waypoints[waypoint_index]) <= self.WAYPOINT_RADIUS):
                return waypoints[waypoint_index + 1]
        return waypoints[-1]





class Point2D:
    """Вспомогательный класс для хранения позиций на карте."""
    def __init__(self, x, y):
        """Инициали"""
        self.x = x
        self.y = y 

    def getDistanceTo(self, point):
        return math.hypot(self.x - point.x, self.y - point.y)

