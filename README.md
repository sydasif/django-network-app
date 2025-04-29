# Network Utilities Web Application

A Django-based web application that provides various network utilities and tools for IP address management and network testing.

## Features

- **TCP Ping Tool**
  - Test TCP port connectivity to remote hosts
  - AJAX-based real-time results

- **IP Address Tools**
  - CIDR to Netmask conversion
  - Netmask to CIDR conversion
  - List all hosts in a network
  - Get broadcast address
  - Find first usable IP address
  - Calculate usable IP range

## Requirements

- Python 3.x
- Django 5.2
- netutils (for network operations)

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/django-network-app.git
cd django-network-app
```

2. Create and activate a virtual environment:

```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac
```

3. Install dependencies:

```bash
pip install django netutils
```

4. Apply migrations:

```bash
python manage.py migrate
```

5. Run the development server:

```bash
python manage.py runserver
```

## Usage

1. Access the application at `http://localhost:8000`
2. Navigate to available tools:
   - TCP Ping Tool: `/ping/`
   - IP Address Tools: `/ip_addr/`

## Project Structure

```bash
django-network-app/
├── network_utilities/     # Project settings
├── network_tools/        # Main application
│   ├── static/          # Static files (JS, CSS)
│   ├── templates/       # HTML templates
│   └── views.py         # Application views
└── manage.py            # Django management script
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
