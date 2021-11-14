from definitions import AVAILABLE, RESERVED, Dict


def validate_player_balance(balance: Dict):
    if balance is None:
        return

    if not isinstance(balance, dict):
        raise TypeError('Player balance should be a dict')

    for key, value in balance.items():
        if (AVAILABLE not in value.keys()) or (RESERVED not in value.keys()):
            raise ValueError('Value has not attribute {} or {}'.format(AVAILABLE, RESERVED))


def validate_fees(fees: Dict):
    if fees is None:
        return

    if not isinstance(fees, dict):
        raise TypeError('Fees data should be a dict')

    for key, value in fees.items():
        if ('fee' not in value.keys()) or ('min_order_size' not in value.keys()):
            raise ValueError('Value has not attribute {} or {}'.format('fee', 'min_order_size'))
