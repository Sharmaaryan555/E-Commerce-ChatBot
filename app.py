import streamlit as st
import openai
import os
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Load product data
with open("products.json", "r") as file:
    products = json.load(file)

# Streamlit UI
st.title("E-Commerce Chatbot 🛒")
st.write("Hi there! I'm your shopping assistant. Ask me about products, prices, or stock availability!")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "system", "content": "You are a helpful e-commerce assistant."}]

# User input form
with st.form("chat_form"):
    user_input = st.text_input("Your query:", "")
    submitted = st.form_submit_button("Send")

if submitted and user_input:
    # Add user input to conversation history
    st.session_state["messages"].append({"role": "user", "content": user_input})

    # Custom logic to handle product queries
    def handle_product_query(query):
        response = ""
        for product in products:
            if product["name"].lower() in query.lower():
                response += (
                    f"**{product['name']}**\n"
                    f"Price: ${product['price']}\n"
                    f"Category: {product['category']}\n"
                    f"Stock: {product['stock']} available\n\n"
                )
        return response if response else "Sorry, I couldn't find any product matching your query."

    # Check if user input is product-related
    product_response = handle_product_query(user_input)

    if product_response:
        # Respond with product details
        st.session_state["messages"].append({"role": "assistant", "content": product_response})
    else:
        # Use OpenAI API for a more general response
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=st.session_state["messages"]
            )
            reply = response["choices"][0]["message"]["content"]
            st.session_state["messages"].append({"role": "assistant", "content": reply})
        except Exception as e:
            st.session_state["messages"].append({"role": "assistant", "content": f"Error: {str(e)}"})

# Display conversation history
for message in st.session_state["messages"]:
    if message["role"] == "user":
        st.markdown(f"**You:** {message['content']}")
    else:
        st.markdown(f"**Bot:** {message['content']}")