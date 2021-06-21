"""Plugin additions to the Nautobot navigation menu."""
from nautobot.extras.plugins import PluginMenuItem, PluginMenuButton
from nautobot.utilities.choices import ButtonColorChoices

menu_items = (
    PluginMenuItem(
        link="plugins:thola_nautobot:tholadevice_list",
        link_text="Thola Devices",
        buttons=(
            PluginMenuButton(
                link="plugins:thola_nautobot:tholadevice_add",
                title="Add",
                icon_class="mdi mdi-plus-thick",
                color=ButtonColorChoices.GREEN,
            ),
        ),
    ),
)