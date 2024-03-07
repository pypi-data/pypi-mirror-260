import sys
import pyaws


sys.path.append("../")


def test_DynamoItem():
    class Movie(pyaws.DynamoItem):
        title: str
        year: int
        price: float

    movie = Movie(title="City of God", year=2002, price=10.99)
    movie_dynamo_dict = movie.to_dynamo_style()

    expected_dynamo_dict = {
        "title": {"S": movie.title},
        "year": {"N": str(movie.year)},
        "price": {"N": str(movie.price)}
    }

    assert movie_dynamo_dict == expected_dynamo_dict
