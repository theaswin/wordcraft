from odoo import models, fields, api
from datetime import timedelta


class ProjectProject(models.Model):
    _inherit = "project.project"

    assignee_ids = fields.Many2many(
        'res.users',
        string="Task Assignees",
        compute="_compute_assignee_ids",
        store=True,
        readonly=True,
        relation='project_task_assignee_rel',
        column1='project_id',
        column2='user_id',
    )

    project_assignee_ids = fields.Many2many(
        'res.users',
        string="Project Assignees",
        relation='project_manual_assignee_rel',
        column1='project_id',
        column2='user_id',
    )


    @api.depends('task_ids.user_ids')
    def _compute_assignee_ids(self):
        for project in self:
            project.assignee_ids = False
            # Collect all users assigned to tasks in this project
            users = project.task_ids.mapped('user_ids')
            project.assignee_ids = users
