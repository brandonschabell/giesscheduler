# GiesScheduler
 
## Installation
`giesscheduler` requires `python>=3.10`.

To use this script, please clone the repository.

If you are using `uv`, you do not need to install anything. If you are not, you may need to install `giesscheduler` with:
```bash
pip install -e .
```

## Usage
Open `giesscheduler/schedules.py` and update the `REQUIRED`, `SPECIALIZATIONS`, and `CAPSTONES` lists at the top of the file.


The following example requires that the student take the `ENTREPRENEURSHIP_AND_STRATIGIC_INNOVATION` and `MERGERS_AND_ACQUISITIONS` 
specializations and the `ENTREPRENEURSHIP_AND_STRATIGIC_INNOVATION` and `FINANCIAL_MANAGEMENT` capstones:

```python
REQUIRED = {
    courses.TermYear(courses.Term.SPRING1, 2025): {courses.MBA597, courses.ACCY500},
    courses.TermYear(courses.Term.SPRING2, 2025): {courses.MBA551},
    courses.TermYear(courses.Term.FALL2, 2025): {courses.ACCY532, courses.CapstoneESI},
}
SPECIALIZATIONS = [
    courses.Specialization.ENTREPRENEURSHIP_AND_STRATIGIC_INNOVATION, 
    courses.Specialization.MERGERS_AND_ACQUISITIONS
]
CAPSTONES = [
    courses.CapstoneESI, 
    courses.CapstoneFM,
]
```

Finally, run the script with:
```bash
uv run giesscheduler/schedules.py

# or `python giesscheduler/schedules.py` if you are not using `uv`.
```

## Word of Caution
I wrote this very quickly for personal use. I make no guarantee of accuracy. The script certainly was not optimized, and may take some time (~2 minutes) to run if no constraints are included.
