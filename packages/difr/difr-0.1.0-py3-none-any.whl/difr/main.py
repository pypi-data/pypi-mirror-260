"""main."""
import argparse
import logging
import pprint
import shutil
from collections.abc import Callable, Generator, Sequence
from pathlib import Path

import numpy as np
import onnxruntime
import tqdm
from PIL import Image

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s %(name)s :%(message)s")
logger = logging.getLogger("DIFR")


def _parse_argument() -> argparse.Namespace:
    parser = argparse.ArgumentParser("", add_help=True)
    parser.add_argument(
        "--target_dir_path",
        "-t",
        type=Path,
        required=True,
        help="Specifies the directory containing the images to be analyzed for similarity. "
        "Images in this directory will be compared against images in the directories specified by --comp_dir_path. "
        "Only images that do not have similar counterparts in the comparison directories will be copied to the "
        "directory specified by --save_dir. "
        "This option is essential for defining the source of images you wish to evaluate for uniqueness.",
    )
    parser.add_argument(
        "--comp_dir_path",
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
        "in addition to comparisons with images in the comparison directories (--comp_dir_path). "
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
        "--save_dir",
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


class FeatureExtractor:
    """Feature extractor class."""

    def __init__(self, model_path: Path) -> None:
        """init."""
        self._model = onnxruntime.InferenceSession(
            str(model_path),
            providers=["CPUExecutionProvider"],
        )
        self._model_type = np.float16
        self._size = (224, 224)
        self._feature_size = 1280
        self._image_mean = np.array((0.4850, 0.4560, 0.4060)).reshape((1, 1, 3))
        self._image_std = np.array((0.2290, 0.2240, 0.2250)).reshape((1, 1, 3))

    def load_data(self, image_path: Path) -> np.ndarray:
        """Load image from image path."""
        image = Image.open(image_path)
        image = image.resize(self._size)
        return (np.array(image, dtype=self._model_type) / 255.0 - self._image_mean) / self._image_std

    def calc_features(self, images: np.ndarray) -> np.ndarray:
        """Extract features from the images."""
        return self._model.run(("output",), {"input": images})[0]

    def _split_iterator(self, iterable: Sequence, n: int) -> tuple[int, Callable]:
        iter_steps = len(iterable) // n + (len(iterable) % n > 0)

        def _batch_generator() -> Generator[Sequence, None, None]:
            for i in range(iter_steps):
                yield iterable[i * n : (i + 1) * n]

        return iter_steps, _batch_generator

    def run(self, paths: Sequence[Path], batch_size: int = 16) -> np.ndarray:
        """Extract features for a given list of image paths.

        Args:
            paths: Paths to the images.
            batch_size: Batch size.

        Returns:
            A numpy array containing the extracted features for each image.
        """
        store_type = np.float16

        features = np.zeros((len(paths), self._feature_size), dtype=store_type)
        total_steps, iter_gen = self._split_iterator(paths, n=batch_size)
        for i, batch_paths in tqdm.tqdm(enumerate(iter_gen()), total=total_steps):
            images = []
            for p in batch_paths:
                try:
                    img = self.load_data(p)
                except Exception:
                    img = np.zeros((self._size[0], self._size[1], 3), dtype=self._model_type)
                images.append(img)

            features[i * batch_size : (i + 1) * batch_size] = self.calc_features(
                np.stack(images).astype(self._model_type).transpose((0, 3, 1, 2))
            ).astype(store_type)

        return features


class SimilarImageFinder:
    """Similar image finder class."""

    def __init__(self, feature_extractor: FeatureExtractor) -> None:
        """init."""
        self._feature_extractor = feature_extractor

    def _normalize(self, vectors: np.ndarray) -> np.ndarray:
        return vectors / np.sqrt(np.sum(vectors * vectors, axis=1)).reshape(-1, 1)

    def find_similars(
        self,
        target_image_paths: list[Path],
        comp_image_paths: list[Path],
        batch_size: int,
        similarity_threshold: float = 0.98,
        compare_self: bool = True,
    ) -> Sequence[tuple[Path, Path, float]]:
        """Identify similar image pairs between target and comparison image sets, and optionally within the target set itself.

        Args:
            target_image_paths: Paths to the images in the target directory to be compared for similarity.
            comp_image_paths: Paths to the images in the comparison directories against which the target images will be compared.
            batch_size: The number of images to process in a single batch.
            similarity_threshold: The cosine similarity score threshold for considering two images as similar.
            compare_self: If True, performs similarity checks within the target image set in addition to comparisons against the comparison image set.

        Returns:
            A sequence of tuples, each containing the paths of two similar images and their similarity score.
        """
        logger.info("Calculating features for images in target_dir_path.")
        target_image_features = self._normalize(self._feature_extractor.run(target_image_paths, batch_size=batch_size))
        logger.info("Calculating features for images in comp_dir_path.")
        comp_features = self._normalize(self._feature_extractor.run(comp_image_paths, batch_size=batch_size))
        similarity = np.dot(target_image_features, comp_features.T)

        if compare_self:
            similarity = np.concatenate([similarity, np.dot(target_image_features, target_image_features.T)], axis=1)
            comp_image_paths = comp_image_paths + target_image_paths

        idx1, idx2 = np.where(similarity > similarity_threshold)
        return [
            (target_image_paths[i1], comp_image_paths[i2], similarity[i1, i2])
            for i1, i2 in zip(idx1, idx2)
            if target_image_paths[i1] != comp_image_paths[i2]
        ]


def _save_images(image_paths: list[Path], removed_images: set[Path], save_dir_path: Path) -> None:
    if save_dir_path.is_dir():
        shutil.rmtree(save_dir_path)
    save_dir_path.mkdir(parents=True)

    for path in tqdm.tqdm(image_paths):
        if path in removed_images:
            continue

        shutil.copy(path, save_dir_path)


def main() -> None:
    """Run."""
    args = _parse_argument()
    fe = FeatureExtractor(Path(__file__).parent / "models" / "feature_extractor.onnx")
    sif = SimilarImageFinder(fe)

    target_image_paths = list(args.target_dir_path.glob("*"))

    all_image_paths = []
    for dir_path in args.comp_dir_path:
        image_paths = list(dir_path.glob("*"))
        all_image_paths.extend(image_paths)

    similars = sif.find_similars(
        target_image_paths,
        all_image_paths,
        batch_size=args.batch_size,
        similarity_threshold=args.similarity_threshold,
        compare_self=args.compare_self,
    )

    logger.info("Found %d pairs of similar images.", len(similars))
    logger.info(
        "The paths of the images found and their similarity scores are as follows:\n %s",
        pprint.pformat([(str(p1), str(p2), s) for p1, p2, s in similars]),
    )

    removed_images = set()
    for p1, p2, _ in similars:
        if args.compare_self and p1.parent == p2.parent and (p1 in removed_images or p2 in removed_images):
            continue

        removed_images.add(p1)

    logger.info("The following images will be deleted:\n %s", pprint.pformat([str(p) for p in removed_images]))
    _save_images(target_image_paths, removed_images, args.save_dir)


if __name__ == "__main__":
    main()
