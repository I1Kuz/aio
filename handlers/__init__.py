"""Import all routers and add them to routers_list."""
from .admin import admin_router
#from .captcha import captcha_router
from .user import user_router

routers_list = [
    
    user_router,
    #admin_router,
    #captcha_router,

]

__all__ = [
    "routers_list",
]

