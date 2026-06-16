# Project Testing Instructions

## Overview

Follow these steps to run unit tests and verify fault detection in the project.

## Setup

1. **(Optional)** Visit the GitHub repository: [Ardavamik/Sng352_Project](https://github.com/Ardavamik/Sng352_Project.git)

## Testing Procedure

### Step 1: Run Initial Tests

Execute the unit tests from the terminal:

Example:

```bash
python -m unittest testfile.py
```

### Step 2: Introduce Faults

If the initial tests pass:

- Edit the source code to intentionally introduce faults
- Follow the comments provided below each function in the **Results** section
- Run the unit tests again:

```bash
python -m unittest testfile.py
```

### Step 3: Verify Fault Detection

- If the output shows **FAIL**, the unit tests have successfully revealed the fault
- This indicates the goal is achieved

### Step 4: Reset and Repeat

- Revert the source code back to its original form
- Repeat the process for the next unit test

# Efe-Project Testing Instructions

## Setup

1. **(Optional)** Visit the GitHub repository: [Ardavamik/Sng352_Project](https://github.com/Ardavamik/Sng352_Project.git)
2. Download the folder [Tests_of_Efe]

## Testing Procedure

- All tests and their explanations are given in the [sng 352.ipynb] jupyter notebook file.
