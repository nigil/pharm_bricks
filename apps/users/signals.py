from django.db.models import F
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from shop.utils import get_shop_basket_id as get_saved_basket_id
from longclaw.longclawbasket.models import BasketItem
from longclaw.longclawbasket.utils import basket_id as get_session_basket_id, BASKET_ID_SESSION_KEY


@receiver(user_logged_in)
def set_user_basket(request, user, **kwargs):
    saved_basket_id = get_saved_basket_id(request)
    user.basket_id = saved_basket_id
    user.save(update_fields=('basket_id',))

    session_basket_id = get_session_basket_id(request)
    if session_basket_id != saved_basket_id:
        # merge baskets
        saved_items = BasketItem.objects\
                        .filter(basket_id=saved_basket_id)\
                        .values_list('variant_id')
        saved_items_variants_ids = [item[0] for item in saved_items]

        session_items = BasketItem.objects.filter(basket_id=session_basket_id)
        for session_item in session_items:
            # squash items
            if session_item.variant_id in saved_items_variants_ids:
                BasketItem.objects\
                    .filter(basket_id=saved_basket_id,
                            variant_id=session_item.variant_id)\
                    .update(date_added=session_item.date_added,
                            quantity=F('quantity')+session_item.quantity)
            # change items basket_id
            else:
                session_item.basket_id = saved_basket_id
                session_item.save(update_fields=('basket_id',))

    request.session[BASKET_ID_SESSION_KEY] = user.basket_id
