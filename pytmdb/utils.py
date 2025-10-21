from typing import Generic, TypeVar, Callable, Any
from pydantic import BaseModel



PageObjT = TypeVar("PageObjT", bound=BaseModel)


__all__ = ["TMDbPaginator"]



class TMDbPaginator(Generic[PageObjT]):

    def __init__(self,
                 model: type[PageObjT],
                 reqfn: Callable[[int], dict[str, Any]],
                 page: int = 1):
        self.data_model = model
        self.reqfn = reqfn
        self.page = page
        self.data: list[PageObjT] = []

        self.total_pages: int | None = None
        self.total_results: int | None = None


    @property
    def has_next_page(self) -> bool:
        return self.total_pages is None or self.page < self.total_pages


    def get_data(self) -> list[PageObjT]:
        res = self.reqfn(self.page)
        self.page = res["page"]
        self.total_pages = res["total_pages"]
        self.total_results = res["total_results"]

        data = []

        for item in res["results"]:
            try:
                obj = self.data_model.model_validate(item)
            except:
                continue
            data.append(obj)

        self.data = data
        return self.data


    def next_page(self) -> list[PageObjT]:
        if self.total_pages and self.page >= self.total_pages:
            raise StopIteration("No more pages")

        self.page += 1
        return self.get_data()


    def get_page(self, page: int) -> list[PageObjT]:
        if page < 1 or (self.total_pages and page > self.total_pages):
            raise ValueError("Invalid page number")

        self.page = page
        return self.get_data()


    def first(self) -> PageObjT | None:
        if not self.data:
            self.get_data()
        return self.data[0] if self.data else None
