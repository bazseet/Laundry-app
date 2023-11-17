
CustomText(
  text: 'Welcome to Our Laundry App',
  textStyle: TextStyle(
    fontSize: 20.0,
    fontWeight: FontWeight.bold,
    color: Colors.blue,
    // Add more styling properties as needed
  ),
)





class HomeScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Laundry App'),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text('Welcome to Our Laundry App'),
            // Add buttons to navigate to different sections
            ElevatedButton(
              onPressed: () {
                Navigator.pushNamed(context, '/services');
              },
              child: Text('View Services'),
            ),
            ElevatedButton(
              onPressed: () {
                Navigator.pushNamed(context, '/orders');
              },
              child: Text('My Orders'),
            ),
          ],
        ),
      ),
    );
  }
}
// services_screen.dart


class ServicesScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Laundry Services'),
      ),
      body: ListView(
        children: [
          ListTile(
            title: Text('Wash and Fold'),
            // Add onTap to navigate to service details or order screen
            onTap: () {
              Navigator.pushNamed(context, '/service_details', arguments: 'Wash and Fold');
            },
          ),
          ListTile(
            title: Text('Dry Cleaning'),
            onTap: () {
              Navigator.pushNamed(context, '/service_details', arguments: 'Dry Cleaning');
            },
          ),
          // Add more services...
        ],
      ),
    );
  }
}
// service_details_screen.dart


class ServiceDetailsScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    final serviceName = ModalRoute.of(context)!.settings.arguments as String;

    return Scaffold(
      appBar: AppBar(
        title: Text('Service Details'),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text('Details for $serviceName'),
            // Add service details and order button...
          ],
        ),
      ),
    );
  }
}
// orders_screen.dart


class OrdersScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('My Orders'),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text('List of Orders'),
            // Display a list of orders...
          ],
        ),
      ),
    );
  }
}
// main.dart


void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Laundry App',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      initialRoute: '/',
      routes: {
        '/': (context) => HomeScreen(),
        '/services': (context) => ServicesScreen(),
        '/service_details': (context) => ServiceDetailsScreen(),
        '/orders': (context) => OrdersScreen(),
      },
    );
  }
}