# Duplicate Image Finder and Remover
DIFR(Duplicate Image Finder and Remover) offers a solution for identifying and managing similar images across multiple directories. Utilizing Convolutional Neural Networks for feature extraction, it provides users with the capability to efficiently compare images, detect similarities, and manage image datasets with ease. Key features include:

* Flexible Directory Comparisons: Specify target and comparison directories to find similar images, ensuring precise dataset management.
* Feature Caching: Reduce computation time on subsequent runs by caching image features in a specified directory.

## Installing
```
pip install difr
```

## Usage
### Use Case 1: Removing Duplicates within a Single Directory
Detect and remove duplicate images within a single directory (--target_dir_path) to declutter your image collection and save space (--save_dir_path).

**Example:**
```
difr --target_dir_path ./path/to/imagedir --save_dir_path ./path/to/savedir -th 0.95 --compare_self
```

### Use Case 2: Comparing Images Across Directories
Identify and remove images in one directory that are duplicates of images in another directory (--compare_dir_path). This is useful for merging collections without retaining duplicates.

**Example:**
```
difr --target_dir_path ./path/to/imagedir --save_dir ./path/to/savedir -th 0.95 --compare_dir_path comp_dir_1 comp_dir_2
```

### Advanced Options
* --cache_dir_path: Specify a directory to cache image features.
* --batch_size: Specifies the number of images to process in a single batch when extracting features. A larger batch size can speed up the processing by taking advantage of parallel computing capabilities, but it will also require more memory. 
* --workers: Set the number of workers for parallel image loading.
* --similarity_threshold: Set the cosine similarity score threshold for considering two images as similar. The value must be between 0 (no similarity) and 1 (identical images), where a higher value means a stricter criterion for similarity.

### Example Usage and Output
Command:
```
difr --target_dir_path ./data/train --save_dir_path ./data/train_unique --compare_dir_path data/val data/test --cache_dir_path .difr_cache --similarity_threshold 0.7 --batch_size 32 --workers 16
```

Output:  
![output1](https://github.com/opqrstuvcut/DIFR/blob/main/images/output_example.png)
