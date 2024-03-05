import pytest

from sqlgen.joins import resolve_model_joins, NoValidJoins
from test_data.models import Project, Host, Webserver, Request, User, VulnerabilityInstance, VulnerabilityClass


@pytest.mark.parametrize("source,destination,expected_joins", [
    (Host, Project, [Host.project_id]),
    (Webserver, Project, [Webserver.host, Host.project_id]),
    (Request, Project, [Request.webserver, Webserver.host, Host.project_id]),
    (VulnerabilityInstance, Project, [VulnerabilityInstance.request, Request.webserver, Webserver.host, Host.project_id]),
    (Request, VulnerabilityClass, [Request.vulnerabilities, VulnerabilityInstance.vulnerability_class_id]),
])
def test_resolve_model_joins_should_return_list_of_joins(source, destination, expected_joins):
    assert resolve_model_joins(source, destination) == expected_joins


def test_resolve_model_joins_should_raise_if_no_relation_exist_between_models():
    with pytest.raises(NoValidJoins) as exc_info:
        resolve_model_joins(User, Project)
    assert str(exc_info.value) == ("No Relation between self.source=<class 'test_data.models.User'> and "
                                   "self.destination=<class 'test_data.models.Project'>")
