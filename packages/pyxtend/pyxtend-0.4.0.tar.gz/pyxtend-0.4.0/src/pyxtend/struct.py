from collections.abc import Iterable
from typing import Any, Union


def struct(obj: Any, level: int = 0, limit: int = 3, examples: bool = False) -> Union[str, dict]:
    """
    Returns the general structure of a given Python object.

    Args:
        obj: The Python object to analyze.
        level: The current depth of recursion (default: 0).
        limit: The maximum number of elements to display for each type (default: 3).
        examples: Whether to include examples of elements in the returned structure (default: False).

    Returns:
        The structure of the input object as a dictionary or string.
    """
    obj_type_name = type(obj).__name__

    if isinstance(obj, (int, float, bool)):
        return obj_type_name
    elif isinstance(obj, str):
        return "str"
    elif obj_type_name in ["Tensor", "EagerTensor"]:
        # This works for both TensorFlow and PyTorch
        return {obj_type_name: [f"{obj.dtype}, shape={tuple(getattr(obj, 'shape', ()))}"]}
    elif obj_type_name == "ndarray":
        inner_structure = "empty" if obj.size == 0 else struct(obj.item(0), level + 1)
        shape = tuple(obj.shape)
        dtype = obj.dtype.name
        return {f"{type(obj).__name__}": [f"{dtype}, shape={shape}"]}
    elif obj_type_name == "Polygon":
        coords = list(getattr(obj, "exterior", {}).coords) if hasattr(obj, "exterior") else []
        shape = (len(coords), len(coords[0]) if coords else 0)
        return {f"{type(obj).__name__}": [f"float64, shape={shape}"]}
    elif obj_type_name == "DataFrameGroupBy":
        return groupby_summary(obj)
    elif isinstance(obj, Iterable) and not isinstance(obj, (str, bytes)):
        if level < limit:
            if examples:
                inner_structure = [x for x in obj]
            else:
                inner_structure = [struct(x, level + 1) for x in obj]
            if len(obj) > 3:
                inner_structure = inner_structure[:3] + [f"...{len(obj)} total"]
            return {type(obj).__name__: inner_structure}
        else:
            return {type(obj).__name__: "..."}
    else:
        # Handle custom objects
        attributes = {key: struct(getattr(obj, key), level + 1) for key in dir(obj) if not key.startswith("_")}
        return {obj_type_name: attributes}


def groupby_summary(groupby_object):
    """
    Provide a comprehensive summary of a DataFrameGroupBy object, focusing on key statistics,
    examples of groups, and overall group description including total items and average items per group.

    Parameters:
    - groupby_object: A pandas DataFrameGroupBy object.

    Returns:
        - summary_data: A dictionary with many keys:
    """
    # Total number of groups and total items across all groups
    num_groups = groupby_object.ngroups
    total_items = sum(len(group) for _, group in groupby_object)
    average_items_per_group = total_items / num_groups if num_groups > 0 else 0

    # Summary statistics of group sizes
    group_sizes = groupby_object.size()

    print("Examples of groups (first row per group):")
    # Initialize a counter
    group_examples = {}
    for name, group in groupby_object:
        group_examples[name] = group.head(2)

    # Global aggregated statistics for numeric columns (mean, median)
    try:
        # Explicitly specify numeric_only=True
        global_mean_values = groupby_object.mean(numeric_only=True).mean(
            numeric_only=True
        )  # Mean of means for each group
    except TypeError:
        global_mean_values = "No numeric columns to calculate mean."

    try:
        # Explicitly specify numeric_only=True
        global_median_values = groupby_object.median(numeric_only=True).median(
            numeric_only=True
        )  # Median of medians for each group
    except TypeError:
        global_median_values = "No numeric columns to calculate median."

    summary_data = {
        "total_items": total_items,
        "num_groups": num_groups,
        "average_items_per_group": average_items_per_group,
        "group_size_stats": group_sizes.describe().to_dict(),  # Convert Series to dictionary
        "group_examples": group_examples,
        "mean_values": global_mean_values,
        "median_values": global_median_values,
    }

    return summary_data
