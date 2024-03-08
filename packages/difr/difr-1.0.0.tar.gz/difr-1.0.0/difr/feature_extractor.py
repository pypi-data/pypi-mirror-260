"""Implementation of the feature extractor."""
import pickle
from collections.abc import Callable, Generator, Sequence
from concurrent.futures.thread import ThreadPoolExecutor
from functools import partial
from pathlib import Path
from typing import Optional

import numpy as np
import onnxruntime
from PIL import Image
from rich.console import Console
from rich.progress import track

console = Console()


class DataLoader:
    """Data loader class."""

    def __init__(self, workers: int) -> None:
        """init."""
        self._workers = workers
        self._size = (224, 224)
        self._image_mean = np.array((0.4850, 0.4560, 0.4060)).reshape((1, 1, 3))
        self._image_std = np.array((0.2290, 0.2240, 0.2250)).reshape((1, 1, 3))

    @staticmethod
    def load_data(
        image_path: Path,
        size: tuple[int, int],
        image_mean: np.ndarray,
        image_std: np.ndarray,
    ) -> np.ndarray:
        """Load image from image path."""
        image = Image.open(image_path).resize(size)
        if image.mode == "P":
            image = image.convert("RGBA")
        image = image.convert("RGB")
        return (np.array(image, dtype=np.float32) / 255.0 - image_mean) / image_std

    @staticmethod
    def _load_or_create_dummy_image(
        path: Path, size: tuple[int, int], image_mean: np.ndarray, image_std: np.ndarray
    ) -> np.ndarray:
        try:
            img = DataLoader.load_data(path, size, image_mean, image_std)
        except Exception:
            img = np.zeros((size[0], size[1], 3), dtype=np.float32)

        return img

    def load_batch(self, paths: list[Path]) -> np.ndarray:
        """Load batch images."""
        with ThreadPoolExecutor(max_workers=self._workers) as executor:
            return np.stack(
                list(
                    executor.map(
                        partial(
                            DataLoader._load_or_create_dummy_image,
                            size=self._size,
                            image_mean=self._image_mean,
                            image_std=self._image_std,
                        ),
                        paths,
                    )
                )
            ).transpose((0, 3, 1, 2))


class FeatureExtractor:
    """Feature extractor class."""

    def __init__(
        self,
        model_path: Path,
        workers: int = 1,
        cache_dir: Optional[Path] = None,
    ) -> None:
        """init."""
        self._model = onnxruntime.InferenceSession(
            str(model_path),
            providers=["CPUExecutionProvider"],
        )
        self._model_type = np.float16
        self._workers = workers
        self._feature_size = 1280
        self._cache_dir = cache_dir
        self._store_type = np.float16

        self._cache_feature_path = cache_dir / "features.npy" if cache_dir else None
        self._cache_index_path = cache_dir / "index" if cache_dir else None
        if (
            self._cache_feature_path
            and self._cache_feature_path.exists()
            and self._cache_index_path
            and self._cache_index_path.exists()
        ):
            self._cache_features = np.load(self._cache_feature_path)
            with open(self._cache_index_path, "rb") as f:
                self._cache_index = pickle.load(f)
        else:
            self._cache_features = np.zeros((0, self._feature_size))
            self._cache_index = {}

        if cache_dir and not cache_dir.exists():
            cache_dir.mkdir(parents=True)

    def calc_features(self, images: np.ndarray) -> np.ndarray:
        """Extract features from the images."""
        return self._model.run(("output",), {"input": images})[0]

    def _split_iterator(self, iterable: Sequence, n: int) -> tuple[int, Callable]:
        iter_steps = len(iterable) // n + (len(iterable) % n > 0)

        def _batch_generator() -> Generator[Sequence, None, None]:
            for i in range(iter_steps):
                yield iterable[i * n : (i + 1) * n]

        return iter_steps, _batch_generator

    def _prepare_cache_data(
        self,
        paths: list[Path],
    ) -> tuple[list[int], list[Path], np.ndarray]:
        features = np.zeros((len(paths), self._feature_size), dtype=self._store_type)
        not_cached_idx = []
        not_cached_paths = []

        if self._cache_index:
            for i, path in enumerate(paths):
                if cache_index := self._cache_index.get(str(path)):
                    features[i] = self._cache_features[cache_index]
                else:
                    not_cached_idx.append(i)
                    not_cached_paths.append(path)
        else:
            not_cached_paths = paths
            not_cached_idx = list(range(len(paths)))
        return not_cached_idx, not_cached_paths, features

    def run(self, paths: list[Path], batch_size: int = 16) -> np.ndarray:
        """Extract features for a given list of image paths.

        Args:
            paths: Paths to the images.
            batch_size: Batch size.

        Returns:
            A numpy array containing the extracted features for each image.
        """
        calc_idx, calc_paths, features = self._prepare_cache_data(paths)

        total_steps, iter_gen = self._split_iterator(calc_paths, n=batch_size)
        loader = DataLoader(workers=self._workers)
        calc_features = np.zeros((len(calc_paths), self._feature_size), dtype=self._store_type)
        for i, batch_paths in track(enumerate(iter_gen()), total=total_steps):
            images = loader.load_batch(batch_paths)
            batch_features = self.calc_features(images.astype(self._model_type))
            calc_features[i * batch_size : (i + 1) * batch_size] = batch_features

            for j, f in enumerate(batch_features):
                features[calc_idx[i * batch_size + j]] = f

        if calc_paths:
            self._cache_features = np.concatenate([self._cache_features, calc_features], axis=0)
            total_cached = len(self._cache_index)
            for i, path in enumerate(calc_paths):
                self._cache_index[str(path)] = i + total_cached

        return features

    def save_cache(self) -> None:
        """Save cache data."""
        assert self._cache_feature_path and self._cache_index_path

        np.save(
            self._cache_feature_path,
            self._cache_features,
        )
        with open(self._cache_index_path, "wb") as f:
            pickle.dump(self._cache_index, f)
