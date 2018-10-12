from longclaw import longclawbasket


def get_shop_basket_id(request):
    """
    Return user's basket_id if it exists, else return session basket_id
    """
    if request.user.is_authenticated:
        if request.user.basket_id:
            return request.user.basket_id

    return longclawbasket.utils.basket_id(request)
