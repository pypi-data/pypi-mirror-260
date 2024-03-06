import logging

from .mixin.announce import AnnouncementMixin
from .mixin.booking import BookingMixin
from .mixin.broadcast import BroadcastMixin
from .mixin.category import CategoryMixin
from .mixin.geocode import GeocodeMixin
from .mixin.menu import MenuMixin
from .mixin.place import PlaceMixin
from .mixin.promotions import PromotionsMixin
from .mixin.review import ReviewMixin

__VERSION__ = "0.1.12"

from .mixin.search import SearchMixin

DEFAULT_LOGGER = logging.getLogger("naverplaceapi")


class Client(
    GeocodeMixin,
    PlaceMixin,
    ReviewMixin,
    BroadcastMixin,
    PromotionsMixin,
    AnnouncementMixin,
    BookingMixin,
    MenuMixin,
    CategoryMixin,
    SearchMixin
):
    pass
