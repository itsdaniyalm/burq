from ..context import container_node, leaf_node
from contextlib import contextmanager


def input(
    label:       str  = None,
    placeholder: str  = None,
    type:        str  = "text",   # text|email|password|number
    value:       str  = None,
    required:    bool = False,
    disabled:    bool = False,
    size:        str  = "md",     # sm|md|lg
    icon:        str  = None,
    icon_pos:    str  = "left",   # left|right
    error:       str  = None,
    helper:      str  = None,
    name:        str  = None,
):
    leaf_node("input", {
        "label":       label,
        "placeholder": placeholder,
        "type":        type,
        "value":       value,
        "required":    required,
        "disabled":    disabled,
        "size":        size,
        "icon":        icon,
        "icon_pos":    icon_pos,
        "error":       error,
        "helper":      helper,
        "name":        name,
    })


def textarea(
    label:       str  = None,
    placeholder: str  = None,
    value:       str  = None,
    required:    bool = False,
    disabled:    bool = False,
    error:       str  = None,
    helper:      str  = None,
    name:        str  = None,
    rows:        int  = 3,
):
    leaf_node("textarea", {
        "label":       label,
        "placeholder": placeholder,
        "value":       value,
        "required":    required,
        "disabled":    disabled,
        "error":       error,
        "helper":      helper,
        "name":        name,
        "rows":        rows,
    })


def select(
    label:       str   = None,
    options:     list  = None,  # list of str or dicts
    value:       str   = None,
    placeholder: str   = "Select...",
    label_key:   str   = None,  # for dict options
    value_key:   str   = None,  # for dict options
    searchable:  bool  = False,
    required:    bool  = False,
    disabled:    bool  = False,
    size:        str   = "md",  # sm|md|lg
    error:       str   = None,
    helper:      str   = None,
    name:        str   = None,
    depends_on:  str   = None,  # name of another select this depends on
):
    leaf_node("select", {
        "label":       label,
        "options":     options or [],
        "value":       value,
        "placeholder": placeholder,
        "label_key":   label_key,
        "value_key":   value_key,
        "searchable":  searchable,
        "required":    required,
        "disabled":    disabled,
        "size":        size,
        "error":       error,
        "helper":      helper,
        "name":        name,
        "depends_on":  depends_on,
    })


def toggle(
    label:    str  = None,
    value:    bool = False,
    checked:  bool = None, 
    disabled: bool = False,
    name:     str  = None,
):
    leaf_node("toggle", {
        "label":    label,
        "value":    checked if checked is not None else value,
        "disabled": disabled,
        "name":     name,
    })


def checkbox(
    label:    str  = None,
    value:    bool = False,
    disabled: bool = False,
    name:     str  = None,
):
    leaf_node("checkbox", {
        "label":    label,
        "value":    value,
        "disabled": disabled,
        "name":     name,
    })


def radio(
    label:    str  = None,
    name:     str  = None,
    value:    str  = None,
    checked:  bool = False,
    disabled: bool = False,
):
    leaf_node("radio", {
        "label":    label,
        "name":     name,
        "value":    value,
        "checked":  checked,
        "disabled": disabled,
    })


def button(
    label:   str  = None,
    variant: str  = "primary",  # primary|secondary|ghost|outline|danger
    size:    str  = "md",       # xs|sm|md|lg
    icon:    str  = None,
    icon_pos:str  = "left",     # left|right
    disabled:bool = False,
    onclick: str  = None,       # JS expression or bq.* helper
    type:    str  = "button",   # button|submit
    name:    str  = None,
):
    leaf_node("button", {
        "label":    label,
        "variant":  variant,
        "size":     size,
        "icon":     icon,
        "icon_pos": icon_pos,
        "disabled": disabled,
        "onclick":  onclick,
        "type":     type,
        "name":     name,
    })


def file_upload(
    label:  str = None,
    accept: str = None,   # e.g. ".csv,.xlsx"
    name:   str = None,
):
    leaf_node("file_upload", {
        "label":  label,
        "accept": accept,
        "name":   name,
    })

def file_upload(
    label:  str = None,
    accept: str = None,
    name:   str = None,
    helper: str = None,
    error:  str = None,
):
    leaf_node("file_upload", {
        "label":  label,
        "accept": accept,
        "name":   name,
        "helper": helper,
        "error":  error,
    })