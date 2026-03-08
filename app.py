import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="401A Data Utility App", page_icon="📊", layout="wide")

if "users" not in st.session_state:
    st.session_state.users = pd.DataFrame(columns=[
        "Name","Age","Tech Stack","UsageHours","Rating"
    ])

if "projects" not in st.session_state:
    st.session_state.projects = pd.DataFrame(columns=[
        "ProjectName","Technology","Progress","Status"
    ])

with st.sidebar:
    st.title("📊 ICS - 01 - 401")
    st.subheader("Data Utility App")

    page = st.radio("Choose Navigation", ["About Page", "Dashboard", "Data Filter", "Calculator", "Projects", "Feedback"])
    st.divider()
    st.caption("Shuuzky - Developer")

def about():
    st.title("About This Data Utility App")
    st.write("This is a simple Data Utility App built with streamlit to showcase various UI components with a meaningful UI flow. It was created as a practice project of the developer, Shuuzky / Lorenz Ivan Mangalino from ICS - 01 - 401, to explore Streamlit's capabilities in building interactive data tools.")   

    st.subheader("Use Case")
    st.write("It demonstrates simple data tools such as dashboards, filters, and calculators using Streamlit.")

    st.subheader("Target Users")
    st.write("Students in ICS - 01 - 401 who are also exploring Streamlit UI components.")

    st.subheader("Inputs Collected")
    st.write("User inputs, numbers for calculations, dropdown selections, and filters.")

    st.subheader("Outputs Shown")
    st.write("Graphs, charts, tables, filtered data, computed metrics, and feedbacks.") 

def dashboard():
    st.title("User Analytics Dashboard")
    df = st.session_state.users
    if df.empty:
        st.warning("No users added yet. Go to the Data Filter page to create users.")
    else:
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Users", len(df))
        col2.metric("Average Usage Hours", round(df["UsageHours"].mean(),2))
        col3.metric("Average Rating", round(df["Rating"].mean(),2))
        chart = st.selectbox(
            "Select Analytics",
            ["Usage by Age","Rating Distribution"]
        )
        if chart == "Usage by Age":
            data = df.groupby("Age")["UsageHours"].mean()
            st.line_chart(data)
        else:
            data = df["Rating"].value_counts().sort_index()
            st.bar_chart(data)
        st.subheader("User Data Table")
        st.dataframe(df, use_container_width=True)

    st.divider()
    st.title("Project Analytics")
    projects_df = st.session_state.projects

    if projects_df.empty:
        st.info("No projects submitted yet.")
    else:
        col1, col2 = st.columns(2)

        col1.metric("Total Projects", len(projects_df))

        completed = len(projects_df[projects_df["Status"] == "Completed"])
        col2.metric("Completed Projects", completed)

        st.subheader("Projects by Status")
        status_chart = projects_df["Status"].value_counts()
        st.bar_chart(status_chart)

        st.subheader("Projects Table")
        st.dataframe(projects_df, use_container_width=True)

def data_filter():
    st.title("User Manager & Filter")

    st.subheader("Add New User")

    name = st.text_input("Name")
    age = st.number_input("Age", 0, 100)
    language = st.selectbox("Tech Stack Use", 
        ["Python","Streamlit","SQL","Pandas","Git"],
        index=None, placeholder="Select a tech stack")
    usage = st.slider("Usage Hours", 0, 24)
    rating = st.slider("Rating", 0, 5)

    if st.button("Add User"):
        if not name:
            st.warning("Please enter a name.")
        elif language is None:
            st.warning("Please select a tech stack.")
        else:
            new_user = pd.DataFrame({
                "Name":[name],
                "Age":[age],
                "Tech Stack":[language],
                "UsageHours":[usage],
                "Rating":[rating]
            })
            st.session_state.users = pd.concat(
                [st.session_state.users, new_user],
                ignore_index=True
            )
            st.success("User added successfully!")
    
    st.divider()
    st.subheader("Filter Users")
    df = st.session_state.users

    if df.empty:
        st.info("No users available.")
        return
    age_range = st.slider(
        "Age Range",
        int(df["Age"].min()),
        int(df["Age"].max()),
        (int(df["Age"].min()), int(df["Age"].max()))
    )
    filtered = df[
        (df["Age"] >= age_range[0]) &
        (df["Age"] <= age_range[1])
    ]   
    st.dataframe(filtered, use_container_width=True)

def calculator():
    st.title("Calculator")
    col1, col2 = st.columns(2)
    num1 = col1.number_input("Number 1", value=0)
    num2 = col2.number_input("Number 2", value=0)

    operation = st.selectbox("Operation", ["Add","Subtract","Multiply","Divide"], 
    index=None, placeholder="Select an operation")

    if st.button("Calculate"):
        if operation == "Add":
            result = num1 + num2
        elif operation == "Subtract":
            result = num1 - num2
        elif operation == "Multiply":
            result = num1 * num2
        else:
            result = "Cannot divide by zero" if num2 == 0 else num1 / num2
        st.success(f"Result: {result}")

    rating = st.radio("Rate this tool", ["Excellent","Good","Average","Poor"])
    st.write("Your rating:", rating)

def projects():
    st.title("Project Submission and Tracking")

    project_name = st.text_input("Project Name")

    tech = st.multiselect(
        "Programming Languages Used",
        ["Python","Streamlit","SQL","Pandas","Git"]
    )

    progress = st.slider("Completion %", 0, 100, 50, 25)

    status = st.selectbox("Status", ["Planning","In Progress","Testing","Completed"],
    index=None, placeholder="Please choose your progress")

    st.progress(progress/100)

    if st.button("Submit Project"):
        new_project = pd.DataFrame({
            "ProjectName":[project_name],
            "Technology":[", ".join(tech)],
            "Progress":[progress],
            "Status":[status]
        })
        st.session_state.projects = pd.concat(
            [st.session_state.projects, new_project],
            ignore_index=True
        )

        st.success("Project Recorded")

    st.divider()
    df = st.session_state.projects
    if df.empty:
        st.info("No projects submitted yet.")
        return
    st.subheader("Manage Projects")
    selected_index = st.selectbox(
        "Select project to edit or delete",
        df.index,
        format_func=lambda x: df.loc[x, "ProjectName"]
    )

    selected_project = df.loc[selected_index]
    edit_name = st.text_input("Edit Project Name", selected_project["ProjectName"])
    edit_tech = st.text_input("Edit Technology", selected_project["Technology"])
    edit_progress = st.slider("Edit Progress", 0, 100, int(selected_project["Progress"]))
    status_options = ["Planning","In Progress","Testing","Completed"]
    edit_status = st.selectbox("Edit Status", status_options,
    index=status_options.index(selected_project["Status"])
    )
    col1, col2 = st.columns(2)

    if col1.button("Update Project"):
        st.session_state.projects.loc[selected_index] = [
            edit_name,
            edit_tech,
            edit_progress,
            edit_status
        ]
        st.success("Project updated successfully!")
    if col2.button("Delete Project"):
        st.session_state.projects = st.session_state.projects.drop(selected_index).reset_index(drop=True)
        st.warning("Project deleted!")
    st.divider()
    st.subheader("All Projects")
    st.dataframe(st.session_state.projects, use_container_width=True)

def feedback():
    st.title("User Feedback")

    with st.form("feedback_form"):
        name = st.text_input("Name")
        email = st.text_input("Email")
        experience = st.select_slider("Experience Level", options=["Beginner", "Average", "Intermediate", "Advanced"])
        comments = st.text_area("Suggestions or Comments")
        submit = st.form_submit_button("Submit")
        if submit:
            st.success("Submitted Feedback")
            st.write(name, email, experience)
            st.write(comments)

if page == "About Page":
    about()
elif page == "Dashboard":
    dashboard()
elif page == "Data Filter":
    data_filter()
elif page == "Calculator":
    calculator()
elif page == "Projects":
    projects()
else:
    feedback()  