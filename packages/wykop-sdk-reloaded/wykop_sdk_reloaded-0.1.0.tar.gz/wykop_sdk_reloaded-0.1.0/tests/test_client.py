from unittest import TestCase
import os

from src.wykop_sdk_reloaded.v3.client import AuthClient, WykopApiClient
from src.wykop_sdk_reloaded.v3.types import LinkType, LinkVoteDownReason, LinkCommentVoteType


env = os.getenv


class TestV3Client(TestCase):
    def setUp(self):
        auth = AuthClient(env("WYKOP_APP_SECRET"), env("WYKOP_APP_KEY"))
        auth.auth_user(
            token=env("WYKOP_USER_TOKEN"),
            refresh_token=env("WYKOP_USER_REFRESH_TOKEN")
        )
        
        self.api = WykopApiClient(auth)
        

    def test_tags(self):
        tag = "wykop"

        self.api.tags_get_detail_of_tag(tag)
        self.api.tags_get_popular()
        self.api.tags_get_popular_user_tags()
        self.api.tags_get_related_tag(tag)
        self.api.tags_get_stream_of_tag(tag)
        self.api.tags_get_tag_owners(tag)

    def test_entries(self):
        response = self.api.entries_create("lorem " * 40)
        entry_id = str(response["data"]["id"])

        self.api.entries_get_entry(entry_id)
        self.api.entries_update_entry(entry_id, 'ipsum'* 20)

        self.api.entry_comments_list(entry_id)

        response = self.api.entry_comments_create_comment(entry_id, "ipsum lorem" * 5)
        entry_comment_id = str(response["data"]["id"])
        
        self.api.entry_comments_list(entry_id)
        self.api.entry_comments_update_comment(entry_id, entry_comment_id, "test " * 5)
        self.api.entry_comments_delete_comment(entry_id, entry_comment_id)

        self.api.entries_delete_entry(entry_id)

    def test_entries_voting(self):
        self.api.entries_list()
        response = self.api.entries_list_by_tag("wykop")
        entry_id = response["data"][0]["id"]

        self.api.entries_vote_up_entry(entry_id)
        self.api.entries_vote_revoke_entry(entry_id)


    def test_links(self):
        response = self.api.links_list(LinkType.HOMEPAGE)
        link_id = response["data"][0]["id"]

        self.api.links_vote_down_link(link_id, LinkVoteDownReason.INAPPROPRIATE)
        self.api.links_vote_revoke_link(link_id)
        self.api.links_vote_up_link(link_id)
        self.api.links_vote_revoke_link(link_id)

        response = self.api.link_comments_list(link_id)
        comment_id = response["data"][0]["id"]
        self.api.link_comments_vote_comment(link_id, comment_id, LinkCommentVoteType.UP)
        self.api.link_comments_vote_revoke_comment(link_id, comment_id)

        response = self.api.link_comments_create_comment(link_id, "test "* 10)
        own_comment_id = response["data"]["id"]

        self.api.link_comments_update_comment(link_id, own_comment_id, content="albo" * 10)
        response = self.api.link_comments_create_comment_to_comment(link_id, own_comment_id, content="albo" * 10)
        own_comment_to_comment_id = response["data"]["id"]

        self.api.link_comments_delete_comment(link_id, own_comment_id)
        self.api.link_comments_delete_comment(link_id, own_comment_to_comment_id)
        
    def test_notifications(self):
        self.api.notifinations_entries_list()
