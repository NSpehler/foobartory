import asyncio
from typing import List
from dataclasses import dataclass, field

from foobartory.robot import Robot


@dataclass
class Factory:
    """Initialize factory and its storage, including locks to prevent robots to perform the same tasks at the same time"""
    cash = 0
    foos_count: int = 0
    bars_count: int = 0
    foobars_count: int = 0
    robots: List[Robot] = field(default_factory=list)
    tasks: list = field(default_factory=list)
    buy_lock = asyncio.Lock()
    sell_lock = asyncio.Lock()
    assemble_lock = asyncio.Lock()


    def __repr__(self):
        state = f"""
🏭 Foobartory store:
🔧 {self.foos_count} foos
🔩 {self.bars_count} bars
🦾 {self.foobars_count} foobars 
🤖 {len(self.robots)} robots
💰 {self.cash}€
        """

        return state


    async def start(self):
        """Start initial robots asyncronously"""
        self.tasks = [asyncio.create_task(robot.work()) for robot in self.robots]
        await asyncio.gather(*self.tasks)


    def stop(self):
        """Stop all running asynchronous tasks"""
        for task in self.tasks:
            task.cancel()