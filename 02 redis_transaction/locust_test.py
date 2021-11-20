from locust import HttpUser, task


class BuyProductUser(HttpUser):
    @task()
    def buy(self):
        self.client.post('/buy')


if __name__ == '__main__':
    import os

    os.system('locust -f locust_test.py --host=http://localhost:8000')
