#!/usr/bin/env python3
"""
main.py — Entry point for the Autonomous Multi-Agent Platform.

Usage:
    python main.py --file SimpleTest.java --mode both
    python main.py --file OrderProcessor.java --mode refactor
    python main.py --file SimpleTest.java --mode document
"""

# ── Must be the very first lines — before ANY import ─────────────────────────
import os
import warnings

# Fix 1: Prevents safetensors background thread from calling HuggingFace API
# This kills the 50-line ConnectError / OSError traceback entirely
os.environ["TRANSFORMERS_OFFLINE"]        = "1"

# Fix 2: Suppresses tqdm progress bars from safetensors / HF Hub loading
os.environ["HF_HUB_DISABLE_PROGRESS_BARS"] = "1"

# Fix 3: Suppress tokenizer parallelism warning
os.environ["TOKENIZERS_PARALLELISM"]      = "false"

# Fix 4: Suppress all Python warnings
warnings.filterwarnings("ignore")

# Fix 5: Silence all third-party loggers — must be before any transformers import
import logging

_SILENT = [
    "transformers",
    "transformers.modeling_utils",
    "transformers.configuration_utils",
    "transformers.tokenization_utils_base",
    "transformers.safetensors_conversion",
    "peft",
    "torch",
    "safetensors",
    "accelerate",
    "datasets",
    "huggingface_hub",
    "huggingface_hub.utils._http",
    "huggingface_hub.utils._headers",
    "httpx",
    "httpcore",
    "urllib3",
    "filelock",
]
for _lib in _SILENT:
    logging.getLogger(_lib).setLevel(logging.CRITICAL)

# Pipeline logger — WARNING only (our own messages)
logging.basicConfig(level=logging.WARNING, format="  ⚠  %(message)s")

# ─────────────────────────────────────────────────────────────────────────────

import sys
import argparse
from pathlib import Path

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT))


def parse_args():
    parser = argparse.ArgumentParser(
        description="Autonomous Multi-Agent Platform — Java"
    )
    parser.add_argument("--file", "-f", default="SimpleTest.java",
                        help="Java file to process (default: SimpleTest.java)")
    parser.add_argument("--mode", "-m",
                        choices=["refactor", "document", "both"],
                        default="both",
                        help="Pipeline mode (default: both)")
    return parser.parse_args()


def main():
    args = parse_args()

    print()
    print("=" * 60)
    print("  Autonomous Multi-Agent Platform")
    print("  Java Code Refactoring + Documentation")
    print("=" * 60)
    print(f"  File : {args.file}")
    print(f"  Mode : {args.mode}")

    input_path = ROOT / args.file
    if not input_path.exists():
        print(f"\n  ❌ File not found: {args.file}")
        print("     Put your Java file in the project root.")
        sys.exit(1)

    source_code = input_path.read_text(encoding="utf-8")
    if not source_code.strip():
        print(f"\n  ❌ File is empty: {args.file}")
        sys.exit(1)

    print(f"  Lines: {len(source_code.splitlines())}")

    from pipeline import Pipeline
    pipeline = Pipeline()
    result   = pipeline.run(source_code, mode=args.mode)

    sys.exit(0 if result.get("success") else 1)


if __name__ == "__main__":
    main()