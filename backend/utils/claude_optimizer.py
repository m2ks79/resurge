"""
Claude AI integration for platform-specific caption generation (Phase 2)

One API call generates captions for every requested platform at once,
using structured outputs so the response is always valid JSON.
"""

import anthropic

MODEL = "claude-opus-5"

SUPPORTED_PLATFORMS = ('tiktok', 'instagram', 'youtube', 'linkedin')

PLATFORM_STYLE_GUIDE = """You write social media captions for content creators.
Follow each platform's conventions exactly:

- tiktok: Gen Z voice, trendy, punchy, max 150 characters before hashtags.
  3-5 hashtags mixing broad reach (#fyp-style) with niche tags. Playful emojis.
- instagram: Engaging and personable, max 300 characters. Open with a hook line,
  end with a question or call-to-action. 3-5 hashtags, 2-3 emojis.
- youtube: Clear and informative for Shorts, max 200 characters. Key topic in the
  first few words, one call-to-action (subscribe/watch). 2-3 hashtags, 0-2 emojis.
- linkedin: Professional, insight-led, max 250 characters. Lead with a takeaway
  or lesson, thought-leadership tone. 2-3 industry hashtags, at most 1 emoji.

Hashtags go in the "hashtags" array only - never inside the caption text.
Captions must be ready to paste as-is."""


class ClaudeOptimizer:
    """Generate platform-optimized captions with the Claude API"""

    def __init__(self):
        self._client = None

    def _get_client(self):
        # Lazy init so the app starts fine without credentials configured;
        # Anthropic() resolves ANTHROPIC_API_KEY (loaded from .env by config.py)
        # or a local `ant auth login` profile.
        if self._client is None:
            self._client = anthropic.Anthropic()
        return self._client

    @staticmethod
    def _captions_schema(platforms):
        platform_schema = {
            "type": "object",
            "properties": {
                "caption": {"type": "string"},
                "hashtags": {"type": "array", "items": {"type": "string"}},
            },
            "required": ["caption", "hashtags"],
            "additionalProperties": False,
        }
        return {
            "type": "object",
            "properties": {p: platform_schema for p in platforms},
            "required": list(platforms),
            "additionalProperties": False,
        }

    def generate_captions(self, description, platforms=SUPPORTED_PLATFORMS, draft_caption=None):
        """
        Generate captions for all requested platforms in a single API call.

        Args:
            description: What the video is about.
            platforms: Which platforms to write for (default: all four).
            draft_caption: Optional existing caption to adapt instead of
                writing from scratch.

        Returns:
            {"tiktok": {"caption": str, "hashtags": [str, ...]}, ...}
        """
        import json

        platforms = [p for p in platforms if p in SUPPORTED_PLATFORMS]
        if not platforms:
            raise ValueError(
                f"No valid platforms given. Supported: {', '.join(SUPPORTED_PLATFORMS)}"
            )

        if draft_caption:
            task = (
                f'Adapt this draft caption for each platform: "{draft_caption}"\n'
                f"Video context: {description or 'not provided'}"
            )
        else:
            task = f"Write a caption for each platform. The video is about: {description}"

        client = self._get_client()
        response = client.messages.create(
            model=MODEL,
            max_tokens=2048,
            system=PLATFORM_STYLE_GUIDE,
            messages=[{"role": "user", "content": task}],
            output_config={
                "format": {
                    "type": "json_schema",
                    "schema": self._captions_schema(platforms),
                }
            },
        )

        text = next(block.text for block in response.content if block.type == "text")
        return json.loads(text)

    def optimize_for_platform(self, caption, platform='instagram'):
        """Backward-compatible single-platform helper used by /api/optimize-caption."""
        result = self.generate_captions(
            description=None, platforms=[platform], draft_caption=caption
        )[platform]
        return {
            'caption': result['caption'],
            'hashtags': result['hashtags'],
            'emojis': [],
            'platform': platform,
        }
