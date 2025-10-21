# PyTMDB

A modern Python wrapper for The Movie Database (TMDb) API v3. Built with type hints and Pydantic models for a clean, pythonic interface.

## Features

- 🎬 Full support for movies, TV series, seasons, and episodes
- 🔍 Search functionality for movies and TV shows
- 📊 Browse popular, top-rated, upcoming content
- 🎭 Get detailed information including cast, crew, images, and videos
- 📄 Automatic pagination support
- 🔒 Type-safe with Pydantic models
- 🐍 Modern Python 3.13+ syntax

## Installation

```bash
pip install pytmdb
```

## Getting Started

### Authentication

You need a TMDb API key or bearer token to use this library. Get yours at [The Movie Database](https://www.themoviedb.org/settings/api).

```python
from pytmdb import TMDbClient

# Using API key
client = TMDbClient(api_key="your_api_key_here")

# OR using bearer token
client = TMDbClient(bearer_token="your_bearer_token_here")

# With language preference
client = TMDbClient(api_key="your_api_key_here", language="en-US")
```

## Usage Examples

### Discovering Movies

```python
from pytmdb import TMDbClient

client = TMDbClient(api_key="your_api_key_here")

# Get popular movies
popular = client.popular_movies()
movies = popular.get_data()

for movie in movies:
    print(f"{movie.title} ({movie.release_date.year if movie.release_date else 'N/A'})")
    print(f"  Rating: {movie.vote_average}/10")
    print(f"  Overview: {movie.overview[:100]}...")
    print(f"  Poster: {movie.poster_url}")
    print()
```

### Searching for Movies

```python
# Search for a specific movie
results = client.search_movies("The Matrix")
movies = results.get_data()

for movie in movies:
    print(f"{movie.title} - {movie.release_date}")
    
# Search with filters
results = client.search_movies("Avatar", year=2009, include_adult=False)
first_result = results.first()
if first_result:
    print(f"Found: {first_result.title}")
```

### Getting Movie Details

```python
# Get detailed information about a movie
movie = client.movie_detail(movie_id=550)  # Fight Club

print(f"Title: {movie.title}")
print(f"Tagline: {movie.tagline}")
print(f"Runtime: {movie.runtime} minutes")
print(f"Budget: ${movie.budget:,}")
print(f"Revenue: ${movie.revenue:,}")
print(f"Genres: {', '.join(g.name for g in movie.genres)}")
print(f"IMDb ID: {movie.imdb_id}")

# Get movie images
images = client.get_movie_images(movie_id=550, language="en")
print(f"Posters: {len(images.posters)}")
print(f"Backdrops: {len(images.backdrops)}")

# Get movie videos (trailers, teasers, etc.)
videos = client.get_movie_videos(movie_id=550)
for video in videos:
    if video.type == "Trailer":
        print(f"Trailer: {video.name} - https://youtube.com/watch?v={video.key}")
```

### Working with Cast and Crew

```python
# Get movie credits
credits = client.get_movie_credits(movie_id=550)

print("Top Cast:")
for actor in credits.cast[:5]:
    print(f"  {actor.name} as {actor.character}")

print("\nKey Crew:")
for crew_member in credits.crew[:5]:
    if crew_member.job:
        print(f"  {crew_member.name} - {crew_member.job}")
```

### TV Series

```python
# Search for TV series
results = client.search_tv_series("Breaking Bad")
series = results.first()

if series:
    print(f"{series.name} - First aired: {series.first_air_date}")
    
    # Get detailed TV series information
    details = client.tv_series_detail(series.id)
    print(f"Seasons: {details.number_of_seasons}")
    print(f"Episodes: {details.number_of_episodes}")
    print(f"Status: {details.status}")
    print(f"Networks: {', '.join(n.name for n in details.networks)}")
    
    # Get season details
    season = client.season_detail(series_id=series.id, season_number=1)
    print(f"\nSeason 1: {len(season.episodes)} episodes")
    
    # Get episode details
    episode = client.episode_detail(
        series_id=series.id,
        season_number=1,
        episode_number=1
    )
    print(f"Episode 1: {episode.name}")
    print(f"Air date: {episode.air_date}")
```

### Discovering Content with Filters

```python
# Discover movies with specific criteria
filters = {
    "with_genres": "28,12",  # Action and Adventure
    "primary_release_year": 2023,
    "sort_by": "popularity.desc",
    "vote_average.gte": 7.0,
}

results = client.discover_movies(filters=filters)
movies = results.get_data()

print(f"Found {len(movies)} movies matching criteria")
for movie in movies[:10]:
    print(f"{movie.title} - Rating: {movie.vote_average}")
```

### Pagination

```python
# Working with paginated results
popular = client.popular_movies()

# Get first page
page1 = popular.get_data()
print(f"Page 1: {len(page1)} movies")

# Check if there are more pages
if popular.has_next_page:
    # Get next page
    page2 = popular.next_page()
    print(f"Page 2: {len(page2)} movies")
    
# Jump to a specific page
page5 = popular.get_page(5)
print(f"Page 5: {len(page5)} movies")

# Get total available pages
print(f"Total pages: {popular.total_pages}")
print(f"Total results: {popular.total_results}")
```

### Getting Recommendations and Similar Content

```python
# Get similar movies
similar = client.get_movie_similar(movie_id=550)
similar_movies = similar.get_data()

print("Movies similar to Fight Club:")
for movie in similar_movies[:5]:
    print(f"  {movie.title}")

# Get movie recommendations
recommendations = client.get_movie_recommendations(movie_id=550)
recommended_movies = recommendations.get_data()

print("\nRecommended movies:")
for movie in recommended_movies[:5]:
    print(f"  {movie.title}")
```

### Browse Different Categories

```python
# Top rated movies
top_rated = client.top_rated_movies()
movies = top_rated.get_data()
print("Top Rated Movies:")
for movie in movies[:5]:
    print(f"  {movie.title} - {movie.vote_average}/10")

# Upcoming movies
upcoming = client.upcoming_movies()
movies = upcoming.get_data()
print("\nUpcoming Movies:")
for movie in movies[:5]:
    print(f"  {movie.title} - Releases: {movie.release_date}")

# Now playing in theaters
now_playing = client.now_playing_movies()
movies = now_playing.get_data()
print("\nNow Playing:")
for movie in movies[:5]:
    print(f"  {movie.title}")

# TV series categories
airing_today = client.airing_today_tv_series()
on_the_air = client.on_the_air_tv_series()
popular_tv = client.popular_tv_series()
top_rated_tv = client.top_rated_tv_series()
```

### Working with Genres

```python
# Get all movie genres
movie_genres = client.get_movie_genres()
print("Movie Genres:")
for genre in movie_genres:
    print(f"  {genre.name} (ID: {genre.id})")

# Get all TV genres
tv_genres = client.get_tv_genres()

# Get a specific genre by ID
action_genre = client.get_genre(28)  # Action
print(f"\nGenre: {action_genre.name}")
```

### Multi-Search

```python
# Search across movies, TV shows, and people
results = client.search_multi("Tom Hanks")

for item in results["results"]:
    media_type = item.get("media_type")
    if media_type == "person":
        print(f"Person: {item['name']}")
    elif media_type == "movie":
        print(f"Movie: {item['title']}")
    elif media_type == "tv":
        print(f"TV: {item['name']}")
```

## API Methods

### Movies
- `discover_movies(filters)` - Discover movies with filters
- `popular_movies()` - Get popular movies
- `top_rated_movies()` - Get top rated movies
- `upcoming_movies()` - Get upcoming movies
- `now_playing_movies()` - Get movies now playing
- `search_movies(query, include_adult, year)` - Search for movies
- `movie_detail(movie_id)` - Get detailed movie information
- `get_movie_images(id, language)` - Get movie images
- `get_movie_videos(id)` - Get movie videos
- `get_movie_credits(id)` - Get movie cast and crew
- `get_movie_similar(id)` - Get similar movies
- `get_movie_recommendations(id)` - Get movie recommendations

### TV Series
- `discover_tv_series(filters)` - Discover TV series with filters
- `popular_tv_series()` - Get popular TV series
- `top_rated_tv_series()` - Get top rated TV series
- `airing_today_tv_series()` - Get TV series airing today
- `on_the_air_tv_series()` - Get TV series on the air
- `search_tv_series(query, include_adult, first_air_date_year, year)` - Search for TV series
- `tv_series_detail(tv_id)` - Get detailed TV series information
- `season_detail(series_id, season_number)` - Get season details
- `episode_detail(series_id, season_number, episode_number)` - Get episode details
- `get_tv_images(id, language)` - Get TV series images
- `get_tv_videos(id)` - Get TV series videos
- `get_tv_credits(id)` - Get TV series cast and crew
- `get_tv_similar(id)` - Get similar TV series
- `get_tv_recommendations(id)` - Get TV series recommendations
- `get_season_images(series_id, season_number, language)` - Get season images
- `get_episode_images(series_id, season_number, episode_number, language)` - Get episode images

### Other
- `search_multi(query, include_adult, page)` - Search across all media types
- `get_movie_genres()` - Get all movie genres
- `get_tv_genres()` - Get all TV genres
- `get_genre(id)` - Get a specific genre by ID

## Models

The library uses Pydantic models for type safety and validation:

- `Movie` - Movie object with basic information
- `MovieDetails` - Detailed movie information
- `TVSeries` - TV series object
- `TVSeriesDetails` - Detailed TV series information
- `SeasonDetails` - Season information with episodes
- `EpisodeDetails` - Episode information
- `Genre` - Genre object
- `MovieCredits` / `TVSeriesCredits` - Cast and crew information
- `MediaImage` - Image object with URL
- `MediaVideo` - Video object (trailers, teasers, etc.)

All models include computed fields for image URLs (e.g., `poster_url`, `backdrop_url`).

## Pagination

Methods that return multiple results use the `TMDbPaginator` class:

```python
paginator = client.popular_movies()

# Get current page data
data = paginator.get_data()

# Navigate pages
next_data = paginator.next_page()
page_3_data = paginator.get_page(3)

# Get first item
first_item = paginator.first()

# Check for more pages
if paginator.has_next_page:
    # More pages available
    pass

# Pagination info
total_pages = paginator.total_pages
total_results = paginator.total_results
current_page = paginator.page
```

## Requirements

- Python 3.13+
- httpx
- pydantic

## License

This project is licensed under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Disclaimer

This library is not affiliated with or endorsed by The Movie Database (TMDb). Please review TMDb's [Terms of Use](https://www.themoviedb.org/terms-of-use) before using this library.
