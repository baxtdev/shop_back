import requests

body = {
  "name": "string",
  "phone": "string",
  "user_id": 1,
  "order_products": [
    {
      "product_id": 1,
      "quantity": 111
    }
  ]
}


response = requests.post('http://127.0.0.1:8000/orders/',json=body,headers={"Authorization":"Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJleHAiOjE3MzQ0MjQ5ODF9.2v3RPvwR522xvn1j878ob5OXoev5t-Qmh2nMNoIQ7gs"})

print(response.status_code)
print(response.text)