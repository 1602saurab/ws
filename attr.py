import streamlit as st
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up the API key for the MakerSuite API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to generate 5 startup ideas
def get_gemini_response(interests, industry, prompt, num_ideas=5):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        startup_ideas = []
        
        # Generate `num_ideas` startup ideas
        for _ in range(num_ideas):
            response = model.generate_content([interests, industry, prompt])
            startup_ideas.append(response.text)
        
        return startup_ideas
    except Exception as e:
        return [f"Error generating startup ideas: {e}"]

# Main function for Streamlit app
def main():
    st.set_page_config(page_title="Startup Idea Generator", layout='wide')
    
    # Chatbot Name and Description
    chatbot_name = "Startup Sage"  # Unique chatbot name
    chatbot_description = "🤖 Your personal advisor for generating innovative startup ideas based on your interests and industry preferences!"

    st.header(f"🚀 {chatbot_name} - {chatbot_description}")
    
    # Instructions
    st.info("Fill out the fields below to generate unique startup ideas based on your interests and preferred industry!")

    # Inputs: User provides their interests and preferred industry
    interests = st.text_area("✏️ Tell us your interests (e.g., AI, Machine Learning, etc.):", key="interests", help="Enter your interests separated by commas.")
    industry = st.text_input("🏭 Tell us your preferred industry (e.g., Healthcare, Finance, etc.):", key="industry", help="Specify the industry you're interested in.")

    # Input prompts for generating startup ideas
    input_prompt = """
    You are a business expert in identifying startup ideas in emerging markets. Based on the provided interests and industry,
    generate a unique startup idea that combines current market trends, data analysis, and emerging technologies.
    """

    # State variable to store the generated startup ideas
    if 'startup_ideas' not in st.session_state:
        st.session_state['startup_ideas'] = []

    # Button to generate 5 startup ideas
    submit1 = st.button("✨ Generate 5 Startup Ideas")
    submit2 = st.button("📝 Get Feedback on a Startup Idea")
    
    # Generate Startup Ideas
    if submit1:
        if interests and industry:
            startup_ideas = get_gemini_response(interests, industry, input_prompt, num_ideas=5)
            st.session_state['startup_ideas'] = startup_ideas
            st.subheader("Here are your 5 AI-generated startup ideas! 🌟")
            
            # Display each idea clearly with a divider for better visual separation
            for i, idea in enumerate(startup_ideas, 1):
                st.write(f"### Idea {i}:")
                st.write(idea)
                st.markdown("---")  # Divider
        else:
            st.warning("⚠️ Please fill out both the 'interests' and 'industry' fields to generate startup ideas.")
    
    # Feedback request for a specific startup idea
    if submit2:
        if st.session_state['startup_ideas']:
            # Let the user select one of the generated ideas for feedback
            selected_idea = st.selectbox("Select a startup idea to get feedback on:", st.session_state['startup_ideas'])
            
            feedback_prompt = f"""
            You are an experienced startup advisor. Provide detailed feedback on how the following startup idea could be improved: 
            {selected_idea}
            """
            feedback_response = get_gemini_response(interests, industry, feedback_prompt, num_ideas=1)
            st.subheader("Feedback on Your Startup Idea 🗨️")
            st.write(feedback_response[0])  # Display feedback for the selected idea
        else:
            st.warning("⚠️ Please generate startup ideas first to get feedback.")

if __name__ == "__main__":
    main()
