## Secret Santa App Django REST

A Secret Santa API Rest based in an example project Django REST: https://github.com/erdem/DRF-TDD-example/

There are two use cases for this project. 
* The user registration
* Get his giver

## API Endpoints

* **/api/users/** (User registration endpoint)
* **/api/users/getGiftee** (Get user to send a gift of certain user)

### Install 

    pip install -r requirements.txt
    cd secretSantaApp
    python manage.py migrate

### Usage

#### Run the test:
    python manage.py test
#### Start the test:
    python manage.py runserver