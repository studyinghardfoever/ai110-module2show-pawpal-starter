# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:
```
=== Today's Schedule ===

sw:
  [✓] 08:00 - Morning walk (daily)
  [x] 18:00 - Dinner (daily)

cc:
  [x] 15:00 - Vet visit (once)

```

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```

============================= test session starts =============================

collected 5 items
tests/test_pawpal.py::test_mark_complete PASSED

tests/test_pawpal.py::test_add_task PASSED

tests/test_pawpal.py::test_sort_by_time PASSED

tests/test_pawpal.py::test_recurring_daily PASSED

tests/test_pawpal.py::test_conflict PASSED
============================== 5 passed in 0.07s ==============================
```

**Confidence Level:** ⭐⭐⭐⭐ (4/5) — All five tests pass, covering the core behaviors (marking complete, adding tasks, sorting, recurrence, conflict detection). I'm confident in the core logic, though edge cases like overlapping-duration conflicts aren't yet handled.

## 📐 Smarter Scheduling


| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.sort_by_time()` | Sorts all tasks chronologically by their "HH:MM" time string |
| Filtering | `Scheduler.filter_incomplete_tasks()`, `Scheduler.filter_by_pet()` | Filter tasks by completion status or by a specific pet |
| Conflict handling | `Scheduler.detect_conflicts()` | Flags tasks scheduled at the same time and returns warning messages |
| Recurring tasks | `Scheduler.complete_and_reschedule()` | When a daily/weekly task is completed, auto-generates the next occurrence using timedelta |


## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. Run the app with `streamlit run app.py`. The PawPal+ page opens in the browser.
2. Under **Owner**, enter the owner's name and click "Update Owner Name" to set who the schedule belongs to.
3. Under **Add a Pet**, enter a pet's name, choose its species (dog/cat/other), set its age, and click "Add Pet". Repeat to add multiple pets.
4. Under **Add a Task**, pick which pet the task is for, enter a description (e.g., "Morning walk"), a time in HH:MM format, and a frequency (once/daily/weekly), then click "Add Task".
5. The **Today's Schedule** section automatically shows all tasks sorted by time, with each task's date, pet, species, age, owner, and completion status.
6. If two tasks are scheduled at the same time, a **Conflicts** section appears with a yellow warning showing which tasks clash.

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->

