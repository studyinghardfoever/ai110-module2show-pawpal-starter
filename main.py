from pawpal_system import Task, Pet, Owner, Scheduler

owner = Owner("serena")

sw = Pet("sw", "dog", 3)
cc = Pet("cc", "cat", 2)
owner.add_pet(sw)
owner.add_pet(cc)


sw.add_task(Task("Morning walk", "18:00", "daily"))
sw.add_task(Task("Dinner", "08:00", "daily"))
cc.add_task(Task("Vet visit", "15:00", "once"))
cc.add_task(Task("Play time", "15:00", "daily")) 
sw.get_tasks()[0].mark_complete()

scheduler = Scheduler(owner)
sorted_tasks = scheduler.sort_by_time()

print("=== Today's Schedule ===")
for task in sorted_tasks:
        status = "✓" if task["completed"] else "x"
        print(f"  [{status}] {task['time']} - {task['description']} ({task['frequency']})")

conflicts = scheduler.detect_conflicts()
if conflicts:
    print("\n=== Conflicts Detected ===")
    for n in conflicts:
        print(" ⚠️ " + n)
else:
    print("\nNo conflicts detected.")



print("\n=== Incomplete Tasks ===")
for task in scheduler.filter_incomplete_tasks():
    print(f"  {task['time']} - {task['description']} ({task['pet_name']})")

print("\n=== sw's Tasks ===")
for task in scheduler.filter_by_pet("sw"):
    print(f"  {task['time']} - {task['description']} ({task['pet_name']})")




# Test recurring tasks: complete a daily task and see if the next one is auto-generated
print("\n=== Test Recurring Tasks ===")
walk_task = sw.get_tasks()[0]      # get sw's first task
print("Task count before completing:", len(sw.get_tasks()))

scheduler.complete_and_reschedule(sw, walk_task)   # complete and auto-schedule next

print("Task count after completing:", len(sw.get_tasks()))
for t in sw.get_tasks():
    status = "done" if t.completed else "pending"
    print(f"  {t.description} - {t.task_date} - {status}")