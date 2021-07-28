### Basic points application


#### Objective:
Manage user points transactions and summarize it.

#### Specification:

- users have points in their accounts
- users see total points balance
- user points are allocated by partner/payer
- spending transaction contains (payer, points, timestamp)
- earning transaction contains (activity, user)


#### Constraints:

1. Each points spent will be deducted from the oldest points based on transaction timestamp
2. No payer's points to go negative (floor 0)


#### Routes

1. ```/transaction/add_points/<user_id>/```  -- POST
2. ```/transaction/spend_points/<user_id>/``` -- POST
3. ```/transaction/get_points/<user_id>/``` -- GET

#### Deployment

1. cd ```points```
2. docker build -t points .
3. docker run --name mycontainer -p 5000:5000 -d points

#### NOTE

1. Instead of using permanent store such as Redis | Mongo - use in-memory cache