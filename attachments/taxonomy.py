"""
Attachment taxonomy for Last Seen.

This module defines normalized attachment types
based on real VK archive inspection.
"""


from dataclasses import dataclass


@dataclass(frozen=True)
class AttachmentType:
    key: str
    downloadable: bool
    source: str
    viewer: str


ATTACHMENT_TYPES = {
    # Media
    "photo": AttachmentType(
        key="photo",
        downloadable=True,
        source="cdn",
        viewer="image",
    ),
    "video": AttachmentType(
        key="video",
        downloadable=False,
        source="vk",
        viewer="video_link",
    ),
    "voice_message": AttachmentType(
        key="voice_message",
        downloadable=True,
        source="cdn",
        viewer="audio",
    ),
    "audio_track": AttachmentType(
        key="audio_track",
        downloadable=False,
        source="vk",
        viewer="audio_stub",
    ),
    "sticker": AttachmentType(
        key="sticker",
        downloadable=False,
        source="vk",
        viewer="sticker",
    ),

    # Links / references
    "link": AttachmentType(
        key="link",
        downloadable=False,
        source="external",
        viewer="link",
    ),
    "forwarded_messages": AttachmentType(
        key="forwarded_messages",
        downloadable=False,
        source="vk",
        viewer="forwarded",
    ),
    "wall_post": AttachmentType(
        key="wall_post",
        downloadable=False,
        source="vk",
        viewer="wall_post",
    ),

    # Events / meta
    "gift": AttachmentType(
        key="gift",
        downloadable=False,
        source="vk",
        viewer="gift",
    ),
    "call": AttachmentType(
        key="call",
        downloadable=False,
        source="vk",
        viewer="call",
    ),
    "story": AttachmentType(
        key="story",
        downloadable=False,
        source="vk",
        viewer="story",
    ),
    "playlist": AttachmentType(
        key="playlist",
        downloadable=False,
        source="vk",
        viewer="playlist",
    ),
    "map": AttachmentType(
        key="map",
        downloadable=False,
        source="vk",
        viewer="map",
    ),

    # Fallback
    "unknown": AttachmentType(
        key="unknown",
        downloadable=False,
        source="unknown",
        viewer="unknown",
    ),
}
