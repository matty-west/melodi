import requests
from bs4 import BeautifulSoup

def get_upcoming_albums(url):
    """
    Scrapes Genius's album release calendar for upcoming albums.

    Args:
        url (str): The URL of the Genius album release calendar.

    Returns:
        list: A list of dictionaries, where each dictionary
              contains the album name, artist, and release date.
    """

    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    albums = []
    # More specific CSS selector
    for li in soup.select("article > ul.release_calendar li"):
        album_artist = li.find("h3").text.strip()
        try:
            album_name, artist = album_artist.split(" - ", 1)
        except ValueError:
            # Handle cases where the artist is not available
            album_name = album_artist
            artist = "N/A"
        release_date_str = li.find("div", class_="date").text.strip()
        # Extract the release date (e.g., '11/1')
        release_date = release_date_str.split(" ")[0]

        albums.append({
            "album": album_name,
            "artist": artist,
            "release_date": release_date
        })

    return albums

if __name__ == "__main__":
    url = "https://genius.com/Genius-november-2024-album-release-calendar-annotated"
    upcoming_albums = get_upcoming_albums(url)

    # Print the results in a formatted table
    print("|Album|Artist|Release Date|")
    print("|---|---|---|")
    for album in upcoming_albums:
        print(f"|{album['album']}|{album['artist']}|{album['release_date']}|")