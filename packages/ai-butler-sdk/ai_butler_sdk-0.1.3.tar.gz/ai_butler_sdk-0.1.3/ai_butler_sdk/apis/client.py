import httpx
import enum
from ai_butler_sdk.settings import settings
from loguru import logger

base_url = settings.AI_BUTLER_SDK_BASE_URL
token = settings.AI_BUTLER_SDK_TOKEN


class TrainStatusEnum(str, enum.Enum):
    """
    训练状态
    """

    WAITING = "WAITING"
    TRAINING = "TRAINING"
    FAILURE = "FAILURE"
    FINISH = "FINISH"


def update_train_task_status(task_id: str, status: TrainStatusEnum):
    """更新训练任务状态"""
    headers = {"Authorization": token}
    url = base_url + f"/ai-models/train-task-groups/train-tasks/{task_id}/status"
    resp = httpx.put(url, json={"status": status}, headers=headers)
    if resp.status_code == 200:
        logger.info(f"训练任务id: {task_id}, 状态变更为: {status}")
    else:
        logger.error(f"训练任务id: {task_id}, 状态变更失败! " f"status_code: {resp.status_code}, 期待变更为: {status}")
