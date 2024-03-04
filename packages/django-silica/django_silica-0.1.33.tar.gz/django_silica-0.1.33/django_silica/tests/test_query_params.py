import time

from django.test import RequestFactory, override_settings
from django.contrib.auth.models import AnonymousUser

from django_silica.SilicaComponent import SilicaComponent
from django_silica.tests.utils import create_test_view
from django_silica.urls import urlpatterns as silica_urlpatterns, path
from django_silica.tests.SilicaTestCase import SilicaTestCase, SilicaTest, SilicaBrowserTestCase

from selenium.webdriver.common.by import By


TestView = create_test_view(f"""
    {{% silica '{__name__}.QueryParamsTestComponent' %}}
    """)


urlpatterns = silica_urlpatterns + [
    path("query-params/", TestView.as_view()),
]


class QueryParamsTestComponent(SilicaComponent):
    property_1 = "foo1"
    property_2 = "foo2"
    property_3 = "foo3"

    query_params = [
        "property_1",
        {"param": "property_2"},
        {"param": "property_3", "as": "p3"}
    ]

    def inline_template(self):
        return """
            <div>
                {{ property_1 }}
                {{ property_2 }}
                {{ property_3 }}
                <button silica:click.prevent="property_1 = 'foo1'" id="set_to_default">Set</button>
            </div>
        """


class QueryParamTests(SilicaTestCase):
    def test_query_params_can_be_dict_format(self):
        (
            SilicaTest(component=QueryParamsTestComponent)
            .assertSet("property_2", "foo2")
            .assertSee("foo2")
            .assertSet("property_3", "foo3")
            .assertSee("foo3")
        )

        request = RequestFactory().get("/?property_2=bar")
        request.user = AnonymousUser()

        (
            SilicaTest(component=QueryParamsTestComponent, request=request)
            .assertSet("property_2", "bar")
            .assertSee("bar")
        )


    def test_query_params_can_be_set(self):
        (
            SilicaTest(component=QueryParamsTestComponent)
            .assertSet("property_1", "foo1")
            .assertSee("foo1")
        )

        request = RequestFactory().get("/?property_1=bar")
        request.user = AnonymousUser()

        (
            SilicaTest(component=QueryParamsTestComponent, request=request)
            .assertSet("property_1", "bar")
            .assertSee("bar")
        )


    def test_aliased_query_params(self):
        (
            SilicaTest(component=QueryParamsTestComponent)
            .assertSet("property_3", "foo3")
            .assertSee("foo3")
        )

        request = RequestFactory().get("/?p3=bar")
        request.user = AnonymousUser()

        (
            SilicaTest(component=QueryParamsTestComponent, request=request)
            .assertSet("property_3", "bar")
            .assertSee("bar")
        )


@override_settings(ROOT_URLCONF=__name__)
class QueryParamBrowserTests(SilicaBrowserTestCase):
    def test_query_params_are_removed_for_default_values(self):
        self.selenium.get(self.live_server_url + "/query-params?property_1=bar")

        self.assertTrue(self.get_query_param("property_1") == "bar", "Param not set in url")

        self.selenium.find_element(By.ID, 'set_to_default').click()
        time.sleep(0.2)

        self.assertTrue(self.get_query_param("property_1") is None, "Param not cleared when set to default")



