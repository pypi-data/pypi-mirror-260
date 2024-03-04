import datetime
from typing import assert_never

from adsdatahub.restapi.schemas.field_type import (
    ArrayTypeDict,
    FieldTypeDict,
    TypeDict,
)
from adsdatahub.restapi.schemas.parameter_type import (
    ParameterTypeDict,
)
from adsdatahub.restapi.schemas.parameter_value import (
    ArrayValueDict,
    ArrayValueValuesDict,
    ParameterValueDict,
    ValueDict,
)

# TODO: 配列の型、デフォルト値などをサポートする必要があるが、後回し。
#
# TODO: デフォルト値や NULL のサポートをするためには、 dataclass や pydantic を利用する必要がある。
#
# NOTE: ドキュメントの記載は一貫性がない。
#       1. STRING または INT64 のプリミティブ型に加えて、配列と構造体をサポートしているように見える。
#          https://developers.google.com/ads-data-hub/reference/rest/v1/FieldType?hl=ja
#
#       2. AdsDataHub のコンソールからはさらに多くのパラメータの型を扱うことができるようだ。
#          https://developers.google.com/ads-data-hub/guides/run-queries?hl=ja#parameter_types
#
PythonParameterType = (
    str
    | int
    | float
    | bool
    | datetime.date
    | datetime.datetime
    | list["PythonParameterType"]
)
"""
クエリのパラメータとして使える Python の型。
"""


def convert_param_types(
    params: dict[str, PythonParameterType],
) -> dict[str, ParameterTypeDict]:
    return {
        key: ParameterTypeDict({"type": convert_parameter_type(value)})
        for key, value in params.items()
    }


def convert_param_values(
    params: dict[str, PythonParameterType],
) -> dict[str, ParameterValueDict]:
    return {key: convert_parameter_value(value) for key, value in params.items()}


def convert_parameter_type(
    value: PythonParameterType,
) -> FieldTypeDict:
    match value:
        case str():
            return TypeDict({"type": "STRING"})

        case int():
            return TypeDict({"type": "INT64"})

        case float():
            return TypeDict({"type": "FLOAT64"})

        case bool():
            return TypeDict({"type": "BOOL"})

        case datetime.date():
            return TypeDict({"type": "DATE"})

        case datetime.datetime():
            return TypeDict({"type": "TIMESTAMP"})

        case list():
            return ArrayTypeDict(
                {
                    "arrayType": convert_parameter_type(
                        # NOTE: 配列の要素が空の場合は、型を推測できないため、文字列を仮に入れる。
                        #       クエリ文の側でパラメータの型が明確である場合、文字列は自動で変換処理されるため、最も安全な選択肢となる。
                        value[0] if len(value) > 0 else "STRING"
                    )
                }
            )

        case _ as unreachable:
            assert_never(unreachable)


def convert_parameter_value(value: PythonParameterType) -> ParameterValueDict:
    match value:
        case str():
            return ValueDict({"value": value})

        case int():
            return ValueDict({"value": str(value)})

        case float():
            return ValueDict({"value": str(value)})

        case bool():
            return ValueDict({"value": str(value)})

        case datetime.date():
            return ValueDict({"value": value.isoformat()})

        case datetime.datetime():
            return ValueDict({"value": value.isoformat()})

        case list():
            return ArrayValueDict(
                {
                    "arrayValue": ArrayValueValuesDict(
                        {"values": [convert_parameter_value(v) for v in value]}
                    )
                }
            )

        case _ as unreachable:
            assert_never(unreachable)
