import re
from rest_framework.serializers import ValidationError


class NoLinkValidator:

    def __init__(self, field='video_url'):
        self.field = field

    def __call__(self, value):
        reg = re.compile('^(https?://)?(www/.)?youtube/.com/?$')
        tmp_val = dict(value).get(self.field)
        if tmp_val is None: return
        if not bool(reg.match(tmp_val)):
            raise ValidationError('Ссылка недействительна. Разрешены только ссылки на youtube.com.')
