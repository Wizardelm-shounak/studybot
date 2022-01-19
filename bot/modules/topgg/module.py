from LionModule import LionModule
from LionContext import register_reply_callback, unregister_reply_callback
from core.lion import Lion

from .utils import get_last_voted_timestamp, lion_loveemote, lion_yayemote
from .webhook import init_webhook

module = LionModule("Topgg")

upvote_info = "You have a boost available {}, to support our project and earn **25% more LionCoins** type `{}vote` {}"


@module.launch_task
async def register_hook(client):
    init_webhook()
    register_reply_callback(reply)
    Lion.register_economy_bonus(economy_bonus)

    client.log("Registered LionContext reply util hook.", context="Topgg")


@module.unload_task
async def unregister_hook(client):
    unregister_reply_callback(reply)
    Lion.unregister_economy_bonus(economy_bonus)

    client.log("Unregistered LionContext reply util hook.", context="Topgg")


def reply(util_func, *args, **kwargs):
    # *args will have LionContext
    # **kwargs should have the actual reply() call's extra arguments

    if not get_last_voted_timestamp(args[0].author.id):
        args = list(args)

        upvote_info_formatted = upvote_info.format(lion_yayemote, args[0].best_prefix, lion_loveemote)

        if 'embed' in kwargs:
            kwargs['embed'].add_field(
                name="\u200b",
                value=(
                    upvote_info_formatted
                ),
                inline=False
            )
        elif 'content' in args and args['content'] and len(args['content']) + len(upvote_info_formatted) < 1998:
            args['content'] += '\n\n' + upvote_info_formatted
        elif len(args) > 1 and len(args[1]) + len(upvote_info_formatted) < 1998:
            args[1] += '\n\n' + upvote_info_formatted
        else:
            args['content'] = '\n\n' + upvote_info_formatted

        args = tuple(args)

    return [args, kwargs]


def economy_bonus(lion):
    return 1.25 if get_last_voted_timestamp(lion.userid) else 1
