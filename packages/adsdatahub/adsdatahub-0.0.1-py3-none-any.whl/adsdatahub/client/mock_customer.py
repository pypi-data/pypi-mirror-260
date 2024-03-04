import datetime

from typing_extensions import override

import adsdatahub
from adsdatahub.client.customer import CustomerClient
from adsdatahub.client.parameters import PythonParameterType
from adsdatahub.client.query_result import QueryResult
from adsdatahub.types import CustomerId


class MockCustomerClient(CustomerClient):
    def __init__(
        self,
        client: adsdatahub.MockClient,
        customer_id: CustomerId,
    ):
        self._client = client
        self.customer_id = customer_id

    def query(
        self,
        query_text: str,
        /,
        parameters: dict[str, PythonParameterType] | None = None,
        *,
        start_date: str | datetime.date,
        end_date: str | datetime.date,
        dest_table: str,
    ) -> QueryResult:
        # TODO: モックのインターフェースを検討する。
        raise NotImplementedError()

    @override
    def validate(
        self,
        query_text: str,
        /,
        parameters: dict[str, PythonParameterType] | None = None,
    ) -> None:
        # TODO: モックのインターフェースを検討する。
        raise NotImplementedError()
