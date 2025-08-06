from app.core.logging import get_logging

log = get_logging(__name__)


async def simulate_task_assignment_email(user_email: str, task_title: str) -> None:
    log.info(f"Simulated notification sent to {user_email} " f"for task '{task_title}'")
