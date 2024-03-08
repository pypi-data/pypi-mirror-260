"""Implementation of the similar image finder."""
from collections.abc import Sequence
from pathlib import Path

import numpy as np
from rich.console import Console

from .feature_extractor import FeatureExtractor

console = Console()


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
        console.print("Calculating features for images in target_dir_path.")
        target_image_features = self._normalize(self._feature_extractor.run(target_image_paths, batch_size=batch_size))
        console.print("Calculating features for images in comp_dir_path.")
        comp_features = self._normalize(self._feature_extractor.run(comp_image_paths, batch_size=batch_size))
        similarity = np.dot(target_image_features, comp_features.T)

        if compare_self:
            similarity = np.concatenate(
                [similarity, np.triu(np.dot(target_image_features, target_image_features.T), k=1)], axis=1
            )
            comp_image_paths = comp_image_paths + target_image_paths

        idx1, idx2 = np.where(similarity > similarity_threshold)
        return [(target_image_paths[i1], comp_image_paths[i2], similarity[i1, i2]) for i1, i2 in zip(idx1, idx2)]
