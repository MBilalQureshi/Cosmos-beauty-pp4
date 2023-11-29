# Testing

## Table of Contents

## Validator Testing

### HTML

Every page is run through [W3C HTML Validator](https://validator.w3.org/). Results are mentioned below.

| Page                 | Errors     | Notes     |
|----------------------|------------|-----------|
| base.html            | No Errors  | Note 1    |
| index.html           | No errors  | Note 1    |
| products.html        | No errors  | No errors |
| product_detail.html  | N/A        | No errors |
| cart.html            | N/A        | No errors |
| user_checkout.html   | No errors  | No errors |
| order_complete.html  | N/A        | No errors |
| my_orders.html       | N/A        | No errors |
| wishlist.html        | N/A        | No errors |
| paginator.html       | No errors  | No errors |
| recipe_detail.html   | No errors  | No errors |
| login.html           | No errors  | N/A       |
| logout.html          | N/A        | No errors |
| signup.html          | No errors  | N/A       |
| 400.html             | No errors  | No errors |
| 403.html             | N/A        | No errors |
| 404.html             | No errors  | No errors |
| 500.html             | No errors  | No errors |

#### Note 1
The error shown here are related to django critaria of manipulating html using {% %}. There is nothing can be done to fix this as per my understanding. 
