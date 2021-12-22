from time import sleep
from typing import TYPE_CHECKING
from random import random, uniform

from foobartory.config import *
from foobartory.decorators import change_activity

if TYPE_CHECKING:
    from foobartory.factory import Factory


class Robot:
    def __init__(self, robot_id: int, factory: "Factory"):
        self.robot_id: int = robot_id
        self.factory: Factory = factory
        self.current_activity: str = None


    def __repr__(self):
        return str(self.robot_id)


    def work(self):
        """Choose next activity for robot"""
        if self.factory.foos_count >= ROBOT_COST_FOOS and self.factory.cash >= ROBOT_COST_EUROS:
            self.buy_robot()
        elif self.factory.foobars_count >= FOOBAR_SELL_MAX:
            self.sell_foobars()
        elif self.factory.foos_count > ROBOT_COST_FOOS and self.factory.bars_count >= 1:
            self.assemble_foobars()
        elif self.factory.foos_count < self.factory.bars_count:
            self.mine_foo()
        else:
            self.mine_bar()
            

    def wait(self, duration):
        sleep(duration * DURATION_MODIFIER)


    @change_activity
    def mine_foo(self):
        self.wait(duration=FOO_MINING_TIME)
        self.factory.foos_count += 1


    @change_activity
    def mine_bar(self):
        duration = uniform(BAR_MINING_TIME_MIN, BAR_MINING_TIME_MAX)
        self.wait(duration=duration)
        self.factory.bars_count += 1

    
    @change_activity
    def assemble_foobars(self):
        self.wait(duration=FOOBAR_ASSEMBLY_TIME)
        self.factory.foos_count -= 1

        success = random() < FOOBAR_ASSEMBLY_SUCCESS_RATE
        if success:
            self.factory.bars_count -= 1
            self.factory.foobars_count += 1

    
    @change_activity
    def sell_foobars(self):
        self.wait(duration=FOOBAR_SELL_TIME)
        self.factory.foobars_count -= FOOBAR_SELL_MAX
        self.factory.cash += FOOBAR_SELL_MAX * FOOBAR_SELL_PRICE

    
    @change_activity
    def buy_robot(self):
        self.factory.cash -= ROBOT_COST_EUROS
        self.factory.foos_count -= ROBOT_COST_FOOS
        
        robot_id = len(self.factory.robots) + 1
        robot = Robot(robot_id=robot_id, factory=self.factory)
        self.factory.robots.append(robot)
        print(f"🏗  Made {len(self.factory.robots)} robots (made by robot #{self.robot_id})")