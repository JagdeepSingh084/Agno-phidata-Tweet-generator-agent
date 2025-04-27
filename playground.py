from fastapi import FastAPI
import phi.api
from phi.agent import Agent
from phi.model.groq import Groq
from phi.tools.duckduckgo import DuckDuckGo
from dotenv import load_dotenv
import os
import datetime
import phi
from phi.playground import Playground, serve_playground_app

from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


load_dotenv()

#Load environment variable if using OPENAI fallbacks
phi.api = os.getenv("PHI_API_KEY")
OPENAI_API_KEY = os.getenv("GROQ_API_KEY")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

from dotenv import load_dotenv
load_dotenv()
import datetime

# Fetch the latest AI/ML/DS news using DuckDuckGo search
news_tool = DuckDuckGo()

# Set up the Groq model for generating a trendy tweet
tweet_model = Groq(id="llama3-70b-8192", temperature=0.2 )

# Step 1: News Agent - Fetch the latest news articles related to AI, ML, Data Science
news_fetching_agent = Agent(
    name="news_fetcher",
    role = "Fetch the latest news related to Data Science, AI AND Machine Learning",
    model=tweet_model,  # No model needed here, just fetching news
    tools=[news_tool],
    stream =True,
    instructions=["""
            When no input is provided:
1. Search for the latest AI/ML/Data Science articles published in the last 24 hours (IST)
2. Focus on breakthroughs, research papers, and major announcements
3. Return the most relevant article with its source URL

When asked 'Tell me about yourself' or 'What are your special skills?':
1. Respond with: 'I'm an AI-powered news analyst specialized in technology trends'
2. Mention: 'I can find and summarize the latest AI research in seconds'
3. Add: 'My skills include real-time news analysis and engaging content creation'
    """],
    show_tool_calls=True,
    markdown=True,
)
# Tweet generator agent
tweet_agent = Agent( 
    name="Tweet_generator",
    role= "Generate a short, trendy, and crisp tweet from the latest news article fetched only by {news_fetching_agent}",
    model=tweet_model,
    stream =True,
    tools = [news_tool],
    instructions=["""
        1. Summarize articles into engaging 200-character tweets
2. Always include:
   - catchy title
   - Main point
   - Source link
   - Published date
   - 2-3 relevant hashtags (#AI, #MachineLearning, #DataScience)
3. For 'Tell me about yourself':
   - Respond with: 'I transform complex tech news into viral tweets'
   - Highlight: 'Specialized in making technical content accessible'
4. Use emojis sparingly (1-2 per tweet)
            """],
            
    show_tool_calls=True,
    markdown=True,
)

tweet_team = Agent(
    name="Tweeter_team",
    model=tweet_model,
    stream=True,  # ← Enable streaming
    role="Social Media Content Creator",
    instructions=[
        f"""Default workflow:
1. Use {news_fetching_agent} to get latest article
2. filter and select top articles having latest published date from the current datetime.
2. Then use {tweet_agent} to generate the tweet with source link AND published date.
'"""],

    show_tool_calls=True,
    markdown=True,
)

app = Playground(agents = [news_fetching_agent, tweet_agent, tweet_team]).get_app()

if __name__ == "__main__":
    import asyncio
    from rich.prompt import Prompt
    from rich.console import Console
    from rich.markdown import Markdown
    
    console = Console()
    
    async def tweet_generation_workflow():
        """Professional workflow for generating AI/ML/DS tweets"""
        console.print("\n[bold cyan]🚀 Starting Tweet Generation Workflow[/bold cyan]")
        console.print(f"[dim]{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}[/dim]\n")
        
        try:
            # Step 1: Fetch latest news
            console.print("[bold]🔍 Step 1: Fetching Latest AI/ML/DS News...[/bold]")
            news_task = await news_fetching_agent.arun()
            if not news_task:
                console.print("[red]❌ Failed to fetch news articles[/red]")
                return
            
            # Extract the relevant string from the RunResponse object
            if hasattr(news_task, "content"):
                news_task = news_task.content  # Extract the content if it's a RunResponse object
            
            
            if not isinstance(news_task, str):
                console.print("[red]❌ Invalid response type from news_fetching_agent[/red]")
                return
            

            # Step 2: Generate tweet
            console.print("\n[bold]✍️ Step 2: Generating Trendy Tweet...[/bold]")
            tweet_task = await tweet_agent.arun(news_task)
            if not tweet_task:
                console.print("[red]❌ Failed to generate tweet[/red]")
                return
            
             # Extract the relevant string from the RunResponse object
            if hasattr(tweet_task, "content"):
                tweet_task = tweet_task.content  # Extract the content if it's a RunResponse object
            
            if not isinstance(tweet_task, str):
                console.print("[red]❌ Invalid response type from tweet_agent[/red]")
                return
            
            # Step 3: Final output from tweet team
            console.print("\n[bold]📢 Step 3: Final Tweet Content:[/bold]")
            final_output = await tweet_team.arun(tweet_task)

             # Extract the relevant string from the RunResponse object
            if hasattr(final_output, "content"):
                final_output = final_output.content  # Extract the content if it's a RunResponse object
            
            if not isinstance(final_output, str):
                console.print("[red]❌ Invalid response type from tweet_team[/red]")
                return
            
            # Display final results
            console.print("\n[green]✅ Workflow Completed Successfully![/green]")
            console.print(Markdown("---"))
            console.print(Markdown("### Final Tweet:"))
            console.print(Markdown(final_output))
            console.print(Markdown("---"))
            
        except Exception as e:
            console.print(f"[red]⚠️ Error in workflow: {str(e)}[/red]")
    
    # Run the workflow
    asyncio.run(tweet_generation_workflow())
    
    # Also serve the playground app for interactive use
    serve_playground_app("playground:app", reload=True)

    