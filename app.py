import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/api/recipes/"

# Sidebar: Token-based Authentication
st.sidebar.title("🔐 Authentication (Optional)")
token = st.sidebar.text_input("Enter your token", type="password")
headers = {"Authorization": f"Bearer {token}"} if token else {}

# Show detail page
if 'selected_recipe' in st.session_state:
    recipe = st.session_state['selected_recipe']
    st.title(recipe['title'])
    
    if recipe['image']:
        st.image(recipe['image'], width=400)

    st.write(f"📂 *Category*: {recipe['category']}")
    st.write(f"📝 {recipe['description']}")
    st.write(f"🥘 *Ingredients*: {recipe['ingredients']}")
    st.write(f"👨‍🍳 *Instructions*: {recipe['instructions']}")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ Back"):
            del st.session_state['selected_recipe']
            st.rerun()
    with col2:
        if st.button("🗑️ Delete Recipe"):
            delete_url = f"{API_URL}{recipe['id']}/"
            try:
                res = requests.delete(delete_url, headers=headers)
                if res.status_code == 204:
                    st.success("✅ Recipe deleted successfully!")
                    del st.session_state['selected_recipe']
                    st.rerun()
                else:
                    st.error(f"❌ Delete failed: {res.text}")
            except Exception as e:
                st.error(f"❌ Error deleting recipe: {e}")
    st.stop()

# Recipe List
st.title("📖 Recipe Book")

try:
    res = requests.get(API_URL, headers=headers)
    if res.status_code == 401:
        st.error("❌ Unauthorized. Please enter a valid token.")
        recipes = []
    else:
        res.raise_for_status()
        recipes = res.json()
except Exception as e:
    st.error(f"❌ Failed to load recipes: {e}")
    recipes = []

for recipe in recipes:
    with st.container():
        st.subheader(recipe["title"])
        if recipe["image"]:
            st.image(recipe["image"], width=300)
        st.caption(f"📂 {recipe['category']}")
        st.write(recipe["description"][:100] + "...")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("View Details", key=f"view_{recipe['id']}"):
                st.session_state['selected_recipe'] = recipe
                st.rerun()
        with col2:
            if st.button("🗑️ Delete", key=f"delete_{recipe['id']}"):
                delete_url = f"{API_URL}{recipe['id']}/"
                try:
                    response = requests.delete(delete_url, headers=headers)
                    if response.status_code == 204:
                        st.success("✅ Deleted successfully!")
                        st.rerun()
                    else:
                        st.error(f"❌ Delete failed: {response.text}")
                except Exception as e:
                    st.error(f"❌ Error deleting: {e}")
    st.divider()

# Upload New Recipe Form
st.header("➕ Add New Recipe")

with st.form("recipe_form"):
    col1, col2 = st.columns(2)
    with col1:
        title = st.text_input("Title")
        category = st.text_input("Category")
        image_file = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"])
        if image_file:
            st.image(image_file, caption="Preview", use_container_width=True)


    with col2:
        description = st.text_area("Description")
        ingredients = st.text_area("Ingredients (comma-separated)")
        instructions = st.text_area("Instructions")

    submit = st.form_submit_button("Upload")

    if submit:
        if not all([title, description, ingredients, instructions, category, image_file]):
            st.warning("⚠️ All fields including image are required.")
        else:
            files = {"image": (image_file.name, image_file, image_file.type)}
            data = {
                "title": title,
                "description": description,
                "ingredients": ingredients,
                "instructions": instructions,
                "category": category,
            }
            try:
                response = requests.post(API_URL, data=data, files=files, headers=headers)
                if response.status_code in [200, 201]:
                    st.success("✅ Recipe uploaded successfully!")
                    st.toast("🎉 Added!", icon="✅")
                    st.rerun()
                else:
                    try:
                        err_json = response.json()
                        err_msg = "\n".join([f"{k}: {v}" for k, v in err_json.items()])
                    except:
                        err_msg = response.text
                    st.error(f"❌ Upload failed:\n{err_msg}")
            except Exception as e:
                st.error(f"❌ Error uploading: {e}")
