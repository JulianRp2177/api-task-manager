import pytest
from unittest.mock import patch
from app.utils.send_email import simulate_task_assignment_email

pytestmark = pytest.mark.asyncio


class TestSendEmailUtils:

    @patch("app.utils.send_email.log")
    async def test_simulate_task_assignment_email_logs_correctly(self, mock_log):
        user_email = "test@example.com"
        task_title = "Important Task"

        await simulate_task_assignment_email(user_email, task_title)

        mock_log.info.assert_called_once_with(
            f"Simulated notification sent to {user_email} for task '{task_title}'"
        )
