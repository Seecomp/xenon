from os import environ as env
import logging

log = logging.getLogger(__name__)


class Config:
    token = None
    shard_count = 1
    per_cluster = 1

    prefix = "x!"

    dbl_token = None

    support_guild = 795800607906070650
    owner_id = 778428586192797696
    invite_url = None  # Set to None to generate one automatically

    identifier = "xenon"

    db_host = "localhost"
    db_user = None
    db_password = None

    redis_host = "localhost"

    template_approval = 795800809886711860
    template_list = 795800607906070654
    template_featured = 795800772377837578

    extensions = [
        "errors",
        "help",
        "admin",
        "backups",
        "templates",
        "users",
        "basics",
        "sharding",
        "botlist",
        "api",
        "builder"
    ]


def __getattr__(name):
    default = getattr(Config, name, None)
    value = env.get(name.upper())

    if value is not None:
        if isinstance(default, int):
            return int(value)

        if isinstance(default, float):
            return float(value)

        if isinstance(default, bool):
            valid = ["y", "yes", "true"]
            return value.lower() in valid

        if isinstance(default, list):
            return value.split(",")

        return value

    return default
