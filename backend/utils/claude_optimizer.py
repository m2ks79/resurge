"""
Claude AI integration for caption/content optimization
(Phase 2 feature - smart captions per platform)
"""

import os

# Lazy load Anthropic client to avoid import errors
client = None


class ClaudeOptimizer:
    """Use Claude to optimize captions for each platform"""

    PLATFORM_PROMPTS = {
        'tiktok': """Optimize this caption for TikTok (Gen Z audience, trendy, fun, max 150 chars).
        - Use trending slang
        - Add 3-5 relevant hashtags
        - Include fun emojis
        - Make it punchy and engaging""",

        'instagram': """Optimize this caption for Instagram (professional yet engaging, max 300 chars).
        - Use 3-5 relevant hashtags
        - Professional tone but personable
        - Include 2-3 strategic emojis
        - Focus on engagement (questions, calls-to-action)""",

        'youtube': """Optimize this caption for YouTube Shorts (clear, informative, max 200 chars).
        - Include 2-3 relevant hashtags
        - Add call-to-action
        - Include 1-2 emojis
        - Mention key topic upfront""",

        'linkedin': """Optimize this caption for LinkedIn (professional, B2B focus, max 250 chars).
        - Use industry-relevant hashtags (2-3)
        - Professional tone
        - Include insights or takeaways
        - Minimal emojis (0-1)
        - Add thought leadership angle"""
    }

    def __init__(self):
        self.api_key = os.getenv('ANTHROPIC_API_KEY')
        self.client = None
        # Note: Client is lazily initialized on first use
        # This prevents import errors if ANTHROPIC_API_KEY is not set

    def _get_client(self):
        """Lazily initialize Anthropic client on first use"""
        if self.client is None:
            if not self.api_key:
                raise ValueError("ANTHROPIC_API_KEY not set in .env")
            try:
                from anthropic import Anthropic
                self.client = Anthropic(api_key=self.api_key)
            except Exception as e:
                raise Exception(f"Failed to initialize Anthropic client: {e}")
        return self.client

    def optimize_for_platform(self, caption, platform='instagram'):
        """
        Use Claude to optimize caption for specific platform

        Args:
            caption: Original caption text
            platform: 'tiktok', 'instagram', 'youtube', or 'linkedin'

        Returns:
            {
                'caption': 'optimized caption',
                'hashtags': ['#tag1', '#tag2', ...],
                'emojis': ['🎬', '📸', ...],
                'platform': 'instagram'
            }
        """
        if platform not in self.PLATFORM_PROMPTS:
            raise ValueError(f"Unknown platform: {platform}")

        prompt = self.PLATFORM_PROMPTS[platform]

        claude = self._get_client()
        message = claude.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": f"""{prompt}

Original caption: "{caption}"

Return response in JSON format:
{{
    "optimized_caption": "your optimized caption here",
    "hashtags": ["#tag1", "#tag2", "#tag3"],
    "emojis": ["emoji1", "emoji2"],
    "reasoning": "brief explanation of changes"
}}"""
                }
            ]
        )

        # Parse response
        response_text = message.content[0].text

        # Extract JSON from response
        import json
        try:
            # Try to parse as JSON directly
            result = json.loads(response_text)
        except json.JSONDecodeError:
            # Claude might wrap it in markdown code blocks
            import re
            json_match = re.search(r'```(?:json)?\n(.*?)\n```', response_text, re.DOTALL)
            if json_match:
                result = json.loads(json_match.group(1))
            else:
                # Fallback: return original with empty extras
                result = {
                    'optimized_caption': caption,
                    'hashtags': [],
                    'emojis': [],
                    'reasoning': 'Could not parse Claude response'
                }

        return {
            'caption': result.get('optimized_caption', caption),
            'hashtags': result.get('hashtags', []),
            'emojis': result.get('emojis', []),
            'platform': platform,
            'reasoning': result.get('reasoning', '')
        }

    def generate_caption(self, video_description, platform='instagram'):
        """
        Generate a full caption from scratch for a video

        Args:
            video_description: Brief description of video content
            platform: Target platform

        Returns:
            Same format as optimize_for_platform()
        """
        prompt = f"Create an engaging {platform} caption for a video about: {video_description}\n{self.PLATFORM_PROMPTS.get(platform, '')}"

        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": f"""{prompt}

Return response in JSON format:
{{
    "optimized_caption": "your generated caption",
    "hashtags": ["#tag1", "#tag2"],
    "emojis": ["emoji1", "emoji2"]
}}"""
                }
            ]
        )

        response_text = message.content[0].text

        import json
        import re
        try:
            result = json.loads(response_text)
        except json.JSONDecodeError:
            json_match = re.search(r'```(?:json)?\n(.*?)\n```', response_text, re.DOTALL)
            if json_match:
                result = json.loads(json_match.group(1))
            else:
                result = {'optimized_caption': video_description, 'hashtags': [], 'emojis': []}

        return {
            'caption': result.get('optimized_caption', ''),
            'hashtags': result.get('hashtags', []),
            'emojis': result.get('emojis', []),
            'platform': platform
        }
