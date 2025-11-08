# Content MCP Server

A Python-based MCP (Model Context Protocol) server that provides tools for content creation, including idea generation from multiple sources and AI-powered script generation.

## Features

### 1. Content Idea Generation
Analyze trending topics from multiple sources:
- **Reddit**: Hot and trending posts using PRAW
- **YouTube**: Trending videos using YouTube Data API v3
- **Google News**: Recent news articles via RSS feeds

### 2. Script Generation
Generate monologue scripts using OpenRouter or Groq with:
- **Automatic fallback**: If primary provider fails, automatically uses backup
- Configurable duration and word count
- Multiple style options
- **Intelligent context integration**: Advanced context processing with ranking, sentiment analysis, and cross-source correlation
- Support for various AI models from both providers

### 3. Voice Generation
Generate audio from scripts using ElevenLabs voice cloning:
- **Voice Cloning**: Clone any voice from a video sample (10-60 seconds)
- **Text-to-Speech**: Convert scripts to natural-sounding audio
- **Complete Workflow**: From topic research to final audio in one call
- **Three composite tools**: Full workflow, script+audio, or audio-only generation

### 4. Enhanced Context Intelligence
The server uses advanced context processing to provide the best information to AI models:
- **Intelligent Ranking**: Items are scored by relevance (40%), engagement (30%), recency (20%), and credibility (10%)
- **Rich Content Extraction**: 
  - Reddit: Selftext, top comments, engagement metrics
  - YouTube: Descriptions, tags, engagement ratios
  - News: Full summaries, publication dates, source credibility
- **Theme Extraction**: Identifies key themes and keywords across all sources
- **Sentiment Analysis**: Understands overall tone (positive/negative/mixed) from all sources
- **Trend Detection**: 
  - **Emerging Trends**: Identifies new topics gaining attention
  - **Gaining Traction**: Detects rapidly growing topics
  - **Losing Traction**: Identifies declining topics
  - **Unique Angles**: Finds niche perspectives with high relevance but niche engagement
- **Cross-Source Correlation**: Finds connections and common themes between Reddit, YouTube, and News
- **AI-Powered Summarization**: Uses Groq AI to generate intelligent summaries of trends and insights (with automatic fallback to rule-based summaries)
- **Structured Summarization**: Creates intelligent, prioritized context summaries instead of raw data dumps

## Tools Available

### `generate_ideas`
Aggregates trending content from all sources (Reddit, YouTube, Google News).

**Parameters:**
- `topic` (string, required): The topic to search for (e.g., "AI", "climate change")
- `limit` (integer, optional): Maximum results per source (default: 10)

**Returns:** Structured JSON with trending topics from all sources

### `generate_reddit_ideas`
Fetch trending posts from Reddit only.

**Parameters:**
- `topic` (string, required): Search topic
- `subreddit` (string, optional): Target subreddit (default: "all")
- `limit` (integer, optional): Maximum results (default: 10)

### `generate_youtube_ideas`
Fetch trending videos from YouTube only.

**Parameters:**
- `topic` (string, required): Search topic
- `order` (string, optional): Sort order - "viewCount", "relevance", "date", "rating" (default: "viewCount")
- `limit` (integer, optional): Maximum results (default: 10)

### `generate_news_ideas`
Fetch recent news articles from Google News only.

**Parameters:**
- `topic` (string, required): Search topic
- `limit` (integer, optional): Maximum results (default: 10)

### `generate_script`
Generate a monologue script based on a topic.

**Parameters:**
- `topic` (string, required): Main subject for the script
- `duration_seconds` (integer, required): Target duration in seconds
- `model` (string, optional): Model to use (default: from config based on provider)
- `style` (string, optional): Style/tone (default: "informative and engaging")
- `trending_info` (string, optional): Additional context to incorporate
- `provider` (string, optional): "openrouter" or "groq" (default: from config, with automatic fallback)

**Returns:** Generated script with metadata (word count, estimated duration, provider used, etc.)

### `generate_script_from_ideas`
Generate a script incorporating trending data from `generate_ideas()`.

**Parameters:**
- `ideas_data` (object, required): Output from `generate_ideas()`
- `duration_seconds` (integer, required): Target duration in seconds
- `model` (string, optional): Model to use (default: from config based on provider)
- `style` (string, optional): Style/tone (default: "informative and engaging")
- `provider` (string, optional): "openrouter" or "groq" (default: from config, with automatic fallback)

**Note:** This tool uses intelligent context processing to rank, analyze, and summarize the trending data before generating the script. It extracts key themes, analyzes sentiment, and finds cross-source correlations to provide the best context to the AI model.

### `generate_complete_script`
Generate a complete script in one step: automatically fetches trending topics AND generates script. Perfect for agents - no need to orchestrate multiple tool calls.

**Parameters:**
- `topic` (string, required): The topic to research and create a script about
- `duration_seconds` (integer, required): Target duration in seconds
- `provider` (string, optional): "openrouter" or "groq" (default: from config)
- `style` (string, optional): Style/tone (default: "informative and engaging")
- `limit` (integer, optional): Number of items to fetch per source (default: 3)
- `model` (string, optional): Model to use (default: from config based on provider)

**Returns:** Generated script with metadata, plus the trending data used for context

### `generate_complete_content`
Complete end-to-end workflow: Generate ideas, script, and audio with voice cloning. Perfect for complete content creation in one call.

**Parameters:**
- `topic` (string, required): The topic to research and create content about
- `duration_seconds` (integer, required): Target duration in seconds
- `video_path` (string, required): Path to video file for voice cloning
- `provider` (string, optional): "openrouter" or "groq" (default: from config)
- `style` (string, optional): Style/tone (default: "informative and engaging")
- `limit` (integer, optional): Number of items to fetch per source (default: 3)
- `model` (string, optional): Model to use (default: from config)
- `output_audio_path` (string, optional): Path for output audio (default: temp file)

**Returns:** Script, audio file path, voice ID, and all metadata

### `generate_script_with_audio`
Generate script from trending data and create audio with voice cloning.

**Parameters:**
- `ideas_data` (object, required): Output from `generate_ideas()`
- `duration_seconds` (integer, required): Target duration in seconds
- `video_path` (string, required): Path to video file for voice cloning
- `provider` (string, optional): "openrouter" or "groq" (default: from config)
- `style` (string, optional): Style/tone (default: "informative and engaging")
- `model` (string, optional): Model to use (default: from config)
- `output_audio_path` (string, optional): Path for output audio (default: temp file)

**Returns:** Script, audio file path, voice ID, and metadata

### `generate_audio_from_script`
Generate audio from a script using voice cloning. Simplest tool for audio-only generation.

**Parameters:**
- `script` (string, required): The script text to convert to audio
- `video_path` (string, required): Path to video file for voice cloning
- `output_audio_path` (string, optional): Path for output audio (default: temp file)

**Returns:** Audio file path, voice ID, and metadata

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Steps

1. **Clone or download this repository:**
```bash
cd Content-MCP
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Set up API keys** (see Configuration section below)

## Configuration

### Required API Keys

#### 1. Reddit API (Free)
- Visit [Reddit App Preferences](https://www.reddit.com/prefs/apps)
- Click "Create App" or "Create Another App"
- Select "script" as the app type
- Note your `client_id` (under the app name) and `client_secret`
- **Free Tier:** 100 queries per minute for authenticated requests

#### 2. YouTube Data API v3 (Free)
- Go to [Google Cloud Console](https://console.cloud.google.com/)
- Create a new project or select an existing one
- Enable "YouTube Data API v3"
- Go to "Credentials" → "Create Credentials" → "API Key"
- Copy your API key
- **Free Tier:** 10,000 units per day (typical search = 100 units)

#### 3. Google News (Free)
- No API key needed! Uses public RSS feeds
- **Free Tier:** Unlimited

#### 4. OpenRouter (Paid - Optional)
- Visit [OpenRouter](https://openrouter.ai/keys)
- Create an account and generate an API key
- **Usage:** Based on selected model (paid, but flexible model selection)

#### 5. Groq (FREE - Recommended as backup!)
- Visit [Groq Console](https://console.groq.com/keys)
- Create a free account and generate an API key
- **Free Tier:** Very generous limits with fast inference
- **Models:** Llama 3.1, Mixtral, and more

#### 6. ElevenLabs (For Voice Generation)
- Visit [ElevenLabs](https://elevenlabs.io/)
- Create an account and get your API key
- **Usage:** Voice cloning and text-to-speech (paid service)
- **Free Tier:** Limited characters per month

### Environment Variables

Create a `.env` file in the project root:

```bash
# Reddit API Configuration
REDDIT_CLIENT_ID=your_reddit_client_id_here
REDDIT_CLIENT_SECRET=your_reddit_client_secret_here
REDDIT_USER_AGENT=ContentMCP/0.1.0 by YourUsername

# YouTube Data API v3
YOUTUBE_API_KEY=your_youtube_api_key_here

# Inference APIs (at least one required)
OPENROUTER_API_KEY=your_openrouter_api_key_here
GROQ_API_KEY=your_groq_api_key_here

# ElevenLabs API (for voice generation)
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here

# Inference Provider Selection
INFERENCE_PROVIDER=openrouter  # or "groq"

# Model Configuration (optional - adjust as needed)
OPENROUTER_MODEL=anthropic/claude-3-sonnet
GROQ_MODEL=llama-3.1-70b-versatile

# Optional: Speaking rate for script generation (words per minute)
SPEAKING_RATE_WPM=150
```

## Automatic Fallback System

The script generation tools feature an **automatic fallback system** for reliability:

1. **Primary Provider**: Uses the provider specified in `INFERENCE_PROVIDER` (default: OpenRouter)
2. **Automatic Fallback**: If the primary provider fails, automatically tries the backup provider
3. **Flexible Configuration**: Set only one provider (OpenRouter or Groq) or configure both for maximum reliability

### Example Scenarios:

**Scenario 1: Both APIs configured**
- Primary: OpenRouter fails (out of credits)
- System automatically switches to Groq
- Script generation succeeds

**Scenario 2: Only Groq configured (FREE!)**
- Uses Groq exclusively
- Perfect for getting started without payment

**Scenario 3: Custom provider per request**
- Override default with `provider` parameter
- Still falls back to alternative if primary fails

## Usage

### Running the MCP Server

```bash
python -m src.server
```

The server will start and listen for MCP protocol messages via stdio.

### Using with Claude Desktop or Other MCP Clients

Add this server to your MCP client configuration. For Claude Desktop, add to your config file:

**MacOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows:** `%APPDATA%/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "content-mcp": {
      "command": "python",
      "args": ["-m", "src.server"],
      "cwd": "/absolute/path/to/Content-MCP"
    }
  }
}
```

### Example Workflows

#### 1. Generate Ideas and Create a Script
```
1. Call generate_ideas with topic="AI breakthroughs"
2. Review the trending content from Reddit, YouTube, and News
3. Call generate_script_from_ideas with the results and duration_seconds=60
4. Receive a 60-second script incorporating all trending information
```

#### 2. Focused Research
```
1. Call generate_reddit_ideas for community discussions
2. Call generate_youtube_ideas for video content
3. Call generate_news_ideas for recent news
4. Manually combine insights and create a custom script
```

#### 3. Complete Content Creation with Voice
```
1. Call generate_complete_content with topic="AI breakthroughs", duration_seconds=60, video_path="/path/to/sample.mp4"
2. Receive script, audio file, and all metadata in one call
3. The tool automatically:
   - Fetches trending topics
   - Generates script
   - Extracts audio from video
   - Clones voice
   - Generates final audio
```

#### 4. Audio-Only Generation
```
1. Already have a script
2. Call generate_audio_from_script with your script and video_path
3. Receive audio file with cloned voice
```

## Project Structure

```
Content-MCP/
├── src/
│   ├── __init__.py
│   ├── server.py              # Main MCP server
│   ├── config.py              # Configuration management
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── ideas.py           # Idea generation tools
│   │   ├── script.py          # Script generation tools
│   │   ├── voice.py           # Voice generation tools (NEW)
│   │   └── context_processor.py  # Intelligent context processing
│   ├── utils/
│   │   ├── __init__.py
│   │   └── audio.py           # Audio extraction utilities (NEW)
│   └── sources/
│       ├── __init__.py
│       ├── reddit.py          # Reddit API integration (enhanced with comments, engagement)
│       ├── youtube.py         # YouTube API integration (enhanced with descriptions, tags)
│       ├── google_news.py     # Google News RSS integration (enhanced with metadata)
│       └── elevenlabs_voice.py  # ElevenLabs voice cloning integration (NEW)
├── requirements.txt
├── README.md
└── .env                       # Your API keys (create this)
```

## API Rate Limits & Costs

| Service | Free Tier | Limit | Notes |
|---------|-----------|-------|-------|
| Reddit | ✅ Yes | 100 queries/min | Requires authentication |
| YouTube | ✅ Yes | 10,000 units/day | ~100 searches/day |
| Google News | ✅ Yes | Unlimited | RSS feeds, no key needed |
| OpenRouter | ❌ Paid | Usage-based | Depends on model selected |
| Groq | ✅ Yes | Very generous | FREE with fast inference! |

## Troubleshooting

### "Reddit API credentials not configured"
- Ensure `REDDIT_CLIENT_ID` and `REDDIT_CLIENT_SECRET` are set in your `.env` file
- Verify you created a "script" type app on Reddit

### "YouTube API key not configured"
- Ensure `YOUTUBE_API_KEY` is set in your `.env` file
- Verify the YouTube Data API v3 is enabled in your Google Cloud project

### "No inference API configured"
- Ensure at least one of `OPENROUTER_API_KEY` or `GROQ_API_KEY` is set
- Groq is FREE - get a key at https://console.groq.com/keys

### "OpenRouter API request failed"
- Ensure `OPENROUTER_API_KEY` is set correctly
- Check your OpenRouter account has available credits
- Verify the model name is correct
- **Tip:** The system will automatically fall back to Groq if configured

### "Groq API error"
- Ensure `GROQ_API_KEY` is set correctly
- Verify your Groq account is active
- Check the model name is valid
- **Tip:** The system will automatically fall back to OpenRouter if configured

### "ElevenLabs API key not configured"
- Ensure `ELEVENLABS_API_KEY` is set in your `.env` file
- Get a key at https://elevenlabs.io/
- Voice generation tools require this API key

### "Audio validation failed"
- Video file must exist at the specified path
- Video should contain clear speech (10-60 seconds recommended)
- Ensure video format is supported (MP4, MOV, AVI, etc.)
- Audio should not be silent or too quiet

### "Quota exceeded" errors
- **YouTube**: You've exceeded 10,000 units/day. Wait until the next day (resets midnight Pacific Time)
- **Reddit**: You've exceeded 100 queries/min. Slow down your requests
- **OpenRouter**: Check your account balance
- **Groq**: Check your rate limits (very generous on free tier)

## Enhanced Context Intelligence

The server now includes advanced context processing capabilities that significantly improve script quality:

### How It Works

1. **Data Extraction**: Enhanced source integrations extract rich content:
   - Reddit: Post content, top comments, engagement scores
   - YouTube: Video descriptions, tags, engagement ratios
   - News: Full summaries, publication dates, source credibility

2. **Intelligent Ranking**: Each item is scored using a composite algorithm:
   - Relevance (40%): How well it matches the topic
   - Engagement (30%): Virality signals (upvotes, views, comments)
   - Recency (20%): How recent the content is
   - Credibility (10%): Source reputation and quality

3. **Analysis & Correlation**:
   - **Theme Extraction**: Identifies key themes and keywords across sources
   - **Sentiment Analysis**: Determines overall tone (positive/negative/mixed)
   - **Trend Detection**: Classifies trends as emerging, gaining traction, losing traction, or stable
   - **Unique Angle Discovery**: Finds niche perspectives with high relevance but lower engagement
   - **Cross-Source Correlation**: Finds connections between Reddit discussions, YouTube videos, and news articles

4. **AI-Powered Intelligence**:
   - **Groq AI Analysis**: Uses Groq API to generate intelligent summaries of trends and insights
   - **Automatic Fallback**: Falls back to rule-based summaries if AI is unavailable
   - **Actionable Insights**: AI identifies key takeaways and unique angles for content creators

5. **Structured Summarization**: Creates intelligent context summaries that:
   - Prioritize most relevant and engaging content
   - Include key insights and quotes
   - Highlight emerging trends and topics gaining traction
   - Identify unique angles and niche perspectives
   - Highlight cross-source connections
   - Provide sentiment context for appropriate tone

### Benefits

- **Better Scripts**: AI models receive rich, prioritized context instead of raw data
- **Efficiency**: Summarized context uses fewer tokens while providing more value
- **Intelligence**: Cross-source correlation reveals insights that single-source analysis would miss
- **Trend Awareness**: Explicit trend detection helps identify what's hot, emerging, or declining
- **Unique Angles**: Discovers niche perspectives that others might miss
- **AI-Powered Analysis**: Groq AI generates intelligent summaries with actionable insights
- **Quality**: Ranking ensures only the most relevant and engaging content is included

## Voice Generation Features

The server now includes complete voice generation capabilities:

### How It Works

1. **Video Input**: Provide a video file path (10-60 seconds recommended)
2. **Audio Extraction**: Tool automatically extracts audio from video using ffmpeg
3. **Voice Cloning**: Audio sample is sent to ElevenLabs for instant voice cloning
4. **Text-to-Speech**: Generated script is converted to audio using the cloned voice
5. **Output**: Receive MP3 audio file with natural-sounding speech

### Three Workflow Options

1. **Complete Workflow** (`generate_complete_content`):
   - Input: Topic + Video
   - Process: Ideas → Script → Audio
   - Output: Everything (script, audio, metadata)

2. **Script + Audio** (`generate_script_with_audio`):
   - Input: Trending data + Video
   - Process: Script → Audio
   - Output: Script and audio

3. **Audio Only** (`generate_audio_from_script`):
   - Input: Script + Video
   - Process: Audio generation
   - Output: Audio file

### Video Requirements

- **Format**: MP4, MOV, AVI, or other common formats
- **Duration**: 10-60 seconds (10-20 seconds ideal for voice cloning)
- **Content**: Clear speech, minimal background noise
- **Quality**: Higher quality audio = better voice cloning

## Future Enhancements

Planned features for future phases:
- **Video Generation**: Talking head videos with D-ID
- Additional data sources and analytics
- Voice customization options (pitch, speed, emotion)

## License

MIT License - Feel free to use and modify as needed.

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## Support

For issues or questions:
1. Check the Troubleshooting section above
2. Verify your API keys are configured correctly
3. Check that you're within the free tier limits for each service
4. Review the error messages in the server output

## Acknowledgments

- Built with [Anthropic's MCP Python SDK](https://github.com/anthropics/mcp)
- Uses PRAW for Reddit API access
- Uses Google's API clients for YouTube
- Uses feedparser for Google News RSS feeds
- Script generation powered by OpenRouter

