import kopf

@kopf.on.create('zalando.org', 'v1', 'ephemeralvolumeclaims')
def create_fn(body, **kwargs):
    print(f"A handler is called with body: {body}")
