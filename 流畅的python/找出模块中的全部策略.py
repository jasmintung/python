def fidelity_promo():
    pass


def bulk_item_promo():
    pass


def large_order_promo():
    pass


def abc():
    pass


promos = [globals()[name] for name in globals() if name.endswith('_promo') and name != 'best_promo']
print(promos)


def best_promo(args):
    return max(promo(args) for promo in promos)
