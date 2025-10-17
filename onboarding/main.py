from air import Air
from datetime import datetime
from jinja2 import Environment, FileSystemLoader

# Create your Air application instance
app = Air()

# Set up Jinja2 template engine
# FileSystemLoader tells Jinja2 to look for templates in the 'templates' folder
env = Environment(loader=FileSystemLoader('templates'))

# A simple way to track state - in a real app, you'd use a database
click_counter = 0

@app.get("/")
def homepage():
    # Load the template file
    template = env.get_template("index.html")
    # Render it with the user_name variable
    return template.render(user_name="Developer")

@app.get("/greeting")
def get_greeting():
    global click_counter
    click_counter += 1

    # Get the current time formatted nicely
    now = datetime.now().strftime("%I:%M:%S %p")

    # Load and render the greeting template with dynamic data
    template = env.get_template("greeting.html")
    return template.render(
        current_time=now,
        click_count=click_counter
    )
# This is the crucial part - it tells Air to start the development server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)