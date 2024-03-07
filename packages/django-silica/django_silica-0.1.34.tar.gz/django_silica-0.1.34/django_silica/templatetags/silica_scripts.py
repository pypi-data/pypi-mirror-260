from django import template
from django.templatetags.static import static
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def silica_scripts():
    silica_js = static("silica.js")
    morphdom_js = static("morphdom.js")
    alpine_js = static("alpine3.min.js")
    # style_url = static("css/your_styles.css")
    return mark_safe(f"""
        <script src="{silica_js}"></script>
        <script src="{morphdom_js}"></script>
        <script src="{alpine_js}" defer></script>
        <style>[silica\:loading], [silica\:loading\.class] {{ display: none }}</style>
    """)
