# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class PurchaseOrder(models.Model):
    _name = "purchase.order"
    _inherit = [
        "purchase.order",
        "mixin.policy",
        "mixin.sequence",
    ]
    _document_number_field = "name"

    def _compute_policy(self):
        _super = super(PurchaseOrder, self)
        _super._compute_policy()

    type_id = fields.Many2one(
        comodel_name="purchase_order_type",
        string="Type",
        required=True,
        readonly=True,
        states={
            "draft": [("readonly", False)],
        },
    )
    email_ok = fields.Boolean(
        string="Can Send by Email",
        compute="_compute_policy",
        compute_sudo=True,
    )
    resend_email_ok = fields.Boolean(
        string="Can Re-Send by Email",
        compute="_compute_policy",
        compute_sudo=True,
    )
    email_po_ok = fields.Boolean(
        string="Can Send PO by Email",
        compute="_compute_policy",
        compute_sudo=True,
    )
    print_ok = fields.Boolean(
        string="Can Print RFQ",
        compute="_compute_policy",
        compute_sudo=True,
    )
    confirm_ok = fields.Boolean(
        string="Can Confirm Order",
        compute="_compute_policy",
        compute_sudo=True,
    )
    approve_ok = fields.Boolean(
        string="Can Approve Order",
        compute="_compute_policy",
        compute_sudo=True,
    )
    invoice_ok = fields.Boolean(
        string="Can Create Bill",
        compute="_compute_policy",
        compute_sudo=True,
    )
    reminder_mail_ok = fields.Boolean(
        string="Can Confirm Receipt Date",
        compute="_compute_policy",
        compute_sudo=True,
    )
    draft_ok = fields.Boolean(
        string="Can Set to Draft",
        compute="_compute_policy",
        compute_sudo=True,
    )
    cancel_ok = fields.Boolean(
        string="Can Cancel",
        compute="_compute_policy",
        compute_sudo=True,
    )
    done_ok = fields.Boolean(
        string="Can Lock",
        compute="_compute_policy",
        compute_sudo=True,
    )
    unlock_ok = fields.Boolean(
        string="Can Unlock",
        compute="_compute_policy",
        compute_sudo=True,
    )
    manual_number_ok = fields.Boolean(
        string="Can Input Manual Document Number",
        compute="_compute_policy",
        compute_sudo=True,
    )

    @api.model
    def default_get(self, fields):
        _super = super(PurchaseOrder, self)
        res = _super.default_get(fields)

        res["name"] = "/"

        return res

    @api.model
    def create(self, vals):
        vals["name"] = "/"
        _super = super(PurchaseOrder, self)
        res = _super.create(vals)
        return res

    def button_approve(self, force=False):
        _super = super(PurchaseOrder, self)
        res = _super.button_approve(force=force)
        for record in self:
            if record.state == "purchase" and (not record.name or record.name == "/"):
                record._create_sequence()
        return res

    @api.model
    def _get_policy_field(self):
        res = super(PurchaseOrder, self)._get_policy_field()
        policy_field = [
            "email_ok",
            "resend_email_ok",
            "email_po_ok",
            "print_ok",
            "confirm_ok",
            "approve_ok",
            "invoice_ok",
            "reminder_mail_ok",
            "draft_ok",
            "cancel_ok",
            "done_ok",
            "unlock_ok",
            "manual_number_ok",
        ]
        res += policy_field
        return res

    def name_get(self):
        result = []
        for record in self:
            if getattr(record, self._document_number_field) == "/":
                name = "*" + str(record.id)
            else:
                name = record.name
            result.append((record.id, name))
        return result
