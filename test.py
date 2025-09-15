import requests
import telegram
import asyncio
import os

# --- CONFIGURATION ---
# Best practice: Use environment variables to keep your secrets safe!
# For this example, you can just paste your keys here.
OWM_API_KEY = "3f9d6e247277936a22871b0b90575cef"
TELEGRAM_TOKEN = "8221011321:AAEnf8hrGob3nJ76zsJ2gD35EnJ1i-5dM78"
TELEGRAM_CHAT_ID = "8221011321"

# The city you want the weather for
CITY_NAME = "Adelaide,AU"  # Example: "London,UK" or "New York,US"


# --- 1. GET WEATHER DATA ---
def get_weather(api_key, city):
    """Fetches weather data from OpenWeatherMap API."""

    # API endpoint URL with query parameters
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    try:
        response = requests.get(url)
        # This will raise an exception for bad responses (4xx or 5xx)
        response.raise_for_status()

        # Parse the JSON response
        data = response.json()

        # --- Extract and format the relevant weather details ---
        main_weather = data['weather'][0]['main']
        description = data['weather'][0]['description']
        temp = data['main']['temp']
        feels_like = data['main']['feels_like']
        humidity = data['main']['humidity']

        # Emoji mapping for a nicer look!
        weather_emojis = {
            "Clear": "☀️",
            "Clouds": "☁️",
            "Rain": "🌧️",
            "Drizzle": "💧",
            "Thunderstorm": "⛈️",
            "Snow": "❄️",
            "Mist": "🌫️"
        }

        # Get the emoji, or a default one if the condition isn't in our map
        weather_icon = weather_emojis.get(main_weather, "🤷")

        # Create the message string
        message = (
            f"Good Morning! ☕\n\n"
            f"Here is your daily weather report for that big culotee {city.split(',')[0]}:\n\n"
            f"{weather_icon} Forecast: {main_weather} ({description})\n"
            f"🌡️ Temperature: {temp}°C\n"
            f"🤔 Feels Like: {feels_like}°C\n"
            f"💧 Humidity: {humidity}%"
        )

        return message

    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None
    except KeyError:
        print("Error: Invalid data format received from weather API.")
        return None


# --- 2. SEND TELEGRAM MESSAGE ---
async def send_telegram_message(token, chat_id, message):
    """Sends a message to a Telegram chat using the bot."""
    if not message:
        print("No message to send.")
        return

    try:
        bot = telegram.Bot(token=token)
        await bot.send_message(chat_id=chat_id, text=message)
        print("✅ Weather update sent successfully to Telegram!")
    except Exception as e:
        print(f"❌ Failed to send Telegram message: {e}")


# --- 3. MAIN FUNCTION TO RUN THE BOT ---
async def main():
    """Main function to run the weather agent."""
    print("Fetching weather data...")
    weather_report = get_weather(OWM_API_KEY, CITY_NAME)

    print("Sending message to Telegram...")
    await send_telegram_message(TELEGRAM_TOKEN, TELEGRAM_CHAT_ID, weather_report)


if __name__ == "__main__":
    # The python-telegram-bot library is asynchronous, so we need to run our main function like this.
    asyncio.run(main())
