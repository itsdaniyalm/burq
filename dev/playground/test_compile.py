import sys
sys.path.insert(0, "../../")

import burq as bq
from burq.compiler import compile_app

# ── APP ──
app = bq.App(
    title="Burq CRM",
    author="Daniyal",
    api_base="http://localhost:8000",
    layout=bq.Layout(sidebar=True, topbar=True),
    theme=bq.Theme(
        radius="md",
        spacing_unit=4,
        font_sans="Space Grotesk",
        font_mono="Space Mono",
        font_size_base=14,
        border_width=1,
        shadow_strength="md",
        mode="dark",
        toggle=True,
    )
)

app.nav([
    bq.NavItem("Dashboard", icon="layout-dashboard", href="/"),
    bq.NavItem("Contacts",  icon="users",            href="/contacts"),
    bq.NavItem("Deals",     icon="circle-dollar-sign",href="/deals"),
], footer=[
    bq.NavItem("Settings",  icon="settings",         href="/settings"),
])

# ── PAGES ──
@app.page("/")
def dashboard():
    bq.title("Dashboard")

    with bq.grid(cols=4, gap="md"):
        with bq.span(cols=1):
            bq.metric("Contacts", "2,480", trend="+12%", trend_dir="up", icon="users")
        with bq.span(cols=1):
            bq.metric("Deals", "143", trend="-4%", trend_dir="down", icon="circle-dollar-sign")
        with bq.span(cols=1):
            bq.metric("Revenue", "$84k", trend_dir="flat")
        with bq.span(cols=1):
            bq.metric("Won", "38", trend="+8%", trend_dir="up", variant="accent")

    bq.spacer(size="md")

    with bq.grid(cols=3, gap="md"):
        with bq.span(cols=2):
            with bq.card("Recent Contacts", variant="raised"):
                bq.table(
                    data=bq.fetch("GET", "/contacts/"),
                    columns=["name", "company", "title"],
                    column_config={
                        "name": bq.AvatarColumn(sub_key="email"),
                    },
                    searchable=True,
                    sortable=True,
                    actions=["edit", "delete"],
                )
        with bq.span(cols=1):
            with bq.card("Pipeline"):
                bq.progress("Leads",     value=72)
                bq.progress("Qualified", value=45, variant="success")
                bq.progress("Won",       value=28, variant="warning")


@app.page("/contacts")
def contacts():
    bq.title("Contacts")
    bq.table(
        data=bq.fetch("GET", "/contacts/"),
        columns=["name", "company", "status", "created_at"],
        column_config={
            "name": bq.AvatarColumn(sub_key="email"),
            "status": bq.BadgeColumn(variant_map={
                "lead":      "default",
                "qualified": "info",
                "proposal":  "warning",
                "won":       "success",
                "lost":      "danger",
            }),
            "created_at": bq.DateColumn(),
        },
        searchable=True,
        sortable=True,
        checkable=True,
        actions=["edit", "delete"],
    )

# ── MODALS ──
@app.modal("add-contact")
def add_contact_modal():
    with bq.modal("add-contact", title="Add Contact", size="md"):
        with bq.modal_body():
            with bq.grid(cols=2, gap="md"):
                bq.input("Full Name", required=True, icon="user")
                bq.input("Email",     type="email",  icon="mail")
                bq.input("Company")
                bq.select("Status",
                    options=["Lead","Qualified","Won","Lost"],
                    searchable=True
                )
        with bq.modal_footer():
            bq.button("Cancel", variant="secondary", onclick=bq.close_modal())
            bq.button("Save",   variant="primary",   icon="save")


# ── COMPILE ──
compile_app(app, output_dir="../../dist")