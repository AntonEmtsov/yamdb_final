import re
from datetime import date

from django.core.exceptions import ValidationError


def username_validate(value):
    if value == 'me':
        raise ValidationError(
            f'Нельзя использовать username: {value} '
        )
    if re.findall(r'[^\w@.+-]+', value):
        value_re = re.sub(r'[\w@.+-]+', '', value, flags=re.UNICODE)
        value_re_single_sample = set(value_re)
        raise ValidationError(
            (
                f'Некорректное имя Пользователя: {value}! '
                f'Недопустимые символы: {value_re_single_sample} !! '
                'Имя пользователя может содержать только:'
                'Буквы, цифры, и символы: @/./+/-/_'
            )
        )
    return value


def validate_year(year):
    current_year = date.today().year
    if year > current_year:
        raise ValidationError(
            f'Год выпуска {year} не может быть больше {current_year}'
        )
    return year
