import streamlit as st
import requests
import pandas as pd
import plotly.express as px


server_url = st.secrets["backend_server_url"]

st.title("Expense Tracker Application")

option = st.sidebar.selectbox("Choose Any One", [
    "Add expenses", "View expenses", "Update expenses", 
    "Delete expenses", "Search expenses", "Sort expenses", 
    "Filter expenses", "Analyze spending"
])

categories_list = ["Food 🍛", "Travel 🚌", "Bills 📱", "Entertainment 🎬", "Health 💊", "Shopping 👕", "Others"]

if option == "Add expenses":
    st.subheader("Add Expenses")
    title = st.text_input("Enter the title")
    amount = st.text_input("Enter the amount")
    category = st.selectbox("Choose the category", categories_list)

    add_button = st.button("Add")
    if add_button:
        try:
            new_data = {"t": title, "a": float(amount), "c": category}
            res = requests.post(f"{server_url}/add_exp", json=new_data)
            if res.status_code == 200:
                st.success(f"'{title}' Details Added successfully...")
            else:
                st.error("Failed to add expense.")
        except ValueError:
            st.error("Please enter a valid numeric amount.")

elif option == "View expenses":
    st.subheader("View Expense Details")
    view_button = st.button("VIEW Expenses")
    if view_button:
        res = requests.get(f"{server_url}/view_exp")
        if res.status_code == 200:
            all_exp_data = res.json().get("expense", [])
            if all_exp_data:
                st.dataframe(pd.DataFrame(all_exp_data))
            else:
                st.info("No expenses recorded yet.")

elif option == "Update expenses":
    st.subheader("Update Expenses")
    exp_id = st.number_input("Enter ID to Update", min_value=1, step=1, format="%d")

    if "show_update_form" not in st.session_state:
        st.session_state.show_update_form = False
    if "title" not in st.session_state:
        st.session_state.title = ""
    if "amount" not in st.session_state:
        st.session_state.amount = 0.0
    if "category" not in st.session_state:
        st.session_state.category = "Others"

    fetch_button = st.button("Fetch Expenses")
    if fetch_button:
        res = requests.get(f"{server_url}/get_exp/{exp_id}")
        if res.status_code == 200:
            exp_data = res.json().get("exp_data")
            if exp_data:
                st.session_state.show_update_form = True
                st.session_state.title = exp_data.get("title", "")
                st.session_state.amount = float(exp_data.get("amount", 0.0))
                st.session_state.category = exp_data.get("category", "Others")
            else:
                st.session_state.show_update_form = False
                st.error(f"Expense ID {exp_id} Not Found")

    if st.session_state.show_update_form:
        title = st.text_input("Title", value=st.session_state.title)
        amount = st.number_input("Amount", value=st.session_state.amount)
        category = st.selectbox("Choose the category", categories_list, index=categories_list.index(st.session_state.category) if st.session_state.category in categories_list else 0)
        
        update_button = st.button("Update Expenses")
        if update_button:
            update_exp_data = {"t": title, "a": amount, "c": category}
            res = requests.put(f"{server_url}/update_exp/{exp_id}", json=update_exp_data)
            if res.status_code == 200:
                st.success(res.json()["msg"])
                st.session_state.show_update_form = False

elif option == "Delete expenses":
    st.subheader("Delete expenses from the data")
    res = requests.get(f"{server_url}/view_exp")
    if res.status_code == 200:
        all_exp_data = res.json().get("expense", [])
        if all_exp_data:
            pd_df = pd.DataFrame(all_exp_data)
            st.dataframe(pd_df)
            
            id_to_delete = st.number_input("Enter ID to Delete", min_value=1, step=1, format="%d")
            delete_button = st.button("Delete Expense")
            if delete_button:
                if id_to_delete not in pd_df["exp_id"].values:
                    st.error(f"ID {id_to_delete} not found in the data")
                else:
                    res_del = requests.delete(f"{server_url}/delete_exp/{id_to_delete}")
                    if res_del.status_code == 200:
                        st.success(res.json()["msg"])
        else:
            st.info("No records available to delete.")

elif option == "Search expenses":
    st.subheader("Search Expenses")
    search_text = st.text_input("Enter title or category")
    search_button = st.button("Search")

    if search_button and search_text:
        res = requests.get(f"{server_url}/search_exp/{search_text}")
        if res.status_code == 200:
            all_search_data = res.json().get("search_result", [])
            if not all_search_data:
                st.error("No matching expenses found")
            else:
                st.dataframe(pd.DataFrame(all_search_data))

elif option == "Sort expenses":
    st.subheader("Sort Expenses")
    column_mapping = {"Title": "title", "Amount": "amount", "Category": "category"}
    sort_column_ui = st.selectbox("Select Column", list(column_mapping.keys()))
    sort_order_ui = st.selectbox("Select Order", ["Asc", "Desc"])
    sort_button = st.button("Sort Expense")

    if sort_button:
        backend_column = column_mapping[sort_column_ui]
        backend_order = sort_order_ui.lower()
        res = requests.get(f"{server_url}/sort_exp/{backend_column}/{backend_order}")

        if res.status_code == 200:            
            all_sort_data = res.json().get("sorted_expenses", [])
            st.dataframe(pd.DataFrame(all_sort_data))
        else:
            st.error("Sorting Failed")

elif option == "Filter expenses":
    st.subheader("Filter Expenses")
    selected_category = st.selectbox("Enter Category", categories_list)
    filter_button = st.button("Filter Expense")

    if filter_button:
        res = requests.get(f"{server_url}/filter_exp/{selected_category}")
        if res.status_code == 200:
            all_exp_data = res.json().get("filtered_expenses", [])
            if not all_exp_data:
                st.error("No expenses found for this category")
            else:
                st.dataframe(pd.DataFrame(all_exp_data))

elif option == "Analyze spending":
    st.subheader("Analyze Spending")
    analyze_button = st.button("Show Analysis")

    if analyze_button:
        res = requests.get(f"{server_url}/analyze_spending")
        if res.status_code == 200:
            data = res.json()
            total = data.get("total_spending", 0)
            category_data = data.get("category_spending", [])
            
            st.success(f"Total Spending: {total}")
            
            if category_data:
                pd_df = pd.DataFrame(category_data)
                fig = px.bar(pd_df, x="category", y="total", title="Spending by Category")
                st.plotly_chart(fig)
                
                fig2 = px.pie(pd_df, names="category", values="total", title="Spending Distribution")
                st.plotly_chart(fig2)
                st.dataframe(pd_df)
            else:
                st.info("No data available for analytical visualization.")
        else:
            st.error("Analysis Failed")