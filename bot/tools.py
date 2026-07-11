import aiohttp
import asyncio
import random
import qrcode
import feedparser
import re
from io import BytesIO
from datetime import datetime
from typing import Dict, Any, Optional, List
import pycountry
from bs4 import BeautifulSoup
import requests
import json

class Tools:
    """Collection of 50+ free tools with no API keys required"""

    @staticmethod
    async def web_search(query: str) -> str:
        """1. Web Search - DuckDuckGo"""
        try:
            url = f"https://html.duckduckgo.com/html/?q={query}"
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers) as response:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    results = soup.find_all('a', class_='result__a')[:5]
                    if not results:
                        return "❌ No results found."
                    output = "🔍 **Search Results:**\n\n"
                    for i, result in enumerate(results, 1):
                        output += f"{i}. {result.text}\n"
                    return output
        except Exception as e:
            return f"❌ Error: {str(e)}"

    @staticmethod
    async def website_scraper(url: str) -> str:
        """2. Website Scraper - Extract text content"""
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers, timeout=10) as response:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    # Remove script and style elements
                    for script in soup(["script", "style"]):
                        script.decompose()
                    text = soup.get_text()
                    lines = [line.strip() for line in text.splitlines() if line.strip()]
                    content = '\n'.join(lines[:50])  # Limit to 50 lines
                    return f"📄 **Content from {url}:**\n\n{content[:3500]}"
        except Exception as e:
            return f"❌ Error scraping: {str(e)}"

    @staticmethod
    async def website_screenshot(url: str) -> Optional[BytesIO]:
        """3. Website Screenshot"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f'https://api.screenshotmachine.com/?key=demo&url={url}&dimension=1024x768',
                    timeout=15
                ) as response:
                    if response.status == 200:
                        return BytesIO(await response.read())
                    return None
        except:
            return None

    @staticmethod
    async def sitemap_crawler(url: str) -> str:
        """4. Sitemap Crawler"""
        try:
            sitemap_url = url.rstrip('/') + '/sitemap.xml'
            async with aiohttp.ClientSession() as session:
                async with session.get(sitemap_url, timeout=10) as response:
                    if response.status == 200:
                        content = await response.text()
                        soup = BeautifulSoup(content, 'xml')
                        urls = soup.find_all('loc')
                        output = f"🗺️ **Sitemap for {url}**\n\n"
                        for loc in urls[:10]:
                            output += f"• {loc.text}\n"
                        return output
                    return "❌ Sitemap not found"
        except:
            return "❌ Error fetching sitemap"

    @staticmethod
    async def rss_reader(feed_url: str) -> str:
        """5. RSS Reader"""
        try:
            feed = feedparser.parse(feed_url)
            if feed.entries:
                output = f"📡 **{feed.feed.title if hasattr(feed.feed, 'title') else 'RSS Feed'}**\n\n"
                for entry in feed.entries[:5]:
                    output += f"📰 **{entry.title}**\n"
                    output += f"   {entry.link}\n\n"
                return output
            return "❌ No entries found"
        except Exception as e:
            return f"❌ Error: {str(e)}"

    @staticmethod
    async def github_search(query: str) -> str:
        """6. GitHub Search"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f'https://api.github.com/search/repositories?q={query}&per_page=5',
                    headers={'Accept': 'application/vnd.github.v3+json'}
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        output = "🐙 **GitHub Results:**\n\n"
                        for repo in data.get('items', []):
                            output += f"📦 **{repo['name']}**\n"
                            output += f"   ⭐ {repo['stargazers_count']} | 🍴 {repo['forks_count']}\n"
                            desc = repo['description'][:100] if repo['description'] else 'No description'
                            output += f"   📝 {desc}\n\n"
                        return output
                    return "❌ No results found"
        except Exception as e:
            return f"❌ Error: {str(e)}"

    @staticmethod
    async def github_file_reader(repo_url: str) -> str:
        """7. GitHub File Reader"""
        try:
            # Extract owner/repo/path from URL
            parts = repo_url.replace('https://github.com/', '').split('/')
            if len(parts) >= 2:
                owner, repo = parts[0], parts[1]
                path = '/'.join(parts[2:]) if len(parts) > 2 else ''
                api_url = f'https://api.github.com/repos/{owner}/{repo}/contents/{path}'
                async with aiohttp.ClientSession() as session:
                    async with session.get(api_url, headers={'Accept': 'application/vnd.github.v3+json'}) as response:
                        if response.status == 200:
                            data = await response.json()
                            if isinstance(data, dict) and 'content' in data:
                                import base64
                                content = base64.b64decode(data['content']).decode('utf-8')
                                return f"📄 **File Content:**\n\n{content[:3500]}"
                            return "❌ Not a file or empty"
                        return "❌ File not found"
            return "❌ Invalid GitHub URL"
        except Exception as e:
            return f"❌ Error: {str(e)}"

    @staticmethod
    async def hacker_news() -> str:
        """8. Hacker News Top Stories"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get('https://hacker-news.firebaseio.com/v0/topstories.json') as response:
                    ids = await response.json()
                    output = "📰 **Hacker News Top Stories**\n\n"
                    for i, story_id in enumerate(ids[:10], 1):
                        async with session.get(f'https://hacker-news.firebaseio.com/v0/item/{story_id}.json') as resp:
                            story = await resp.json()
                            title = story.get('title', 'Untitled')
                            score = story.get('score', 0)
                            output += f"{i}. {title} (⭐{score})\n"
                    return output
        except Exception as e:
            return f"❌ Error: {str(e)}"

    @staticmethod
    async def wikipedia_lookup(query: str) -> str:
        """9. Wikipedia Lookup"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f'https://en.wikipedia.org/api/rest_v1/page/summary/{query.replace(" ", "_")}'
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        return f"📖 **{data.get('title', query)}**\n\n{data.get('extract', 'No summary available')[:3000]}"
                    return "❌ Page not found"
        except:
            return "❌ Error fetching Wikipedia"

    @staticmethod
    async def dictionary_lookup(word: str) -> str:
        """10. Dictionary Lookup"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f'https://api.dictionaryapi.dev/api/v2/entries/en/{word}') as response:
                    if response.status == 200:
                        data = await response.json()
                        if data:
                            word_data = data[0]
                            output = f"📖 **{word_data.get('word', word)}**\n"
                            for meaning in word_data.get('meanings', [])[:3]:
                                pos = meaning.get('partOfSpeech', '')
                                output += f"\n🔹 **{pos}:**"
                                for definition in meaning.get('definitions', [])[:2]:
                                    output += f"\n  • {definition.get('definition', '')}"
                                    if 'example' in definition:
                                        output += f"\n    ✏️ _{definition['example']}_"
                            return output
                    return f"❌ No definition found for '{word}'"
        except:
            return "❌ Error fetching definition"

    @staticmethod
    async def qr_code_generator(data: str) -> Optional[BytesIO]:
        """11. QR Code Generator"""
        try:
            qr = qrcode.QRCode(version=1, box_size=10, border=4)
            qr.add_data(data)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            img_bytes = BytesIO()
            img.save(img_bytes, format='PNG')
            img_bytes.seek(0)
            return img_bytes
        except:
            return None

    @staticmethod
    async def url_shortener(url: str) -> str:
        """12. URL Shortener"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f'https://tinyurl.com/api-create.php?url={url}'
                ) as response:
                    if response.status == 200:
                        short_url = await response.text()
                        return f"🔗 **Shortened URL:** {short_url}"
                    return "❌ Failed to shorten URL"
        except:
            return "❌ Error shortening URL"

    @staticmethod
    async def ip_lookup(ip: str) -> str:
        """13. IP Lookup"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f'http://ip-api.com/json/{ip}') as response:
                    data = await response.json()
                    if data.get('status') == 'success':
                        return f"""🌐 **IP:** {ip}
📍 **Country:** {data.get('country')} ({data.get('countryCode')})
🏙️ **City:** {data.get('city')}
📮 **ZIP:** {data.get('zip')}
📍 **Region:** {data.get('regionName')}
📱 **ISP:** {data.get('isp')}
🔄 **Timezone:** {data.get('timezone')}
📍 **Coordinates:** {data.get('lat')}, {data.get('lon')}"""
                    return "❌ Invalid IP address"
        except:
            return "❌ Error looking up IP"

    @staticmethod
    async def batch_ip_lookup(ips: str) -> str:
        """14. Batch IP Lookup"""
        ip_list = [ip.strip() for ip in ips.split(',')][:5]
        output = "🌐 **Batch IP Lookup**\n\n"
        for ip in ip_list:
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(f'http://ip-api.com/json/{ip}') as response:
                        data = await response.json()
                        if data.get('status') == 'success':
                            output += f"**{ip}:** {data.get('country')} ({data.get('countryCode')})\n"
                        else:
                            output += f"**{ip}:** Invalid\n"
            except:
                output += f"**{ip}:** Error\n"
        return output

    @staticmethod
    async def world_time(timezone: str) -> str:
        """15. World Time"""
        try:
            from pytz import timezone as tz
            t = tz(timezone)
            current_time = datetime.now(t)
            return f"🕐 **Time in {timezone}:**\n{current_time.strftime('%Y-%m-%d %H:%M:%S %Z')}"
        except:
            return "❌ Invalid timezone. Use format: Asia/Kolkata"

    @staticmethod
    async def public_holidays(country: str, year: int = None) -> str:
        """16. Public Holidays"""
        if not year:
            year = datetime.now().year
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f'https://date.nager.at/api/v3/PublicHolidays/{year}/{country.upper()}'
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        output = f"📅 **Public Holidays in {country.upper()} ({year})**\n\n"
                        for holiday in data[:10]:
                            output += f"📌 {holiday.get('date')} - {holiday.get('localName')}\n"
                            output += f"   {holiday.get('name')}\n\n"
                        return output
                    return "❌ No holidays found"
        except:
            return "❌ Error fetching holidays"

    @staticmethod
    async def cryptocurrency_prices() -> str:
        """17. Cryptocurrency Prices"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=5'
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        output = "💰 **Top Cryptocurrencies**\n\n"
                        for coin in data:
                            output += f"🪙 **{coin['name']}** ({coin['symbol'].upper()})\n"
                            output += f"   💵 Price: ${coin['current_price']:,}\n"
                            output += f"   📈 Change 24h: {coin['price_change_percentage_24h']:.2f}%\n"
                            output += f"   💰 Market Cap: ${coin['market_cap']:,}\n\n"
                        return output
                    return "❌ Failed to fetch crypto data"
        except:
            return "❌ Crypto API unavailable"

    @staticmethod
    async def stock_market_lookup(symbol: str) -> str:
        """18. Stock Market Lookup (Free API)"""
        try:
            # Using free Alpha Vantage demo
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey=demo'
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        quote = data.get('Global Quote', {})
                        if quote:
                            return f"""📈 **{quote.get('01. symbol', symbol)}**
💵 Price: ${quote.get('05. price', 'N/A')}
📊 Change: {quote.get('09. change', 'N/A')}
📈 Change %: {quote.get('10. change percent', 'N/A')}
📅 Latest: {quote.get('07. latest trading day', 'N/A')}"""
                        return "❌ Stock not found"
                    return "❌ API unavailable"
        except:
            return "❌ Error fetching stock data"

    @staticmethod
    async def gold_price() -> str:
        """19. Gold Price Checker"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    'https://api.gold-api.com/price/XAU'
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        price = data.get('price', 0)
                        return f"🥇 **Gold Price (XAU/USD)**\n💵 ${price} per ounce"
                    return "❌ Failed to fetch gold price"
        except:
            return "❌ Gold API unavailable"

    @staticmethod
    async def currency_converter(amount: float, from_currency: str, to_currency: str) -> str:
        """20. Currency Converter"""
        try:
            # Using free exchangerate-api
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f'https://api.exchangerate-api.com/v4/latest/{from_currency.upper()}'
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        rate = data.get('rates', {}).get(to_currency.upper())
                        if rate:
                            converted = amount * rate
                            return f"💱 **Currency Conversion**\n{amount} {from_currency.upper()} = {converted:.2f} {to_currency.upper()}"
                        return "❌ Currency not found"
                    return "❌ API unavailable"
        except:
            return "❌ Error converting currency"

    @staticmethod
    async def book_search(query: str) -> str:
        """21. Book Search (Open Library)"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f'https://openlibrary.org/search.json?q={query}&limit=5'
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        output = "📚 **Book Search Results**\n\n"
                        for doc in data.get('docs', [])[:5]:
                            title = doc.get('title', 'Unknown Title')
                            author = doc.get('author_name', ['Unknown'])[0]
                            year = doc.get('first_publish_year', 'N/A')
                            output += f"📖 **{title}**\n"
                            output += f"   ✍️ {author}\n"
                            output += f"   📅 {year}\n\n"
                        return output
                    return "❌ No books found"
        except:
            return "❌ Error searching books"

    @staticmethod
    async def country_info(country_name: str) -> str:
        """22. Country Info"""
        try:
            country = pycountry.countries.search_fuzzy(country_name)[0]
            output = f"""🌍 **Country: {country.name}**
🔤 **Official Name:** {getattr(country, 'official_name', country.name)}
📋 **Alpha-2 Code:** {country.alpha_2}
📋 **Alpha-3 Code:** {country.alpha_3}
🔢 **Numeric Code:** {country.numeric}
"""
            return output
        except:
            return "❌ Country not found"

    @staticmethod
    async def geocoding(address: str) -> str:
        """23. Geocoding"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f'https://geocode.maps.co/search?q={address}'
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        if data:
                            loc = data[0]
                            return f"📍 **Location:** {address}\n🌐 **Coordinates:** {loc.get('lat')}, {loc.get('lon')}\n📍 **Display:** {loc.get('display_name', 'N/A')[:200]}"
                        return "❌ Location not found"
                    return "❌ API unavailable"
        except:
            return "❌ Error geocoding"

    @staticmethod
    async def reverse_geocoding(lat: float, lon: float) -> str:
        """24. Reverse Geocoding"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f'https://geocode.maps.co/reverse?lat={lat}&lon={lon}'
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        if data and 'display_name' in data:
                            return f"📍 **Address:** {data.get('display_name', 'N/A')}"
                        return "❌ No address found"
                    return "❌ API unavailable"
        except:
            return "❌ Error reverse geocoding"

    @staticmethod
    async def distance_calculator(lat1: float, lon1: float, lat2: float, lon2: float) -> str:
        """25. Distance Calculator"""
        try:
            from math import radians, sin, cos, sqrt, atan2
            R = 6371  # Earth's radius in km
            
            lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
            dlat = lat2 - lat1
            dlon = lon2 - lon1
            a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
            c = 2 * atan2(sqrt(a), sqrt(1-a))
            distance = R * c
            
            return f"📏 **Distance:** {distance:.2f} km\n📍 **Route:** ({lat1}, {lon1}) → ({lat2}, {lon2})"
        except:
            return "❌ Error calculating distance"

    @staticmethod
    async def iss_location() -> str:
        """26. ISS Location Tracker"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get('http://api.open-notify.org/iss-now.json') as response:
                    if response.status == 200:
                        data = await response.json()
                        loc = data.get('iss_position', {})
                        return f"🛰️ **ISS Location**\n🌐 Latitude: {loc.get('latitude', 'N/A')}\n🌐 Longitude: {loc.get('longitude', 'N/A')}"
                    return "❌ ISS API unavailable"
        except:
            return "❌ Error tracking ISS"

    @staticmethod
    async def trivia_question() -> str:
        """27. Trivia Question"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get('https://opentdb.com/api.php?amount=1&type=multiple') as response:
                    if response.status == 200:
                        data = await response.json()
                        if data.get('response_code') == 0:
                            q = data['results'][0]
                            output = f"❓ **{q['question']}**\n\n"
                            output += f"✅ **Correct Answer:** {q['correct_answer']}\n"
                            output += f"📚 **Category:** {q['category']}\n"
                            output += f"⭐ **Difficulty:** {q['difficulty']}"
                            return output
                    return "❌ No trivia available"
        except:
            return "❌ Trivia API unavailable"

    @staticmethod
    async def random_quote() -> str:
        """28. Random Quote"""
        quotes = [
            ("The only way to do great work is to love what you do", "Steve Jobs"),
            ("Innovation distinguishes between a leader and a follower", "Steve Jobs"),
            ("Stay hungry, stay foolish", "Steve Jobs"),
            ("Life is what happens when you're busy making other plans", "John Lennon"),
            ("Get busy living or get busy dying", "Stephen King"),
            ("Be yourself; everyone else is already taken", "Oscar Wilde"),
            ("Two things are infinite: the universe and human stupidity", "Albert Einstein"),
            ("The future belongs to those who believe in the beauty of their dreams", "Eleanor Roosevelt"),
            ("It does not matter how slowly you go as long as you do not stop", "Confucius"),
            ("The only impossible journey is the one you never begin", "Tony Robbins"),
        ]
        quote, author = random.choice(quotes)
        return f"💭 *\"{quote}\"*\n\n— **{author}**"

    @staticmethod
    async def random_meal() -> str:
        """29. Random Meal Recipe"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get('https://www.themealdb.com/api/json/v1/1/random.php') as response:
                    if response.status == 200:
                        data = await response.json()
                        meal = data.get('meals', [{}])[0]
                        if meal:
                            output = f"🍽️ **{meal.get('strMeal')}**\n"
                            output += f"🌍 {meal.get('strArea')} Cuisine\n"
                            output += f"📋 **Category:** {meal.get('strCategory')}\n\n"
                            output += "🛒 **Ingredients:**\n"
                            for i in range(1, 21):
                                ingredient = meal.get(f'strIngredient{i}')
                                measure = meal.get(f'strMeasure{i}')
                                if ingredient and ingredient.strip():
                                    output += f"• {ingredient} - {measure}\n"
                            return output
                    return "❌ No recipe found"
        except:
            return "❌ Meal API unavailable"

    @staticmethod
    async def space_facts() -> str:
        """30. Space Facts"""
        facts = [
            "A day on Venus is longer than its year",
            "There are more stars in the universe than grains of sand on Earth",
            "The Sun makes up 99.86% of the mass in our solar system",
            "Astronauts grow up to 2 inches taller in space",
            "The largest known star is UY Scuti, 1,700 times larger than our Sun",
            "There's a planet where it rains glass sideways",
            "One day on Jupiter is only 9 hours and 55 minutes",
            "The moon is moving away from Earth at 3.8 cm per year",
        ]
        return f"🚀 **Space Fact:**\n{random.choice(facts)}"

    @staticmethod
    async def animal_facts() -> str:
        """31. Animal Facts"""
        facts = [
            "Octopuses have three hearts",
            "A group of flamingos is called a 'flamboyance'",
            "Sloths can hold their breath longer than dolphins",
            "Honeybees can recognize human faces",
            "Elephants are the only mammals that can't jump",
            "A shrimp's heart is in its head",
            "Cows have best friends and get stressed when separated",
        ]
        return f"🐾 **Animal Fact:**\n{random.choice(facts)}"

    @staticmethod
    async def meal_search(ingredient: str) -> str:
        """32. Search Meal by Ingredient"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f'https://www.themealdb.com/api/json/v1/1/filter.php?i={ingredient}'
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        meals = data.get('meals', [])[:5]
                        if meals:
                            output = f"🍽️ **Meals with {ingredient}**\n\n"
                            for meal in meals:
                                output += f"• {meal.get('strMeal')}\n"
                            return output
                        return f"❌ No meals found with {ingredient}"
                    return "❌ API unavailable"
        except:
            return "❌ Error searching meals"

    @staticmethod
    async def movie_search(query: str) -> str:
        """33. Movie Search (OMDb API - free key)"""
        try:
            # Using OMDb API (free, no key needed for demo)
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f'https://www.omdbapi.com/?s={query}&apikey=7035c60c'
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        if data.get('Search'):
                            output = "🎬 **Movie Results**\n\n"
                            for movie in data['Search'][:5]:
                                output += f"📽️ **{movie.get('Title')}** ({movie.get('Year')})\n"
                                output += f"   ⭐ {movie.get('imdbID')}\n\n"
                            return output
                        return "❌ No movies found"
                    return "❌ API unavailable"
        except:
            return "❌ Error searching movies"

    @staticmethod
    async def meme_generator() -> Optional[BytesIO]:
        """34. Meme Generator"""
        try:
            memes = [
                "https://imgflip.com/s/meme/Dogecoin.jpg",
                "https://imgflip.com/s/meme/This-Is-Fine.jpg",
                "https://imgflip.com/s/meme/Change-My-Mind.jpg",
                "https://imgflip.com/s/meme/Distracted-Boyfriend.jpg",
            ]
            # Return a random meme URL (user can view it directly)
            return random.choice(memes)
        except:
            return None

    @staticmethod
    async def music_artist_lookup(artist: str) -> str:
        """35. Music Artist Lookup (MusicBrainz)"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f'https://musicbrainz.org/ws/2/artist/?query=artist:{artist}&fmt=json'
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        artists = data.get('artists', [])[:5]
                        if artists:
                            output = f"🎵 **Artist Search: {artist}**\n\n"
                            for a in artists:
                                output += f"🎤 **{a.get('name')}**\n"
                                output += f"   📅 {a.get('life-span', {}).get('begin', 'N/A')}\n"
                                output += f"   🌍 {', '.join(a.get('country', ['N/A']))}\n\n"
                            return output
                        return "❌ No artists found"
                    return "❌ API unavailable"
        except:
            return "❌ Error searching artists"

    @staticmethod
    async def itunes_search(song: str) -> str:
        """36. iTunes Song Search"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f'https://itunes.apple.com/search?term={song}&limit=5&media=music'
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        results = data.get('results', [])
                        if results:
                            output = "🎵 **iTunes Results**\n\n"
                            for track in results:
                                output += f"🎶 **{track.get('trackName')}**\n"
                                output += f"   👤 {track.get('artistName')}\n"
                                output += f"   💿 {track.get('collectionName')}\n\n"
                            return output
                        return "❌ No songs found"
                    return "❌ API unavailable"
        except:
            return "❌ Error searching iTunes"

    @staticmethod
    async def dictionary_alternative(word: str) -> str:
        """37. Dictionary.com Alternative"""
        return await Tools.dictionary_lookup(word)

    @staticmethod
    async def quran_ayah(random: bool = True) -> str:
        """38. Quran Ayah"""
        try:
            async with aiohttp.ClientSession() as session:
                if random:
                    ayah_num = random.randint(1, 6236)
                else:
                    ayah_num = 1
                async with session.get(
                    f'https://api.alquran.cloud/v1/ayah/{ayah_num}/en.asad'
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        ayah = data.get('data', {})
                        return f"🕌 **Quran Ayah {ayah.get('number')}**\n\n{ayah.get('text')}"
                    return "❌ Quran API unavailable"
        except:
            return "❌ Error fetching ayah"

    @staticmethod
    async def hadith_search() -> str:
        """39. Random Hadith"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    'https://api.sunnah.com/v1/hadiths/random?collection=bukhari'
                ) as response:
                    if response.status == 200:
                        data = await response
