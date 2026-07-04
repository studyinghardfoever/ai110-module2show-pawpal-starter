# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?


My initial UML design has four classes, each with a single clear responsibility:

- **Task** — represents one pet care activity. It stores a description, time, frequency, and completion status, and can mark itself complete via `mark_complete()`.

- **Pet** — represents one pet and owns its tasks. It stores the pet's name, species, and age, holds a list of Tasks, and can add tasks via `add_task()`.

- **Owner** — represents the pet owner and owns their pets. It stores the owner's name, holds a list of Pets, and can add pets via `add_pet()`.

- **Scheduler** — the "brain" of the system, responsible for all scheduling logic across pets. It takes an Owner, gathers every task from every pet, and provides sorting by time (`sort_by_time()`), conflict detection (`detect_conflicts()`), filtering (`filter_incomplete_tasks()`, `filter_by_pet()`), and recurring-task rescheduling (`complete_and_reschedule()`).

The relationships between classes are: an **Owner has many Pets**, a **Pet has many Tasks**, and a **Scheduler manages one Owner** to access all the pets and their tasks. The first three classes act as data containers, while the Scheduler is the processing layer that operates on all the collected tasks.




**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.


As I built the system, I made deliberate choices to keep it focused:


- I initially considered adding a `medical_history` attribute to the `Pet` class, since medical history feels important for pet care. I decided against it because it isn't used by any scheduling logic, and actionable medical items (medication, vet visits) are already captured as Tasks. Adding it would be unused "dead data" that blurs the system's scope.

- I also considered adding weather and map features to the app. I rejected these because they fall outside the project's scope (task scheduling), require external APIs that add significant complexity, and don't serve the core scheduling logic. Keeping the system focused on scheduling was more valuable than adding unrelated features.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

- What constraints does your scheduler consider (for example: time, priority, preferences)?

My scheduler's main constraint is **time**. Tasks are scheduled at a specific time (in "HH:MM" format), and the scheduler uses time as the basis for:
- **Sorting** — all tasks are ordered chronologically by their time (`sort_by_time()`).
- **Conflict detection** — if two tasks share the exact same time, the scheduler flags them as a conflict (`detect_conflicts()`).

It also considers **frequency** (once / daily / weekly) as a constraint for recurring tasks: when a daily or weekly task is completed, the scheduler automatically generates the next occurrence on the correct future date (`complete_and_reschedule()`).

I chose not to include priority or owner preferences in this version, to keep the system focused.

- How did you decide which constraints mattered most?

I decided **time** mattered most because a pet owner's core problem is knowing *what to do and when*, and avoiding double-booking themselves. Sorting by time answers "what's next," and conflict detection answers "can I actually do both of these." **Frequency** was the second priority because recurring care (daily walks, weekly baths) is the most repetitive part of pet care, so automating it saves the owner the most manual effort. I treated priority and preferences as lower-value for a first version, since they add complexity without solving the owner's most immediate need.



**b. Tradeoffs**



- Describe one tradeoff your scheduler makes.

My conflict detection only flags tasks that share the **exact same start time** (e.g., two tasks both at "08:00"). It does not detect **overlapping durations** — for example, a 30-minute walk starting at 08:00 and a feeding at 08:15 would actually overlap in real life, but my scheduler would not flag them as a conflict because their start times are different.

- Why is that tradeoff reasonable for this scenario?

This tradeoff is reasonable for a first version because it keeps the logic simple and reliable while still catching the most common and clearest conflicts (two things booked at the exact same time). Detecting overlapping durations would require every task to track a duration, plus time-range math to check for overlaps — significantly more complexity. For a busy pet owner, exact-time clashes are the most obvious scheduling mistake, so catching those delivers most of the value with much less complexity. Overlap detection could be added later as an enhancement if needed.


---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?

I used AI throughout the project, but in a specific way: instead of asking it to write full solutions, I wrote the code myself first and asked the AI to review and correct it. Concretely:

- **Design brainstorming** — In Phase 1, the AI helped me think through what each class should hold and how they relate (Owner → Pet → Task), and helped me turn that into a Mermaid UML diagram.
- **Debugging** — This was the biggest use. The AI caught many small mistakes in my code: indentation errors (like a `.sort()` placed inside the wrong loop), missing steps (forgetting `pet.add_task(next_task)` in the recurring logic), wrong return values (`return schedule` instead of `return all_tasks`), and typos (`retrun`, using `pet` instead of `Pet` for a class name).
- **Explaining concepts** — When I didn't understand something (like why `sort_by_time` needs `key=lambda`, or how `st.session_state` keeps data across refreshes), I asked the AI to explain it step by step.
- **Refactoring** — The AI suggested cleaner versions of my methods, such as returning warning strings instead of tuples in `detect_conflicts()`.

- What kinds of prompts or questions were most helpful?

The most helpful prompts were **specific and code-focused**, not vague. For example:
- Pasting my actual code and asking "what's wrong with this and why" was far more useful than asking "how do I write a scheduler."
- Asking "why" questions ("why does the return go outside the loop?") helped me actually understand the fix instead of just copying it.
- Asking the AI to **walk through an example step by step** (like tracing how the recurring task generates tomorrow's task) helped me see the logic concretely.

Vague prompts that just asked for a full solution were less helpful, because they didn't teach me anything and made it harder to debug later.



**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?


- Describe one moment where you did not accept an AI suggestion as-is.

When I wrote `detect_conflicts()`, I chose to store each conflict as a tuple of the two task dictionaries `(current_task, next_task)`. The AI suggested storing a formatted warning string instead. I didn't just accept its version — I first thought about the tradeoff: my tuple version kept the full task data (useful if I wanted to display details later), while the AI's string version was cleaner to print. I ended up switching to the string version because it matched the project requirement ("return a warning message") and displayed more clearly in both the CLI and Streamlit UI — but it was my decision after weighing both, not an automatic acceptance.

Another example: the AI (and my own instinct) considered adding features like `medical_history`, weather, and maps. I rejected these to keep the system focused on scheduling, even though they seemed appealing.

- How did you evaluate or verify what the AI suggested?

I verified AI suggestions in a few ways:
- **Running the code** — I ran `python3 main.py` and checked the actual output matched what I expected (e.g., tasks sorted correctly, the conflict warning appearing at the right time).
- **Writing tests** — My pytest suite (5 tests) automatically verified core behaviors like sorting order, recurrence creating a next-day task, and conflict detection. If the AI's suggestion broke a test, I knew something was wrong.
- **Tracing examples by hand** — For logic I wasn't sure about, I traced through a concrete example step by step (e.g., how a daily task becomes tomorrow's task) to confirm the behavior made sense before trusting it.
- **Checking against the requirements** — I compared suggestions to what the project actually asked for, rather than assuming the AI's "cleaner" version was always better.


---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?

I wrote five tests covering the core behaviors of the system:

1. **Task completion** (`test_mark_complete`) — verifies that calling `mark_complete()` changes a task's `completed` status from False to True.
2. **Adding tasks** (`test_add_task`) — verifies that adding a task to a Pet increases its task count.
3. **Sorting** (`test_sort_by_time`) — adds tasks out of order and verifies they come back sorted chronologically by time.
4. **Recurring tasks** (`test_recurring_daily`) — verifies that completing a daily task automatically generates a new task, increasing the task count.
5. **Conflict detection** (`test_conflict`) — creates two tasks at the same time and verifies the scheduler flags the conflict.

- Why were these tests important?

These tests were important because they cover the system's most critical and error-prone logic — the parts where a bug would directly break the app's core promise to the user. Sorting, recurrence, and conflict detection are the "smart" features that make PawPal+ useful, so if any of them silently failed, the schedule would be wrong or misleading. 

Automated tests also let me verify changes quickly and safely: instead of manually running the app and checking the output by eye every time, I could run `pytest` and instantly confirm nothing broke. This was especially valuable when I refactored methods or accepted AI suggestions — if a change broke a test, I knew immediately, rather than discovering the bug later. The tests act as a safety net that protects the core behaviors as the code evolves.



**b. Confidence**

- How confident are you that your scheduler works correctly?

I'm fairly confident (about 4 out of 5) in the core logic. All five automated tests pass, and they cover the most important behaviors: marking tasks complete, adding tasks, sorting by time, recurring-task generation, and conflict detection. I also manually verified the app through the CLI (`main.py`) and the Streamlit UI, and the outputs matched what I expected.

My confidence isn't a full 5/5 because the system makes some simplifying assumptions that I haven't stress-tested — for example, conflict detection only catches tasks with the exact same start time, not overlapping durations, and time is stored as a plain "HH:MM" string rather than a proper time object.

- What edge cases would you test next if you had more time?

If I had more time, I would test:

1. **Overlapping durations** — e.g., a 30-minute task at 08:00 and another at 08:15, which overlap in reality but aren't currently flagged as a conflict.
2. **Invalid or malformed time input** — e.g., "8:00" (missing leading zero) or "25:00", which could break the string-based sorting.
3. **Empty cases** — a pet with no tasks, or an owner with no pets, to make sure the scheduler handles them gracefully instead of crashing.
4. **Recurring across month/year boundaries** — e.g., completing a daily task on Dec 31 should correctly roll over to Jan 1 (timedelta should handle this, but I'd want to confirm).
5. **Same time across different pets vs. the same pet** — confirming conflicts are reported sensibly whether the clash is within one pet's schedule or across two pets.

---

## 5. Reflection

**a. What went well**


- What part of this project are you most satisfied with?

I'm most satisfied with the Scheduler class and its algorithms. Getting the recurring-task logic to work — where completing a daily task automatically generates the next day's task using timedelta — felt rewarding because it combined several ideas (object relationships, date math, and updating the pet's task list) into one working feature. I'm also satisfied that all five tests pass and that the Streamlit UI actually connects to my backend logic, so the whole system works end to end rather than just in isolation.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

I would improve how time is represented. Right now time is a plain "HH:MM" string, which works for sorting but is fragile — it can't handle durations or overlapping tasks, and it breaks if the input isn't formatted with a leading zero. In another iteration, I'd store time as a proper time/datetime object and give each task a duration, so the scheduler could detect overlapping conflicts (not just exact-time clashes) and validate input automatically. I'd also add input validation in the UI so users can't enter malformed times.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

The biggest thing I learned is that being the "architect" means making deliberate decisions about scope — deciding what NOT to build is as important as what to build. I turned down features like medical history, weather, and maps because they didn't serve the core scheduling purpose. Working with AI reinforced this: the AI could generate code quickly, but it was my job to judge whether a suggestion fit the design, verify it with tests, and keep the system focused. Writing the code myself first and using AI to review and explain — rather than to hand me answers — helped me actually understand my own system.
