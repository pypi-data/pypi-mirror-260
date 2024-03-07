from .utils import parse_info, struct_start_seeds


class Task:

    def __init__(
            self,
            model=None,
            seeds=None,
            project=None,
            task_name=None,
            oss_config=None,
            redis_info=None,
            storer_info=None,
            scheduler_info=None,
            spider_num=None,
            max_retries=None,
            storer_queue_length=None,
            scheduler_queue_length=None,
    ):
        """

        :param seeds:
        :param project:
        :param task_name:
        :param redis_info:
        :param storer_info:
        :param scheduler_info: dict(DB="", table="", size="", config="")
        :param spider_num:
        :param max_retries:
        :param storer_queue_length:
        :param scheduler_queue_length:
        """
        self.model = model

        self.seeds = struct_start_seeds(seeds)
        self.project = project or "test"
        self.task_name = task_name or "spider"

        self.oss_config = oss_config

        self.redis_info = parse_info(redis_info)
        self.storer_info = parse_info(storer_info)
        self.scheduler_info = parse_info(scheduler_info)

        self.spider_num = spider_num or 1
        self.max_retries = max_retries or 5
        self.storer_queue_length = storer_queue_length or 100
        self.scheduler_queue_length = scheduler_queue_length or 100

