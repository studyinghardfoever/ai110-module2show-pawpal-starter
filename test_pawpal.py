from pawpal_system import Task, Pet, Owner, Scheduler


def test_mark_complete():
    task = Task("Walk", "08:00", "daily")
    assert task.completed == False
    task.mark_complete()
    assert task.completed == True


def test_add_task():
    pet = Pet("sw", "dog", 3)
    assert len(pet.get_tasks()) == 0
    pet.add_task(Task("Walk", "08:00"))
    assert len(pet.get_tasks()) == 1


def test_sort_by_time():
    owner = Owner("serena")
    pet = Pet("sw", "dog", 3)
    owner.add_pet(pet)
    pet.add_task(Task("Dinner", "18:00"))
    pet.add_task(Task("Walk", "08:00"))
    scheduler = Scheduler(owner)
    sorted_tasks = scheduler.sort_by_time()
    assert sorted_tasks[0]["time"] == "08:00"

def test_recurring_daily():
    owner = Owner("serena")
    pet = Pet("sw", "dog", 3)
    owner.add_pet(pet)
    task = Task("Walk", "08:00", "daily")
    pet.add_task(task)
    scheduler = Scheduler(owner)
    scheduler.complete_and_reschedule(pet, task)
    assert len(pet.get_tasks()) == 2


def test_conflict():
    owner = Owner("serena")
    pet = Pet("sw", "dog", 3)
    owner.add_pet(pet)
    pet.add_task(Task("Walk", "08:00"))
    pet.add_task(Task("Feed", "08:00"))
    scheduler = Scheduler(owner)
    conflicts = scheduler.detect_conflicts()
    assert len(conflicts) > 0