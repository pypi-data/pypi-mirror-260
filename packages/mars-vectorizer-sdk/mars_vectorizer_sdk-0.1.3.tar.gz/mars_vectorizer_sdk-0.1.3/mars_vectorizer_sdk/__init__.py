import numpy as np

from dataclasses import dataclass
from typing import List, Union, Dict, Callable, Tuple, Optional
from enum import Enum
from functools import reduce
from itertools import starmap, chain

@dataclass
class Property:

    name: str
    value: Union[str, float]

@dataclass
class Group:

    name: str
    values: List[Union["Group", Property]]

@dataclass
class PropertyParser:

    name: str
    dtype: type
    path: List[str]

    def __call__(self, data: dict) -> Optional[Property]:
        try:
            return Property(
                name=self.name, 
                value=self.dtype(reduce(lambda x,y: x[y], self.path, data))
            )
        except:
            return None
        
@dataclass
class ListPropertyParser:

    name: str
    parser: Union["GroupParser", "PropertyParser"]
    path: List[str]

    def __call__(self, data: dict) -> Group:
        return Group(
            name=self.name,
            values=list(
                map(
                    self.parser, 
                    reduce(lambda x,y: x[y], self.path, data)
                )
            )
        )
    
@dataclass
class GroupParser:

    name: str
    children: List[Union["GroupParser", "PropertyParser"]]

    def __call__(self, data: dict) -> Group:
        return Group(
            name=self.name,
            values=list(
                filter(
                    lambda x: x is not None, 
                    map(
                        lambda parser: parser(data), 
                        self.children
                    )
                )
            )
        )

@dataclass
class Vectorizer:

    """
        Interface for vectorizers. Turns a set of key-value pairs into a numpy matrix.
    """

    def __call__(self, key_value_set: List[Tuple[str, Union[str, float]]]) -> np.ndarray:
        raise NotImplementedError
        
@dataclass
class VectorProperty:

    name: str
    vector: np.ndarray

@dataclass
class VectorGroup:

    name: str
    values: List[Union["VectorGroup", VectorProperty]]
    aggregator: Callable[[np.ndarray], np.ndarray] = lambda x: x.mean(axis=0)

    def aggregate(self, weights: Dict[str, float] = {}) -> VectorProperty:
        """
            Aggregates the vectors of the group. It will aggregate the vectors of the subgroups and the properties recursively.

            Args:
                agg: The aggregation function to be used.

            Returns:
                A VectorProperty with the aggregated vector.
        """
        return VectorProperty(
            name=self.name,
            vector=self.aggregator(
                np.array(
                    list(
                        filter(
                            lambda x: not np.isnan(x).any(), 
                            chain(
                                map(
                                    lambda x: x.aggregate(weights).vector * weights.get(x.name, 1.0),
                                    filter(
                                        lambda x: issubclass(x.__class__, VectorGroup),
                                        self.values
                                    ),
                                ),
                                map(
                                    lambda x: x.vector * weights.get(x.name, 1.0),
                                    filter(
                                        lambda x: issubclass(x.__class__, VectorProperty),
                                        self.values
                                    )
                                )
                            )
                        )
                    )
                )
            )
        )

@dataclass
class GroupVectorizer:

    vectorizer: Vectorizer

    def __call__(self, group: Group) -> VectorGroup:
        return VectorGroup(
            name=group.name,
            values=list(
                chain(
                    map(
                        lambda sub_group: self(sub_group),
                        filter(
                            lambda x: issubclass(x.__class__, Group),
                            group.values
                        ),
                    ),
                    starmap(
                        lambda p, v: VectorProperty(
                            name=p.name,
                            vector=v,
                        ),
                        zip(
                            filter(
                                lambda x: issubclass(x.__class__, Property),
                                group.values,
                            ),
                            self.vectorizer(
                                list(
                                    map(
                                        lambda x: (x.name, x.value),
                                        filter(
                                            lambda x: issubclass(x.__class__, Property),
                                            group.values,
                                        )
                                    )
                                )
                            )
                        )
                    )
                )
            )
        )
