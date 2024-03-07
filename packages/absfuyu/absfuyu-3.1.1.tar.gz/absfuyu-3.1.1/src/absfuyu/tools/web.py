"""
Absfuyu: Web
------------
Web, ``request``, ``BeautifulSoup`` stuff

Version: 1.0.1
Date updated: 24/11/2023 (dd/mm/yyyy)
"""


# Library
###########################################################################
from bs4 import BeautifulSoup
import requests

from absfuyu.logger import logger


# Function
###########################################################################
def soup_link(link: str) -> BeautifulSoup:
    """
    ``BeautifulSoup`` the link

    Parameters
    ----------
    link : str
        Link to BeautifulSoup

    Returns
    -------
    BeautifulSoup
        ``BeautifulSoup`` instance
    """
    try:
        page = requests.get(link)
        soup = BeautifulSoup(page.content, "html.parser")
        logger.debug("Soup completed!")
        return soup
    except:
        logger.error("Can't soup")
        raise SystemExit("Something wrong")


def gen_random_commit_msg() -> str:
    """
    Generate random commit message

    :returns: Random commit message
    :rtype: str
    """
    out = soup_link("https://whatthecommit.com/").get_text()[34:-20]
    logger.debug(out)
    return out


# Run
###########################################################################
if __name__ == "__main__":
    logger.setLevel(10)
    gen_random_commit_msg()
