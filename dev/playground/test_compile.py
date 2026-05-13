import sys
sys.path.insert(0, "../../")

import burq as bq
from burq.compiler import compile_app

# ── APP ──
app = bq.App(
    title="Burq CRM",
    author="Daniyal",
    api_base="http://localhost:8000/api",
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
    bq.NavItem("Deals",     icon="circle-dollar-sign", href="/deals"),
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
    bq.button("Add Contact", variant="primary", icon="plus", onclick=bq.open_modal("add-contact"))
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
        row_href="/contacts/{id}",
    )


@app.page("/deals")
def deals():
    bq.title("Deals")
    bq.table(
        data=bq.fetch("GET", "/deals/"),
        columns=["title", "status", "value", "created_at"],
        column_config={
            "title": bq.TextColumn(),
            "status": bq.BadgeColumn(variant_map={
                "lead":      "default",
                "qualified": "info",
                "proposal":  "warning",
                "won":       "success",
                "lost":      "danger",
            }),
            "value":      bq.CurrencyColumn(prefix="$", decimals=2),
            "created_at": bq.DateColumn(),
        },
        searchable=True,
        sortable=True,
        checkable=True,
        actions=["edit", "delete"],
    )


@app.page("/contacts/{contact_id}")
def contact_detail(contact_id):
    bq.breadcrumb(items=[
        {"label": "Contacts", "href": "/contacts"},
        {"label": "Contact Detail"},
    ])
    bq.spacer(size="sm")

    # profile header — hydrates client-side
    bq.contact_profile(endpoint="/contacts/{contact_id}")

    bq.spacer(size="md")

    with bq.tabs(["Deals", "Activities"]):
        with bq.tab("Deals"):
            bq.table(
                data=bq.fetch("GET", "/contacts/{contact_id}/deals"),
                columns=["title", "status", "value", "created_at"],
                column_config={
                    "status": bq.BadgeColumn(variant_map={
                        "lead":      "default",
                        "qualified": "info",
                        "proposal":  "warning",
                        "won":       "success",
                        "lost":      "danger",
                    }),
                    "value":      bq.CurrencyColumn(prefix="$", decimals=2),
                    "created_at": bq.DateColumn(),
                },
                searchable=True,
                sortable=True,
            )

        with bq.tab("Activities"):
            bq.table(
                data=bq.fetch("GET", "/contacts/{contact_id}/activities"),
                columns=["type", "note", "created_at"],
                column_config={
                    "type": bq.BadgeColumn(variant_map={
                        "call":    "info",
                        "email":   "default",
                        "meeting": "success",
                        "note":    "warning",
                    }),
                    "created_at": bq.DateColumn(),
                },
                searchable=True,
                sortable=True,
            )

@app.page("/settings")
def settings():
    bq.title("Settings")

    with bq.tabs(["General", "Team", "Notifications", "Danger Zone"]):

        with bq.tab("General"):
            with bq.card("Workspace"):
                bq.input("Workspace Name", value="Burq CRM", icon="building-2")
                bq.input("API Base URL",   value="http://localhost:8000/api", icon="link")
                bq.select("Timezone", options=[
                    "UTC", "America/New_York", "America/Chicago", "America/Los_Angeles", "Asia/Karachi"
                ])
                bq.button("Save Changes", variant="primary", icon="save")

            bq.spacer(size="md")

            with bq.card("Import Data"):
                bq.file_upload(
                    label="Upload CSV",
                    accept=".csv",
                    name="import_file",
                    helper="Contacts or deals CSV, max 10MB"
                )
                bq.button("Import", variant="primary", icon="upload")

            bq.spacer(size="md")

            bq.accordion(items=[
                {"title": "How does billing work?",
                 "content": "Burq CRM is billed monthly per seat. You can add or remove seats at any time and your bill will be prorated."},
                {"title": "Can I export my data?",
                 "content": "Yes — every table has an Export button that downloads a CSV. For a full data export, go to Danger Zone below."},
                {"title": "How do I connect my API?",
                 "content": "Set your API Base URL above. Burq will proxy all fetch calls through that base. Auth headers are configured per-app."},
            ])

        with bq.tab("Team"):
            with bq.card("Team Members"):
                bq.table(
                    data=bq.fetch("GET", "/contacts/"),
                    columns=["name", "company", "status"],
                    column_config={
                        "name":   bq.AvatarColumn(sub_key="email"),
                        "status": bq.BadgeColumn(variant_map={
                            "lead":      "default",
                            "qualified": "info",
                            "won":       "success",
                            "lost":      "danger",
                        }),
                    },
                    searchable=True,
                )
            bq.button("Invite Member", variant="primary", icon="user-plus")

        with bq.tab("Notifications"):
            with bq.card("Email Notifications"):
                bq.toggle("New contact assigned to me",  name="notif_contact",  checked=True)
                bq.toggle("Deal status changed",         name="notif_deal",     checked=True)
                bq.toggle("Weekly summary digest",       name="notif_digest",   checked=False)
                bq.toggle("Activity reminders",          name="notif_activity", checked=True)
                bq.divider()
                bq.button("Save Preferences", variant="primary", icon="save")

        with bq.tab("Danger Zone"):
            bq.alert(
                type="warning",
                title="Irreversible actions",
                message="These actions cannot be undone. Please proceed with caution."
            )
            bq.spacer(size="md")
            with bq.card("Export All Data"):
                bq.text("Download a full CSV export of all contacts, deals, and activities.", muted=True)
                bq.button("Export Everything", variant="secondary", icon="download")
            with bq.card("Delete Workspace"):
                bq.text("Permanently delete this workspace and all associated data.", muted=True)
                bq.button("Delete Workspace", variant="danger", icon="trash-2")

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
                    options=["Lead", "Qualified", "Won", "Lost"],
                    searchable=True
                )
        with bq.modal_footer():
            bq.button("Cancel", variant="secondary", onclick=bq.close_modal("add-contact"))
            bq.button("Save",   variant="primary",   icon="save")


# ── COMPILE ──
compile_app(app, output_dir="../../dist")