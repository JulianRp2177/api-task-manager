from tortoise import fields, models


class TaskList(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    created_at = fields.DatetimeField(auto_now_add=True)

    tasks: fields.ReverseRelation["Task"]


class Task(models.Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=255)
    description = fields.TextField(null=True)
    completed = fields.BooleanField(default=False)
    priority = fields.IntField(default=1)
    created_at = fields.DatetimeField(auto_now_add=True)
    task_list = fields.ForeignKeyField(
        "models.TaskList", related_name="tasks", on_delete=fields.CASCADE
    )

    assigned_to = fields.ForeignKeyField(
        "models.User",
        related_name="assigned_tasks",
        null=True,
        on_delete=fields.SET_NULL,
    )
