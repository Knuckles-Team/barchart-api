from typing import Union, List, Dict, Optional, Any, TypeVar, Generic

import requests
from pydantic import (
    BaseModel,
    Field,
    ConfigDict,
    field_validator,
)
from barchart_api.exceptions import (
    ParameterError,
)


########################################################################################################################
#                                               Input Models                                                           #
########################################################################################################################


class InputModel(BaseModel):
    """
    Pydantic model representing parameters for retrieving stock historical data.

    Attributes:
    - symbol (str): The stock symbol (required).
    - data (Optional[str]): Data frequency (e.g., 'daily').
    - volume (Optional[str]): Volume type (e.g., 'contract').
    - order (Optional[str]): Sort order (e.g., 'asc').
    - dividends (Optional[bool]): Include dividends.
    - backadjust (Optional[bool]): Back-adjust for splits.
    - daystoexpiration (Optional[int]): Days to expiration.
    - contractroll (Optional[str]): Contract roll method (e.g., 'expiration').
    - max_records (Optional[int]): Maximum records to return.

    Note:
    The class includes field_validators for type checking.
    Builds api_parameters in model_post_init.
    """

    model_config = ConfigDict(validate_assignment=True)
    symbol: str
    data: Optional[str] = 'daily'
    volume: Optional[str] = 'contract'
    order: Optional[str] = 'asc'
    dividends: Optional[bool] = False
    backadjust: Optional[bool] = False
    daystoexpiration: Optional[int] = 1
    contractroll: Optional[str] = 'expiration'
    max_records: Optional[int] = 640
    order_dir: Optional[str] = 'asc'
    order_by: Optional[str] = 'symbol'
    meta: Optional[str] = 'field.shortName%2Cfield.type%2Cfield.description%2Clists.lastUpdate'
    fields: Optional[str] = 'symbol%2CsymbolName%2ClastPrice%2CpriceChange%2CpercentChange%2Copinion%2CopinionPrevious%2CopinionLastWeek%2CopinionLastMonth%2CsymbolCode%2CsymbolType%2ChasOptions'
    has_options: Optional[bool] = True
    max_pages: Optional[int] = 1
    per_page: Optional[int] = 100
    api_parameters: Dict = Field(description="API Parameters", default_factory=dict)

    @field_validator('symbol', 'data', 'volume', 'order', 'contractroll')
    def validate_string_parameters(cls, v):
        """
        Validate string parameters.

        Args:
        - v: The value.

        Returns:
        - str: Validated value.

        Raises:
        - ValueError: If not a string.
        """
        if v is not None and not isinstance(v, str):
            raise ValueError("Invalid optional params")
        return v

    @field_validator('dividends', 'backadjust')
    def validate_bool_parameters(cls, v):
        """
        Validate boolean parameters.

        Args:
        - v: The value.

        Returns:
        - bool: Validated value.

        Raises:
        - ValueError: If not a bool.
        """
        if v is not None and not isinstance(v, bool):
            raise ValueError("Invalid optional params")
        return v

    @field_validator('daystoexpiration', 'max_records')
    def validate_int_parameters(cls, v):
        """
        Validate integer parameters.

        Args:
        - v: The value.

        Returns:
        - int: Validated value.

        Raises:
        - ValueError: If not an int.
        """
        if v is not None and not isinstance(v, int):
            raise ValueError("Invalid optional params")
        return v

    def model_post_init(self, __context):
        """
        Build the API parameters.
        """
        self.api_parameters = {'symbol': self.symbol}
        if self.data:
            self.api_parameters['data'] = self.data
        if self.volume:
            self.api_parameters['volume'] = self.volume
        if self.order:
            self.api_parameters['order'] = self.order
        if self.dividends is not None:
            self.api_parameters['dividends'] = str(self.dividends).lower()
        if self.backadjust is not None:
            self.api_parameters['backadjust'] = str(self.backadjust).lower()
        if self.daystoexpiration:
            self.api_parameters['daystoexpiration'] = self.daystoexpiration
        if self.contractroll:
            self.api_parameters['contractroll'] = self.contractroll
        if self.max_records:
            self.api_parameters['maxrecords'] = self.max_records
        if self.order_dir:
            self.api_parameters['orderDir'] = self.order_dir
        if self.order_by:
            self.api_parameters['orderBy'] = self.order_by
        if self.meta:
            self.api_parameters['meta'] = self.meta
        if self.fields:
            self.api_parameters['fields'] = self.fields
        if self.has_options is not None:
            self.api_parameters['hasOptions'] = str(self.has_options).lower()

########################################################################################################################
#                                               Output Models                                                          #
########################################################################################################################


class Stock(BaseModel):
    """
    Pydantic model representing a single historical stock data entry (from CSV parse).

    Attributes:
    - symbol (Optional[str]): Stock symbol.
    - symbolName (Optional[str]): Name.
    - lastPrice (Optional[float]): Last price.
    - priceChange (Optional[float]): Price change.
    - percentChange (Optional[float]): Percent change.
    - opinion (Optional[str]): Opinion.
    - opinionPrevious (Optional[str]): Previous opinion.
    - opinionLastWeek (Optional[str]): Last week opinion.
    - opinionLastMonth (Optional[str]): Last month opinion.
    - symbolCode (Optional[str]): Symbol code.
    - symbolType (Optional[int]): Symbol type.
    - hasOptions (Optional[bool]): Has options.
    - timestamp (Optional[str]): Date/timestamp.
    - open (Optional[float]): Open price.
    - high (Optional[float]): High price.
    - low (Optional[float]): Low price.
    - close (Optional[float]): Close price.
    - volume (Optional[int]): Volume.
    - openInterest (Optional[int]): Open interest (if available).
    """

    model_config = ConfigDict(extra="allow")
    symbol: Optional[str] = None
    symbolName: Optional[str] = None
    lastPrice: Optional[float] = None
    priceChange: Optional[float] = None
    percentChange: Optional[float] = None
    opinion: Optional[str] = None
    opinionPrevious: Optional[str] = None
    opinionLastWeek: Optional[str] = None
    opinionLastMonth: Optional[str] = None
    symbolCode: Optional[str] = None
    symbolType: Optional[int] = None
    hasOptions: Optional[bool] = None
    timestamp: Optional[str] = None
    open: Optional[float] = None
    high: Optional[float] = None
    low: Optional[float] = None
    close: Optional[float] = None
    volume: Optional[int] = None
    openInterest: Optional[int] = None



T = TypeVar("T")


class Response(BaseModel, Generic[T]):
    """
    A wrapper class to hold the original requests.Response along with the parsed Pydantic data.
    This allows access to response metadata (e.g., status_code, headers) while providing
    the parsed result in Pydantic models.
    """

    model_config = ConfigDict(extra="forbid", arbitrary_types_allowed=True)
    response: requests.Response = Field(
        default=None, description="The original requests.Response object", exclude=True
    )
    result: Optional[Union[T, List[T]]] = Field(
        default=None, description="The Pydantic models converted from the response"
    )