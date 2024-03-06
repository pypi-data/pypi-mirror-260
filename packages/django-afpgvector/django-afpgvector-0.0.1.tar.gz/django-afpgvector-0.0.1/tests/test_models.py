import pytest

from afpgvector.models import Document


@pytest.mark.django_db(databases=["vector"])
class TestDocument:
    def test_query(self):
        embedding = [1, 2, 3]
        ds = Document.query(embedding, n_results=2, score_threshold=0.2)
        list(ds)
