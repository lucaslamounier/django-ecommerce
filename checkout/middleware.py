# coding=utf-8

from .models import CartItem


def cart_item_middleware(get_response):
    def middleware(request):
        session_key = request.session.session_key
        response = get_response(request)
<<<<<<< HEAD
        if session_key != request.session.session_key and request.session.session_key:
=======
        if session_key != request.session.session_key:
>>>>>>> 2533ec4fe3943df55b3b4e7a648caf069bcfdb9f
            CartItem.objects.filter(cart_key=session_key).update(
                cart_key=request.session.session_key
            )
        return response
    return middleware
