import frappe  # type: ignore
from frappe import _

@frappe.whitelist()
def on_submit(doc, method):
    for item in doc.items:
        item_code = item.item_code
        rate = (item.rate + item.applicable_charges) * (1 + item.custom_selling_price / 100)

        # Ensure required fields are provided
        if not item_code or not rate:
            frappe.throw(_("Item Code and Rate are required for all items."))

        # Check if an Item Price already exists for the item and price list
        existing_price = frappe.get_value(
            'Item Price',
            {'item_code': item_code, 'price_list': 'Standard Selling'},
            ['name', 'price_list_rate']
        )

        if existing_price:
            # Update the existing Item Price
            item_price_doc = frappe.get_doc('Item Price', existing_price[0])
            if item_price_doc.price_list_rate != rate:
                item_price_doc.price_list_rate = rate
                item_price_doc.save()
                # frappe.msgprint(
                #     _("Updated Item Price for {0} with new rate: {1}")
                #     .format(item_code, rate),
                #     alert=True
                # )
        else:
            # Create a new Item Price
            frappe.get_doc({
                'doctype': 'Item Price',
                'item_code': item_code,
                'price_list': 'Standard Selling',
                'price_list_rate': rate
            }).insert()
            # frappe.msgprint(
            #     _("Created new Item Price for {0} with rate: {1}")
            #     .format(item_code, rate),
            #     alert=True
            # )
    frappe.msgprint(
        msg="Item Price Updated Successfully!",
        title="Success",
        indicator="green"  # Options: green, red, orange
    )
