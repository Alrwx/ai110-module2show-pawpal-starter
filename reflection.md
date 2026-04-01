# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

My first UML draft had four main classes: Task, Pet, Owner, and Scheduler.

The Task class handles one activity, including description, time, frequency, and completion status.

The Pet class stores each pet's info (name, species, age) and keeps that pet's task list.

The Owner class groups multiple pets together and can aggregate all tasks into one master list.

The Scheduler is the logic layer; it talks to Owner to sort, filter, detect conflicts, and handle recurring tasks.

I used Python dataclasses for Task, Pet, and Owner to keep things clean and avoid writing a bunch of __init__ boilerplate.

**b. Design changes**

The architecture changed a bit while building. At first I planned for Scheduler to hold its own task list. I refactored so Scheduler asks Owner for tasks across all pets instead. This keeps Owner as the "source of truth" and means newly added pets are picked up automatically.

I also added a pet_name field to Task. That became important once tasks were aggregated, since users need to see which pet each task belongs to.
---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- my scheduler considers time (when a task is scheduled), priority (high/medium/low), and frequency (once/daily/weekly).
- time is the main sorting key because a pet owner needs to see their day in chronological order. priority is used as a secondary view so they can focus on what matters most.
- i decided time mattered most because a daily routine is driven by the clock — you need to know what's next, not just what's important.

**b. Tradeoffs**

- one tradeoff is that conflict detection only flags exact matching start times, not overlap by duration. so if there's a 30-minute walk at 08:00 and feeding at 08:15, it won't warn yet. i kept this simpler model because most pet tasks are short and usually scheduled on the hour/half-hour. duration-aware overlap checks would've added complexity that felt out of scope.

---

## 3. AI Collaboration

**a. How you used AI**

I used AI throughout the project for brainstorming, class skeletons, unit test drafts, and debugging small issues.

The most useful prompts were specific asks like "Generate a Mermaid class diagram for these classes" and "Create pytest scripts for sorting and recurring logic."

Having AI review my early structure also helped; one suggestion pushed me to include pet_name in task objects earlier.

**b. Judgment and verification**

At one point AI suggested using a heapq priority queue. I passed on that and used Python sorted() with a lambda key. With only a small number of tasks, a queue felt like extra overhead and made the code less readable.

I validated AI-generated snippets by running them in main.py first, then locking behavior in with pytest so regressions are less likely.

---

## 4. Testing and Verification

**a. What you tested**

My test suite checks key paths: status toggling (mark_complete), task registration (pet task counts), sorting, and filtering by pet/status. I also tested identical-time conflict alerts and automatic creation of daily recurring tasks.

These tests matter because the app depends on schedule accuracy. If sorting fails, the timeline is messy; if recurrence fails, the app loses a core benefit.

**b. Confidence**

I feel reasonably confident in scheduler stability right now, around a 4/5.

With more time, I'd expand tests for overlapping intervals, bad time formats, and Streamlit session-state persistence so data survives refreshes.

---

## 5. Reflection

**a. What went well**

- i'm most satisfied with how clean the class structure turned out. the separation between owner, pet, task, and scheduler makes it easy to understand and extend. the cli-first workflow (building main.py before the ui) was really helpful — it let me verify logic without dealing with streamlit's rerun behavior.

**b. What you would improve**

- if i had another iteration, i'd add duration-aware conflict detection and a way to persist data (like saving to a json file) so tasks don't disappear when the app restarts. i'd also add more advanced scheduling like auto-suggesting optimal times based on the owner's free slots.

**c. Key takeaway**

- this project reinforced that AI is great for boilerplate and scaffolding, but the developer still has to drive the architecture. AI gives options, but it can't really weigh tradeoffs or pick the right level of simplicity for you. good judgment is knowing when to use a suggestion and when to keep things straightforward.
