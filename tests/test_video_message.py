import pytest
from pydantic.error_wrappers import ValidationError

from infobip_channels.whatsapp.models.core import MessageBody
from tests.conftest import VideoMessageBodyFactory, get_random_string


def test_video_message_body__is_an_instance_of_message_body():
    assert isinstance(VideoMessageBodyFactory.build(), MessageBody) is True


@pytest.mark.parametrize("content", [None, "", {}])
def test_when_content_is_invalid__validation_error_is_raised(content):
    with pytest.raises(ValidationError):
        VideoMessageBodyFactory.build(**{"content": content})


@pytest.mark.parametrize(
    "media_url",
    [None, "", {}, "ftp://myfile.com", f"http://myfile.com/{get_random_string(2031)}"],
)
def test_when_content_media_url_is_invalid__validation_error_is_raised(media_url):
    with pytest.raises(ValidationError):
        VideoMessageBodyFactory.build(**{"content": {"mediaUrl": media_url}})


@pytest.mark.parametrize("caption", [{}, get_random_string(3001)])
def test_when_content_caption_is_invalid__validation_error_is_raised(caption):
    with pytest.raises(ValidationError):
        VideoMessageBodyFactory.build(
            **{"content": {"mediaUrl": "http://mymedia.com", "caption": caption}}
        )