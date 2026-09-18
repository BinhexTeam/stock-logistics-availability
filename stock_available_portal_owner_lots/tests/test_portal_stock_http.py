from odoo.tests import tagged

from .common import ConsignedStockLotsHttpCommon


@tagged("post_install", "-at_install")
class TestPortalConsignedStockLotsHttp(ConsignedStockLotsHttpCommon):
    def test_anonymous_user_redirected(self):
        """Un usuario sin autenticar debe ser redirigido al login."""
        response = self.url_open(
            f"/my/consigned-stock/lots/{self.product_a.id}", allow_redirects=False
        )
        self.assertIn(response.status_code, (302, 303))
        self.assertIn("/web/login", response.headers.get("Location", ""))

    def test_portal_user_can_access_lots(self):
        """El dueño A accede a la ruta y ve sus lotes renderizados en el HTML."""
        self.authenticate(self.portal_user.login, "consigned.portal")
        response = self.url_open(f"/my/consigned-stock/lots/{self.product_a.id}")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"LOT-A1", response.content)
        self.assertNotIn(b"LOT-B1", response.content)
