from itertools import zip_longest, chain
from functools import reduce, partial
from random import choices
from uuid import uuid4


class Customer:
    queue = []
    preferred_queue = []
    wait_queue = []

    def add_customer_to_queue(self, name, age):
        if age < 65:
            self.queue.append({
                'name': name,
                'age': age,
                'order': None
            })
        else:
            self.preferred_queue.append({
                'name': name,
                'age': age,
                'order': None
            })

    def get_queue_position(self, name):
        for customer, preferred_customer in \
             zip_longest(enumerate(self.queue), enumerate(self.preferred_queue)):
            if preferred_customer and preferred_customer[1].get('name') == name:
                return preferred_customer[0]
            if customer and customer[1].get('name') == name:
                return customer[0]

        return -1
    
    def get_customer(self, name, age):
        if age < 65:
            return self.queue[self.get_queue_position(name)]
        return self.preferred_queue[self.get_queue_position(name)]
    
    def get_customer_by_order(self, order_number):
        for customer in self.wait_queue:
            if customer.get('order') == order_number:
                return customer
        return None

    def add_wait_queue(self, order_number):
        customer = None
        if order_number.find('NL') > 0:
            customer = [x for x in self.queue if x.get('order') == order_number]
            self.queue = [x for x in self.queue if x.get('order') != order_number]
        else:
            customer = [x for x in self.preferred_queue if x.get('order') == order_number]
            self.preferred_queue = [x for x in self.preferred_queue if x.get('order') != order_number]
        
        if customer:
            self.wait_queue.append(customer[-1])

    def print_queue(self):
        print('Customers Queue')
        for customer in chain(self.preferred_queue, self.queue):
            print(f'Name: {customer["name"]} - Age: {customer["age"]}')

        for waiter in self.wait_queue:
            print(f'Name: {customer["name"]} - Age: {customer["age"]} - Order Number: {customer["order"]}')


class Order:
    order_queue = []
    def new_order(self, customer):
        order_number = str(uuid4()).split("-")[1]
        if customer['age'] < 65:
            order_number = f'NL-{order_number}'
        else:
            order_number = f'PF-{order_number}'
        items = self.add_items()
        total = reduce(lambda x, y:  x + (y.get('price') * y.get('quantity')), items, 0)
        self.order_queue.append({
            'number': order_number,
            'total': total,
            'items': items,
        })
        customer['order'] = order_number
        return order_number

    def add_items(self):
        items = []
        while True:
            try:
                name = input('Enter the product\'s name: ')
                price = float(input('Enter the product\'s price: '))
                quantity = int(input('Enter the product\'s quantity: '))

                items.append({
                    'name': name,
                    'price': price,
                    'quantity': quantity,
                })

                print()
                add_new = input('Wanna add another item? [y/n] \n').lower()
                if add_new == 'n':
                    break
            except Exception:
                print('An error ocurred, please try again!')
        
        return items

    def fulfill_order(self):
        if self.order_queue:
            order = choices(self.order_queue)[0]
            self.order_queue = [x for x in self.order_queue if x.get('number') != order.get('number')]
            return order.get('number')
        return None


customers = Customer()

customers.add_customer_to_queue('Marcelo', 99)
customers.add_customer_to_queue('André', 27)
customers.add_customer_to_queue('Vini', 21)
customers.add_customer_to_queue('Vinicius Vieira', 19)
customers.add_customer_to_queue('Caio Teixeira', 25)
customers.add_customer_to_queue('Orlando', 10000)

customers.print_queue()

cs = []
cs.append(customers.get_customer('Marcelo', 99))
# cs.append(customers.get_customer('André', 27))
# cs.append(customers.get_customer('Vini', 21))
# cs.append(customers.get_customer('Vinicius Vieira', 19))
# cs.append(customers.get_customer('Caio Teixeira', 25))
# cs.append(customers.get_customer('Orlando', 10000))

orders = Order()
for c in cs:
    order_number = orders.new_order(c)
    customers.add_wait_queue(order_number)


customers.print_queue()

for order in iter(orders.fulfill_order, ''):
    c = customers.get_customer_by_order(order)
    print(f'Order nº {order} is done')
    ans = input(f'{c.get('name')}, want to rate our attendance? [y/n]').lower()
    if ans == 'y':
        rate = int(input('Enter your rate: '))
        if 0 < rate <= 5:
            print(f'Your rating was {rate}. Thanks for your avaliation!')
