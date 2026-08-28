from pathlib import Path
from huggingface_hub import snapshot_download

ROOT = Path(__file__).resolve().parent
TARGET = ROOT / "models" / "nllb-200-distilled-600M"
TARGET.mkdir(parents=True, exist_ok=True)

print("Downloading NLLB-200 distilled 600M...")
snapshot_download(
    repo_id="facebook/nllb-200-distilled-600M",
    local_dir=str(TARGET),
    local_dir_use_symlinks=False,
)
print(f"Done. Model stored at: {TARGET}")
print("You can now disconnect Internet and run Streamlit.")
