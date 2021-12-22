from functools import wraps

from foobartory.config import ROBOT_CHANGE_ACTIVITY_TIME


def change_activity(activity):
    """Wait if robot needs to change activity, and register current activity in state"""
    @wraps(activity)
    def wrapper(self, *args, **kwargs):
        if self.current_activity is not None and self.current_activity != activity.__name__:
            self.wait(duration=ROBOT_CHANGE_ACTIVITY_TIME)

        self.current_activity = activity.__name__
        return activity(self, *args, **kwargs)

    return wrapper