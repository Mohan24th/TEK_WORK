import streamlit as st
st.markdown("<h2 style='color:Blue'>MOHAN</h2>", unsafe_allow_html=True)
st.title("Anurag university student management system")
st.divider()
st.header("Welcome to the Student Management System of Anurag University")   
st.divider()
st.subheader("Manage student records efficiently and effectively")
st.write("Here you can add, view, update, and delete student information with ease.")
st.write(123)
st.write([1,2,3,4,5])
st.write({"name":"anurag","age":22})
st.divider()
st.markdown("**Bold Text**")
st.markdown("_Italic Text_")
st.markdown("<h2 style='color:red'>Red Heading</h2>", unsafe_allow_html=True)
st.divider()
st.code("print('Hello, Anurag University!')", language='python')
st.latex(r'''a + ar + a r^2 + a r^3 =c^2''')
st.divider()
if st.button("Click Me"):
    st.write("Button Clicked!")
    st.success("Success! You clicked the button.")
    st.snow()
else:
    st.write("Button not clicked yet.")
    st.error("Please click the button.")
st.divider()
name=st.text_input("Enter your name:")
if name=="":
    st.warning("Please enter your name.")
elif not name.isalpha():
    st.warning("Please enter a valid name.")
else:
    st.write(f"Hello, {name}!")
st.divider()
st.text_area("Enter your feedback")
st.divider()
if st.checkbox("Show more info"):
    st.write("Here is some more information about the Student Management System.")
st.radio("Select your role:", ("Student", "Teacher", "Admin"))
st.divider()
st.selectbox("Select your department:", ("CSE", "ECE", "MECH", "CIVIL"))

st.divider()
st.slider("Select your age:", 18, 30, 22)
st.divider()
st.date_input("Select your date of birth:")
st.divider()
st.time_input("Select your preferred time for meetings:")
st.divider()
st.file_uploader("Upload your profile picture:")
st.divider()
st.color_picker("Pick your favorite color:")
data= {
    'lat': [17.420744911090768],
    'lon': [78.65470249830989]
}
st.write("University Location:")
st.map(data)
st.divider()
with st.form("Login Form"):
    user=st.text_input("Username:")
    password=st.text_input("Password:", type="password")
    submit_button=st.form_submit_button("Submit")
    if submit_button:
        st.write(f"Welcome, {user}!")
st.divider()
st.sidebar.title("Student Management System")
st.sidebar.write("Welcome to the Student Management System!")
option=st.sidebar.selectbox("Navigate to:", ("Home", "Add Student", "View Students", "Update Student", "Delete Student"))
st.sidebar.write(f"You selected: {option}")

st.divider()
col1, col2, col3=st.columns(3)
with col1:
    st.header("Column 1")
    st.write("This is column 1")
    st.write("hello")
with col2:
    st.header("Column 2")
    st.write("This is column 2")
with col3:
    st.header("Column 3")  
    st.write("This is column 3") 
st.divider()

data = {
    'Name': ['Anurag', 'Sumit', 'Rohit'],
    'Age': [21, 22, 20],
    'Course': ['B.Tech', 'M.Tech', 'BBA']
}
st.table(data)

st.divider()

@st.cache_data
def load_data(n):

    return [1,2,3,4,5]

data=load_data()
st.write(data)

st.divider()

