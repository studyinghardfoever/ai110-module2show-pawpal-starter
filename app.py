'''import streamlit as st

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Quick Demo Inputs (UI only)")
owner_name = st.text_input("Owner name", value="Jordan")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])

st.markdown("### Tasks")
st.caption("Add a few tasks. In your final version, these should feed into your scheduler.")

if "tasks" not in st.session_state:
    st.session_state.tasks = []

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

if st.button("Add task"):
    st.session_state.tasks.append(
        {"title": task_title, "duration_minutes": int(duration), "priority": priority}
    )

if st.session_state.tasks:
    st.write("Current tasks:")
    st.table(st.session_state.tasks)
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("This button should call your scheduling logic once you implement it.")

if st.button("Generate schedule"):
    st.warning(
        "Not implemented yet. Next step: create your scheduling logic (classes/functions) and call it here."
    )
    st.markdown(
        """
Suggested approach:
1. Design your UML (draft).
2. Create class stubs (no logic).
3. Implement scheduling behavior.
4. Connect your scheduler here and display results.
"""
    )'''




import streamlit as st
from pawpal_system import Task, Pet, Owner, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")
st.title("🐾 PawPal+")

# 用 session_state 保存 owner,防止刷新丢数据
if "owner" not in st.session_state:
    st.session_state.owner = Owner("Me")   # 默认名字,下面可以改

owner = st.session_state.owner
scheduler = Scheduler(owner)

# --- 设置主人名字 ---
st.header("Owner")
new_owner_name = st.text_input("Owner name", value=owner.name)
if st.button("Update Owner Name"):
    owner.name = new_owner_name
    st.success(f"Owner name set to: {owner.name}")

st.write(f"👤 Current owner: **{owner.name}**")


# --- 添加宠物 ---
st.header("Add a Pet")
pet_name = st.text_input("Pet name")
species = st.selectbox("Species", ["dog", "cat", "other"])
age = st.number_input("Age", min_value=0, max_value=30, value=1)
if st.button("Add Pet"):
    if pet_name:
        owner.add_pet(Pet(pet_name, species, int(age)))
        st.success(f"Added pet: {pet_name}")
    else:
        st.warning("Please enter a pet name.")

# --- 添加任务 ---
st.header("Add a Task")
pets = owner.get_pets()
if pets:
    chosen_pet_name = st.selectbox("Which pet?", [p.name for p in pets])
    task_desc = st.text_input("Task description", value="Morning walk")
    task_time = st.text_input("Time (HH:MM)", value="08:00")
    frequency = st.selectbox("Frequency", ["once", "daily", "weekly"])
    if st.button("Add Task"):
        for p in pets:
            if p.name == chosen_pet_name:
                p.add_task(Task(task_desc, task_time, frequency))
                st.success(f"Added task '{task_desc}' to {chosen_pet_name}")
else:
    st.info("Add a pet first before adding tasks.")

st.divider()

# --- 显示排序后的日程 ---
st.header(" Today's Schedule (sorted by time)")
sorted_tasks = scheduler.sort_by_time()
if sorted_tasks:
    for task in sorted_tasks:
        status = "✅" if task["completed"] else "⬜"
        st.write(
            f"{status} **{task['time']}** ({task['task_date']}) — "
            f"{task['description']} — "
            f"{task['pet_name']} ({task['species']}, age {task['age']}) — "
            f"owner: {task['owner_name']} [{task['frequency']}]"
        )
else:
    st.info("No tasks yet.")

# --- 显示冲突警告 ---
conflicts = scheduler.detect_conflicts()
if conflicts:
    st.header("⚠️ Conflicts")
    for c in conflicts:
        st.warning(c)



