import pytest
from django.core.management import call_command

from currencies.models import Currency
from currencies.schemas import CurrencySchema
from currencies.vat_comply_api import VATComplyAPI


@pytest.fixture
def mock_vat_comply_api(mocker):
    api_mock = mocker.Mock(spec=VATComplyAPI)
    api_mock.get_currencies.return_value = [
        CurrencySchema.parse_obj({"code": "USD", "name": "US Dollar", "symbol": "$"}),
        CurrencySchema.parse_obj({"code": "EUR", "name": "Euro", "symbol": "€"}),
    ]
    return api_mock


@pytest.mark.django_db
def test_populate_currencies_table_command(mock_vat_comply_api, capsys, mocker):
    with mocker.patch(
        "currencies.management.commands.populate_currencies_table.VATComplyAPI", return_value=mock_vat_comply_api
    ):
        call_command("populate_currencies_table")

    captured = capsys.readouterr()
    assert "Currencies fetched and added successfully." in captured.out
    assert Currency.objects.count() == 2


@pytest.mark.django_db
def test_populate_currencies_table_command_error(mock_vat_comply_api, capsys, mocker):
    mock_vat_comply_api.get_currencies.return_value = None

    with mocker.patch(
        "currencies.management.commands.populate_currencies_table.VATComplyAPI", return_value=mock_vat_comply_api
    ):
        call_command("populate_currencies_table")

    captured = capsys.readouterr()
    assert "Couldn't fetch currencies, please try again later.\n" in captured.out
    assert Currency.objects.count() == 0
