# PyTMDb

A modern, type-safe Python client for The Movie Database (TMDb) API.

## Features

- 🎬 **Comprehensive Coverage**: Support for movies, TV series, seasons, episodes, and collections
- 🔍 **Powerful Search**: Search across movies, TV series, and multi-media content
- 📊 **Discovery & Filtering**: Discover content with advanced filters
- 🎯 **Type-Safe**: Built with Pydantic models for type safety and validation
- 📄 **Pagination**: Built-in paginator for handling large result sets
- 🖼️ **Media Support**: Access images, videos, and credits for all content types
- 🔑 **Flexible Authentication**: Supports both API keys and bearer tokens
- 🌍 **Multi-language**: Language support for localized content

## Installation

```bash
pip install pytmdb
```

Or using Poetry:

```bash
poetry add pytmdb
```

## Requirements

- Python 3.13 or higher
- httpx >= 0.28.1
- pydantic >= 2.12.3

## Quick Start

### Authentication

First, you'll need a TMDb API key or bearer token. You can obtain one by creating an account at [TMDb](https://www.themoviedb.org/) and visiting your API settings.

```python
from pytmdb import TMDbClient

# Using an API key
client = TMDbClient(api_key="your_api_key_here")

# Or using a bearer token
client = TMDbClient(bearer_token="your_bearer_token_here")

# With language preference
client = TMDbClient(api_key="your_api_key_here", language="en-US")
```

### Basic Usage

```python
from pytmdb import TMDbClient

client = TMDbClient(api_key="your_api_key_here")

# Search for movies
movies = client.search_movies("The Matrix")
results = movies.get_data()
for movie in results:
    print(f"{movie.title} ({movie.release_date.year if movie.release_date else 'N/A'})")
    print(f"  Rating: {movie.vote_average}/10")
    print(f"  Poster: {movie.poster_url}")

# Get popular movies
popular = client.popular_movies()
for movie in popular.get_data():
    print(movie.title)

# Get movie details
movie_details = client.movie_detail(603)  # The Matrix
print(f"Title: {movie_details.title}")
print(f"Runtime: {movie_details.runtime} minutes")
print(f"Budget: ${movie_details.budget:,}")
print(f"Revenue: ${movie_details.revenue:,}")
```

## Usage Examples

### Searching

#### Search Movies

```python
# Basic movie search
movies = client.search_movies("Inception")
results = movies.get_data()

# Search with filters
movies = client.search_movies(
    query="The Dark Knight",
    year=2008,
    include_adult=False
)

# Navigate through pages
page1 = movies.get_data()
page2 = movies.next_page()
```

#### Search TV Series

```python
# Basic TV series search
shows = client.search_tv_series("Breaking Bad")
results = shows.get_data()

# Search with year filter
shows = client.search_tv_series(
    query="Game of Thrones",
    first_air_date_year=2011
)
```

#### Multi-Search

```python
# Search across movies, TV series, and people
results = client.search_multi("Tom Hanks", page=1)
print(results)  # Returns raw JSON data
```

### Discovery

#### Discover Movies

```python
# Discover movies with filters
movies = client.discover_movies({
    "with_genres": "28,12",  # Action & Adventure
    "primary_release_year": 2023,
    "sort_by": "popularity.desc",
    "vote_average.gte": 7.0
})

for movie in movies.get_data():
    print(f"{movie.title} - {movie.vote_average}/10")
```

#### Discover TV Series

```python
# Discover TV series
shows = client.discover_tv_series({
    "with_genres": "18",  # Drama
    "first_air_date_year": 2023,
    "sort_by": "vote_average.desc"
})

for show in shows.get_data():
    print(f"{show.name} - {show.vote_average}/10")
```

### Popular & Top Rated Content

```python
# Popular movies
popular_movies = client.popular_movies()
for movie in popular_movies.get_data():
    print(movie.title)

# Top rated movies
top_movies = client.top_rated_movies()
for movie in top_movies.get_data():
    print(f"{movie.title} - {movie.vote_average}/10")

# Upcoming movies
upcoming = client.upcoming_movies()
for movie in upcoming.get_data():
    print(f"{movie.title} - {movie.release_date}")

# Now playing movies
now_playing = client.now_playing_movies()

# Popular TV series
popular_tv = client.popular_tv_series()

# Top rated TV series
top_tv = client.top_rated_tv_series()

# Airing today
airing_today = client.airing_today_tv_series()

# On the air
on_air = client.on_the_air_tv_series()
```

### Detailed Information

#### Movie Details

```python
movie = client.movie_detail(550)  # Fight Club
print(f"Title: {movie.title}")
print(f"Tagline: {movie.tagline}")
print(f"Overview: {movie.overview}")
print(f"Runtime: {movie.runtime} minutes")
print(f"Budget: ${movie.budget:,}")
print(f"Revenue: ${movie.revenue:,}")
print(f"Genres: {', '.join(g.name for g in movie.genres)}")
print(f"IMDB: {movie.imdb_id}")
```

#### TV Series Details

```python
series = client.tv_series_detail(1396)  # Breaking Bad
print(f"Name: {series.name}")
print(f"Status: {series.status}")
print(f"Number of Seasons: {series.number_of_seasons}")
print(f"Number of Episodes: {series.number_of_episodes}")
print(f"Networks: {', '.join(n.name for n in series.networks)}")

# Access seasons
for season in series.seasons:
    print(f"Season {season.season_number}: {season.name}")
```

#### Season Details

```python
season = client.season_detail(series_id=1396, season_number=1)
print(f"Season: {season.name}")
print(f"Episodes: {len(season.episodes)}")

for episode in season.episodes:
    print(f"  Episode {episode.episode_number}: {episode.name}")
    print(f"    Air Date: {episode.air_date}")
    print(f"    Rating: {episode.vote_average}/10")
```

#### Episode Details

```python
episode = client.episode_detail(
    series_id=1396,
    season_number=1,
    episode_number=1
)
print(f"Episode: {episode.name}")
print(f"Overview: {episode.overview}")
print(f"Runtime: {episode.runtime} minutes")
print(f"Crew: {len(episode.crew)} members")
```

#### Collection Details

```python
collection = client.collection_detail(10)  # Star Wars Collection
print(f"Collection: {collection.name}")
print(f"Movies in collection: {len(collection.parts)}")

for movie in collection.parts:
    print(f"  - {movie.title} ({movie.release_date.year if movie.release_date else 'N/A'})")
```

### Images, Videos & Credits

#### Images

```python
# Movie images
images = client.get_movie_images(id=550, language="en")
print(f"Backdrops: {len(images.backdrops)}")
print(f"Posters: {len(images.posters)}")
print(f"Logos: {len(images.logos)}")

for poster in images.posters[:5]:
    print(f"  {poster.url} - {poster.width}x{poster.height}")

# TV series images
tv_images = client.get_tv_images(id=1396, language="en")

# Season images
season_images = client.get_season_images(
    series_id=1396,
    season_number=1,
    language="en"
)

# Episode images
episode_images = client.get_episode_images(
    series_id=1396,
    season_number=1,
    episode_number=1,
    language="en"
)
```

#### Videos

```python
# Movie videos (trailers, teasers, etc.)
videos = client.get_movie_videos(id=550)
for video in videos:
    print(f"{video.name} - {video.type}")
    print(f"  Site: {video.site}")
    print(f"  Key: {video.key}")

# TV series videos
tv_videos = client.get_tv_videos(id=1396)
```

#### Credits

```python
# Movie credits
credits = client.get_movie_credits(id=550)
print("Cast:")
for actor in credits.cast[:10]:
    print(f"  {actor.name} as {actor.character}")

print("\nCrew:")
for crew_member in credits.crew[:10]:
    print(f"  {crew_member.name} - {crew_member.job}")

# TV series credits
tv_credits = client.get_tv_credits(id=1396)
```

### Recommendations & Similar Content

```python
# Similar movies
similar_movies = client.get_movie_similar(id=550)
for movie in similar_movies.get_data():
    print(movie.title)

# Similar TV series
similar_tv = client.get_tv_similar(id=1396)

# Movie recommendations
recommendations = client.get_movie_recommendations(id=550)
for movie in recommendations.get_data():
    print(movie.title)

# TV recommendations
tv_recommendations = client.get_tv_recommendations(id=1396)
```

### Working with Genres

```python
# Get all movie genres
movie_genres = client.get_movie_genres()
for genre in movie_genres:
    print(f"{genre.name} (ID: {genre.id})")

# Get all TV genres
tv_genres = client.get_tv_genres()

# Get a specific genre by ID
genre = client.get_genre(28)  # Action
print(genre.name)
```

### Using the Paginator

The paginator provides a convenient way to navigate through large result sets:

```python
# Get paginated results
paginator = client.popular_movies()

# Get first page
page1 = paginator.get_data()
print(f"Page 1: {len(page1)} movies")
print(f"Total pages: {paginator.total_pages}")
print(f"Total results: {paginator.total_results}")

# Navigate to next page
page2 = paginator.next_page()

# Jump to a specific page
page5 = paginator.get_page(5)

# Check if more pages are available
if paginator.has_next_page:
    next_page = paginator.next_page()

# Get first item quickly
first_movie = paginator.first()
if first_movie:
    print(first_movie.title)
```

## API Reference

### TMDbClient

The main client class for interacting with the TMDb API.

#### Constructor

```python
TMDbClient(
    api_key: str | None = None,
    bearer_token: str | None = None,
    language: str | None = None
)
```

**Parameters:**
- `api_key`: Your TMDb API key (required if bearer_token is not provided)
- `bearer_token`: Your TMDb bearer token (required if api_key is not provided)
- `language`: Language code for localized content (e.g., "en-US", "fr-FR")

#### Methods

##### Search Methods

- `search_movies(query: str, include_adult: bool | None = None, year: int | None = None) -> TMDbPaginator[Movie]`
- `search_tv_series(query: str, include_adult: bool | None = None, first_air_date_year: int | None = None, year: int | None = None) -> TMDbPaginator[TVSeries]`
- `search_multi(query: str, include_adult: bool | None = None, page: int = 1) -> dict`

##### Discovery Methods

- `discover_movies(filters: dict[str, str | int] | None = None) -> TMDbPaginator[Movie]`
- `discover_tv_series(filters: dict[str, str | int] | None = None) -> TMDbPaginator[TVSeries]`

##### Popular & Top Rated Methods

- `popular_movies() -> TMDbPaginator[Movie]`
- `popular_tv_series() -> TMDbPaginator[TVSeries]`
- `top_rated_movies() -> TMDbPaginator[Movie]`
- `top_rated_tv_series() -> TMDbPaginator[TVSeries]`
- `upcoming_movies() -> TMDbPaginator[Movie]`
- `now_playing_movies() -> TMDbPaginator[Movie]`
- `airing_today_tv_series() -> TMDbPaginator[TVSeries]`
- `on_the_air_tv_series() -> TMDbPaginator[TVSeries]`

##### Detail Methods

- `movie_detail(movie_id: int) -> MovieDetails`
- `tv_series_detail(tv_id: int) -> TVSeriesDetails`
- `season_detail(series_id: int, season_number: int) -> SeasonDetails`
- `episode_detail(series_id: int, season_number: int, episode_number: int) -> EpisodeDetails`
- `collection_detail(collection_id: int) -> CollectionDetails`

##### Genre Methods

- `get_movie_genres() -> list[Genre]`
- `get_tv_genres() -> list[Genre]`
- `get_genre(id: int) -> Genre`

##### Image Methods

- `get_movie_images(id: int, language: str | None) -> MovieImages`
- `get_tv_images(id: int, language: str | None) -> TVSeriesImages`
- `get_season_images(series_id: int, season_number: int, language: str | None) -> SeasonImages`
- `get_episode_images(series_id: int, season_number: int, episode_number: int, language: str | None) -> EpisodeImages`

##### Video Methods

- `get_movie_videos(id: int) -> list[MediaVideo]`
- `get_tv_videos(id: int) -> list[MediaVideo]`

##### Credits Methods

- `get_movie_credits(id: int) -> MovieCredits`
- `get_tv_credits(id: int) -> TVSeriesCredits`

##### Recommendation & Similar Methods

- `get_movie_similar(id: int) -> TMDbPaginator[Movie]`
- `get_tv_similar(id: int) -> TMDbPaginator[TVSeries]`
- `get_movie_recommendations(id: int) -> TMDbPaginator[Movie]`
- `get_tv_recommendations(id: int) -> TMDbPaginator[TVSeries]`

### TMDbPaginator

A generic paginator for handling paginated API responses.

#### Properties

- `has_next_page: bool` - Check if more pages are available
- `total_pages: int | None` - Total number of pages
- `total_results: int | None` - Total number of results
- `page: int` - Current page number
- `data: list[PageObjT]` - Current page data

#### Methods

- `get_data() -> list[PageObjT]` - Get current page data
- `next_page() -> list[PageObjT]` - Navigate to next page
- `get_page(page: int) -> list[PageObjT]` - Jump to specific page
- `first() -> PageObjT | None` - Get first item from current page

## Models

PyTMDb uses Pydantic models for type safety and validation. All models include computed fields for convenient URL generation.

### Core Models

- `Movie` - Basic movie information
- `MovieDetails` - Detailed movie information
- `TVSeries` - Basic TV series information
- `TVSeriesDetails` - Detailed TV series information
- `TVSeriesSeason` - Season information
- `SeasonDetails` - Detailed season information
- `TVSeriesEpisode` - Episode information
- `EpisodeDetails` - Detailed episode information
- `Collection` - Collection information
- `CollectionDetails` - Detailed collection information

### Supporting Models

- `Genre` - Genre information
- `MediaImage` - Image information with URL generation
- `MediaVideo` - Video information (trailers, teasers, etc.)
- `MovieImages` - Collection of movie images
- `TVSeriesImages` - Collection of TV series images
- `SeasonImages` - Collection of season images
- `EpisodeImages` - Collection of episode images
- `MovieCredits` - Movie cast and crew
- `TVSeriesCredits` - TV series cast and crew
- `GuestStar` - Guest star information
- `CrewMember` - Crew member information
- `Someone` - Generic person information
- `Network` - Network information
- `Country` - Country information
- `Language` - Language information
- `SpokenLanguage` - Spoken language information

### Computed Fields

Most models include computed fields for convenient URL generation:

- `poster_url` - Full URL for poster images
- `backdrop_url` - Full URL for backdrop images
- `profile_url` - Full URL for profile images
- `logo_url` - Full URL for logo images
- `still_url` - Full URL for still images
- `url` - Full URL for generic images

## Advanced Usage

### Custom Request Parameters

For discover endpoints, you can pass any valid TMDb API parameters:

```python
movies = client.discover_movies({
    "with_genres": "28,12",
    "with_cast": "500",
    "with_crew": "7467",
    "sort_by": "popularity.desc",
    "vote_count.gte": 100,
    "vote_average.gte": 7.0,
    "primary_release_date.gte": "2020-01-01",
    "primary_release_date.lte": "2023-12-31",
})
```

### Error Handling

```python
from httpx import HTTPStatusError

try:
    movie = client.movie_detail(999999999)
except HTTPStatusError as e:
    print(f"HTTP Error: {e.response.status_code}")
    print(f"Details: {e.response.text}")
except ValueError as e:
    print(f"Validation Error: {e}")
```

### Working with Raw Data

If you need to access raw API responses:

```python
# The client uses httpx internally
response = client.req("GET", "/movie/550")
print(response)  # Raw JSON dict
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is not officially associated with The Movie Database. TMDb API is a trademark of The Movie Database.

## Links

- [TMDb API Documentation](https://developers.themoviedb.org/3)
- [TMDb Website](https://www.themoviedb.org/)
- [Get API Key](https://www.themoviedb.org/settings/api)

## Author

Created by Izak (frdev.izak@gmail.com)
