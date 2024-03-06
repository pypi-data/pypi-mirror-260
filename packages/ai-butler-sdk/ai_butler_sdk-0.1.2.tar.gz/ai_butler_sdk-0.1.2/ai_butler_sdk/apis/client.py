import httpx
import enum

base_url = ""


class TrainStatusEnum(str, enum.Enum):
    """
    训练状态
    """

    WAITING = "WAITING"
    TRAINING = "TRAINING"
    FAILURE = "FAILURE"
    FINISH = "FINISH"


def update_train_task_status(task_id: str, status: TrainStatusEnum) -> bool:
    """更新训练任务状态"""
    url = base_url + f"/train-task-groups/train-tasks/{task_id}"
    resp = httpx.put(url, json={"status": status})
    return resp.status_code == 200
