# Routing Table

| Method | Path | Handler | Story it serves |
|--------|------|---------|-----------------|
| POST | /customers | createCustomer | Add new customer information |
| GET | /customers | listCustomers | View all customer records |
| GET | /customers/:id | showCustomer | View customer details |
| PUT | /customers/:id | updateCustomer | Edit customer information |
| DELETE | /customers/:id | deleteCustomer | Remove customer records |
| POST | /laundry-orders | createLaundryOrder | Create a new laundry order |
| GET | /laundry-orders | listLaundryOrders | View all laundry orders and status |
| GET | /laundry-orders/:id | showLaundryOrder | View order details and status |
| PUT | /laundry-orders/:id | updateLaundryOrder | Update order status |
| DELETE | /laundry-orders/:id | deleteLaundryOrder | Cancel or delete orders |
| POST | /pickup-schedules | createPickupSchedule | Schedule a pickup request |
| GET | /pickup-schedules | listPickupSchedules | View pickup schedules |
| GET | /pickup-schedules/:id | showPickupSchedule | View a pickup schedule |
| PUT | /pickup-schedules/:id | updatePickupSchedule | Modify pickup date and time |
| DELETE | /pickup-schedules/:id | deletePickupSchedule | Cancel pickup requests |
| POST | /delivery-records | createDeliveryRecord | Create delivery records |
| GET | /delivery-records | listDeliveryRecords | View delivery status |
| GET | /delivery-records/:id | showDeliveryRecord | View a delivery record |
| PUT | /delivery-records/:id | updateDeliveryRecord | Update delivery information |
| DELETE | /delivery-records/:id | deleteDeliveryRecord | Delete delivery records |
| POST | /payments | createPayment | Add payment transactions |
| GET | /payments | listPayments | View payment history |
| GET | /payments/:id | showPayment | View a payment record |
| PUT | /payments/:id | updatePayment | Update payment status |
| DELETE | /payments/:id | deletePayment | Delete payment records |
