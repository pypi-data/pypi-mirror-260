from enum import Enum


class LinkCommentSortType(Enum):
    NEWEST = "newest"
    BEST = "best"
    OLDEST = "oldest"


class LinkCommentVoteType(Enum):
    UP = "up"
    DOWN = "down"


class LinkType(Enum):
    HOMEPAGE = "homepage"
    UPCOMING = "upcoming"


class LinkVoteDownReason(Enum):
    DUPLICATE = 1
    SPAM = 2
    UNTRUE = 3
    INAPPROPRIATE = 4
    UNSUITABLE = 5
