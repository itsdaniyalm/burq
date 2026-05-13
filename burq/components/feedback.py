from ..context import container_node, leaf_node
from contextlib import contextmanager


def toast(
    title:    str,
    message:  str  = None,
    type:     str  = "info",   # success|error|warning|info
    duration: int  = 3000,     # ms, 0 = no auto-dismiss
):
    leaf_node("toast", {
        "title":    title,
        "message":  message,
        "type":     type,
        "duration": duration,
    })


@contextmanager
def modal(
    id:      str,
    title:   str  = None,
    size:    str  = "md",    # sm|md|lg
):
    with container_node("modal", {
        "id":    id,
        "title": title,
        "size":  size,
    }):
        yield


@contextmanager
def modal_body():
    with container_node("modal_body", {}):
        yield


@contextmanager
def modal_footer():
    with container_node("modal_footer", {}):
        yield


def alert(
    message: str,
    type:    str  = "info",   # success|error|warning|info
    title:   str  = None,
    dismiss: bool = True,
):
    leaf_node("alert", {
        "message": message,
        "type":    type,
        "title":   title,
        "dismiss": dismiss,
    })


# ── API HELPERS ──

def open_modal(id: str) -> str:
    return f"ModalManager.open('{id}')"


def close_modal(id: str = None) -> str:
    return f"ModalManager.close('{id}')" if id else "ModalManager.close(document.querySelector('.overlay--open')?.id)"