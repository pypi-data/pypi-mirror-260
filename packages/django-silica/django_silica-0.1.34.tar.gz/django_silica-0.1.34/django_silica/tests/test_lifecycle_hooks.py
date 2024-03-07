from django_silica.SilicaComponent import SilicaComponent
from django_silica.tests.SilicaTestCase import SilicaTestCase, SilicaTest


class Lifecycle(SilicaComponent):
    called_mount = 0
    called_updated = 0
    called_updated_property = 0

    property = None

    def mount(self):
        self.called_mount += 1

    def updated_property(self, value):
        self.called_updated_property = value

    def updated(self, prop, value):
        self.called_updated = f"{prop}={value}"

    def inline_template(self):
        return """
            <div>
                hi!
            </div>        
        """


class LifecycleTestCase(SilicaTestCase):
    def test_mount_is_called_once(self):
        (
            # Initial request
            SilicaTest(component=Lifecycle)
            .assertSet("called_mount", 1)
            .set("property", "test")
            .assertSet("called_updated_property", "test")
            .assertSet("called_updated", "property=test")
        )

