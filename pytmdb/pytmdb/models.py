from typing import Self, Annotated
from datetime import date
from pydantic import BaseModel, BeforeValidator, computed_field, Field


__all__ = [
    "Movie", "TVSeries", "Genre",
    "SpokenLanguage", "MediaImage", "MovieImages",
    "TVSeriesImages", "SeasonImages", "EpisodeImages",
    "MovieDetails", "TVSeriesSeason", "TVSeriesEpisode",
    "CrewMember", "GuestStar", "EpisodeDetails",
    "Someone", "Network", "Country",
    "Language", "TVSeriesDetails", "SeasonDetails",
    "MovieCredits", "TVSeriesCredits", "Certification",
    "Certifications"
]



def img_url(path: str, size: str = "original") -> str:
    return f"https://image.tmdb.org/t/p/{size}{path}"


def good_release_date(date_str: str) -> str | None:
    return date_str or None


ReleaseDate = Annotated[date | None, BeforeValidator(lambda ds: ds or None)]



class APIObj(BaseModel):

    @classmethod
    def load(cls, data) -> Self:
        return cls.model_validate(data)



class Movie(APIObj):
    id: int
    title: str
    overview: str
    release_date: ReleaseDate
    vote_average: float
    vote_count: int
    poster_path: str | None
    backdrop_path: str | None
    genre_ids: list[int]
    original_language: str
    original_title: str
    popularity: float
    video: bool

    @computed_field
    @property
    def poster_url(self) -> str | None:
        if not self.poster_path:
            return None
        return img_url(self.poster_path)

    @computed_field
    @property
    def backdrop_url(self) -> str | None:
        if not self.backdrop_path:
            return None
        return img_url(self.backdrop_path)



class TVSeries(APIObj):
    id: int
    name: str
    overview: str
    first_air_date: ReleaseDate
    vote_average: float
    vote_count: int
    poster_path: str | None
    backdrop_path: str | None
    genre_ids: list[int]
    origin_country: list[str]
    original_language: str
    original_name: str
    popularity: float

    @computed_field
    @property
    def poster_url(self) -> str | None:
        if not self.poster_path:
            return None
        return img_url(self.poster_path)

    @computed_field
    @property
    def backdrop_url(self) -> str | None:
        if not self.backdrop_path:
            return None
        return img_url(self.backdrop_path)
    


class Genre(BaseModel):
    id: int
    name: str



class SpokenLanguage(BaseModel):
    english_name: str
    iso_639_1: str
    name: str


class MediaImage(BaseModel):
    aspect_ratio: float
    file_path: str
    height: int
    width: int
    iso_639_1: str | None
    vote_average: float
    vote_count: int

    @computed_field
    @property
    def url(self) -> str:
        return img_url(self.file_path)



class MovieImages(APIObj):
    backdrops: list[MediaImage]
    logos: list[MediaImage]
    posters: list[MediaImage]



class TVSeriesImages(APIObj):
    backdrops: list[MediaImage]
    logos: list[MediaImage]
    posters: list[MediaImage]



class SeasonImages(APIObj):
    posters: list[MediaImage]



class EpisodeImages(APIObj):
    stills: list[MediaImage]



class MovieDetails(Movie):
    adult: bool
    budget: int
    homepage: str | None
    imdb_id: str | None
    revenue: int
    runtime: int | None
    status: str | None
    tagline: str | None
    genre_ids: None = Field(default=None, exclude=True) # type: ignore
    spoken_languages: list[SpokenLanguage]



class TVSeriesSeason(BaseModel):
    id: int
    air_date: ReleaseDate
    episode_count: int | None = None
    name: str
    overview: str
    poster_path: str | None
    season_number: int
    vote_average: float

    @computed_field
    @property
    def poster_url(self) -> str | None:
        if not self.poster_path:
            return None
        return img_url(self.poster_path)



class TVSeriesEpisode(BaseModel):
    id: int
    name: str
    overview: str
    vote_average: float
    vote_count: int
    air_date: ReleaseDate
    episode_number: int
    production_code: str
    runtime: int | None
    season_number: int
    show_id: int | None = None
    still_path: str | None

    @computed_field
    @property
    def still_url(self) -> str | None:
        if not self.still_path:
            return None
        return img_url(self.still_path)



class CrewMember(BaseModel):
    id: int
    credit_id: str
    name: str
    original_name: str
    adult: bool
    gender: int
    profile_path: str | None
    department: str | None = None
    job: str | None = None
    known_for_department: str
    popularity: float

    @computed_field
    @property
    def profile_url(self) -> str | None:
        if not self.profile_path:
            return None
        return img_url(self.profile_path)



class GuestStar(CrewMember):
    character: str


class EpisodeDetails(TVSeriesEpisode):
    crew: list[CrewMember]
    # guest_stars: list[GuestStar]



class Someone(BaseModel):
    id: int
    credit_id: str
    name: str
    gender: int
    profile_path: str | None

    @computed_field
    @property
    def profile_url(self) -> str | None:
        if not self.profile_path:
            return None
        return img_url(self.profile_path)



class Network(BaseModel):
    id: int
    name: str
    logo_path: str | None
    origin_country: str

    @computed_field
    @property
    def logo_url(self) -> str | None:
        if not self.logo_path:
            return None
        return img_url(self.logo_path)



class Country(BaseModel):
    iso_3166_1: str
    name: str



class Language(BaseModel):
    english_name: str
    iso_639_1: str
    name: str



class TVSeriesDetails(TVSeries):
    created_by: list[Someone]
    episode_run_time: list[int]
    genre_ids: None = Field(default=None, exclude=True) # type: ignore
    genres: list[Genre]
    homepage: str
    in_production: bool
    languages: list[str]
    last_air_date: ReleaseDate
    last_episode_to_air: TVSeriesEpisode | None
    next_episode_to_air: TVSeriesEpisode | None
    networks: list[Network]
    number_of_episodes: int
    number_of_seasons: int
    production_companies: list[Network]
    production_countries: list[Country]
    seasons: list[TVSeriesSeason] # TVSeason
    spoken_languages: list[Language]
    status: str
    tagline: str
    type: str



class SeasonDetails(TVSeriesSeason):
    id: int
    name: str
    overview: str
    poster_path: str | None
    season_number: int
    episodes: list[EpisodeDetails]
    air_date: ReleaseDate

    @computed_field
    @property
    def poster_url(self) -> str | None:
        if not self.poster_path:
            return None
        return img_url(self.poster_path)



class MediaVideo(BaseModel):
    id: str
    iso_639_1: str
    iso_3166_1: str
    key: str
    name: str
    site: str
    size: int
    type: str
    official: bool
    published_at: str


class MovieCredits(APIObj):
    id: int
    cast: list[GuestStar]
    crew: list[CrewMember]


class TVSeriesCredits(APIObj):
    id: int
    cast: list[GuestStar]
    crew: list[CrewMember]


class Certification(BaseModel):
    certification: str
    meaning: str
    order: int


class Certifications(APIObj):
    certifications: dict[str, list[Certification]]
