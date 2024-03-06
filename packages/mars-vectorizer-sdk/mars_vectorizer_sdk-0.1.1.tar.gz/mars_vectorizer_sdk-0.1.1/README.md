# Mars Vectorizer
Parses some json/dictionary data object into a grouping and then vectorizes it. Requires that you implement the `Vectorizer` interface.

# Example

Here's a small example of how to use it. First, a parser is defined with class type `GroupParser` on top. Such a parser takes children of class type `PropertyParser`, which is the lowest type of parser, or a `GroupParser` (it is recursively defined). A parser object is returned. It is simply a function taking any dictionary object as its input, and returns a `Group` object, which's just a mirror of the parser but with names and values set. Then, in this example, the vectorizer will vectorize every parsed object, such that in the end we'll have vectors as values (instead of original floats and strings). Finally, we aggregate all vectors into one object using a `weights` -dictionary as input, which is a mapping from a group or property name into a float value. That value will be multiplied onto its corresponding vector, if it exists. Otherwise it will be ignored. So in this example, the vector for "b group" will be multiplied with `10`.

```python
import numpy as np
from typing import List, Tuple, Union
from mars_vectorizer_sdk import GroupParser, PropertyParser, VectorizedGroupParser, Vectorizer, Dtype

class ExampleVectorizer(Vectorizer):

    def __call__(self, key_value_set: List[Tuple[str, Union[str, float]]]) -> np.ndarray:
        return np.random.uniform(size=(len(key_value_set), 10))

parser = GroupParser(
    name="some object", 
    children=[
        GroupParser(
            name="some group", 
            children=[
                PropertyParser(name="first value", path=["something", "something-under"], dtype=Dtype.STRING),
            ],
        ),
        GroupParser(
            name="another group", 
            children=[
                PropertyParser(name="some value", path=["something", "something-else", "some-value-a"], dtype=Dtype.STRING),
                PropertyParser(name="some other value", path=["something", "something-else", "some-value-b"], dtype=Dtype.FLOAT),
            ],
        )
    ]
)
vec_parser = VectorizedGroupParser.from_group(
    parser,
    vectorizer=ExampleVectorizer(),
)

# Example of usage
json_data = {
    "something": {
        "something-under": "text is here",
        "something-else": {
            "some-value-a": "a value",
            "some-value-b": 10.0,
        },
    }
}
# Parse json data
res = vec_parser(json_data)
print(res) # Full data
print(res.aggregate({"b group": 10}).vector) # aggregated weighted vector
```