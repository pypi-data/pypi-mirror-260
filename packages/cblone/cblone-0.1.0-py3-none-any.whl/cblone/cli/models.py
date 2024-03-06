from pydantic import BaseModel, ConfigDict, RootModel


class User(BaseModel):
    login: str

    model_config = ConfigDict(extra="allow")


class Repository(BaseModel):
    default_branch: str
    name: str
    owner: User

    model_config = ConfigDict(extra="allow")


class RepositoryList(RootModel[list[Repository]]):
    root: list[Repository]

    def __iter__(self):
        return iter(self.root)

    def __len__(self) -> int:
        return len(self.root)
