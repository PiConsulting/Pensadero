from .views import UserView


# list with each access point in dict format
urls = [
    {
        'resource': UserView,
        'path': '/users',
        'endpoint': 'users',
    },
]
