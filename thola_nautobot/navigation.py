"""Plugin additions to the Nautobot navigation menu."""
from nautobot.extras.plugins import PluginMenuItem, PluginMenuButton
from nautobot.utilities.choices import ButtonColorChoices

menu_items = (
    PluginMenuItem(
        link="plugins:thola_nautobot:tholaconfig_list",
        link_text="Configurations",
        buttons=(
            PluginMenuButton(
                link="plugins:thola_nautobot:tholaconfig_add",
                title="Add",
                icon_class="mdi mdi-plus-thick",
                color=ButtonColorChoices.GREEN,
            ),
        ),
    ),
    PluginMenuItem(
        link="plugins:thola_nautobot:tholaonboarding_list",
        link_text="Onboardings",
        buttons=(
            PluginMenuButton(
                link="plugins:thola_nautobot:tholaonboarding_add",
                title="Add",
                icon_class="mdi mdi-plus-thick",
                color=ButtonColorChoices.GREEN
            ),
        ),
    ),
)
