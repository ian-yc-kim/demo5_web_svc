import streamlit as st
import requests
import logging
from demo5_web_svc import config

"""
Module for rendering the Forum page using Streamlit.
This page fetches, creates, updates, and deletes forum posts by interfacing with the backend forum API endpoints.
It uses the authentication token stored in session_state as 'jwt_token'.
"""

POSTS_PER_PAGE = 5


def paginate_posts(posts: list, page_number: int, posts_per_page: int = POSTS_PER_PAGE) -> list:
    """Return a slice of posts for the given page number."""
    start_idx = (page_number - 1) * posts_per_page
    end_idx = start_idx + posts_per_page
    return posts[start_idx:end_idx]


def fetch_posts(token: str) -> list:
    """Fetch forum posts from the backend service."""
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{config.AUTH_SERVICE_URL}/forum", headers=headers)
        response.raise_for_status()
        posts = response.json()
        return posts
    except Exception as e:
        logging.error(e, exc_info=True)
        st.error("Error fetching forum posts")
        return []


def create_post(token: str, title: str, content: str) -> bool:
    """Create a new forum post."""
    try:
        payload = {"title": title, "content": content}
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.post(f"{config.AUTH_SERVICE_URL}/forum", json=payload, headers=headers)
        response.raise_for_status()
        return True
    except Exception as e:
        logging.error(e, exc_info=True)
        st.error("Error creating forum post")
        return False


def update_post(token: str, post_id: int, title: str, content: str) -> bool:
    """Update an existing forum post."""
    try:
        payload = {"title": title, "content": content}
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.put(f"{config.AUTH_SERVICE_URL}/forum/{post_id}", json=payload, headers=headers)
        response.raise_for_status()
        return True
    except Exception as e:
        logging.error(e, exc_info=True)
        st.error(f"Error updating forum post with id {post_id}")
        return False


def delete_post(token: str, post_id: int) -> bool:
    """Delete a forum post."""
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.delete(f"{config.AUTH_SERVICE_URL}/forum/{post_id}", headers=headers)
        response.raise_for_status()
        return True
    except Exception as e:
        logging.error(e, exc_info=True)
        st.error(f"Error deleting forum post with id {post_id}")
        return False


def render_forum_page() -> None:
    """Render the forum page UI with pagination and CRUD operations."""
    try:
        st.set_page_config(page_title="Forum")
    except Exception as e:
        logging.error(e, exc_info=True)

    st.title("Forum")

    # Check for authentication token in session state
    if 'jwt_token' not in st.session_state or not st.session_state.jwt_token:
        st.error("Please login to view the forum.")
        return

    token = st.session_state.jwt_token
    
    # Section to create a new post
    st.subheader("Create New Post")
    with st.form(key="create_post_form"):
        new_title = st.text_input("Title", key="new_title")
        new_content = st.text_area("Content", key="new_content")
        submit_new = st.form_submit_button(label="Create Post")
        if submit_new:
            if not new_title or not new_content:
                st.error("Title and Content are required.")
            else:
                if create_post(token, new_title, new_content):
                    st.success("Post created successfully!")
                    # Rerun to fetch new posts
                    st.experimental_rerun()

    # Fetch posts
    posts = fetch_posts(token)

    if not posts:
        st.info("No posts available.")
        return

    # Pagination logic
    page_number = st.number_input("Page", min_value=1, value=1, step=1, key="page_number")
    current_posts = paginate_posts(posts, page_number)

    # Display posts
    st.subheader("Posts")
    for post in current_posts:
        st.markdown(f"**{post.get('title', 'No Title')}**")
        st.write(post.get('content', ''))

        # Edit post functionality
        edit_button = st.button(label=f"Edit Post {post.get('id')}", key=f"edit_{post.get('id')}")
        if edit_button:
            with st.expander(f"Edit Post {post.get('id')}"):
                new_title_edit = st.text_input("Title", value=post.get('title', ''), key=f"edit_title_{post.get('id')}")
                new_content_edit = st.text_area("Content", value=post.get('content', ''), key=f"edit_content_{post.get('id')}")
                if st.button(label="Submit Edit", key=f"submit_edit_{post.get('id')}"):
                    if not new_title_edit or not new_content_edit:
                        st.error("Title and Content are required for editing.")
                    else:
                        if update_post(token, post.get('id'), new_title_edit, new_content_edit):
                            st.success("Post updated successfully!")
                            st.experimental_rerun()

        # Delete post functionality
        delete_button = st.button(label=f"Delete Post {post.get('id')}", key=f"delete_{post.get('id')}")
        if delete_button:
            st.warning("Are you sure you want to delete this post?")
            confirm_delete = st.button(label="Confirm Delete", key=f"confirm_delete_{post.get('id')}")
            if confirm_delete:
                if delete_post(token, post.get('id')):
                    st.success("Post deleted successfully!")
                    st.experimental_rerun()
                else:
                    st.error("Failed to delete post.")

# For Streamlit to run the page when executed
if __name__ == "__main__":
    render_forum_page()
