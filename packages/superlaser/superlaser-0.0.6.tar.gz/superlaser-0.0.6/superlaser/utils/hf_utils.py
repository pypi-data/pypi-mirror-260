from huggingface_hub import HfApi, snapshot_download, create_repo


class HuggingFaceHandler:
    def __init__(
        self,
        token,
        model_id,
        local_dir,
        repo_id,
        max_workers=4,
        repo_type="model",
        private_repo=False,
    ):
        self.api = HfApi(token=token)
        self.model_id = model_id
        self.local_dir = local_dir
        self.max_workers = max_workers
        self.repo_id = repo_id
        self.repo_type = repo_type
        self.private_repo = private_repo

    def download_model_snapshot(self):
        snapshot_download(
            self.model_id, local_dir=self.local_dir, max_workers=self.max_workers
        )

    def upload_folder(self):
        self.api.upload_folder(
            folder_path=self.local_dir, repo_id=self.repo_id, repo_type=self.repo_type
        )

    def create_repository(self, repo_name):
        create_repo(
            repo_name,
            token=self.api.token,
            private=self.private_repo,
            repo_type=self.repo_type,
        )


# Example usage:
# hf_handler = HuggingFaceHandler(
#     token="your_token_here",
#     model_id="mistralai/Mistral-7B-Instruct-v0.2",
#     local_dir="tmp/hf_models/mistral-7b-instruct-v0.2",
#     repo_id="your_repo_id",
#     repo_type="model",
#     private_repo=True
# )
# hf_handler.create_repository("zeroshot/test")
# hf_handler.download_model_snapshot()
# hf_handler.upload_folder()
