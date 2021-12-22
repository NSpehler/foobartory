import asyncio
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


    async def work(self):
        """Choose next activity for robot"""
        while len(self.factory.robots) < ROBOT_MAX:
            if self.factory.foos_count >= ROBOT_COST_FOOS and self.factory.cash >= ROBOT_COST_EUROS and not self.factory.buy_lock.locked():
                async with self.factory.buy_lock:
                    await self.buy_robot()
            elif self.factory.foobars_count >= FOOBAR_SELL_MAX and not self.factory.sell_lock.locked():
                async with self.factory.sell_lock:
                    await self.sell_foobars()
            elif self.factory.foos_count >= ROBOT_COST_FOOS and self.factory.bars_count >= 1 and not self.factory.assemble_lock.locked():
                async with self.factory.assemble_lock:
                    await self.assemble_foobars()
            elif self.factory.bars_count < FOOBAR_SELL_MAX:
                await self.mine_bar()
            elif self.factory.foos_count < ROBOT_COST_FOOS:
                await self.mine_foo()

            await asyncio.sleep(0.01)
                    

    async def wait(self, duration):
        await asyncio.sleep(duration * DURATION_MODIFIER)


    @change_activity
    async def mine_foo(self):
        await self.wait(duration=FOO_MINING_TIME)
        self.factory.foos_count += 1


    @change_activity
    async def mine_bar(self):
        duration = uniform(BAR_MINING_TIME_MIN, BAR_MINING_TIME_MAX)
        await self.wait(duration=duration)
        self.factory.bars_count += 1

    
    @change_activity
    async def assemble_foobars(self):
        await self.wait(duration=FOOBAR_ASSEMBLY_TIME)
        self.factory.foos_count -= 1

        success = random() < FOOBAR_ASSEMBLY_SUCCESS_RATE
        if success:
            self.factory.bars_count -= 1
            self.factory.foobars_count += 1

    
    @change_activity
    async def sell_foobars(self):
        await self.wait(duration=FOOBAR_SELL_TIME)
        self.factory.foobars_count -= FOOBAR_SELL_MAX
        self.factory.cash += FOOBAR_SELL_MAX * FOOBAR_SELL_PRICE

    
    @change_activity
    async def buy_robot(self):
        """Buy new robot and start new asynchronous thread"""
        self.factory.cash -= ROBOT_COST_EUROS
        self.factory.foos_count -= ROBOT_COST_FOOS
        
        robot_id = len(self.factory.robots) + 1
        robot = Robot(robot_id=robot_id, factory=self.factory)
        self.factory.robots.append(robot)
        print(f"🏗  Made {len(self.factory.robots)} robots (made by robot #{self.robot_id})")

        if len(self.factory.robots) < ROBOT_MAX:
            self.factory.tasks.append(asyncio.create_task(robot.work()))