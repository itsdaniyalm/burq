import sys
sys.path.insert(0, "../../")

import burq as bq

# ── APP ──
app = bq.App(
    title="CRM",
    api_base="http://localhost:8000",
    layout=bq.Layout(sidebar=True, topbar=True),
    theme=bq.Theme(primary="#F0A202", gray="#0E1428", mode="dark")
)

app.nav([
    bq.NavItem("Dashboard", icon="layout-dashboard", href="/"),
    bq.NavItem("Contacts",  icon="users",            href="/contacts"),
    bq.NavItem("Deals",     icon="circle-dollar-sign",href="/deals"),
], footer=[
    bq.NavItem("Settings", icon="settings", href="/settings"),
])

# ── PAGE ──
@app.page("/")
def dashboard():
    bq.title("Dashboard")

    with bq.row(gap="md", justify="between"):
        bq.metric("Contacts", "2,480", trend="+12%", trend_dir="up",   icon="users")
        bq.metric("Deals",    "143",   trend="-4%",  trend_dir="down", icon="circle-dollar-sign")
        bq.metric("Revenue",  "$84k",  trend_dir="flat")
        bq.metric("Won",      "38",    trend="+8%",  trend_dir="up",   variant="accent")

    with bq.grid(cols=3, gap="md"):
        with bq.span(cols=2):
            with bq.card("Recent Contacts", variant="raised"):
                bq.table(
                    data=bq.fetch("GET", "/contacts/"),
                    columns=["name", "company", "status"],
                    searchable=True,
                    sortable=True,
                    actions=["edit", "delete"],
                )

        with bq.span(cols=1):
            with bq.card("Pipeline"):
                bq.progress("Leads",     value=72)
                bq.progress("Qualified", value=45, variant="success")
                bq.progress("Won",       value=28, variant="warning")

# ── MODAL ──
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
            bq.textarea("Notes", placeholder="Add a note...")
        with bq.modal_footer():
            bq.button("Cancel", variant="secondary", onclick=bq.close_modal())
            bq.button("Save",   variant="primary",   icon="save")

# ── RUN ──
import json

tree = app.run_page("/")
print("=== PAGE TREE ===")
print(json.dumps(tree, indent=2, default=str))