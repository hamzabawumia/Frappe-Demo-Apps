# Copyright (c) 2025, self and contributors
# For license information, please see license.txt

# import frappe
# from frappe.model.document import Document
# from frappe import _

# class playing(Document):
#     def validate(self):
#         # Get the current date
#         current_date = frappe.utils.nowdate()
        
#         # Define the target expiration date (4th of December 2024)
#         target_date = "2024-12-04"
        
#         # Compare current date with target date
#         if current_date > target_date:
#             # Raise a validation error with the appropriate message
#             frappe.throw(_("Your software licence has EXPIRED! Kindly renew it WITH PYTHON."))
        
#         # Optionally, if you want to show a warning for 14 days before expiration
#         else:
#             # Calculate the remaining days
#             target_date_obj = frappe.utils.getdate(target_date)
#             remaining_days = (target_date_obj - frappe.utils.getdate(current_date)).days
            
#             if remaining_days <= 14:
#                 # Show warning if 14 days or less
#                 frappe.msgprint(
#                     title=_("Licence Expiry Warning"),
#                     message=_("Your software licence will expire in {} day(s). Kindly renew your licence - PYTHON.".format(remaining_days)),
#                     indicator='orange'
#                 )