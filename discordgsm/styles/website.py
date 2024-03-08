from typing import Dict

from discord.ui import TextInput
from discord import Color, Embed, Emoji, Locale, PartialEmoji, TextStyle

from discordgsm.styles.style import Style
from discordgsm.translator import t


class Website(Style):
    """Website style"""

    @property
    def display_name(self) -> str:
        return t('style.website.display_name', self.locale)

    @property
    def description(self) -> str:
        return t('style.website.description', self.locale)

    @property
    def default_edit_fields(self) -> Dict[str, TextInput]:
        return {
            'description': TextInput(
                label=t('embed.text_input.description.label', self.locale),
                style=TextStyle.long,
                placeholder=t('embed.text_input.description.placeholder', self.locale),
                default=self.server.style_data.get('description', ''),
                required=False,
                max_length=1024
            ),
            'fullname': TextInput(
                label=t('embed.text_input.fullname.label', self.locale),
                placeholder=t('embed.text_input.fullname.placeholder', self.locale),
                default=self.server.style_data.get('fullname', ''),
            )
        }

    def embed(self) -> Embed:
        title, description, color = self.embed_data()
        embed = Embed(title=title, description=description, color=color)

        self.add_status_field(embed)
        self.add_address_field(embed)
        self.add_game_field(embed)

        self.set_footer(embed)

        return embed
