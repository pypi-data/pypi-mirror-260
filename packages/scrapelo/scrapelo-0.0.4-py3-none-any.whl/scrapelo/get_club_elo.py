import requests
from bs4 import BeautifulSoup


def get_club_elo(club: str) -> int:
    """
    Returns the current ELO score for a given club.
    """
    response = requests.get(f"http://clubelo.com/{club}")
    if response.status_code != 200:
        raise ValueError("Can't reach the website. Try again later or check for spelling.")

    soup = BeautifulSoup(response.content, 'html.parser')
    elo_paragraph = soup.find(lambda tag: tag.name == 'p' and 'Elo: ' in tag.text)
    if type(elo_paragraph) == type(None):
        raise ValueError("Club not found. Check for spelling.")
    b_tag = elo_paragraph.find('b')
    return int(b_tag.text)
