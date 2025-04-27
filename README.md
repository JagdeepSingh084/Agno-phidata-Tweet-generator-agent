##Description
This project is a multi-agent AI system designed to automatically generate short, trendy tweets based on the latest AI, Machine Learning, and Data Science news.
Built using Agno (phidata) framework, it leverages Groq's Llama3-70b model, real-time search via DuckDuckGo Tool, and is hosted with FastAPI for scalability and flexibility.

###The system uses a modular multi-agent architecture:

####News Agent: Fetches latest tech articles.

####Tweet Generator Agent: Summarizes articles into viral tweets.

####Team Coordinator Agent: Manages workflow between fetching and tweeting.

The project includes an interactive Agno Playground UI for easy testing and demonstration.

###🚀 Features
Real-time AI/ML/Data Science news fetching

Crisp and trendy tweet generation (with catchy titles, hashtags, links)

Modular multi-agent structure for flexibility

FastAPI backend with CORS enabled

Interactive Playground for easy experimentation

###🛠 Tech Stack
Framework: Agno (phidata)

Language: Python

Model: Groq's Llama3-70b-8192

Tools: DuckDuckGo Search API

Server: FastAPI with CORS Middleware

Frontend: Agno Playground App

###📜 Installation
bash
Copy
Edit
# 1. Clone the repository
git clone https://github.com/your-username/tweet-generator-ai-agent.git
cd tweet-generator-ai-agent

# 2. Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment variables
# Create a .env file and add the following:
PHI_API_KEY=your_phi_api_key
GROQ_API_KEY=your_groq_api_key
OPENAI_API_KEY=your_openai_api_key

# 5. Run the application
python main.py
🧠 How It Works
News Fetching Agent:

Searches DuckDuckGo for latest AI/ML/Data Science articles (past 24 hours).

Returns the most relevant article with source and date.

Tweet Generator Agent:

Converts the news article into a short, engaging tweet.

Adds a title, main point, source link, publish date, and relevant hashtags.

Keeps the tweet under 200 characters.

###Team Coordinator Agent:

Orchestrates the process between fetching and tweeting.

Filters and selects only the latest articles.

Agno Playground:

Visual interface to test and interact with the agents in real time.


