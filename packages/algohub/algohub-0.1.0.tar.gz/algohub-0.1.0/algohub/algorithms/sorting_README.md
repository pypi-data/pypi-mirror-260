# 🔤 SORTING ALGORITHMS 🔤

## Overview

<font size="+1">
Sorting module provides various algorithms and a SortingManager class to manage and execute
sorring opearations using the specifeid algorithm. 
</font>

## Installation

<font size="+1">
To install the "algorithms" library and access this package, you can use pip:<br>
<br>

```
pip install algohub
```

</font>

## Usage

<font size="+1">
Once installed, you can import the sorting module and utilize its functionalities in Python projects.
</font>

<font size="+1">

```
from algohub.algorithms.sorting import (
    QuickSort,
    BubbleSort,
    MergeSort,
    SelectionSort,
    SortingManager
)
```

#### Sorting Manager

```
# Creating an instance of sorting manager, default is QuickSort

sorting_manager = SortingManager()
```

#### Quick Sort

```
data = ["Z", "A", "B", "D"]
sorted_data = sorting_manager.perform_sorting(data)     

print(f'Sorted data: {sorted_data}')       # ['A', 'B', 'D', 'Z']
```  

#### Bubble Sort

```
# Changing sorting strategy

bubble_sort = BubbleSort()
sorting_manager.set_sorting_strategy(bubble_sort)

data = [12, 10, 100, 500, 0, 1, 5]
sorted_data = sorting_manager.perform_sorting(data)

print(f'Sorted data: {sorted_data}')      # [0, 1, 5, 10, 12, 100, 500]
```

#### Merge Sort

```
# Changing sorting strategy

merge_sort = MergeSort()
sorting_manager.set_sorting_strategy(merge_sort)

data = ['dog', 'lion', 'cat', 'anaconda', 'tiger']
sorted_data = sorting_manager.perform_sorting(data)

print(f'Sorted data: {sorted_data}')    # ['anaconda', 'cat', 'dog', 'lion', 'tiger']
```

#### Selection Sort

```
# Changing sorting strategy

selection_sort = SelectionSort()
sorting_manager.set_sorting_strategy(selection_sort)

data = [-10, -100, 30, 50, 200, 100, 5, 0]
sorted_data = sorting_manager.perform_sorting(data)

print(f'Sorted data: {sorted_data}')    # [-100, -10, 0, 5, 30, 50, 100, 200]
```

</font>

