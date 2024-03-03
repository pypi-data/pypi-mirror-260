from pydantic import BaseModel, root_validator, constr, conint, confloat


class LLMSettings(BaseModel):
    MODEL_NAME: str
    MODEL_REVISION: str = None
    MAX_MODEL_LENGTH: int = 512
    BASE_PATH: str = "/runpod-volume"
    LOAD_FORMAT: str = "auto"
    HF_TOKEN: str = None
    QUANTIZATION: str = None
    TRUST_REMOTE_CODE: int = 0
    SEED: int = 0
    KV_CACHE_DTYPE: str = "auto"
    DTYPE: constr(regex=r"auto|half|float16|bfloat16|float|float32") = "auto"

    class Config:
        allow_population_by_field_name = True


class TokenizerSettings(BaseModel):
    TOKENIZER_NAME: str = None
    TOKENIZER_REVISION: str = None
    CUSTOM_CHAT_TEMPLATE: str = None

    class Config:
        allow_population_by_field_name = True


class SystemGPUAndTensorParallelismSettings(BaseModel):
    GPU_MEMORY_UTILIZATION: confloat(ge=0, le=1) = 0.95
    MAX_PARALLEL_LOADING_WORKERS: int = None
    BLOCK_SIZE: conint(gt=0) = 16
    SWAP_SPACE: conint(gt=0) = 4
    ENFORCE_EAGER: int = 0
    MAX_CONTEXT_LEN_TO_CAPTURE: conint(gt=0) = 8192
    DISABLE_CUSTOM_ALL_REDUCE: int = 0

    class Config:
        allow_population_by_field_name = True


class StreamingBatchSizeSettings(BaseModel):
    DEFAULT_BATCH_SIZE: conint(gt=0) = 50
    DEFAULT_MIN_BATCH_SIZE: conint(gt=0) = 1
    DEFAULT_BATCH_SIZE_GROWTH_FACTOR: confloat(gt=0) = 3

    class Config:
        allow_population_by_field_name = True


class OpenAISettings(BaseModel):
    RAW_OPENAI_OUTPUT: int = 1
    OPENAI_SERVED_MODEL_NAME_OVERRIDE: str = None
    OPENAI_RESPONSE_ROLE: constr(regex=r"assistant|other_role") = "assistant"

    class Config:
        allow_population_by_field_name = True


class ServerlessSettings(BaseModel):
    MAX_CONCURRENCY: conint(gt=0) = 300
    DISABLE_LOG_STATS: int = 1
    DISABLE_LOG_REQUESTS: int = 1

    class Config:
        allow_population_by_field_name = True


class AllSettings(BaseModel):
    LLM_Settings: LLMSettings
    Tokenizer_Settings: TokenizerSettings
    System_GPU_and_Tensor_Parallelism_Settings: SystemGPUAndTensorParallelismSettings
    Streaming_Batch_Size_Settings: StreamingBatchSizeSettings
    OpenAI_Settings: OpenAISettings
    Serverless_Settings: ServerlessSettings

    class Config:
        allow_population_by_field_name = True

    @root_validator
    def check_settings(cls, values):
        if (
            values["LLM_Settings"].LOAD_FORMAT == "auto"
            and values["LLM_Settings"].MODEL_REVISION is not None
        ):
            raise ValueError(
                "MODEL_REVISION cannot be specified when LOAD_FORMAT is set to 'auto'"
            )
        return values
