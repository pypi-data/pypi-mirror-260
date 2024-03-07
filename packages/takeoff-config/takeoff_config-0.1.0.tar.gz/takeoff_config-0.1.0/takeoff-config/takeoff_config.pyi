from typing import Optional

class AppConfig:
    max_batch_size: int
    batch_duration_millis: int
    echo: bool
    port: int
    enable_metrics: bool
    heartbeat_check_interval: int
    launch_management_server: bool
    launch_vertex_server: bool
    launch_sagemaker_server: bool
    management_port: int
    vertex_port: int

class ReaderConfig:
    model_name: str
    device: str
    consumer_group: str
    redis_host: Optional[str]
    backend: Optional[str]
    log_level: Optional[str]
    cuda_visible_devices: Optional[str]
    disable_continuous_generation: Optional[bool]
    max_batch_size: Optional[int]

    def dict_without_optionals(self) -> dict[str, str | int | bool]:
        """Creates Dictionary from ReaderConfig, with optional values removed.
        Returns:
            dict[str, Optional[str | int]]: Dict without optionals.
        """
        ...

def read_takeoff_readers_config(path: str, reader_id: str) -> ReaderConfig:
    """Fetches ReaderConfig from a yaml on the given path and reader_id.
    Returns:
        ReaderConfig: ReaderConfig object corresponding to the given reader_id.
    """
    ...
