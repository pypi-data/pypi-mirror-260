from typing import Any, Callable, Optional

from bittrade_binance_websocket.models import endpoints
from bittrade_binance_websocket.models import request
from bittrade_binance_websocket.models.rest import margin_account

from bittrade_binance_websocket.rest.http_factory_decorator import http_factory


@http_factory(dict)
def query_margin_price_index_http_factory(
    symbol: str,
):
    return request.RequestMessage(
        method="GET",
        endpoint=endpoints.BinanceEndpoints.QUERY_MARGIN_PRICE_INDEX
        params={"symbol": symbol},
    )
