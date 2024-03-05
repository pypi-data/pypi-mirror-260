from pydantic import BaseModel, Field

from utils.tabular.preprocessing.validation_base import ArgsBase


class Test(ArgsBase):
    k_neighbors: int | object = Field(5, gt=1)


res = Test()
print(res.dict())
