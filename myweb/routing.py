from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.http import AsgiHandler
import apps.myapp.routing
import os
from channels.security.websocket import AllowedHostsOriginValidator


'''
ProtocolTypeRouter： ASIG支持多种不同的协议，在这里可以指定特定协议的路由信息，我们只使用了websocket协议，这里只配置websocket即可

AuthMiddlewareStack： django的channels封装了django的auth模块，使用这个配置我们就可以在consumer中通过下边的代码获取到用户的信息

self.scope类似于django中的request，包含了请求的type、path、header、cookie、session、user等等有用的信息
'''

application = ProtocolTypeRouter({
    #'websocket': AuthMiddlewareStack(
    'websocket': AllowedHostsOriginValidator(
        AuthMiddlewareStack(
        URLRouter(
            apps.myapp.routing.websocket_urlpatterns
        )
        )
    ),
})