import stripe
from flask import Flask, jsonify, request, Response, json, render_template, make_response, url_for
from flask_restful import Resource, Api

# creating the flask app
app = Flask(__name__)
# creating an API object
api = Api(app)

app.config[
    'STRIPE_PUBLIC_KEY'] = 'pk_test_51IBOaDDfKNGwe0ABkH5iZzXim5YrgaL3EGD5dbSGi5ZvXQxHjvyU07WKdgpVxonLeKB8eJKHHfkDz7cMHKbxI9eU005qoSqGW2'
app.config[
    'STRIPE_SECRET_KEY'] = 'sk_test_51IBOaDDfKNGwe0ABsS8miBGwE29xzOeQw8zNCcyCv29mTCt1PH8s4gGQhCiW6CG4zBm8WCpsp7ZnTA6YEOSoxZ1y00Fi7ErLBo'

stripe.api_key = app.config['STRIPE_SECRET_KEY']


class Home(Resource):

    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('index.html'), 200, headers)

    def post(self):
        json_data = request.get_json()
        print(json_data)
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                # 'name': 'T-Shirt',
                # 'amount': '1768',
                'name': json_data['name'],
                'amount': json_data['amount'],
                'currency': 'eur',
                'quantity': 1,
            }],
            mode='payment',
            success_url=url_for('myapp', _external=True) + '?msg=success&amt=' + json_data[
                'amount'] + '&session_id={CHECKOUT_SESSION_ID}',
            cancel_url=url_for('myapp', _external=True) + '?msg=success&amt=' + json_data['amount'],
        )
        return {
            'checkout_session_id': session['id'],
            'checkout_public_key': app.config['STRIPE_PUBLIC_KEY']
        }


# Rest Class
class MyApp(Resource):

    # Corresponds Get Method
    def get(self):
        try:
            data = request.args
            print(data)
            amt = int(data['amt'])
            if 2000 >= amt:
                msg = 'CheapPaymentGateway'
            elif 2000 < amt <= 50000:
                msg = 'ExpensivePaymentGateway'
            elif amt > 50000:
                msg = 'PremiumPaymentGateway'

            if data['msg'] == 'success':
                return Response(
                    response=json.dumps({
                        "data": {
                            'Amount': amt,
                            'Message': msg + " process is done",
                        }
                    }),
                    status=200,
                    mimetype="application/json"
                )
            else:
                return Response(
                    response=json.dumps({
                        "data": {
                            'Amount': amt,
                            'Message': msg + " process is failed",
                        }
                    }),
                    status=400,
                    mimetype="application/json"
                )
            # return jsonify({'msg': 'Welcome Flask REST GET Method'})
        except Exception as e:
            return Response(
                response=json.dumps({
                    "data": {
                        'msg': 'Error',
                    }
                }),
                status=500,
                mimetype="application/json"
            )


# adding the defined resources along with their corresponding urls
routes = [
    '/',
    '/home/',
]
api.add_resource(Home, *routes)
app_routes = [
    '/myapp/',
    # '/myapp/<string:msg>/<string:amt>',
]
api.add_resource(MyApp, *app_routes)

if __name__ == '__main__':
    app.run(debug=True)
