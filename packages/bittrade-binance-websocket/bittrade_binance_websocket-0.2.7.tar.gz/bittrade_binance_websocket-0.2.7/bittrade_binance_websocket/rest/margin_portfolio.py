from typing import Any, Callable, Optional

from bittrade_binance_websocket.models import endpoints
from bittrade_binance_websocket.models import request
from bittrade_binance_websocket.models import portfolio

from bittrade_binance_websocket.rest.http_factory_decorator import http_factory


@http_factory(portfolio.PortfolioMarginAccountInfo)
def portfolio_margin_account_info_http_factory(
):
    return request.RequestMessage(
        method="GET",
        endpoint=endpoints.BinanceEndpoints.MARGIN_PORTFOLIO_ACCOUNT_INFORMATION,
    )
