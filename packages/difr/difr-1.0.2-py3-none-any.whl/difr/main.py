"""main."""
import argparse
import shutil
import sys
from pathlib import Path
from typing import Sequence

from rich.console import Console
from rich.progress import track
from rich.table import Table
from rich.traceback import install

from .feature_extractor import FeatureExtractor
from .similar_image_finder import SimilarImageFinder

install()
console = Console()


def _parse_argument() -> argparse.Namespace:
    parser = argparse.ArgumentParser("", add_help=True)
    parser.add_argument(
        "--target_dir_path",
        "-t",
        type=Path,
        required=True,
        help="Specifies the directory containing the images to be analyzed for similarity. "
        "Images in this directory will be compared against images in the directories specified by --compare_dir_path. "
        "Only images that do not have similar counterparts in the comparison directories will be copied to the "
        "directory specified by --save_dir. "
        "This option is essential for defining the source of images you wish to evaluate for uniqueness.",
    )
    parser.add_argument(
        "--compare_dir_path",
        "-c",
        nargs="+",
        type=Path,
        default=[],
        help="Specifies one or more directories against which images in the target directory (--target_dir_path) "
        "will be compared to identify similar images. Separate multiple directory paths with a space. "
        "This option allows you to define the scope of your comparison to detect similarities across "
        "different image collections.",
    )
    parser.add_argument(
        "--compare_self",
        "-cs",
        action="store_true",
        help="Enables the comparison of images within the target directory (--target_dir_path) against each other, "
        "in addition to comparisons with images in the comparison directories (--compare_dir_path). "
        "This option ensures that the target directory itself does not contain duplicate or similar images, "
        "providing a more thorough cleaning of your image dataset.",
    )
    parser.add_argument(
        "--batch_size",
        "-b",
        type=int,
        default=16,
        help="Specifies the number of images to process in a single batch when extracting "
        "features using the CNN model. A larger batch size can improve computational efficiency "
        "by taking advantage of parallel processing capabilities, "
        "but it will also increase memory consumption. "
        "Choose a batch size that balances the speed of processing with the available memory resources on your system. "
        "Default value is recommended for most users, "
        "but you can adjust it according to your system's specifications and memory capacity.",
    )
    parser.add_argument(
        "--similarity_threshold",
        "-th",
        type=float,
        default=0.98,
        help="Specifies the cosine similarity threshold for determining if two images are considered similar. "
        "The value should be between 0 and 1, where a higher value means a stricter criterion for similarity. "
        "Images with a cosine similarity score above this threshold will be considered similar. "
        "Adjusting this value allows you to control the sensitivity of the similarity detection: "
        "a lower threshold may result in more images being identified as similar, "
        "while a higher threshold may reduce the number of images classified as similar. "
        "Choose a threshold that best fits your requirements for similarity in the context of your task. ",
    )
    parser.add_argument(
        "--cache_dir_path",
        "-e",
        type=Path,
        default=None,
        help="Specifies a directory to cache the computed features. "
        "If provided, the tool will save the extracted features to the specified directory after the first run, "
        "and will attempt to load them from this cache for subsequent runs. "
        "This can greatly reduce computation time when processing the same images multiple times. "
        "Ensure that the specified directory exists and you have "
        "the necessary permissions to write to and read from it.",
    )
    parser.add_argument(
        "--workers",
        "-w",
        type=int,
        default=4,
        help="Specifies the number of workers to be used for parallel image loading. ",
    )
    parser.add_argument(
        "--save_dir_path",
        "-s",
        type=Path,
        required=True,
        help="Specifies the directory where images that are not identified as similar will be saved. "
        "After processing all images and identifying similar ones based on the specified similarity threshold, "
        "the remaining images will be stored in this directory. "
        "This option allows you to easily separate and keep only the unique images from your dataset. "
        "If the directory does not exist, the tool attempts to create it, depending on permissions.",
    )

    return parser.parse_args()


def _save_images(image_paths: list[Path], removed_images: set[Path], save_dir_path: Path) -> None:
    if save_dir_path.is_dir():
        shutil.rmtree(save_dir_path)
    save_dir_path.mkdir(parents=True)

    for path in track(image_paths):
        if path in removed_images:
            continue

        shutil.copy(path, save_dir_path)

    console.print(f"{len(image_paths) - len(removed_images)} images have been saved to {save_dir_path}.")


def _print_results(similars: Sequence[tuple[Path, Path, float]], removed_images: set[Path]) -> None:
    console.print(f"Found {len(similars)} pairs of similar images.")
    table = Table(show_header=True)
    table.add_column("image1")
    table.add_column("image2")
    table.add_column("similarity")
    for p1, p2, s in similars:
        table.add_row(str(p1), str(p2), str(s))
    console.print(table)

    console.print("The following images will not be saved.")
    table = Table(show_header=True)
    table.add_column("deleted image")
    for p in removed_images:
        table.add_row(str(p))
    console.print(table)


def _process_for_wrong_directory(path: Path) -> None:
    console.print(f"{path} is not an existing directory.")
    sys.exit(-1)


def _get_comp_image_paths(compare_dir_paths: list[Path]) -> list[Path]:
    all_image_paths = []
    for dir_path in compare_dir_paths:
        if not dir_path.is_dir():
            _process_for_wrong_directory(dir_path)

        image_paths = list(dir_path.glob("*"))
        all_image_paths.extend(image_paths)
    return all_image_paths


def _get_removed_images(compare_self: bool, similars: Sequence[tuple[Path, Path, float]]) -> set[Path]:
    removed_images = set()
    for p1, p2, _ in similars:
        if compare_self and p1.parent == p2.parent and (p1 in removed_images or p2 in removed_images):
            continue

        removed_images.add(p1)
    return removed_images


def main() -> None:
    """Run."""
    args = _parse_argument()
    target_dir_path: Path = args.target_dir_path
    if not target_dir_path.is_dir():
        _process_for_wrong_directory(target_dir_path)

    fe = FeatureExtractor(
        Path(__file__).parent / "models" / "feature_extractor.onnx", workers=args.workers, cache_dir=args.cache_dir_path
    )
    sif = SimilarImageFinder(fe)

    target_image_paths = list(args.target_dir_path.glob("*"))
    comp_image_paths = _get_comp_image_paths(args.compare_dir_path)

    similars = sif.find_similars(
        target_image_paths,
        comp_image_paths,
        batch_size=args.batch_size,
        similarity_threshold=args.similarity_threshold,
        compare_self=args.compare_self,
    )

    removed_images = _get_removed_images(args.compare_self, similars)

    _print_results(similars, removed_images)
    _save_images(target_image_paths, removed_images, args.save_dir_path)

    cache_dir: Path = args.cache_dir_path
    if cache_dir:
        if not cache_dir.exists():
            cache_dir.mkdir(parents=True)

        fe.save_cache()


if __name__ == "__main__":
    main()
