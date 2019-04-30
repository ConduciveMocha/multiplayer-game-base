def decode_dict(d):
    return {
        k.decode("utf-8"): decode_dict(v) if isinstance(v, dict) else v.decode("utf-8")
        for k, v in d.items()
    }


# TODO: Find better place for this
def make_redis_url(host, port, db):
    return f"redis://{host}:{port}/{db}"
