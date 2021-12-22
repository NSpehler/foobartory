import asyncio
from time import perf_counter, gmtime, strftime

from foobartory.robot import Robot
from foobartory.factory import Factory
from foobartory.config import DURATION_MODIFIER, ROBOT_MIN, ROBOT_MAX


async def start():
    factory = Factory()
    start = perf_counter()
    
    print(f"🚀 Initializing robots")
    for robot_id in range(ROBOT_MIN):
        robot = Robot(robot_id=robot_id + 1, factory=factory)
        factory.robots.append(robot)

    print(f"🏗  Making new robots")
    await factory.start()

    factory.stop()
    end = perf_counter()
    duration = get_duration(start=start, end=end)

    print(f"🏁 Made {len(factory.robots)} robots in {duration}")
    print(factory)
    return True


def get_duration(start, end):
    """Get actual duration regardless of duration modifier"""
    time_total = (end - start) / DURATION_MODIFIER
    time_total = strftime("%H:%M:%S", gmtime(time_total))

    return time_total


if __name__ == "__main__":
    asyncio.run(start())