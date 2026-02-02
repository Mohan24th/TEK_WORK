import streamlit as st
import pandas as pd
from db import get_connection
from billing import init_cart, add_to_cart, save_bill,generate_invoice_text

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Inventory & Billing",
    page_icon="🧾",
    layout="wide"
)

st.title(" Inventory & Billing Management System")
st.caption("Simple shop inventory and billing application")

st.divider()

menu = st.sidebar.radio(
    " Navigation",
    ["Add Product", "Billing", "Daily Sales"]
)

init_cart()

# ---------------- ADD PRODUCT ----------------
if menu == "Add Product":
    st.subheader(" Add New Product")

    col1, col2 = st.columns(2)

    with col1:
        name = st.text_input("Product Name")
        price = st.number_input("Price (₹)", min_value=1.0, step=1.0)

    with col2:
        stock = st.number_input("Stock Quantity", min_value=1, step=1)

    if st.button("➕ Add Product", use_container_width=True):
        if name.strip() == "":
            st.warning("Product name cannot be empty")
        else:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO products (name, price, stock) VALUES (%s, %s, %s)",
                (name, price, stock)
            )
            conn.commit()
            conn.close()
            st.success("Product added successfully")

# ---------------- BILLING ----------------
elif menu == "Billing":
    st.subheader(" Generate Bill")

    conn = get_connection()
    df = pd.read_sql("SELECT * FROM products", conn)
    conn.close()

    if df.empty:
        st.info("No products available. Please add products first.")
    else:
        col1, col2, col3 = st.columns([3, 2, 2])

        with col1:
            product = st.selectbox("Select Product", df["name"])

        product_data = df[df["name"] == product].iloc[0]

        with col2:
            quantity = st.number_input(
                "Quantity",
                min_value=1,
                max_value=int(product_data["stock"]),
                step=1
            )

        with col3:
            st.metric("Price", f"₹ {product_data['price']}")

        if st.button("🛒 Add to Cart", use_container_width=True):
            add_to_cart(
                product_data["id"],
                product_data["name"],
                product_data["price"],
                quantity
            )
            st.success("Added to cart")

        st.divider()

        # ---------------- CART ----------------
        if st.session_state.cart:
            st.subheader(" Cart Summary")

            cart_df = pd.DataFrame(st.session_state.cart)
            cart_df.index = range(1, len(cart_df) + 1)

            st.dataframe(
                cart_df[["name", "price", "quantity", "total"]],
                use_container_width=True
            )

            col1, col2 = st.columns(2)

            with col1:
                st.metric("Total Items", cart_df["quantity"].sum())

            with col2:
                total = cart_df["total"].sum()
                st.metric("Total Amount", f"₹ {total}")

            if st.button(" Generate Bill", use_container_width=True):
                invoice_text = generate_invoice_text()
                save_bill()

                st.success("Bill generated successfully")

                st.download_button(
                    label="⬇️ Download Invoice",
                    data=invoice_text,
                    file_name="invoice.txt",
                    mime="text/plain"
                )
                
        else:
            st.info("Cart is empty")



# ---------------- DAILY SALES ----------------
elif menu == "Daily Sales":
    st.subheader(" Daily Sales Summary")

    conn = get_connection()
    df = pd.read_sql(
        """
        SELECT bill_date, SUM(total_amount) AS total_sales
        FROM bills
        GROUP BY bill_date
        ORDER BY bill_date DESC
        """,
        conn
    )
    conn.close()

    if df.empty:
        st.info("No sales data available")
    else:
        today_sales = df.iloc[0]["total_sales"]
        st.metric(" Latest Day Sales", f"₹ {today_sales}")

        st.divider()
        st.dataframe(df, use_container_width=True)
