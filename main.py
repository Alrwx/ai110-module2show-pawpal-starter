"""quick terminal demo to sanity-check pawpal+ backend logic."""

from pawpal_system import Task, Pet, Owner, Scheduler


def main():
    # set up the owner
    owner = Owner(name="Jordan")
    print(f"owner: {owner.name}\n")

    # add two pets
    mochi = Pet(name="Mochi", species="dog", age=3)
    luna = Pet(name="Luna", species="cat", age=5)
    owner.add_pet(mochi)
    owner.add_pet(luna)
    print(f"pets: {mochi}, {luna}\n")

    # add mochi's tasks (out of order on purpose)
    mochi.add_task(Task(description="evening walk", time="18:00", priority="high", duration_minutes=30, frequency="daily"))
    mochi.add_task(Task(description="morning walk", time="07:30", priority="high", duration_minutes=30, frequency="daily"))
    mochi.add_task(Task(description="breakfast", time="08:00", priority="high", duration_minutes=10, frequency="daily"))

    # add luna's tasks
    luna.add_task(Task(description="feed luna", time="08:00", priority="high", duration_minutes=10, frequency="daily"))
    luna.add_task(Task(description="play time", time="14:00", priority="medium", duration_minutes=20))
    luna.add_task(Task(description="vet appointment", time="10:00", priority="high", duration_minutes=60, frequency="once"))

    # spin up the scheduler
    scheduler = Scheduler(owner)

    # print today's full schedule (time-sorted)
    print("=" * 45)
    print(scheduler.generate_schedule_summary())
    print("=" * 45)

    # check conflict detection (both pets have an 08:00 task)
    print("\nchecking for conflicts...")
    conflicts = scheduler.detect_conflicts()
    if conflicts:
        for c in conflicts:
            print(f"  {c}")
    else:
        print("  no conflicts found")

    # check pet filter
    print(f"\ntasks for mochi only:")
    for task in scheduler.filter_by_pet("Mochi"):
        print(f"  {task}")

    # check status filter
    print(f"\npending tasks: {len(scheduler.filter_by_status(completed=False))}")

    # mark a task done and test recurring behavior
    print("\nmarking 'morning walk' as complete...")
    scheduler.mark_task_complete("Mochi", "morning walk")

    # make sure the recurring task got re-added
    mochi_tasks = scheduler.filter_by_pet("Mochi")
    print(f"mochi now has {len(mochi_tasks)} tasks (new recurring one added):")
    for task in scheduler.sort_by_time(mochi_tasks):
        print(f"  {task}")

    # show priority sort
    print("\nall tasks sorted by priority:")
    for task in scheduler.sort_by_priority():
        print(f"  {task}")


if __name__ == "__main__":
    main()
