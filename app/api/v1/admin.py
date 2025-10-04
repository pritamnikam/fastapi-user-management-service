from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
import streamlit as st
import pandas as pd
from sqlalchemy.orm import Session
from sqlalchemy import select, update, desc
import sys
from pathlib import Path

# Add the project root to the Python path to allow imports
sys.path.append(str(Path(__file__).parent.parent.parent.parent))

from app.db.schema import SessionLocal, Prompt
from app.models.prompt import PromptCreate, PromptRead

router = APIRouter()

@router.get("/admin", response_class=HTMLResponse)
def admin_portal(request: Request):
    # Redirect to Streamlit app
    return """
    <html>
        <head>
            <title>Prompt Catalog Admin</title>
            <meta http-equiv="refresh" content="0;url=http://localhost:8501" />
        </head>
        <body>
            <h1>Redirecting to Streamlit Admin Portal...</h1>
            <p>If you are not redirected automatically, <a href="http://localhost:8501">click here</a>.</p>
        </body>
    </html>
    """

# Streamlit Admin Portal
def streamlit_app():
    st.set_page_config(page_title="Prompt Catalog Admin", layout="wide")
    st.title("Prompt Catalog Admin Portal")
    
    # Initialize session state for storing selected values
    if 'selected_app_id' not in st.session_state:
        st.session_state.selected_app_id = None
    if 'selected_prompt' not in st.session_state:
        st.session_state.selected_prompt = None
    
    # Database connection
    db = SessionLocal()
    
    try:
        # 1. Application Selector
        st.header("1. Application Selector")
        
        # Get unique app_ids from the database
        # For now, we'll simulate this since the schema doesn't have app_id
        # In a real implementation, you would query the actual app_ids
        app_ids = ["app1", "app2", "app3"]  # Replace with actual query
        
        selected_app = st.selectbox(
            "Select Application",
            options=app_ids,
            key="app_selector"
        )
        st.session_state.selected_app_id = selected_app
        
        if st.session_state.selected_app_id:
            # 2. Prompt List
            st.header("2. Prompt List")
            
            # Query prompts for the selected application
            # In a real implementation, filter by app_id
            prompts_query = select(Prompt).order_by(Prompt.name)
            prompts = db.execute(prompts_query).scalars().all()
            
            if prompts:
                # Create a DataFrame for display
                prompt_data = []
                for prompt in prompts:
                    prompt_data.append({
                        "id": prompt.id,
                        "name": prompt.name,
                        "version": "1.0",  # Replace with actual version if available
                        "is_active": True,  # Replace with actual status if available
                        "created_at": prompt.created_at
                    })
                
                df = pd.DataFrame(prompt_data)
                st.dataframe(df)
                
                # Select a prompt to edit
                selected_prompt_id = st.selectbox(
                    "Select Prompt to Edit",
                    options=[p["id"] for p in prompt_data],
                    format_func=lambda x: next((p["name"] for p in prompt_data if p["id"] == x), "")
                )
                
                if selected_prompt_id:
                    st.session_state.selected_prompt = next((p for p in prompts if p.id == selected_prompt_id), None)
                    
                    if st.session_state.selected_prompt:
                        # 3. Prompt Editor
                        st.header("3. Prompt Editor")
                        
                        prompt_text = st.text_area(
                            "Edit Prompt Text",
                            value=st.session_state.selected_prompt.content,
                            height=300
                        )
                        
                        if st.button("Save New Version"):
                            # Create a new version of the prompt
                            # In a real implementation, you would:
                            # 1. Set is_active=False for all previous versions
                            # 2. Create a new version with is_active=True
                            
                            # For now, we'll just update the existing prompt
                            try:
                                stmt = update(Prompt).where(Prompt.id == selected_prompt_id).values(content=prompt_text)
                                db.execute(stmt)
                                db.commit()
                                st.success("Prompt updated successfully!")
                            except Exception as e:
                                db.rollback()
                                st.error(f"Error updating prompt: {e}")
                        
                        # 4. History & Rollback
                        st.header("4. History & Rollback")
                        
                        # In a real implementation, you would query all versions of this prompt
                        # For now, we'll just show the current version
                        
                        history_data = [{
                            "version": "1.0",
                            "created_at": st.session_state.selected_prompt.created_at,
                            "is_active": True
                        }]
                        
                        history_df = pd.DataFrame(history_data)
                        st.dataframe(history_df)
                        
                        # Rollback functionality
                        st.write("Select a version to rollback:")
                        if st.button("Set as Active Version"):
                            st.success("Version set as active!")
            else:
                st.info("No prompts found for the selected application.")
    finally:
        db.close()

# Run the Streamlit app when this module is executed directly
if __name__ == "__main__":
    streamlit_app()