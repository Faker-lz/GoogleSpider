"""
:Get data
@author: lingzhi
* @date 2021/10/9 10:31
"""
import os.path
import random
from setting import USER_AGENT


def get_random_user_agent() -> str:
    """
    Get a random user agent string
    :return:
    """
    return random.choice(get_data('user_agents.txt', USER_AGENT))


def get_data(filename: str, default='') -> list:
    """
    Get data from a file
    :param filename:
    :param default:
    :return: List
    """
    root_folder = os.path.dirname(__file__)
    user_file = os.path.join(
        os.path.join(root_folder, 'dict'), filename
    )
    try:
        with open(user_file) as fp:
            data = [_.strip() for _ in fp.readlines()]
    except:
        data = [default]
    return data


if __name__ == '__main__':
    print(get_random_user_agent())