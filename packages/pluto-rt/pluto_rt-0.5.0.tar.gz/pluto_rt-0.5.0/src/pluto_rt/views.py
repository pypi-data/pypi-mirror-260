import asyncio
from typing import AsyncGenerator

from asgiref.sync import sync_to_async
from django.http import (
    HttpRequest,
    HttpResponseBase,
    HttpResponse,
    StreamingHttpResponse,
)
from django.template import loader, TemplateDoesNotExist

from pluto_rt.ops import get_rt_queue_handle

SSE_CLOSE = "event: close\ndata: \n\n"


async def rt_sse_content(
    request: HttpRequest, queue_name: str, item_template: str
) -> AsyncGenerator[str, None]:
    """Deliver event stream of formatted messages from the item template."""
    mqueue = get_rt_queue_handle(queue_name)

    while True:
        item = await sync_to_async(mqueue.pop)()
        if not item:
            await asyncio.sleep(0.1)
            continue
        if item == mqueue.QUEUE_EXHAUSTED:
            yield SSE_CLOSE
            return
        try:
            formatted_item = loader.render_to_string(item_template, {"item": item})
            yield f"data: {formatted_item}\n\n"
        except TemplateDoesNotExist:
            yield "data: template not found\n\n"
            yield SSE_CLOSE
            return


def rt_sse(request: HttpRequest, queue_name: str, item_template: str) -> HttpResponseBase:
    return StreamingHttpResponse(
        streaming_content=rt_sse_content(request, queue_name, item_template),
        content_type="text/event-stream",
    )


def rt_polling(request: HttpRequest, queue_name: str, item_template: str) -> HttpResponse:
    """Private/internal API response generator.

    Query redis for a named queue, and return the last `count` messages from that queue.
    Messages are deleted from the queue (via .pop()) as they are retrieved.

    If the the value of an element on the queue is the string mqueue.QUEUE_EXHAUSTED
    this view will return http 286, which tells htmx to stop polling.

    Args:
        queue_name: Required queue name
        item_template: optional template file location for rendering each row item
    Query params:
        count: Optional number of messages to retrieve "per gulp"

    Returns:
        Last `n` messages in the queue formatted in an html snippet (each rendered by the item_template)
    """
    count = request.GET.get("count")
    count = int(count) if count else 5
    mqueue = get_rt_queue_handle(queue_name)

    items = list()
    status_code = 200
    for _ in range(count):
        temp_obj = mqueue.pop()

        if not temp_obj:  # nothing further to get
            break

        # If sender tells us the queue is done, return 286
        # which instructs htmx to stop polling
        if temp_obj == mqueue.QUEUE_EXHAUSTED:
            status_code = 286
            break

        if temp_obj:
            items.append(temp_obj)

    if request.GET.get("reverse"):
        items.reverse()

    try:
        body = "".join(loader.render_to_string(item_template, {"item": item}) for item in items)
    except TemplateDoesNotExist:
        body = "template not found"
        status_code = 286
    return HttpResponse(body, status=status_code)
