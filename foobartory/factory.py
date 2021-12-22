from typing import List
from dataclasses import dataclass, field

from foobartory.robot import Robot


@dataclass
class Factory:
    cash = 0
    foos_count: int = 0
    bars_count: int = 0
    foobars_count: int = 0
    robots: List[Robot] = field(default_factory=list)


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