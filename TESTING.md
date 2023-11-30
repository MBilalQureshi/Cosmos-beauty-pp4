# Testing

## Table of Contents

## Validator Testing

### HTML

Every page is run through [W3C HTML Validator](https://validator.w3.org/). Results are mentioned below.

| Page                 | Logged in     | Logged out     |
|----------------------|---------------|----------------|
| base.html            | N/A           | N/A            |
| index.html           | No errors  | Note 1    |
| products.html        | No Errors  | Note 1    |
| product_detail.html  | No Errors  | Note 1    |
| cart.html            | No Errors  | Note 1    |
| user_checkout.html   | No Errors  | Note 1, 2 |
| order_complete.html  | No Errors  | Note 1    |
| my_orders.html       | No Errors  | Note 1    |
| wishlist.html        | No Errors  | Note 1    |
| paginator.html       | No Errors  | Note 1    |
| login.html           | No Errors  | Note 1    |
| logout.html          | No Errors  | Note 1    |
| signup.html          | No Errors  | Note 1    |
| 400.html             | No Errors  | Note 1    |
| 403.html             | No Errors  | Note 1    |
| 404.html             | No Errors  | Note 1    |
| 500.html             | No Errors  | Note 1    |

#### Note 1
The error shown here are related to django critaria of manipulating html using {% %}. There is nothing can be done to fix this as per my understanding. 
#### Note 2