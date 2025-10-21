from httpx import Client
from . import utils
from . import models


__all__ = [
    "TMDbClient"
]



class TMDbClient:

    def __init__(self,
                 *,
                 api_key: str | None = None,
                 bearer_token: str | None = None,
                 language: str | None = None) -> None:
        """
        Initialize the TMDb client.
        """
        self.api_key = api_key
        """The API key used to do requests."""
        self.bearer_token = bearer_token
        """The bearer token used to do requests."""
        self.language = language
        """The language of the data returned by the TMDb API."""

        self.client = Client(
            base_url="https://api.themoviedb.org/3"
        )
        """The httpx HTTP client."""

        if not (bool(self.api_key) ^ bool(self.bearer_token)):
            raise ValueError("You must provide either an API key or a bearer token, but not both or none.")

        if self.api_key:
            self.client.params = self.client.params.set("api_key", self.api_key)

        if self.bearer_token:
            self.client.headers["Authorization"] = f"Bearer {self.bearer_token}"

        if self.language:
            self.client.params = self.client.params.set("language", self.language)

        self.cached_genres: dict[str, list[models.Genre] | None] = {
            "movie": None,
            "tv": None,
        }

        self.get_movie_genres()
        self.get_tv_genres()


    def req(self,
            method: str,
            endpoint: str,
            params: dict | None = None,
            body: dict | None = None):
        response = self.client.request(method, endpoint, params=params, json=body)
        response.raise_for_status()
        return response.json()


    def discover_movies(self,
                        filters: dict[str, str | int] | None = None) -> utils.TMDbPaginator[models.Movie]:
        def reqfn(page: int):
            return self.req("GET", "/discover/movie", params=(filters or {}) | {
                "page": page,
            })

        pagi = utils.TMDbPaginator(models.Movie, reqfn, 1)
        return pagi


    def discover_tv_series(self,
                        filters: dict[str, str | int] | None = None) -> utils.TMDbPaginator[models.TVSeries]:
        def reqfn(page: int):
            return self.req("GET", "/discover/tv", params=(filters or {}) | {
                "page": page,
            })

        pagi = utils.TMDbPaginator(models.TVSeries, reqfn, 1)
        return pagi


    def popular_movies(self) -> utils.TMDbPaginator[models.Movie]:
        def reqfn(page: int):
            return self.req("GET", "/movie/popular", params={"page": page})

        pagi = utils.TMDbPaginator(models.Movie, reqfn, 1)
        return pagi


    def popular_tv_series(self) -> utils.TMDbPaginator[models.TVSeries]:
        def reqfn(page: int):
            return self.req("GET", "/tv/popular", params={"page": page})

        pagi = utils.TMDbPaginator(models.TVSeries, reqfn, 1)
        return pagi


    def top_rated_movies(self) -> utils.TMDbPaginator[models.Movie]:
        def reqfn(page: int):
            return self.req("GET", "/movie/top_rated", params={"page": page})

        pagi = utils.TMDbPaginator(models.Movie, reqfn, 1)
        return pagi


    def upcoming_movies(self) -> utils.TMDbPaginator[models.Movie]:
        def reqfn(page: int):
            return self.req("GET", "/movie/upcoming", params={"page": page})

        pagi = utils.TMDbPaginator(models.Movie, reqfn, 1)
        return pagi


    def top_rated_tv_series(self) -> utils.TMDbPaginator[models.TVSeries]:
        def reqfn(page: int):
            return self.req("GET", "/tv/top_rated", params={"page": page})

        pagi = utils.TMDbPaginator(models.TVSeries, reqfn, 1)
        return pagi


    def now_playing_movies(self) -> utils.TMDbPaginator[models.Movie]:
        def reqfn(page: int):
            return self.req("GET", "/movie/now_playing", params={"page": page})

        pagi = utils.TMDbPaginator(models.Movie, reqfn, 1)
        return pagi


    def airing_today_tv_series(self) -> utils.TMDbPaginator[models.TVSeries]:
        def reqfn(page: int):
            return self.req("GET", "/tv/airing_today", params={"page": page})

        pagi = utils.TMDbPaginator(models.TVSeries, reqfn, 1)
        return pagi


    def on_the_air_tv_series(self) -> utils.TMDbPaginator[models.TVSeries]:
        def reqfn(page: int):
            return self.req("GET", "/tv/on_the_air", params={"page": page})

        pagi = utils.TMDbPaginator(models.TVSeries, reqfn, 1)
        return pagi


    def search_movies(self,
                      query: str,
                      include_adult: bool | None = None,
                      year: int | None = None) -> utils.TMDbPaginator[models.Movie]:
        params = {"query": query}

        if include_adult is not None:
            params["include_adult"] = "true" if include_adult else "false"

        if year is not None:
            params["year"] = str(year)

        def reqfn(page: int):
            return self.req("GET", "/search/movie", params=params | {"page": page})

        pagi = utils.TMDbPaginator(models.Movie, reqfn, 1)
        return pagi


    def search_tv_series(self,
                         query: str,
                         include_adult: bool | None = None,
                         first_air_date_year: int | None = None,
                         year: int | None = None) -> utils.TMDbPaginator[models.TVSeries]:
        params = {"query": query}

        if include_adult is not None:
            params["include_adult"] = "true" if include_adult else "false"

        if first_air_date_year is not None:
            params["first_air_date_year"] = str(first_air_date_year)

        if year is not None:
            params["year"] = str(year)

        def reqfn(page: int):
            return self.req("GET", "/search/tv", params=params | {"page": page})

        pagi = utils.TMDbPaginator(models.TVSeries, reqfn, 1)
        return pagi


    def search_multi(self,
                     query: str,
                     include_adult: bool | None = None,
                     page: int = 1): # NOTE: don't return a paginator, but the JSON data
        params = {"query": query, "page": page}

        if include_adult is not None:
            params["include_adult"] = "true" if include_adult else "false"

        data = self.req("GET", "/search/multi", params=params)
        return data


    def movie_detail(self, movie_id: int) -> models.MovieDetails:
        data = self.req("GET", f"/movie/{movie_id}")
        return models.MovieDetails.model_validate(data)


    def tv_series_detail(self, tv_id: int) -> models.TVSeriesDetails:
        data = self.req("GET", f"/tv/{tv_id}")
        return models.TVSeriesDetails.model_validate(data)


    def episode_detail(self, series_id: int, season_number: int, episode_number: int) -> models.EpisodeDetails:
        data = self.req("GET", f"/tv/{series_id}/season/{season_number}/episode/{episode_number}")
        return models.EpisodeDetails.model_validate(data)


    def season_detail(self, series_id: int, season_number: int) -> models.SeasonDetails:
        data = self.req("GET", f"/tv/{series_id}/season/{season_number}")
        return models.SeasonDetails.model_validate(data)


    def get_movie_genres(self) -> list[models.Genre]:
        data = self.req("GET", "/genre/movie/list")
        genres = [models.Genre.model_validate(genre) for genre in data["genres"]]
        self.cached_genres["movie"] = genres
        return genres


    def get_tv_genres(self) -> list[models.Genre]:
        data = self.req("GET", "/genre/tv/list")
        genres = [models.Genre.model_validate(genre) for genre in data["genres"]]
        self.cached_genres["tv"] = genres
        return genres


    def get_genre(self, id: int) -> models.Genre:
        if self.cached_genres["movie"] is None:
            self.get_movie_genres()

        if self.cached_genres["tv"] is None:
            self.get_tv_genres()

        assert self.cached_genres["movie"] is not None \
            and self.cached_genres["tv"] is not None, "Genres not loaded."

        for genre in self.cached_genres["movie"] + self.cached_genres["tv"]:
            if genre.id == id:
                return genre

        raise ValueError(f"Genre with ID {id} not found.")


    def get_movie_images(self,
                         id: int,
                         language: str | None) -> models.MovieImages:
        """Get the images for a movie.
        The parameter "language" is required, cuz there is no images for most of the movies with a non-english language.
        """
        data = self.req("GET", f"/movie/{id}/images", params={"language": language})
        return models.MovieImages.model_validate(data)


    def get_tv_images(self,
                      id: int,
                      language: str | None) -> models.TVSeriesImages:
        """Get the images for a TV series.
        The parameter "language" is required, cuz there is no images for most of the movies with a non-english language.
        """
        data = self.req("GET", f"/tv/{id}/images", params={"language": language})
        return models.TVSeriesImages.model_validate(data)


    def get_season_images(self,
                          series_id: int,
                          season_number: int,
                          language: str | None) -> models.SeasonImages:
        """Get the images for a season of a TV series.
        The parameter "language" is required, cuz there is no images for most of the movies with a non-english language.
        """
        data = self.req("GET", f"/tv/{series_id}/season/{season_number}/images", params={"language": language})
        return models.SeasonImages.model_validate(data)


    def get_episode_images(self,
                           series_id: int,
                           season_number: int,
                           episode_number: int,
                           language: str | None) -> models.EpisodeImages:
        """Get the images for an episode of a TV series.
        The parameter "language" is required, cuz there is no images for most of the movies with a non-english language.
        """
        data = self.req("GET", f"/tv/{series_id}/season/{season_number}/episode/{episode_number}/images", params={"language": language})
        return models.EpisodeImages.model_validate(data)


    def get_movie_similar(self, id: int) -> utils.TMDbPaginator[models.Movie]:
        def reqfn(page: int):
            return self.req("GET", f"/movie/{id}/similar", params={"page": page})

        pagi = utils.TMDbPaginator(models.Movie, reqfn, 1)
        return pagi


    def get_tv_similar(self, id: int) -> utils.TMDbPaginator[models.TVSeries]:
        def reqfn(page: int):
            return self.req("GET", f"/tv/{id}/similar", params={"page": page})

        pagi = utils.TMDbPaginator(models.TVSeries, reqfn, 1)
        return pagi


    def get_movie_recommendations(self, id: int) -> utils.TMDbPaginator[models.Movie]:
        def reqfn(page: int):
            return self.req("GET", f"/movie/{id}/recommendations", params={"page": page})

        pagi = utils.TMDbPaginator(models.Movie, reqfn, 1)
        return pagi


    def get_tv_recommendations(self, id: int) -> utils.TMDbPaginator[models.TVSeries]:
        def reqfn(page: int):
            return self.req("GET", f"/tv/{id}/recommendations", params={"page": page})

        pagi = utils.TMDbPaginator(models.TVSeries, reqfn, 1)
        return pagi


    def get_movie_videos(self, id: int) -> list[models.MediaVideo]:
        data = self.req("GET", f"/movie/{id}/videos")
        return [models.MediaVideo.model_validate(video) for video in data["results"]]


    def get_tv_videos(self, id: int) -> list[models.MediaVideo]:
        data = self.req("GET", f"/tv/{id}/videos")
        return [models.MediaVideo.model_validate(video) for video in data["results"]]


    def get_movie_credits(self, id: int) -> models.MovieCredits:
        data = self.req("GET", f"/movie/{id}/credits")
        return models.MovieCredits.model_validate(data)


    def get_tv_credits(self, id: int) -> models.TVSeriesCredits:
        data = self.req("GET", f"/tv/{id}/credits")
        return models.TVSeriesCredits.model_validate(data)
