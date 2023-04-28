from unittest.mock import patch, MagicMock

from django.core import mail
from django.template.loader import render_to_string

from main.models import Task
from main.services.mail import send_assign_notification
from test.base import TestViewSetBase
from test.factories import TaskFactory, DeveloperFactory


class TestSendEmail(TestViewSetBase):
    @patch.object(mail, "send_mail")
    def test_send_assign_notification(self, fake_sender: MagicMock) -> None:
        task = TaskFactory()
        developer = DeveloperFactory()
        task.assigned_to.add(developer)
        assignees = [assignee.email for assignee in task.assigned_to.all()]
        send_assign_notification(task.id)

        fake_sender.assert_called_once_with(
            subject="You've assigned a task.",
            message="",
            from_email=None,
            recipient_list=assignees,
            html_message=render_to_string(
                "emails/notification.html",
                context={"task": Task.objects.get(pk=task.id)},
            ),
        )
