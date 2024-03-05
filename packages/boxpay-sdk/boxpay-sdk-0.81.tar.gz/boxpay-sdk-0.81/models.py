from typing import List, Optional, Dict, Any
from dataclasses import dataclass
from pydantic import BaseModel, validator, ValidationError , Field


class LegalEntity(BaseModel):
    code: str

class Context(BaseModel):
    legal_entity: LegalEntity
    country_code: str
    client_pos_id: Optional[str]
    order_id: str
    locale_code: Optional[str] = None 
    
    
class DeliveryAddress(BaseModel):
    address1: str
    address2: Optional[str]  
    address3: Optional[str]
    city: str
    state: str
    country_code: str
    postal_code: str
    country_name: str

class Item(BaseModel):
    id: str
    item_name: str
    description: str
    quantity: int
    manufacturer: str
    brand: Optional[str] 
    color: Optional[str] 
    product_url: Optional[str]
    image_url: Optional[str]
    categories: List[str]
    amount_without_tax: float
    tax_amount: float
    tax_percentage: float

    @validator('quantity', pre=True)  
    def quantity_must_be_positive(cls, value):
        if value <= 0:
            raise ValueError('Quantity must be positive')
        return value

    @validator('amount_without_tax', 'tax_amount', 'tax_percentage', pre=True)
    def validate_price_info(cls, value):
        if value < 0:
            raise ValueError('Price and tax values cannot be negative')
        return value

class Order(BaseModel):
    voucher_code: Optional[str]   
    shipping_amount: Optional[float]
    tax_amount: Optional[float]
    original_amount: Optional[float]
    items: Optional[List[Item]] = None  



class Money(BaseModel):
    amount: float
    currency_code: str

    @validator('amount', pre=True)
    def amount_must_be_positive(cls, value):
        if value <= 0:
            raise ValueError('Amount must be positive')
        return value

class BillingAddress(BaseModel):
    address1: str
    address2: Optional[str] = None
    address3: Optional[str] = None
    city: str
    state: str
    country_code: str
    postal_code: str
    country_name: str 

class Shopper(BaseModel):
    first_name: str
    last_name: str
    gender: str
    phone_number: str
    email: str 
    unique_reference: str
    delivery_address: DeliveryAddress

class ShopperAuthentication(BaseModel):
    three_ds_authentication: str

class Descriptor(BaseModel):
    line1: str
    line2: str

class CheckoutSessionRequest(BaseModel):
    context: Context
    paymentType: str
    shopper: Shopper
    order: Order
    frontendReturnUrl: str
    frontendBackUrl: str
    statusNotifyUrl: str
    shopperAuthentication: ShopperAuthentication
    money: Money
    descriptor: Descriptor
    billingAddress: BillingAddress
    expiryDurationSec: Optional[int]
    metadata: Dict[str, Any] = None
    def to_dict(self):
        return {k: v for k, v in self.dict().items() if v is not None}


@dataclass
class CheckoutSessionResponse:
    status_code: int
    token: Optional[str] = None
    url: Optional[str] = None
    errorCode: Optional[str] = None
    message: Optional[str] = None
    timestamp: Optional[str] = None
    fieldErrorItems: Optional[List[Dict[str, str]]] = None
    retryable: Optional[bool] = None
    reasonCode: Optional[str] = None

    @classmethod
    def from_dict(cls, response_dict: Dict[str, Any]) -> 'CheckoutSessionResponse':
        status_code = response_dict.get('status_code', 200)
        token = response_dict.get('token', '')
        url = response_dict.get('url', '')
        errorCode = response_dict.get('errorCode', '')
        message = response_dict.get('message', '')
        timestamp = response_dict.get('timestamp', '')
        fieldErrorItems = response_dict.get('fieldErrorItems', [])
        retryable = response_dict.get('retryable', False)
        reasonCode = response_dict.get('reasonCode', '')

        return cls(
            status_code=status_code,
            token=token,
            url=url,
            errorCode=errorCode,
            message=message,
            timestamp=timestamp,
            fieldErrorItems=fieldErrorItems,
            retryable=retryable,
            reasonCode=reasonCode
        )

class PaymentMethod(BaseModel):
    type: str
    brand: str 
    classification: str
    subBrand: Optional[str]

class RecurringInstruction(BaseModel):
    enabled: bool
    expiry: str 
    minAmount: Optional[float]
    maxAmount: Optional[float]

class RecurringReference(BaseModel):
    source: str
    token: str

class Recurring(BaseModel):
    instruction: RecurringInstruction
    reference: RecurringReference
    pspReference: RecurringReference 

class PSPError(BaseModel):
    code: str 
    description: str

class PSPErrorDetails(BaseModel):
    pspError: PSPError 
    networkError: PSPError  
    issuerError: PSPError

class PSPOperationItem(BaseModel):
    pspReference: str
    money: Money 
    status: str 
    reason: str

class Caller(BaseModel):
    token: str
    callerType: str = Field(default="CHECKOUT")

class Status(BaseModel):
    operation: str 
    status: str
    reason: str 
    reasonCode: str

class FieldErrorItem(BaseModel):
    message: str
    fieldErrorCode: str 

class TransactionInquiryDetails(BaseModel):
    id: Optional[str]  
    transactionId: str
    name: str = Field(default="Authorisation")  

class TransactionInquiryResponse(BaseModel):
    operationId: str
    eventId: str 
    status: Status 
    captureRequired: bool 
    legalEntityCode: str 
    clientPosId: str
    orderId: str 
    caller: Caller 
    pspCode: str 
    pspReference: str
    pspOperationItems: List[PSPOperationItem]
    timestamp: str
    authCode: str
    money: Money  
    actions: List[str]
    additionalData: Dict[str, Any]  
    pspErrorDetails: PSPErrorDetails
    shopper: Shopper
    paymentMethod: PaymentMethod 
    recurring: Recurring
