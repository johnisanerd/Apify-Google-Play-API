# 🤖 Google Play API: Android app data, listings and reviews as JSON

Actor: [johnvc/google-play-api](https://apify.com/johnvc/google-play-api?fpr=9n7kx3) · [Input schema](https://apify.com/johnvc/google-play-api/input-schema?fpr=9n7kx3)

This repo shows two ways to use the [Google Play API](https://apify.com/johnvc/google-play-api?fpr=9n7kx3) on Apify: a Python quick start and MCP installs for five AI clients. Search Android apps, pull full listings with version history signals and data safety declarations, and export user reviews. It does the job of a google play scraper library without the maintenance, and pairs with the Apple App Store Actors for cross-platform work.

## Video Walkthrough

[![Watch the walkthrough](https://img.youtube.com/vi/jREWahDGhJM/maxresdefault.jpg)](https://www.youtube.com/watch?v=jREWahDGhJM)

### Text walkthrough

The google play api takes a search_mode of search, product or reviews. Search returns ranked apps with position, title, developer, category, rating, a downloads band and the package name. Product is the rich one: version, updatedOn and releasedOn build an app version history Google Play never shows, and containsAds, hasInAppPurchases and dataSafety expose how an app monetises and what data it declares. Reviews returns snippet, rating, likes and reviewDate twenty at a time. The version_history recipe in this repo is the release-cadence check, and the reviews_export recipe feeds sentiment pipelines. Downloads are bands like 100,000,000+, never exact counts.

## Quick Start

You need Python 3.11+ and a free Apify API key: sign up at [apify.com](https://apify.com?fpr=9n7kx3), then copy your token from Console Settings.

```bash
git clone https://github.com/johnisanerd/Apify-Google-Play-API.git
cd Apify-Google-Play-API
uv sync
cp .env.example .env   # then paste your APIFY_API_TOKEN
uv run python google-play-api-example.py
```

Run a specific recipe:

```bash
uv run python google-play-api-example.py --example version_history
```

## Why use this API

- Search, full listings and reviews behind one input
- version, updatedOn and releasedOn for release-cadence tracking
- dataSafety declarations plus ad and in-app purchase flags for privacy audits
- Ranked search results with position for ASO tracking
- Country and language targeting; pairs with the [Apple App Store Actors](https://apify.com/johnvc/apple-app-store-search?fpr=9n7kx3)

## Recipes

The example script ships ready-made recipes that mirror this API's main use cases:

- **Track an app's version history** (`--example version_history`): Pulls version, updatedOn and releasedOn for one package; schedule it to catch every release.
- **Export app reviews** (`--example reviews_export`): Pulls user reviews with rating, likes and dates for sentiment work.

**Schedule tip:** save any of these inputs as a task in the [Apify Console](https://apify.com/johnvc/google-play-api?fpr=9n7kx3) and attach a schedule. A daily or weekly run turns a one-off pull into a pipeline with zero manual work.

## Usage Examples

Basic input:

```json
{
  "search_mode": "search",
  "query": "fitness",
  "max_results": 10
}
```

Advanced input:

```json
{
  "search_mode": "product",
  "product_id": "homeworkout.homeworkouts.noequipment",
  "country": "us",
  "language": "en"
}
```

## Input Parameters

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `search_mode` | string | yes | `"search"` | What to fetch. |
| `query` | string | no | none | Required when search mode is 'search'. |
| `product_id` | string | no | none | Required for product and reviews modes. |
| `max_results` | integer | no | `100` | How many rows to return before stopping. |
| `country` | string | no | `"us"` | Optional two letter country code such as us, gb or de. |
| `language` | string | no | `"en"` | Optional two letter language code such as en, es or fr. |

## Output Format

One row from a real run:

```json
{
  "resultType": "appDetail",
  "productId": "homeworkout.homeworkouts.noequipment",
  "title": "Home Workout - No Equipment",
  "developer": "Leap Fitness Group",
  "rating": 4.9,
  "downloads": "100,000,000+",
  "version": "1.3.7",
  "updatedOn": "Jul 16, 2026",
  "releasedOn": "Nov 8, 2017",
  "containsAds": true,
  "hasInAppPurchases": true,
  "inAppPurchases": "$0.99 - $59.99 per item",
  "dataSafety": ["No data shared with third parties"]
}
```

## n8n integration

Available as an n8n community node, **[n8n-nodes-google-play-api](https://www.npmjs.com/package/n8n-nodes-google-play-api)**. In n8n: Settings, Community Nodes, install `n8n-nodes-google-play-api`, then use it in any workflow (it also works as an AI Agent tool).

## People also search for

### Is this a google play scraper?

It covers what the scraper libraries cover, as a maintained API: search, listings and reviews as JSON, with paging and billing handled. No npm or pip package to babysit.

### How do I see an app's version history?

Google Play only shows the current version. Run the version_history recipe on a schedule and store version plus updatedOn per run; the series is the history.

### Are download numbers exact?

No. The store publishes bands like 100,000,000+ and that is what the downloads field carries. Anything claiming exact Play installs is estimating.

### Can I audit an app's data safety section?

Yes. Product mode returns the declared dataSafety list per app, so a compliance sweep over an app list is a loop.

## Install in Claude Cowork Desktop

![Install in Claude Cowork Desktop](https://raw.githubusercontent.com/johnisanerd/ApifyPublicData/main/assets/guides/install_mcp_into_claude_desktop.png)

Cowork is the desktop app's automation mode. To give it the Google Play API as a tool, add the Apify MCP server as a connector.

1. Open the Claude desktop app and go to **Settings -> Connectors** (or **Settings -> Developer -> Edit Config** to edit `claude_desktop_config.json` directly).
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`
2. Add the Apify MCP server, preloaded with only this Actor:

```json
{
  "mcpServers": {
    "apify": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote",
        "https://mcp.apify.com/?tools=actors,docs,johnvc/google-play-api"
      ]
    }
  }
}
```

3. Restart the app. When Cowork first calls the tool, complete the OAuth prompt in your browser, or add your Apify API token in the connector settings to skip OAuth.
4. In a Cowork chat, confirm the tool is available and ask it to run the Google Play API.

Download the desktop app and start a free trial: https://claude.ai/referral/uIlpa7nPLg
More help: https://docs.apify.com/platform/integrations/claude-desktop

## Install in Claude Code

![Install in Claude Code](https://raw.githubusercontent.com/johnisanerd/ApifyPublicData/main/assets/guides/install_mcp_into_claude_code.png)

Claude Code is the command-line tool. Add the Actor's MCP server with one command:

```bash
claude mcp add --transport http apify \
  "https://mcp.apify.com/?tools=actors,docs,johnvc/google-play-api"
```

To use a token instead of browser OAuth:

```bash
claude mcp add --transport http apify \
  "https://mcp.apify.com/?tools=actors,docs,johnvc/google-play-api" \
  --header "Authorization: Bearer YOUR_APIFY_TOKEN"
```

Then verify with `claude mcp list`, or run `/mcp` inside a session. Ask Claude Code to call the Google Play API.

Try Claude Code free: https://claude.ai/referral/uIlpa7nPLg
Claude Code MCP docs: https://code.claude.com/docs/en/mcp

## Install in Claude (website)

![Install in Claude (website)](https://raw.githubusercontent.com/johnisanerd/ApifyPublicData/main/assets/guides/install_mcp_into_claude_ai.png)

On claude.ai you add Apify as a connector, then enable just this Actor's tool.

1. Go to **Settings -> Connectors -> Browse connectors** and search for **Apify MCP server**. Install it (enable or update if prompted).
2. When connecting, authenticate with your Apify API token, and enable the tool `johnvc/google-play-api`.
3. In any chat, open **+ -> Connectors** and turn on **Apify**.
4. Alternatively, choose **Add custom connector** and paste the full MCP URL `https://mcp.apify.com/?tools=actors,docs,johnvc/google-play-api`, using OAuth when prompted.
5. Ask Claude to run the Google Play API.

Open Claude on the web: https://claude.ai

## Install in Cursor

![Install in Cursor](https://raw.githubusercontent.com/johnisanerd/ApifyPublicData/main/assets/guides/install_mcp_into_cursor.png)

Cursor reads MCP servers from a project file at `.cursor/mcp.json`.

1. In your project, create `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "apify": {
      "url": "https://mcp.apify.com/?tools=actors,docs,johnvc/google-play-api"
    }
  }
}
```

2. If you prefer token auth over browser OAuth, add a header:

```json
{
  "mcpServers": {
    "apify": {
      "url": "https://mcp.apify.com/?tools=actors,docs,johnvc/google-play-api",
      "headers": { "Authorization": "Bearer YOUR_APIFY_TOKEN" }
    }
  }
}
```

3. Open **Cursor -> Settings -> MCP** and confirm the **apify** server is connected (green dot).
4. In Composer or Chat, ask Cursor to call the Google Play API.

New to Cursor? Get it here: https://cursor.com/referral?code=XQP4VBLI3NNX

## Install in ChatGPT

![Install in ChatGPT](https://raw.githubusercontent.com/johnisanerd/ApifyPublicData/main/assets/guides/install_mcp_into_ChatGPT.png)

ChatGPT connects to the Apify MCP server through Developer mode (available on ChatGPT Pro, Plus, Business, Enterprise, and Education plans).

1. Click your profile icon, then go to **Settings > Apps**. If you do not see a **Create app** button, open **Advanced settings** and enable **Developer mode**.
2. Click **Create app** and fill out the form:
   - **Name:** Apify
   - **MCP Server URL:** `https://mcp.apify.com/?tools=actors,docs,johnvc/google-play-api`
   - **Authentication:** OAuth
3. Click **Create** and authorize the connection with Apify.
4. To use the app in a conversation, click **+** in the chat, choose **Developer mode**, and select **Apify**.

More help: https://docs.apify.com/platform/integrations/mcp


---

Made with care by [johnvc on Apify](https://apify.com/johnvc?fpr=9n7kx3). This example repo is part of [Alpha OSINT](https://www.alphaosint.com), toolset of financial and operations data sources and APIs.

Last Updated: 2026.08.09
