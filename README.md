# serviceApp-backend
FastAPI backend with secured routes using PyJWT.

## Usage
Clone this repo
```bash
git clone https://github.com/ot-movimento/serviceApp-backend.git
```

install requirements using pip
```bash
cd serviceApp-backend
pip install -r requirements.txt
```

add `.env` to `/src`. Set following variables in `.env`
```
"AUTH0_ALGORITHMS": ,
"AUTH0_AUDIENCE": ,
"AUTH0_ISSUER":
```

go to `/src` and start app using uvicorn
```bash
cd src
uvicorn main:app --port 5000 --host '0.0.0.0'
