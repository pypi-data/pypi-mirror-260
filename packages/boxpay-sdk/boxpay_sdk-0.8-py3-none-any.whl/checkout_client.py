from .sdk_client import APIClient
from .exceptions import APIError
from .models import CheckoutSessionResponse, CheckoutSessionRequest, TransactionInquiryDetails, TransactionInquiryResponse

class CheckoutClient(APIClient):
    def __init__(self, api_key: str, merchant_id: str):
        base_url = 'https://test-apis.boxpay.tech/v0/merchants/{merchant_id}'
        super().__init__(api_key, merchant_id, base_url)

    def create_checkout_session(self, request_data: CheckoutSessionRequest) -> CheckoutSessionResponse:
        try:
            response = self.create_session('sessions', request_data.to_dict())
            return CheckoutSessionResponse(**response)
        except APIError as e:
            raise

    def verify_payment(self, token: str, inquiry_details: TransactionInquiryDetails) -> TransactionInquiryResponse:
        data = {
            "token": token,
            "inquiryDetails": inquiry_details.dict()
        }

        response = self._make_request('POST', 'transactions/inquiries', data=data)
        return TransactionInquiryResponse(**response)
