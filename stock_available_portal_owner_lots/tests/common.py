from odoo.addons.stock_available_portal_owner.tests.common import (
    ConsignedStockCommon,
    ConsignedStockHttpCommon,
)


class ConsignedStockLotsDataMixin:
    @classmethod
    def _create_lot(cls, name, product, company=None):
        return cls.env["stock.lot"].create(
            {
                "name": name,
                "product_id": product.id,
                "company_id": (company or cls.company).id,
            }
        )

    @classmethod
    def _create_consigned_stock_lots_data(cls):
        # 1. Aseguramos que el usuario tiene permisos para ver lotes
        cls.env.user.groups_id += cls.env.ref("stock.group_production_lot")

        # 2. Creamos lotes
        cls.lot_a1 = cls._create_lot("LOT-A1", cls.product_a)
        cls.lot_a2 = cls._create_lot("LOT-A2", cls.product_a)
        cls.lot_b1 = cls._create_lot("LOT-B1", cls.product_b)

        # 3. Asignamos stock con lote a los dueños
        cls.env["stock.quant"].sudo()._update_available_quantity(
            cls.product_a,
            cls.warehouse.lot_stock_id,
            5,
            lot_id=cls.lot_a1,
            owner_id=cls.owner_a,
        )
        cls.env["stock.quant"].sudo()._update_available_quantity(
            cls.product_a,
            cls.warehouse.lot_stock_id,
            5,
            lot_id=cls.lot_a2,
            owner_id=cls.owner_a,
        )
        # Lote para el dueño B (aislamiento)
        cls.env["stock.quant"].sudo()._update_available_quantity(
            cls.product_b,
            cls.warehouse.lot_stock_id,
            10,
            lot_id=cls.lot_b1,
            owner_id=cls.owner_b,
        )


class ConsignedStockLotsCommon(ConsignedStockCommon, ConsignedStockLotsDataMixin):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls._create_consigned_stock_lots_data()


class ConsignedStockLotsHttpCommon(
    ConsignedStockHttpCommon, ConsignedStockLotsDataMixin
):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls._create_consigned_stock_lots_data()
