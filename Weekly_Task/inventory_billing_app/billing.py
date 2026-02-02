import streamlit as st
from db import get_connection
from datetime import date

def init_cart():
    if "cart" not in st.session_state:
        st.session_state.cart = []

def add_to_cart(product_id, name, price, quantity):
    st.session_state.cart.append({
        "product_id": product_id,
        "name": name,
        "price": price,
        "quantity": quantity,
        "total": price * quantity
    })

def save_bill():
    conn = get_connection()
    cur = conn.cursor()

    total_amount = sum(float(item["total"]) for item in st.session_state.cart)

    cur.execute(
        "INSERT INTO bills (bill_date, total_amount) VALUES (%s, %s)",
        (date.today(), float(total_amount))
    )
    bill_id = cur.lastrowid

    for item in st.session_state.cart:
        cur.execute(
            "INSERT INTO bill_items (bill_id, product_id, quantity) VALUES (%s, %s, %s)",
            (
                int(bill_id),
                int(item["product_id"]),
                int(item["quantity"])
            )
        )

        cur.execute(
            "UPDATE products SET stock = stock - %s WHERE id = %s",
            (
                int(item["quantity"]),
                int(item["product_id"])
            )
        )

    conn.commit()
    conn.close()
    st.session_state.cart = []

def generate_invoice_text():
    lines = []
    lines.append("INVOICE")
    lines.append("-" * 30)

    total = 0
    for item in st.session_state.cart:
        line = (
            f"{item['name']} | "
            f"Qty: {item['quantity']} | "
            f"Price: ₹{item['price']} | "
            f"Total: ₹{item['total']}"
        )
        lines.append(line)
        total += item["total"]

    lines.append("-" * 30)
    lines.append(f"Grand Total: ₹{total}")

    return "\n".join(lines)
