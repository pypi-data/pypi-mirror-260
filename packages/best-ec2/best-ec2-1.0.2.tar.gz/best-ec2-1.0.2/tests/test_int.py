def test_on_demand_instance_types_lack_az_price():
    import logging

    from botocore.config import Config

    from best_ec2 import (
        BestEc2,
        InstanceTypeRequest,
        InstanceTypeResponse,
        RequestConfig,
    )

    ec2 = BestEc2({"log_level": logging.INFO})

    request: InstanceTypeRequest = {
        "vcpu": 1,
        "memory_gb": 1,
    }

    request_config: RequestConfig = {
        "ec2_client_config": Config(
            max_pool_connections=20, retries={"max_attempts": 15, "mode": "standard"}
        )
    }

    response: InstanceTypeResponse = ec2.get_types(request, request_config)

    assert response is not None, "Response should not be None"

    for instance_type in response:
        assert (
            "az_price" not in instance_type
        ), f"Instance type {instance_type.get('instance_type', 'unknown')} should not have 'az_price' key."


def test_spot_instance_types_have_az_price():
    from botocore.config import Config

    from best_ec2 import BestEc2, InstanceTypeRequest, InstanceTypeResponse, UsageClass

    ec2 = BestEc2()

    request: InstanceTypeRequest = {
        "vcpu": 1,
        "memory_gb": 1,
        "usage_class": UsageClass.SPOT.value,
    }

    request_config: RequestConfig = {
        "ec2_client_config": Config(
            max_pool_connections=20, retries={"max_attempts": 15, "mode": "standard"}
        )
    }

    response: InstanceTypeResponse = ec2.get_types(request, request_config)

    assert response is not None, "Response should not be None"

    for instance_type in response:
        assert (
            "az_price" in instance_type
        ), f"Instance type {instance_type.get('instance_type', 'unknown')} must have 'az_price' key."


def test_on_demand_gpu():
    from botocore.config import Config

    from best_ec2 import BestEc2, InstanceTypeRequest, InstanceTypeResponse, UsageClass

    ec2 = BestEc2()

    request: InstanceTypeRequest = {
        "vcpu": 1,
        "memory_gb": 1,
        "usage_class": UsageClass.ON_DEMAND.value,
        "has_gpu": True,
    }

    request_config: RequestConfig = {
        "ec2_client_config": Config(
            max_pool_connections=20, retries={"max_attempts": 15, "mode": "standard"}
        )
    }

    response: InstanceTypeResponse = ec2.get_types(request, request_config)

    for instance_type in response:
        assert "gpu_memory_gb" in instance_type

    assert response is not None, "Response should not be None"


def test_advanced():
    import logging

    from botocore.config import Config

    from best_ec2 import (
        BestEc2,
        BestEc2Options,
        InstanceTypeRequest,
        InstanceTypeResponse,
        UsageClass,
        Architecture,
        ProductDescription,
        FinalSpotPriceStrategy,
    )

    options: BestEc2Options = {
        "describe_spot_price_history_concurrency": 20,
        "describe_on_demand_price_concurrency": 15,
        "result_cache_ttl_in_minutes": 120,
        "instance_type_cache_ttl_in_minutes": 2880,
        "on_demand_price_cache_ttl_in_minutes": 720,
        "spot_price_cache_ttl_in_minutes": 5,
    }

    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s: %(levelname)s: %(message)s"
    )
    logger = logging.getLogger()

    ec2 = BestEc2(options, logger)

    request: InstanceTypeRequest = {
        "vcpu": 1,
        "memory_gb": 2,
        "usage_class": UsageClass.SPOT.value,
        "region": "eu-central-1",
        "burstable": False,
        "architecture": Architecture.X86_64.value,
        "product_description": ProductDescription.LINUX_UNIX.value,
        "is_current_generation": True,
        "is_instance_storage_supported": True,
        "max_interruption_frequency": 0,
        "availability_zones": [
            "eu-central-1a",
            "eu-central-1b",
        ],
        "final_spot_price_strategy": FinalSpotPriceStrategy.MIN.value,
    }

    request_config: RequestConfig = {
        "ec2_client_config": Config(
            max_pool_connections=20, retries={"max_attempts": 15, "mode": "standard"}
        )
    }

    response: InstanceTypeResponse = ec2.get_types(request, request_config)

    assert response is not None, "Response should not be None"


def test_simple():
    from botocore.config import Config

    from best_ec2 import (
        BestEc2,
        InstanceTypeRequest,
        InstanceTypeResponse,
    )

    ec2 = BestEc2()

    request: InstanceTypeRequest = {
        "vcpu": 1,
        "memory_gb": 1,
    }

    request_config: RequestConfig = {
        "ec2_client_config": Config(
            max_pool_connections=20, retries={"max_attempts": 15, "mode": "standard"}
        )
    }

    response: InstanceTypeResponse = ec2.get_types(request, request_config)

    assert response is not None, "Response should not be None"


def test_final_spot_price_strategy():
    from botocore.config import Config

    from best_ec2 import (
        BestEc2,
        InstanceTypeRequest,
        InstanceTypeResponse,
        UsageClass,
        Architecture,
        ProductDescription,
        FinalSpotPriceStrategy,
    )

    ec2 = BestEc2()

    request: InstanceTypeRequest = {
        "vcpu": 1,
        "memory_gb": 2,
        "usage_class": UsageClass.SPOT.value,
        "architecture": Architecture.X86_64.value,
        "product_description": ProductDescription.LINUX_UNIX.value,
        "max_interruption_frequency": 100,
        "availability_zones": ["us-east-1a", "us-east-1b", "us-east-1c"],
        "final_spot_price_strategy": FinalSpotPriceStrategy.MIN.value,
        "region": "us-east-1",
    }

    request_config: RequestConfig = {
        "ec2_client_config": Config(
            max_pool_connections=20, retries={"max_attempts": 15, "mode": "standard"}
        )
    }

    response: InstanceTypeResponse = ec2.get_types(request, request_config)

    assert response is not None, "Response should not be None"


def test_spot_instance_types_none_input_params():
    import logging

    from botocore.config import Config

    from best_ec2 import (
        BestEc2,
        InstanceTypeRequest,
        InstanceTypeResponse,
        RequestConfig,
    )

    ec2 = BestEc2({"log_level": logging.INFO})

    request: InstanceTypeRequest = {
        "vcpu": 1.0,
        "memory_gb": 1.0,
        "usage_class": "spot",
        "burstable": None,
        "architecture": None,
        "product_description": None,
        "is_current_generation": None,
        "has_gpu": None,
        "gpu_memory": None,
        "is_instance_storage_supported": None,
        "max_interruption_frequency": None,
        "availability_zones": None,
        "final_spot_price_strategy": None,
        "region": None,
    }

    request_config: RequestConfig = {
        "ec2_client_config": Config(
            max_pool_connections=20, retries={"max_attempts": 15, "mode": "standard"}
        )
    }

    response: InstanceTypeResponse = ec2.get_types(request, request_config)

    assert response is not None, "Response should not be None"
