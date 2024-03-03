from .user_agent_data import USER_AGENTS
import random


def random_user_agent():
    return random.choice(USER_AGENTS)
